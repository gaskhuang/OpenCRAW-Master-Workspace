#!/bin/bash
# Threads 自動爬蟲腳本
# 每天早上抓取 Threads Following 動態

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$HOME/memory/daily-reports"
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/${DATE}-threads-digest.html"

mkdir -p "$OUTPUT_DIR"

echo "🧵 開始抓取 Threads..."

# 使用 Playwright/Puppeteer 腳本抓取內容
# 這裡會由子代理執行具體的瀏覽器操作

cat > /tmp/threads-scraper.js << 'EOF'
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    userDataDir: '/Users/user/Library/Application Support/Google/Chrome',
    args: ['--profile-directory=Default', '--no-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://www.threads.net', { waitUntil: 'networkidle2', timeout: 60000 });
  
  // 等待內容載入
  await page.waitForTimeout(5000);
  
  // 抓取帖子內容
  const posts = await page.evaluate(() => {
    const articles = document.querySelectorAll('article');
    const results = [];
    
    articles.forEach((article, index) => {
      if (index >= 20) return; // 只抓前20篇
      
      const usernameEl = article.querySelector('a[href^="/"]');
      const contentEl = article.querySelector('div[data-pressable-container="true"] span');
      const timeEl = article.querySelector('time');
      
      if (usernameEl && contentEl) {
        results.push({
          username: usernameEl.textContent || '',
          content: contentEl.textContent || '',
          time: timeEl ? timeEl.getAttribute('datetime') : '',
          link: 'https://threads.net' + (usernameEl.getAttribute('href') || '')
        });
      }
    });
    
    return results;
  });
  
  console.log(JSON.stringify(posts, null, 2));
  await browser.close();
})();
EOF

# 檢查是否有相關內容（AI/自動化/OpenClaw/GAS）
filter_relevant_posts() {
  local content="$1"
  local keywords="AI|人工智能|自動化|automation|OpenClaw|Google Apps Script|GAS|LLM|GPT|Claude|機器學習|ML|程式|coding|開發"
  
  if echo "$content" | grep -iE "$keywords" > /dev/null; then
    return 0
  else
    return 1
  fi
}

# 生成 HTML 報告
generate_html() {
  cat > "$OUTPUT_FILE" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Threads 每日摘要 - DATE</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    .header {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }
    .header h1 { font-size: 2.5em; margin-bottom: 10px; }
    .header .date { opacity: 0.9; font-size: 1.1em; }
    .post-card {
      background: white;
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      transition: transform 0.2s;
    }
    .post-card:hover { transform: translateY(-2px); }
    .post-header {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
    }
    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      margin-right: 12px;
    }
    .username {
      font-weight: 600;
      color: #1a1a2e;
    }
    .time {
      font-size: 0.85em;
      color: #888;
      margin-left: auto;
    }
    .content {
      color: #333;
      line-height: 1.6;
      margin-bottom: 12px;
    }
    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .tag {
      background: #f0f0f0;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85em;
      color: #667eea;
    }
    .footer {
      text-align: center;
      color: white;
      margin-top: 30px;
      opacity: 0.8;
    }
    .no-posts {
      text-align: center;
      color: white;
      padding: 40px;
      font-size: 1.2em;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🧵 Threads 每日摘要</h1>
      <div class="date">DATE · G大的科技動態追蹤</div>
    </div>
    <!-- POSTS_PLACEHOLDER -->
    <div class="footer">
      <p>由小龍蝦 🦞 自動生成 · OpenClaw</p>
    </div>
  </div>
</body>
</html>
HTMLEOF

  # 替換日期
  sed -i.bak "s/DATE/$DATE/g" "$OUTPUT_FILE"
  rm -f "$OUTPUT_FILE.bak"
}

# 主程序
echo "✅ Threads 腳本已就緒"
echo "📁 報告將儲存至: $OUTPUT_FILE"

# 未來這裡會加入實際的爬蟲執行邏輯
