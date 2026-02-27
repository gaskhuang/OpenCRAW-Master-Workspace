#!/usr/bin/env node
/**
 * Threads Top News Reporter - 新文記者版
 * 抓取 Threads Top，自動分類，生成 MD 報告
 */

const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 六大類別關鍵詞定義（依內容動態歸納）
const CATEGORY_DEFINITIONS = {
  '科技創新': ['AI', '人工智能', 'artificial intelligence', 'LLM', 'GPT', 'Claude', 'machine learning', 'tech', '科技', '晶片', 'chip', 'semiconductor', 'NVIDIA', 'Apple', 'Google', 'OpenAI', 'startup', '創新', '區塊鏈', 'blockchain', 'crypto', 'bitcoin', '電動車', 'EV', 'Tesla', '機器人', 'robotics', '自動化', 'automation', '程式', 'coding', '軟體', '軟件', '開發'],
  '財經商業': ['stock', '股市', 'market', '經濟', 'economy', 'finance', '金融', '投資', 'invest', 'trading', 'trade', '匯率', '央行', 'Fed', '利率', 'inflation', '通膨', 'recession', '衰退', 'GDP', 'IPO', 'merger', '併購', 'earnings', '財報', 'startup', '創業', 'funding', '融資', 'valuation', '估值', '賺錢', '副業'],
  '政治國際': ['politics', '政治', 'election', '選舉', 'government', '政府', 'policy', '政策', 'war', '戰爭', 'Ukraine', '烏克蘭', 'Israel', '以色列', 'China', '中國', 'Biden', 'Trump', 'EU', 'NATO', 'UN', '聯合國', 'sanctions', '制裁', 'diplomacy', '外交', 'geopolitics', '地緣政治', 'trade war', '貿易戰', '總統', '立法院', '民意代表'],
  '社會民生': ['health', '健康', '醫療', 'healthcare', 'education', '教育', 'housing', '住房', 'job', '就業', 'work', '工作', 'social', '社會', 'environment', '環境', 'climate', '氣候', 'crime', '犯罪', 'law', '法律', 'justice', '司法', 'inequality', '不平等', 'poverty', '貧困', 'welfare', '福利', 'transport', '交通', '生活', '家庭'],
  '娛樂文化': ['movie', '電影', 'music', '音樂', 'celebrity', '名人', 'entertainment', '娛樂', 'sport', '體育', 'NBA', 'football', 'soccer', 'fashion', '時尚', 'art', '藝術', 'culture', '文化', 'game', '遊戲', 'gaming', 'Netflix', 'Disney', 'K-pop', 'meme', '迷因', 'viral', '走紅', '偶像', '明星', '演唱會'],
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

// 提取貼文
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
          // 尋找有 data-pressable-container 的 div
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
                if (match && !seenIds.has(match[1])) {
                  postId = match[1];
                  seenIds.add(postId);
                  postUrl = href.startsWith('http') ? href.split('?')[0] : 'https://www.threads.net' + href.split('?')[0];
                  break;
                }
              }
            }
            
            // 如果沒有找到 post ID，跳過
            if (!postId) continue;
            
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
  
  return categories;
}

// 生成記者評註 - 挑選最值得關注的議題
function generateHighlights(posts) {
  if (posts.length === 0) return [];
  
  // 按互動數排序取前 5，再從中選出 3 個最有新聞價值的
  const sorted = [...posts].sort((a, b) => b.engagement - a.engagement).slice(0, 5);
  
  // 簡單選擇前 3 個（可根據內容相關性進一步篩選）
  return sorted.slice(0, 3).map((post, idx) => ({
    rank: idx + 1,
    author: post.author,
    handle: post.authorHandle,
    text: post.text.substring(0, 100) + (post.text.length > 100 ? '...' : ''),
    postId: post.postId,
    url: post.url,
    engagement: post.engagement
  }));
}

// 生成 Markdown 報告
function generateReport(categories, posts, blockedReason = null) {
  const now = new Date();
  const timestamp = now.toLocaleString('zh-TW', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hour12: false
  });
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  
  let md = `# Threads 動態深度摘要（過去 3 小時）

> 任務時間：${timestamp} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重
> 本輪新增貼文（去重後）：${posts.length}

`;

  if (blockedReason) {
    md += `## ⚠️ 抓取受阻

**原因：** ${blockedReason}

請確認 Threads 已登入，並重新執行抓取。
`;
    return { md, dateStr, timeStr };
  }

  // 依類別輸出
  let lineNumber = 1;
  
  for (const [category, catPosts] of Object.entries(categories)) {
    if (catPosts.length === 0) continue;
    
    md += `## ${category}\n\n`;
    
    catPosts.forEach(post => {
      const shortId = post.postId.substring(0, 15);
      md += `[${lineNumber}] ${post.text.substring(0, 100)}${post.text.length > 100 ? '...' : ''} [（${shortId}...）](${post.url})\n\n`;
      lineNumber++;
    });
  }

  // 記者評註
  const highlights = generateHighlights(posts);
  md += `---

## 本輪最值得關注的 3 個議題（記者評註）

`;
  
  highlights.forEach(h => {
    md += `${h.rank}. **@${h.handle}**（${h.engagement} 互動）: ${h.text}...
`;
  });

  // 風險訊號
  md += `
---

## 風險訊號

- 本輪貼文時間跨度依 Threads 演算法推送決定。
- 互動欄位（按讚/留言）結構化抽取可能有 null 缺值。
- 若 Threads 出現反爬機制，部分內容可能未被完整載入。
`;

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

// 載入已見過的貼文 ID
function loadSeenIds() {
  const seenFile = '/Users/user/data/threads_last_seen.json';
  try {
    if (fs.existsSync(seenFile)) {
      const data = JSON.parse(fs.readFileSync(seenFile, 'utf8'));
      return new Set(data.ids || []);
    }
  } catch (e) {}
  return new Set();
}

// 保存已見過的貼文 ID
function saveSeenIds(seenIds) {
  const seenFile = '/Users/user/data/threads_last_seen.json';
  const data = { ids: [...seenIds], updatedAt: new Date().toISOString() };
  fs.writeFileSync(seenFile, JSON.stringify(data, null, 2));
}

// 主函數
async function main() {
  console.log('🚀 Threads Top News Reporter 啟動...');
  
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  
  // 檢查 CDP
  const cdpAvailable = await checkCDP();
  if (!cdpAvailable) {
    console.log('❌ CDP 端口 19222 無法連線');
    const { md } = generateReport({}, [], 'CDP 端口 19222 無法連線，請確認 Chrome 已啟動');
    
    const mdPath = `/Users/user/reports/threads_top_news_${dateStr}_${timeStr}.md`;
    fs.writeFileSync(mdPath, md);
    
    console.log('OUTPUT_FILE:', mdPath);
    console.log('BLOCKED_REASON: CDP unavailable');
    return { blocked: true, mdPath };
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
    
    // 檢查頁面狀態
    const pageStatus = await Runtime.evaluate({
      expression: `
        (function() {
          return {
            url: window.location.href,
            title: document.title,
            hasLoginForm: !!document.querySelector('input[type="password"]'),
            hasContent: document.querySelectorAll('div[data-pressable-container="true"]').length > 0
          };
        })()
      `,
      returnByValue: true
    });
    
    console.log('📄 頁面狀態:', JSON.stringify(pageStatus.result.value));
    
    const status = pageStatus.result.value;
    if (status.url.includes('login') || status.hasLoginForm) {
      blockedReason = 'Threads 需要登入，請先手動登入 Threads 帳號';
      console.log('⚠️', blockedReason);
    } else if (!status.hasContent) {
      blockedReason = 'Threads 頁面沒有內容，可能需要重新整理或登入';
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
        await sleep(800 + Math.random() * 400);
        
        if ((i + 1) % 10 === 0) {
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
  
  // 分類
  const categories = categorizePosts(allPosts);
  
  // 生成報告
  const { md, dateStr: ds, timeStr: ts } = generateReport(categories, allPosts, blockedReason);
  const mdPath = `/Users/user/reports/threads_top_news_${ds}_${ts}.md`;
  
  fs.writeFileSync(mdPath, md);
  
  console.log('\n💾 報告已生成:');
  console.log('  MD:', mdPath);
  
  console.log('\nOUTPUT_FILE:', mdPath);
  console.log('TOTAL_POSTS:', allPosts.length);
  if (blockedReason) {
    console.log('BLOCKED_REASON:', blockedReason);
  }
  
  return { blocked: !!blockedReason, mdPath, totalPosts: allPosts.length };
}

// 執行
main().then(result => {
  process.exit(result && result.blocked ? 1 : 0);
}).catch(err => {
  console.error('❌ 執行失敗:', err);
  process.exit(1);
});
