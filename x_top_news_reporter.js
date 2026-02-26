#!/usr/bin/env node
/**
 * X Top News Reporter - 新文記者版
 * 抓取 X Top，自動分類，生成 HTML/MD 報告
 */

const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 六大類別關鍵詞定義
const CATEGORY_DEFINITIONS = {
  '科技創新': ['AI', '人工智能', 'artificial intelligence', 'LLM', 'GPT', 'Claude', 'machine learning', 'tech', '科技', '晶片', 'chip', 'semiconductor', 'NVIDIA', 'Apple', 'Google', 'OpenAI', 'startup', '創新', '區塊鏈', 'blockchain', 'crypto', 'bitcoin', '電動車', 'EV', 'Tesla', '機器人', 'robotics', '自動化', 'automation'],
  '財經商業': ['stock', '股市', 'market', 'market', '經濟', 'economy', 'finance', '金融', '投資', 'invest', 'trading', 'trade', '匯率', '央行', 'Fed', '利率', 'inflation', '通膨', 'recession', '衰退', 'GDP', 'IPO', 'merger', '併購', 'earnings', '財報', 'startup', '創業', 'funding', '融資', 'valuation', '估值'],
  '政治國際': ['politics', '政治', 'election', '選舉', 'government', '政府', 'policy', '政策', 'war', '戰爭', 'Ukraine', '烏克蘭', 'Israel', '以色列', 'China', '中國', 'Biden', 'Trump', 'EU', 'NATO', 'UN', '聯合國', 'sanctions', '制裁', 'diplomacy', '外交', 'geopolitics', '地緣政治', 'trade war', '貿易戰'],
  '社會民生': ['health', '健康', '醫療', 'healthcare', 'education', '教育', 'housing', '住房', 'job', '就業', 'work', '工作', 'social', '社會', 'environment', '環境', 'climate', '氣候', 'crime', '犯罪', 'law', '法律', 'justice', '司法', 'inequality', '不平等', 'poverty', '貧困', 'welfare', '福利', 'transport', '交通'],
  '娛樂文化': ['movie', '電影', 'music', '音樂', 'celebrity', '名人', 'entertainment', '娛樂', 'sport', '體育', 'NBA', 'football', 'soccer', 'fashion', '時尚', 'art', '藝術', 'culture', '文化', 'game', '遊戲', 'gaming', 'Netflix', 'Disney', 'K-pop', 'meme', '迷因', 'viral', '走紅'],
  '其他': [] // 其他未分類
};

// 檢查 CDP 是否可用
async function checkCDP() {
  try {
    const response = await fetch(`http://${CDP_HOST}:${CDP_PORT}/json/version`);
    return response.ok;
  } catch (e) {
    return false;
  }
}

// 檢查 X 頁面狀態
async function checkXPageStatus(client) {
  const { Runtime } = client;
  
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const url = window.location.href;
        const title = document.title;
        const hasLoginForm = !!document.querySelector('input[name="text"], input[name="password"], input[type="password"]');
        const hasTimeline = !!document.querySelector('[data-testid="primaryColumn"], article, [data-testid="cellInnerDiv"]');
        return { url, title, hasLoginForm, hasTimeline };
      })()
    `,
    returnByValue: true
  });
  
  return result.result.value;
}

// 提取推文
async function extractTweets(client) {
  const { Runtime } = client;
  
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const articles = document.querySelectorAll('article');
        const extracted = [];
        
        articles.forEach((article, idx) => {
          try {
            const timeEl = article.querySelector('time');
            if (!timeEl) return;
            
            let linkEl = timeEl.closest('a');
            if (!linkEl) {
              linkEl = article.querySelector('a[href*="/status/"]');
            }
            if (!linkEl) return;
            
            const href = linkEl.getAttribute('href');
            const match = href.match(/status\\/(\\d+)/);
            if (!match) return;
            
            const tweetId = match[1];
            
            const textEl = article.querySelector('[data-testid="tweetText"]');
            const text = textEl ? textEl.innerText.trim() : '';
            
            const authorEl = article.querySelector('a[role="link"] div[dir="ltr"] span');
            const authorName = authorEl ? authorEl.textContent.trim() : '';
            
            const handleEl = article.querySelector('a[role="link"][href^="/"]');
            const authorHandle = handleEl ? handleEl.getAttribute('href').split('/')[1] : '';
            
            const timestamp = timeEl.getAttribute('datetime');
            const timeText = timeEl.textContent.trim();
            
            const getCount = (testid) => {
              const el = article.querySelector('[data-testid="' + testid + '"]');
              if (!el) return 0;
              const spans = el.querySelectorAll('span');
              for (const span of spans) {
                const txt = span.textContent.trim();
                if (txt && !isNaN(parseFloat(txt.replace(/[KM,]/g, '')))) {
                  if (txt.includes('K')) return Math.round(parseFloat(txt.replace('K', '')) * 1000);
                  if (txt.includes('M')) return Math.round(parseFloat(txt.replace('M', '')) * 1000000);
                  return parseInt(txt.replace(/[^0-9]/g, '')) || 0;
                }
              }
              return 0;
            };
            
            extracted.push({
              tweetId,
              authorName,
              authorHandle: '@' + authorHandle,
              text,
              timestamp,
              timeText,
              likes: getCount('like'),
              retweets: getCount('retweet'),
              replies: getCount('reply'),
              bookmarks: getCount('bookmark'),
              url: 'https://x.com' + href.split('?')[0],
              engagement: 0
            });
          } catch (e) {}
        });
        
        return extracted;
      })()
    `,
    returnByValue: true
  });
  
  return result.result.value || [];
}

// 自動分類推文
function categorizeTweets(tweets) {
  const categories = {
    '科技創新': [],
    '財經商業': [],
    '政治國際': [],
    '社會民生': [],
    '娛樂文化': [],
    '其他': []
  };
  
  tweets.forEach(tweet => {
    const text = (tweet.text + ' ' + tweet.authorName + ' ' + tweet.authorHandle).toLowerCase();
    let assigned = false;
    
    for (const [category, keywords] of Object.entries(CATEGORY_DEFINITIONS)) {
      if (category === '其他') continue;
      
      for (const keyword of keywords) {
        if (text.includes(keyword.toLowerCase())) {
          categories[category].push(tweet);
          assigned = true;
          break;
        }
      }
      if (assigned) break;
    }
    
    if (!assigned) {
      categories['其他'].push(tweet);
    }
  });
  
  // 各類別內按互動數排序
  for (const category of Object.keys(categories)) {
    categories[category].sort((a, b) => b.engagement - a.engagement);
  }
  
  return categories;
}

// 生成記者摘要
function generateSummary(categories, totalCount) {
  const categoryCounts = Object.entries(categories)
    .map(([name, tweets]) => ({ name, count: tweets.length }))
    .filter(c => c.count > 0)
    .sort((a, b) => b.count - a.count);
  
  const topCategory = categoryCounts[0];
  const totalEngagement = Object.values(categories).flat()
    .reduce((sum, t) => sum + t.engagement, 0);
  
  return {
    totalCount,
    categoryCounts,
    topCategory: topCategory ? topCategory.name : 'N/A',
    avgEngagement: totalCount > 0 ? Math.round(totalEngagement / totalCount) : 0
  };
}

// 生成 HTML 報告
function generateHTML(categories, summary, blockedReason = null) {
  const now = new Date();
  const timestamp = now.toLocaleString('zh-TW', { 
    year: 'numeric', month: '2-digit', day: '2-digit', 
    hour: '2-digit', minute: '2-digit', hour12: false 
  });
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  
  const formatNumber = (n) => n.toLocaleString();
  
  let tweetsHTML = '';
  let lineNumber = 1;
  
  if (blockedReason) {
    tweetsHTML = `
      <div class="blocked-notice">
        <h2>⚠️ 抓取受阻</h2>
        <p><strong>原因：</strong>${blockedReason}</p>
        <p>請確認 X 已登入，並重新執行抓取。</p>
      </div>
    `;
  } else {
    for (const [category, tweets] of Object.entries(categories)) {
      if (tweets.length === 0) continue;
      
      tweetsHTML += `
        <section class="category">
          <h2 class="category-title">${category} <span class="count">(${tweets.length})</span></h2>
          <div class="tweets">
      `;
      
      tweets.forEach((tweet, idx) => {
        const engagement = tweet.likes + tweet.retweets + tweet.replies;
        const tweetNum = lineNumber++;
        
        tweetsHTML += `
          <div class="tweet" id="L${tweetNum}">
            <div class="tweet-header">
              <span class="line-num" onclick="copyLine(${tweetNum})" title="複製行號">#${tweetNum}</span>
              <span class="author" onclick="copyText('${tweet.authorName} ${tweet.authorHandle}')">${tweet.authorName} <span class="handle">${tweet.authorHandle}</span></span>
              <span class="time">${tweet.timeText}</span>
              <a class="tweet-link" href="${tweet.url}" target="_blank" title="開啟原文">🐦</a>
            </div>
            <div class="tweet-text" onclick="copyTextWithUrl(this, '${tweet.url}')">${escapeHtml(tweet.text)}</div>
            <div class="tweet-stats">
              <span title="愛心">❤️ ${formatNumber(tweet.likes)}</span>
              <span title="轉推">🔄 ${formatNumber(tweet.retweets)}</span>
              <span title="回覆">💬 ${formatNumber(tweet.replies)}</span>
              <span title="總互動">📊 ${formatNumber(engagement)}</span>
            </div>
          </div>
        `;
      });
      
      tweetsHTML += '</div></section>';
    }
  }
  
  const categorySummary = summary.categoryCounts
    .map(c => `${c.name}: ${c.count}`)
    .join(' | ');
  
  return `<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>X Top News - ${dateStr}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
      background: #15202b;
      color: #e7e9ea;
      line-height: 1.6;
    }
    .header {
      text-align: center;
      padding: 20px 0;
      border-bottom: 1px solid #38444d;
      margin-bottom: 20px;
    }
    .header h1 { margin: 0; color: #1d9bf0; font-size: 1.8em; }
    .header .meta { color: #8899a6; font-size: 0.9em; margin-top: 8px; }
    .summary {
      background: #192734;
      padding: 15px 20px;
      border-radius: 12px;
      margin-bottom: 20px;
      border: 1px solid #38444d;
    }
    .summary h3 { margin-top: 0; color: #1d9bf0; }
    .category { margin-bottom: 30px; }
    .category-title {
      color: #1d9bf0;
      font-size: 1.3em;
      padding: 10px 15px;
      background: #192734;
      border-radius: 8px;
      margin-bottom: 15px;
      border-left: 4px solid #1d9bf0;
    }
    .category-title .count { color: #8899a6; font-size: 0.8em; }
    .tweet {
      background: #192734;
      border: 1px solid #38444d;
      border-radius: 12px;
      padding: 15px;
      margin-bottom: 12px;
      transition: border-color 0.2s;
    }
    .tweet:hover { border-color: #1d9bf0; }
    .tweet-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    .line-num {
      color: #8899a6;
      font-size: 0.8em;
      cursor: pointer;
      padding: 2px 6px;
      border-radius: 4px;
      background: #253341;
    }
    .line-num:hover { background: #1d9bf0; color: white; }
    .author {
      font-weight: bold;
      color: #e7e9ea;
      cursor: pointer;
    }
    .author:hover { text-decoration: underline; }
    .handle { color: #8899a6; font-weight: normal; }
    .time { color: #8899a6; font-size: 0.9em; }
    .tweet-link { text-decoration: none; margin-left: auto; font-size: 1.2em; }
    .tweet-text {
      color: #e7e9ea;
      margin-bottom: 10px;
      white-space: pre-wrap;
      cursor: pointer;
      padding: 5px;
      border-radius: 6px;
    }
    .tweet-text:hover { background: #253341; }
    .tweet-stats {
      display: flex;
      gap: 20px;
      color: #8899a6;
      font-size: 0.9em;
    }
    .blocked-notice {
      background: #3a1c1c;
      border: 1px solid #c94c4c;
      padding: 30px;
      border-radius: 12px;
      text-align: center;
    }
    .blocked-notice h2 { color: #c94c4c; }
    .toast {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #1d9bf0;
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      opacity: 0;
      transition: opacity 0.3s;
      z-index: 1000;
    }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🐦 X Top News</h1>
    <div class="meta">${timestamp} | 共 ${summary.totalCount} 條推文</div>
  </div>
  
  <div class="summary">
    <h3>📊 記者摘要</h3>
    <p><strong>總數：</strong>${summary.totalCount} 條 | <strong>熱門類別：</strong>${summary.topCategory} | <strong>平均互動：</strong>${formatNumber(summary.avgEngagement)}</p>
    <p><strong>分類分布：</strong>${categorySummary}</p>
  </div>
  
  ${tweetsHTML}
  
  <div class="toast" id="toast">已複製到剪貼簿</div>
  
  <script>
    function showToast(message) {
      const toast = document.getElementById('toast');
      toast.textContent = message;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }
    
    function copyText(text) {
      navigator.clipboard.writeText(text).then(() => showToast('已複製作者'));
    }
    
    function copyLine(num) {
      const url = window.location.href.split('#')[0] + '#L' + num;
      navigator.clipboard.writeText(url).then(() => showToast('已複製行號連結'));
    }
    
    function copyTextWithUrl(el, url) {
      const text = el.textContent + '\\n' + url;
      navigator.clipboard.writeText(text).then(() => showToast('已複製內文+連結'));
    }
  </script>
</body>
</html>`;
}

// 生成 Markdown 報告
function generateMD(categories, summary, blockedReason = null) {
  const now = new Date();
  const timestamp = now.toLocaleString('zh-TW');
  
  let md = `# 🐦 X Top News Report

**生成時間：** ${timestamp}  
**總數：** ${summary.totalCount} 條推文  
**熱門類別：** ${summary.topCategory}  
**平均互動：** ${summary.avgEngagement}

## 📊 分類分布

`;
  
  summary.categoryCounts.forEach(c => {
    md += `- ${c.name}: ${c.count} 條\n`;
  });
  
  md += '\n---\n\n';
  
  if (blockedReason) {
    md += `## ⚠️ 抓取受阻

**原因：** ${blockedReason}

請確認 X 已登入，並重新執行抓取。
`;
  } else {
    for (const [category, tweets] of Object.entries(categories)) {
      if (tweets.length === 0) continue;
      
      md += `## ${category} (${tweets.length})\n\n`;
      
      tweets.forEach((tweet, idx) => {
        const engagement = tweet.likes + tweet.retweets + tweet.replies;
        md += `### ${idx + 1}. ${tweet.authorName} (${tweet.authorHandle})

${tweet.text}

- ⏰ ${tweet.timeText}
- ❤️ ${tweet.likes.toLocaleString()} | 🔄 ${tweet.retweets.toLocaleString()} | 💬 ${tweet.replies.toLocaleString()} | 📊 ${engagement.toLocaleString()}
- 🔗 [原文](${tweet.url})

---

`;
      });
    }
  }
  
  return md;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 載入已見過的推文 ID
function loadSeenIds() {
  const seenFile = '/Users/user/reports/.x_top_seen_ids.json';
  try {
    if (fs.existsSync(seenFile)) {
      return new Set(JSON.parse(fs.readFileSync(seenFile, 'utf8')));
    }
  } catch (e) {}
  return new Set();
}

// 保存已見過的推文 ID
function saveSeenIds(seenIds) {
  const seenFile = '/Users/user/reports/.x_top_seen_ids.json';
  fs.writeFileSync(seenFile, JSON.stringify([...seenIds], null, 2));
}

// 主函數
async function main() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  
  // 檢查 CDP
  const cdpAvailable = await checkCDP();
  if (!cdpAvailable) {
    console.log('❌ CDP 端口 19222 無法連線');
    const summary = { totalCount: 0, categoryCounts: [], topCategory: 'N/A', avgEngagement: 0 };
    const html = generateHTML({}, summary, 'CDP 端口 19222 無法連線，請確認 Chrome 已啟動');
    const md = generateMD({}, summary, 'CDP 端口 19222 無法連線，請確認 Chrome 已啟動');
    
    const htmlPath = `/Users/user/reports/web/x_top_news_${dateStr}_${timeStr}.html`;
    const mdPath = `/Users/user/reports/x_top_news_${dateStr}_${timeStr}.md`;
    
    fs.writeFileSync(htmlPath, html);
    fs.writeFileSync(mdPath, md);
    
    console.log('OUTPUT_FILE:', htmlPath);
    console.log('BLOCKED_REASON: CDP unavailable');
    return;
  }
  
  console.log('✅ CDP 可用，連線中...');
  
  let client;
  let blockedReason = null;
  let allTweets = [];
  
  try {
    client = await CDP({ host: CDP_HOST, port: CDP_PORT });
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    // 檢查頁面狀態
    console.log('🔍 檢查 X 頁面狀態...');
    const pageStatus = await checkXPageStatus(client);
    console.log('頁面狀態:', JSON.stringify(pageStatus));
    
    // 導航到 X Top
    console.log('🌐 導航到 X...');
    await Page.navigate({ url: 'https://x.com/home' });
    await sleep(8000);
    
    // 檢查 X 頁面狀態
    const xStatus = await checkXPageStatus(client);
    console.log('X 頁面狀態:', JSON.stringify(xStatus));
    
    if (xStatus.hasLoginForm || xStatus.url.includes('login') || xStatus.title.includes('登入')) {
      blockedReason = 'X 需要登入，請先在手動登入 X 帳號';
      console.log('⚠️', blockedReason);
    } else if (!xStatus.hasTimeline) {
      blockedReason = 'X 頁面沒有時間軸內容，可能需要重新整理或登入';
      console.log('⚠️', blockedReason);
    } else {
      // 抓取推文
      console.log('📥 開始抓取 X Top...');
      const seenIds = loadSeenIds();
      const newSeenIds = new Set(seenIds);
      
      // 初始提取
      console.log('📥 初始提取...');
      let tweets = await extractTweets(client);
      let newCount = 0;
      tweets.forEach(t => {
        t.engagement = t.likes + t.retweets + t.replies;
        if (!newSeenIds.has(t.tweetId)) {
          newSeenIds.add(t.tweetId);
          allTweets.push(t);
          newCount++;
        }
      });
      console.log(`  初始: ${newCount} 條新推文`);
      
      // 滾動 80 次
      console.log('📜 開始滾動 80 次...');
      for (let i = 0; i < 80; i++) {
        await Runtime.evaluate({
          expression: 'window.scrollTo(0, document.body.scrollHeight);',
          returnByValue: true
        });
        await sleep(1000 + Math.random() * 500);
        
        if ((i + 1) % 5 === 0) {
          tweets = await extractTweets(client);
          let batchNew = 0;
          tweets.forEach(t => {
            t.engagement = t.likes + t.retweets + t.replies;
            if (!newSeenIds.has(t.tweetId)) {
              newSeenIds.add(t.tweetId);
              allTweets.push(t);
              batchNew++;
            }
          });
          console.log(`  滾動 ${i+1}/80 - 新增 ${batchNew} 條，總計 ${allTweets.length}`);
        }
      }
      
      saveSeenIds(newSeenIds);
      console.log(`\n✅ 完成! 共抓取 ${allTweets.length} 條新推文`);
    }
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    blockedReason = blockedReason || `執行錯誤: ${err.message}`;
  } finally {
    if (client) await client.close();
  }
  
  // 分類和排序
  const categories = categorizeTweets(allTweets);
  const summary = generateSummary(categories, allTweets.length);
  
  // 生成報告
  const htmlPath = `/Users/user/reports/web/x_top_news_${dateStr}_${timeStr}.html`;
  const mdPath = `/Users/user/reports/x_top_news_${dateStr}_${timeStr}.md`;
  
  const html = generateHTML(categories, summary, blockedReason);
  const md = generateMD(categories, summary, blockedReason);
  
  fs.writeFileSync(htmlPath, html);
  fs.writeFileSync(mdPath, md);
  
  console.log('\n💾 報告已生成:');
  console.log('  HTML:', htmlPath);
  console.log('  MD:', mdPath);
  
  console.log('\nOUTPUT_FILE:', htmlPath);
  console.log('TOTAL_TWEETS:', allTweets.length);
  if (blockedReason) {
    console.log('BLOCKED_REASON:', blockedReason);
  }
}

main().catch(console.error);
