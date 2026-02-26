#!/usr/bin/env node
/**
 * OpenClaw X 平台智能分析器
 * 產出網站版報告，對齊 https://x.deepsrt.com/ 風格
 * 
 * 輸出：
 * 1) HTML：reports/web/x_monitor_YYYYMMDD_HHmm.html
 * 2) MD：reports/x_monitor_YYYYMMDD_HHmm.md
 */

const fs = require('fs');
const path = require('path');

// 分類定義（動態命名，根據內容決定）
const DEFAULT_CATEGORIES = [
  { id: 'ai', emoji: '🤖', name: 'AI 模型與產品' },
  { id: 'dev', emoji: '🛠️', name: '開發工具與實踐' },
  { id: 'openclaw', emoji: '🦞', name: 'OpenClaw 生態' },
  { id: 'chip', emoji: '🏭', name: '晶片與算力' },
  { id: 'hot', emoji: '🔥', name: '熱門焦點' },
  { id: 'business', emoji: '💰', name: '商業與新創' }
];

// 從推文內容推斷分類
function categorizeTweet(tweet) {
  const text = (tweet.text || '').toLowerCase();
  const author = (tweet.authorHandle || '').toLowerCase();
  
  // OpenClaw 生態檢測
  if (text.includes('openclaw') || text.includes('龍蝦') || 
      author.includes('openclaw') || text.includes('claw')) {
    return 'openclaw';
  }
  
  // AI 模型與產品
  if (text.includes('gpt') || text.includes('claude') || text.includes('llm') ||
      text.includes('openai') || text.includes('anthropic') || text.includes('gemini') ||
      text.includes('ai model') || text.includes('language model') ||
      text.includes('deepseek') || text.includes('qwen') || text.includes('mistral') ||
      text.includes('codex') || text.includes('cursor')) {
    return 'ai';
  }
  
  // 晶片與算力
  if (text.includes('nvidia') || text.includes('gpu') || text.includes('cpu') ||
      text.includes('chip') || text.includes('semiconductor') || text.includes('training') ||
      text.includes('inference') || text.includes('算力') || text.includes('輝達')) {
    return 'chip';
  }
  
  // 開發工具
  if (text.includes('github') || text.includes('vscode') || text.includes('docker') ||
      text.includes('kubernetes') || text.includes('devops') || text.includes('git') ||
      text.includes('terminal') || text.includes('cli') || text.includes('api')) {
    return 'dev';
  }
  
  // 商業與新創
  if (text.includes('startup') || text.includes('funding') || text.includes('invest') ||
      text.includes('ipo') || text.includes('valuation') || text.includes('series') ||
      text.includes('acquisition') || text.includes('ipo') || text.includes('股票') ||
      text.includes('融資')) {
    return 'business';
  }
  
  // 預設為熱門焦點
  return 'hot';
}

// 生成記者風格摘要
function generateJournalistSummary(tweets, blocked) {
  if (blocked) {
    return `本輪抓取受阻：${blocked}。已維持同版型產出，待服務恢復後自動補齊。`;
  }
  
  if (!tweets || tweets.length === 0) {
    return '本輪未收集到相關推文，可能為低活躍時段或資料源暫時不可用。';
  }
  
  const topTweet = tweets[0];
  const totalEngagement = tweets.reduce((sum, t) => sum + (t.engagement || 0), 0);
  const avgEngagement = Math.round(totalEngagement / tweets.length);
  
  // 找出最活躍的作者
  const authorCounts = {};
  tweets.forEach(t => {
    const author = t.authorHandle || t.authorName || 'Unknown';
    authorCounts[author] = (authorCounts[author] || 0) + 1;
  });
  const topAuthor = Object.entries(authorCounts)
    .sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A';
  
  return `過去 3 小時 X 平台共收集 ${tweets.length} 條熱門推文，總互動數 ${totalEngagement.toLocaleString()}，` +
    `平均每則 ${avgEngagement.toLocaleString()} 互動。最活躍話題來自 ${topAuthor}，` +
    `熱度最高貼文為「${(topTweet.text || '').substring(0, 30)}...」（${topTweet.engagement || 0} 互動）。`;
}

// 生成三行洞察
function generateInsights(tweets, blocked) {
  if (blocked) {
    return [
      `本輪受技術限制無法完整讀取 X 貼文列表：${blocked}`,
      '已維持同版型產出，方便對照與後續補抓。',
      '建議檢查 CDP/登入狀態並補充 API 額度後，再以同流程重跑。'
    ];
  }
  
  if (!tweets || tweets.length === 0) {
    return [
      '本輪未收集到可分析推文，可能為時段性或技術性因素。',
      '建議檢查資料源連線狀態，或稍後重試。',
      '已維持同版型產出，確保監測流程不中斷。'
    ];
  }
  
  // 分析各分類數量
  const categoryCounts = {};
  tweets.forEach(t => {
    const cat = categorizeTweet(t);
    categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
  });
  const topCategory = Object.entries(categoryCounts)
    .sort((a, b) => b[1] - a[1])[0];
  
  // 分析互動趨勢
  const highEngagement = tweets.filter(t => (t.engagement || 0) > 1000).length;
  
  return [
    `內容分佈：${topCategory[1]} 則推文屬於「${DEFAULT_CATEGORIES.find(c => c.id === topCategory[0])?.name || topCategory[0]}」類別，佔總數 ${Math.round(topCategory[1]/tweets.length*100)}%。`,
    `互動熱度：${highEngagement} 則推文互動數超過 1000，顯示話題具有一定傳播力。`,
    `建議追蹤：關注高互動貼文後續發展，適時參與相關討論。`
  ];
}

// HTML 模板
function generateHTML(tweets, timestamp, blocked, blockedReason) {
  const dateStr = timestamp.replace(/[-:]/g, '').slice(0, 12);
  const displayTime = `${timestamp.slice(0, 4)}-${timestamp.slice(4, 6)}-${timestamp.slice(6, 8)} ${timestamp.slice(9, 11)}:${timestamp.slice(11, 13)}`;
  
  // 分類推文
  const categorized = {};
  DEFAULT_CATEGORIES.forEach(c => categorized[c.id] = []);
  
  if (!blocked && tweets) {
    tweets.forEach((t, idx) => {
      const cat = categorizeTweet(t);
      if (categorized[cat]) {
        categorized[cat].push({ ...t, lineNum: idx + 1 });
      }
    });
  }
  
  const summary = generateJournalistSummary(tweets, blocked);
  const insights = generateInsights(tweets, blocked);
  
  // 生成分類 HTML
  let categoriesHTML = '';
  DEFAULT_CATEGORIES.forEach(cat => {
    const items = categorized[cat.id] || [];
    let contentHTML;
    
    if (items.length === 0) {
      contentHTML = '<div class="empty-category">本輪無此類別貼文</div>';
    } else {
      contentHTML = items.map((item, idx) => {
        const lineId = `L${item.lineNum}`;
        const copyText = `${item.text}\n${item.url}`;
        return `
        <div class="tweet-item" id="${lineId}" data-copy="${escapeHtml(copyText)}">
          <div class="tweet-line">
            <a class="line-num" href="#${lineId}" data-line="${item.lineNum}">${String(item.lineNum).padStart(2, '0')}</a>
            <span class="tweet-text">${escapeHtml(item.text || '')}</span>
          </div>
          <div class="tweet-meta">
            <span class="tweet-author">${escapeHtml(item.authorName || 'Unknown')}</span>
            <a class="tweet-id" href="${item.url}" target="_blank" rel="noopener">(${item.tweetId})</a>
            <span class="tweet-stats">❤️ ${item.likes || 0} 🔄 ${item.retweets || 0} 💬 ${item.replies || 0}</span>
          </div>
        </div>`;
      }).join('');
    }
    
    categoriesHTML += `
    <section class="category-section">
      <h2 class="category-title">${cat.emoji} ${cat.name}</h2>
      <div class="category-content">${contentHTML}</div>
    </section>`;
  });
  
  // 阻擋提示
  const blockedBanner = blocked ? `
    <div class="blocked-banner">⚠️ 資料來源受阻：${escapeHtml(blockedReason || blocked)}。已維持同版型產出，待服務恢復後自動補齊。</div>
  ` : '';
  
  return `<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>📋 X 動態摘要（過去 3 小時） | OpenClaw</title>
    <style>
        :root {
            --bg: #0a0e1a;
            --card: #111827;
            --card-hover: #1a2332;
            --text: #e5e7eb;
            --text-muted: #9ca3af;
            --accent: #60a5fa;
            --accent-cyan: #22d3ee;
            --accent-pink: #f472b6;
            --border: #1f2937;
            --line-num: #6b7280;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans TC', sans-serif;
            line-height: 1.7;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        header {
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }
        h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .subtitle {
            color: var(--text-muted);
            font-size: 14px;
        }
        .summary {
            margin-top: 16px;
            padding: 16px;
            background: var(--card);
            border-radius: 8px;
            border-left: 3px solid var(--accent);
            font-size: 14px;
            line-height: 1.8;
        }
        .stats {
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 12px;
            padding: 8px 12px;
            background: var(--card);
            border-radius: 6px;
            display: inline-block;
        }
        .blocked-banner {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 14px;
        }
        .category-section {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .category-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tweet-item {
            padding: 12px 0;
            border-bottom: 1px dashed var(--border);
            transition: background 0.2s;
        }
        .tweet-item:last-child {
            border-bottom: none;
        }
        .tweet-item:hover {
            background: var(--card-hover);
            margin: 0 -12px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 6px;
        }
        .tweet-line {
            display: flex;
            gap: 12px;
            margin-bottom: 6px;
        }
        .line-num {
            color: var(--line-num);
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, monospace;
            min-width: 40px;
            cursor: pointer;
            user-select: none;
            text-decoration: none;
        }
        .line-num:hover {
            color: var(--accent-cyan);
            text-decoration: underline;
        }
        .tweet-text {
            flex: 1;
            cursor: pointer;
            color: var(--text);
            word-break: break-word;
        }
        .tweet-text:hover {
            color: var(--accent-cyan);
        }
        .tweet-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-left: 52px;
            font-size: 13px;
            flex-wrap: wrap;
        }
        .tweet-author {
            color: var(--accent);
            font-weight: 500;
        }
        .tweet-id {
            color: var(--accent-pink);
            text-decoration: none;
            font-family: ui-monospace, monospace;
        }
        .tweet-id:hover {
            text-decoration: underline;
        }
        .tweet-stats {
            color: var(--text-muted);
        }
        .empty-category {
            color: var(--text-muted);
            font-style: italic;
            padding: 12px 0;
        }
        .insights-section {
            background: linear-gradient(135deg, var(--card) 0%, #1a2744 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-top: 24px;
        }
        .insights-section h2 {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent-cyan);
        }
        .insights-list {
            margin: 0;
            padding-left: 20px;
        }
        .insights-list li {
            margin-bottom: 8px;
            color: var(--text);
        }
        .insights-list li:last-child {
            margin-bottom: 0;
        }
        .footer {
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 13px;
            text-align: center;
        }
        .toast {
            position: fixed;
            right: 16px;
            bottom: 16px;
            background: #111827;
            color: #e5e7eb;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 13px;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            border: 1px solid var(--border);
        }
        .toast.show {
            opacity: 1;
        }
        @media (max-width: 640px) {
            body { padding: 12px; }
            .category-section { padding: 16px; }
            .tweet-meta { margin-left: 0; margin-top: 8px; }
            .tweet-line { flex-direction: column; gap: 4px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 X 動態摘要（過去 3 小時）</h1>
            <div class="subtitle">最後更新：${displayTime} (Asia/Taipei)</div>
            <div class="stats">共收集 ${tweets?.length || 0} 條推文，精選 ${tweets?.filter(t => (t.engagement || 0) > 100).length || 0} 條摘要</div>
            <div class="summary">${escapeHtml(summary)}</div>
        </header>
        
        ${blockedBanner}
        ${categoriesHTML}
        
        <section class="insights-section">
            <h2>💡 三行洞察</h2>
            <ol class="insights-list">
                ${insights.map(i => `<li>${escapeHtml(i)}</li>`).join('')}
            </ol>
        </section>
        
        <footer class="footer">
            <p>OpenClaw X 平台智能分析 · 每3小時自動更新</p>
            <p style="margin-top: 8px; font-size: 12px;">
                互動操作：點擊文字複製內容+原文連結 · 點擊行號複製 highlight 連結 · 點擊 tweet_id 跳轉原貼文
            </p>
        </footer>
    </div>
    
    <div class="toast" id="toast">已複製</div>
    
    <script>
        const toast = document.getElementById('toast');
        
        function showToast(msg) {
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 1500);
        }
        
        async function copyText(text) {
            try {
                await navigator.clipboard.writeText(text);
                showToast('已複製');
            } catch (e) {
                showToast('複製失敗');
            }
        }
        
        // 點擊行號：複製 highlight 連結
        document.querySelectorAll('.line-num').forEach(el => {
            el.addEventListener('click', async (e) => {
                e.preventDefault();
                const lineId = el.closest('.tweet-item').id;
                const url = location.origin + location.pathname + '#' + lineId;
                history.replaceState(null, '', '#' + lineId);
                await copyText(url);
            });
        });
        
        // 點擊文字：複製文字+原文連結
        document.querySelectorAll('.tweet-text').forEach(el => {
            el.addEventListener('click', async () => {
                const item = el.closest('.tweet-item');
                const text = item.dataset.copy;
                await copyText(text);
            });
        });
    </script>
</body>
</html>`;
}

// Markdown 生成
function generateMarkdown(tweets, timestamp, blocked, blockedReason) {
  const displayTime = `${timestamp.slice(0, 4)}-${timestamp.slice(4, 6)}-${timestamp.slice(6, 8)} ${timestamp.slice(9, 11)}:${timestamp.slice(11, 13)}`;
  
  // 分類推文
  const categorized = {};
  DEFAULT_CATEGORIES.forEach(c => categorized[c.id] = []);
  
  if (!blocked && tweets) {
    tweets.forEach((t, idx) => {
      const cat = categorizeTweet(t);
      if (categorized[cat]) {
        categorized[cat].push({ ...t, lineNum: idx + 1 });
      }
    });
  }
  
  const summary = generateJournalistSummary(tweets, blocked);
  const insights = generateInsights(tweets, blocked);
  
  let md = `# 📋 X 動態摘要（過去 3 小時）\n\n`;
  md += `**最後更新：** ${displayTime} (Asia/Taipei)\n\n`;
  md += `**統計：** 共收集 ${tweets?.length || 0} 條推文\n\n`;
  md += `---\n\n`;
  
  if (blocked) {
    md += `> ⚠️ **資料來源受阻：** ${blockedReason || blocked}\n\n`;
  }
  
  md += `## 📝 記者摘要\n\n${summary}\n\n`;
  
  // 分類內容
  md += `## 📂 分類摘要\n\n`;
  DEFAULT_CATEGORIES.forEach(cat => {
    const items = categorized[cat.id] || [];
    md += `### ${cat.emoji} ${cat.name}\n\n`;
    if (items.length === 0) {
      md += `_本輪無此類別貼文_\n\n`;
    } else {
      items.forEach(item => {
        md += `**${item.lineNum}.** ${item.text || ''}\n`;
        md += `> 👤 ${item.authorName || 'Unknown'} · [(${item.tweetId})](${item.url}) · ❤️ ${item.likes || 0} 🔄 ${item.retweets || 0}\n\n`;
      });
    }
  });
  
  // 三行洞察
  md += `## 💡 三行洞察\n\n`;
  insights.forEach((insight, idx) => {
    md += `${idx + 1}. ${insight}\n`;
  });
  md += `\n`;
  
  md += `---\n\n`;
  md += `*OpenClaw X 平台智能分析 · 每3小時自動更新*\n`;
  
  return md;
}

// HTML 跳脫
function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 主函數
async function main() {
  const now = new Date();
  const timestamp = now.toISOString()
    .replace(/[-:]/g, '')
    .replace(/\..*/, '')
    .replace('T', '_');
  
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 5).replace(':', '');
  
  // 確保輸出目錄存在
  const webDir = path.join('/Users/user/reports/web');
  const mdDir = path.join('/Users/user/reports');
  
  [webDir, mdDir].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
  
  // 嘗試讀取最新資料
  let tweets = [];
  let blocked = null;
  let blockedReason = null;
  
  try {
    // 查找最新的 x_top_raw 檔案
    const dataDir = '/Users/user/data';
    const files = fs.readdirSync(dataDir)
      .filter(f => f.startsWith('x_top_raw_') && f.endsWith('.json'))
      .map(f => ({ name: f, time: fs.statSync(path.join(dataDir, f)).mtime }))
      .sort((a, b) => b.time - a.time);
    
    if (files.length > 0) {
      const latestFile = path.join(dataDir, files[0].name);
      const data = JSON.parse(fs.readFileSync(latestFile, 'utf8'));
      
      if (Array.isArray(data) && data.length > 0) {
        tweets = data;
        console.log(`✅ 載入 ${tweets.length} 條推文從 ${files[0].name}`);
      } else if (data.status === 'blocked' || data.blocked) {
        blocked = data.blocked || '資料來源受阻';
        blockedReason = data.errors?.join('; ') || blocked;
        console.log(`⚠️ 資料受阻: ${blockedReason}`);
      } else {
        blocked = '無可用資料';
        blockedReason = '資料檔案為空或格式不符';
        console.log('⚠️ 資料檔案為空');
      }
    } else {
      blocked = '找不到資料檔案';
      blockedReason = '未找到 x_top_raw_*.json 檔案';
      console.log('⚠️ 未找到資料檔案');
    }
  } catch (err) {
    blocked = '讀取資料失敗';
    blockedReason = err.message;
    console.error('❌ 讀取資料失敗:', err.message);
  }
  
  // 產生檔案名稱
  const htmlFile = path.join(webDir, `x_monitor_${dateStr}_${timeStr}.html`);
  const mdFile = path.join(mdDir, `x_monitor_${dateStr}_${timeStr}.md`);
  
  // 生成並寫入 HTML
  const html = generateHTML(tweets, timestamp, blocked, blockedReason);
  fs.writeFileSync(htmlFile, html, 'utf8');
  console.log(`✅ HTML 已產出: ${htmlFile}`);
  
  // 生成並寫入 Markdown
  const md = generateMarkdown(tweets, timestamp, blocked, blockedReason);
  fs.writeFileSync(mdFile, md, 'utf8');
  console.log(`✅ Markdown 已產出: ${mdFile}`);
  
  // 輸出摘要
  console.log('\n📊 報告摘要:');
  console.log(`  - 推文數: ${tweets.length}`);
  console.log(`  - 狀態: ${blocked ? '受阻' : '正常'}`);
  if (blocked) {
    console.log(`  - 原因: ${blockedReason}`);
  }
  console.log(`\n📁 輸出檔案:`);
  console.log(`  - HTML: ${htmlFile}`);
  console.log(`  - MD: ${mdFile}`);
  
  return { htmlFile, mdFile, tweets, blocked };
}

// 執行
main().catch(err => {
  console.error('❌ 執行失敗:', err);
  process.exit(1);
});
