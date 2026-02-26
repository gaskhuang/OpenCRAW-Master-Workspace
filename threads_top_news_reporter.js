#!/usr/bin/env node
/**
 * Threads Top News Reporter - 記者版
 * 抓取 Threads，自動分類，生成 Markdown 報告
 */

const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 六大類別關鍵詞定義 - 依內容自動歸納
const CATEGORY_DEFINITIONS = {
  '科技創新': ['AI', '人工智能', 'artificial intelligence', 'LLM', 'GPT', 'Claude', 'machine learning', 'tech', '科技', '晶片', 'chip', 'semiconductor', 'NVIDIA', 'Apple', 'Google', 'OpenAI', 'Anthropic', 'startup', '創新', '區塊鏈', 'blockchain', 'crypto', 'bitcoin', '電動車', 'EV', 'Tesla', '機器人', 'robotics', '自動化', 'automation', '模型', 'model'],
  '財經商業': ['stock', '股市', 'market', '市場', '經濟', 'economy', 'finance', '金融', '投資', 'invest', 'trading', 'trade', '匯率', '央行', 'Fed', '利率', 'inflation', '通膨', 'recession', '衰退', 'GDP', 'IPO', 'merger', '併購', 'earnings', '財報', 'startup', '創業', 'funding', '融資', 'valuation', '估值', '創業', '生意'],
  '政治國際': ['politics', '政治', 'election', '選舉', 'government', '政府', 'policy', '政策', 'war', '戰爭', 'Ukraine', '烏克蘭', 'Israel', '以色列', 'China', '中國', 'Biden', 'Trump', 'EU', 'NATO', 'UN', '聯合國', 'sanctions', '制裁', 'diplomacy', '外交', 'geopolitics', '地緣政治', 'trade war', '貿易戰'],
  '社會民生': ['health', '健康', '醫療', 'healthcare', 'education', '教育', 'housing', '住房', 'job', '就業', 'work', '工作', 'social', '社會', 'environment', '環境', 'climate', '氣候', 'crime', '犯罪', 'law', '法律', 'justice', '司法', 'inequality', '不平等', 'poverty', '貧困', 'welfare', '福利', 'transport', '交通', '生活'],
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

// 檢查 Threads 頁面狀態
async function checkThreadsPageStatus(client) {
  const { Runtime } = client;
  
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const url = window.location.href;
        const title = document.title;
        const hasLoginForm = !!document.querySelector('input[name="username"], input[type="password"], button[type="submit"]');
        const hasContent = !!document.querySelector('article, [data-pressable-container="true"], span[dir="auto"]');
        const bodyText = document.body ? document.body.innerText.substring(0, 500) : '';
        return { url, title, hasLoginForm, hasContent, bodyText };
      })()
    `,
    returnByValue: true
  });
  
  return result.result.value;
}

// 提取 Threads 貼文
async function extractPosts(client) {
  const { Runtime } = client;
  
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const posts = [];
        const seenIds = new Set();
        
        // 策略 1: 尋找所有包含貼文內容的 div
        const allDivs = document.querySelectorAll('div');
        const postContainers = [];
        
        for (const div of allDivs) {
          if (div.getAttribute('data-pressable-container') === 'true') {
            postContainers.push(div);
          }
        }
        
        // 策略 2: 也嘗試 article 標籤
        document.querySelectorAll('article').forEach(a => postContainers.push(a));
        
        for (const container of postContainers) {
          try {
            // 提取文字
            let text = '';
            const spans = container.querySelectorAll('span[dir="auto"]');
            for (const span of spans) {
              const txt = span.innerText.trim();
              if (txt.length > 20 && !txt.match(/^(Like|Reply|Repost|Share|·)$/)) {
                text = txt;
                break;
              }
            }
            
            if (!text || text.length < 20) continue;
            
            // 提取作者
            let author = '';
            let authorHandle = '';
            const links = container.querySelectorAll('a');
            for (const link of links) {
              const href = link.getAttribute('href') || '';
              if (href.startsWith('/@')) {
                const parts = href.split('/');
                if (parts[1]) {
                  authorHandle = parts[1].replace('@', '');
                  author = link.innerText.trim() || authorHandle;
                  break;
                }
              }
            }
            
            // 提取 URL 和 ID
            let postUrl = '';
            let postId = '';
            for (const link of links) {
              const href = link.getAttribute('href') || '';
              if (href.includes('/post/')) {
                const match = href.match(/\\/post\\/([^/?]+)/);
                if (match) {
                  postId = match[1];
                  postUrl = href.startsWith('http') ? href.split('?')[0] : 'https://www.threads.net' + href.split('?')[0];
                  break;
                }
              }
            }
            
            // 如果沒有找到 post ID，創建一個基於內容的 ID
            if (!postId && text) {
              postId = 'text_' + text.substring(0, 30).replace(/\\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '');
              postUrl = authorHandle ? 'https://www.threads.net/@' + authorHandle : '';
            }
            
            // 去重
            if (seenIds.has(postId)) continue;
            seenIds.add(postId);
            
            // 提取時間
            let timeText = '';
            const timeEl = container.querySelector('time');
            if (timeEl) {
              timeText = timeEl.innerText.trim() || timeEl.getAttribute('datetime') || '';
            }
            
            // 提取互動數
            const fullText = container.innerText;
            let likes = 0;
            let comments = 0;
            let reposts = 0;
            
            // 尋找數字模式
            const likePatterns = fullText.match(/(\\d+(?:,\\d+)*)\\s*(?:like|讚|likes)/i);
            if (likePatterns) likes = parseInt(likePatterns[1].replace(/,/g, ''));
            
            const replyPatterns = fullText.match(/(\\d+(?:,\\d+)*)\\s*(?:reply|replies|留言)/i);
            if (replyPatterns) comments = parseInt(replyPatterns[1].replace(/,/g, ''));
            
            const repostPatterns = fullText.match(/(\\d+(?:,\\d+)*)\\s*(?:repost|reposts|轉發)/i);
            if (repostPatterns) reposts = parseInt(repostPatterns[1].replace(/,/g, ''));
            
            posts.push({
              postId,
              author: author || authorHandle || 'unknown',
              authorHandle: authorHandle || '',
              text: text.substring(0, 800),
              timeText,
              likes,
              comments,
              reposts,
              url: postUrl,
              engagement: likes + comments + reposts
            });
          } catch (e) {}
        }
        
        return posts;
      })()
    `,
    returnByValue: true
  });
  
  return result.result.value || [];
}

// 自動分類貼文
function categorizePosts(posts) {
  const categories = {
    '科技創新': [],
    '財經商業': [],
    '政治國際': [],
    '社會民生': [],
    '娛樂文化': [],
    '其他': []
  };
  
  posts.forEach(post => {
    const text = (post.text + ' ' + post.author + ' ' + post.authorHandle).toLowerCase();
    let assigned = false;
    
    for (const [category, keywords] of Object.entries(CATEGORY_DEFINITIONS)) {
      if (category === '其他') continue;
      
      for (const keyword of keywords) {
        if (text.includes(keyword.toLowerCase())) {
          categories[category].push(post);
          assigned = true;
          break;
        }
      }
      if (assigned) break;
    }
    
    if (!assigned) {
      categories['其他'].push(post);
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
    .map(([name, posts]) => ({ name, count: posts.length }))
    .filter(c => c.count > 0)
    .sort((a, b) => b.count - a.count);
  
  const topCategory = categoryCounts[0];
  const totalEngagement = Object.values(categories).flat()
    .reduce((sum, p) => sum + p.engagement, 0);
  
  return {
    totalCount,
    categoryCounts,
    topCategory: topCategory ? topCategory.name : 'N/A',
    avgEngagement: totalCount > 0 ? Math.round(totalEngagement / totalCount) : 0
  };
}

// 載入已見過的貼文 ID
function loadSeenIds() {
  const seenFile = '/Users/user/reports/.threads_monitor_seen_ids.json';
  try {
    if (fs.existsSync(seenFile)) {
      const data = JSON.parse(fs.readFileSync(seenFile, 'utf8'));
      return new Set(Object.keys(data));
    }
  } catch (e) {}
  return new Set();
}

// 保存已見過的貼文 ID
function saveSeenIds(seenIds) {
  const seenFile = '/Users/user/reports/.threads_monitor_seen_ids.json';
  const data = {};
  const now = new Date().toISOString();
  seenIds.forEach(id => {
    data[id] = now;
  });
  fs.writeFileSync(seenFile, JSON.stringify(data, null, 2));
}

// 生成 Markdown 報告
function generateMD(categories, summary, blockedReason = null) {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  const timestamp = now.toLocaleString('zh-TW', { 
    year: 'numeric', month: '2-digit', day: '2-digit', 
    hour: '2-digit', minute: '2-digit', hour12: false 
  });
  
  let md = `# Threads 動態深度摘要（過去 3 小時）

> 任務時間：${timestamp} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重
> 本輪新增貼文（去重後）：${summary.totalCount}

`;
  
  if (blockedReason) {
    md += `## ⚠️ 抓取受阻

**原因：** ${blockedReason}

請確認 Threads 可正常訪問，並重新執行抓取。

`;
  } else {
    let lineNumber = 1;
    
    for (const [category, posts] of Object.entries(categories)) {
      if (posts.length === 0) continue;
      
      md += `## ${category}\n\n`;
      
      posts.forEach(post => {
        const text = post.text.length > 120 ? post.text.substring(0, 120) + '...' : post.text;
        const cleanText = text.replace(/\n/g, ' ').trim();
        const postIdShort = post.postId.substring(0, 12);
        
        md += `[${lineNumber}] ${cleanText} [（${postIdShort}...）](${post.url})\n\n`;
        lineNumber++;
      });
    }
  }
  
  // 記者評註
  md += `---

## 本輪最值得關注的 3 個議題（記者評註）

`;
  
  if (summary.totalCount === 0) {
    md += `1. 本輪新增內容較少，建議稍後重試。\n`;
    md += `2. Threads 演算法推送內容有限。\n`;
    md += `3. 建議擴大追蹤範圍或調整抓取策略。\n`;
  } else {
    const topPosts = Object.values(categories).flat()
      .sort((a, b) => b.engagement - a.engagement)
      .slice(0, 3);
    
    topPosts.forEach((post, i) => {
      const text = post.text.substring(0, 60);
      md += `${i + 1}. **@${post.author}**（${post.engagement} 互動）: ${text}...\n`;
    });
  }
  
  // 風險訊號
  md += `
---

## 風險訊號

- 本輪貼文時間跨度依 Threads 演算法推送決定。\n`;
  if (blockedReason) {
    md += `- ⚠️ 抓取受阻：${blockedReason}\n`;
  }
  md += `- 互動欄位（按讚/留言）結構化抽取可能有 null 缺值。\n`;
  md += `- 若 Threads 出現反爬機制，部分內容可能未被完整載入。\n`;
  
  // 下一輪追蹤關鍵詞
  md += `
---

## 下一輪追蹤關鍵詞

- AI
- 開發
- 產品
- 設計
- 創業
- 科技新聞
`;
  
  return { md, dateStr, timeStr };
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
    const { md } = generateMD({}, summary, 'CDP 端口 19222 無法連線，請確認 Chrome 已啟動並開啟 remote debugging');
    
    const mdPath = `/Users/user/reports/threads_top_news_${dateStr}_${timeStr}.md`;
    fs.writeFileSync(mdPath, md);
    
    console.log('OUTPUT_FILE:', mdPath);
    console.log('BLOCKED_REASON: CDP unavailable');
    return;
  }
  
  console.log('✅ CDP 可用，連線中...');
  
  let client;
  let blockedReason = null;
  let allPosts = [];
  
  try {
    client = await CDP({ host: CDP_HOST, port: CDP_PORT });
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    // 導航到 Threads
    console.log('🌐 導航到 Threads...');
    await Page.navigate({ url: 'https://www.threads.net' });
    await sleep(10000);
    
    // 檢查 Threads 頁面狀態
    const pageStatus = await checkThreadsPageStatus(client);
    console.log('Threads 頁面狀態:', JSON.stringify(pageStatus));
    
    if (pageStatus.hasLoginForm || pageStatus.url.includes('login')) {
      blockedReason = 'Threads 需要登入，請先在手動登入 Threads 帳號';
      console.log('⚠️', blockedReason);
    } else if (!pageStatus.hasContent) {
      blockedReason = 'Threads 頁面沒有內容，可能需要登入或重新整理';
      console.log('⚠️', blockedReason);
    } else {
      // 抓取貼文
      console.log('📥 開始抓取 Threads...');
      const seenIds = loadSeenIds();
      const newSeenIds = new Set(seenIds);
      
      // 初始提取
      console.log('📥 初始提取...');
      let posts = await extractPosts(client);
      let newCount = 0;
      posts.forEach(p => {
        if (!newSeenIds.has(p.postId)) {
          newSeenIds.add(p.postId);
          allPosts.push(p);
          newCount++;
        }
      });
      console.log(`  初始: ${newCount} 條新貼文`);
      
      // 滾動 80 次
      console.log('📜 開始滾動 80 次...');
      for (let i = 0; i < 80; i++) {
        await Runtime.evaluate({
          expression: 'window.scrollTo(0, document.body.scrollHeight);',
          returnByValue: true
        });
        await sleep(1000 + Math.random() * 500);
        
        if ((i + 1) % 5 === 0) {
          posts = await extractPosts(client);
          let batchNew = 0;
          posts.forEach(p => {
            if (!newSeenIds.has(p.postId)) {
              newSeenIds.add(p.postId);
              allPosts.push(p);
              batchNew++;
            }
          });
          console.log(`  滾動 ${i+1}/80 - 新增 ${batchNew} 條，總計 ${allPosts.length}`);
        }
      }
      
      saveSeenIds(newSeenIds);
      console.log(`\n✅ 完成! 共抓取 ${allPosts.length} 條新貼文`);
    }
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    blockedReason = blockedReason || `執行錯誤: ${err.message}`;
  } finally {
    if (client) await client.close();
  }
  
  // 分類和排序
  const categories = categorizePosts(allPosts);
  const summary = generateSummary(categories, allPosts.length);
  
  // 生成報告
  const { md, dateStr: ds, timeStr: ts } = generateMD(categories, summary, blockedReason);
  const mdPath = `/Users/user/reports/threads_top_news_${ds}_${ts}.md`;
  
  fs.writeFileSync(mdPath, md);
  
  console.log('\n💾 報告已生成:');
  console.log('  MD:', mdPath);
  
  console.log('\nOUTPUT_FILE:', mdPath);
  console.log('TOTAL_POSTS:', allPosts.length);
  if (blockedReason) {
    console.log('BLOCKED_REASON:', blockedReason);
  }
}

main().catch(console.error);
