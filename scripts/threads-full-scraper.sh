#!/bin/bash
# Threads 全面爬蟲腳本 - 抓取所有追蹤題目
# 每天早上 8 點執行

set -e

OUTPUT_DIR="$HOME/memory/daily-reports"
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/${DATE}-threads-full-digest.html"
TWO_DAYS_AGO=$(date -v-2d +%Y-%m-%d)

mkdir -p "$OUTPUT_DIR"

echo "🧵 開始抓取 Threads 所有追蹤題目..."
echo "📅 抓取範圍: $TWO_DAYS_AGO 至 $DATE"

# 建立 Playwright 腳本
cat > /tmp/threads-full-scraper.js << 'EOF'
const { chromium } = require('playwright');
const fs = require('fs');

const FEEDS = [
  { name: '為你推薦', selector: 'text=為你推薦' },
  { name: '追蹤中', selector: 'text=追蹤中' },
  { name: 'MCP', selector: 'text=MCP' },
  { name: '徵才', selector: 'text=徵才' },
  { name: 'Elon Musk', selector: 'text=Elon Musk' },
  { name: 'ClaudeAI', selector: 'text=ClaudeAI' },
  { name: '資安', selector: 'text=資安' },
  { name: 'v0', selector: 'text=v0' },
  { name: 'AI程式開發', selector: 'text=AI程式開發' }
];

const TWO_DAYS_MS = 2 * 24 * 60 * 60 * 1000;

async function scrapeFeed(page, feedName) {
  console.log(`📂 正在抓取: ${feedName}`);
  
  // 點擊下拉選單
  await page.click('button:has-text("動態消息")');
  await page.waitForTimeout(1000);
  
  // 選擇題目
  await page.click(`text=${feedName}`);
  await page.waitForTimeout(3000);
  
  // 滾動載入更多內容
  for (let i = 0; i < 5; i++) {
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(2000);
  }
  
  // 抓取帖子
  const posts = await page.evaluate((twoDaysMs) => {
    const articles = document.querySelectorAll('article');
    const results = [];
    const now = Date.now();
    
    articles.forEach((article) => {
      const timeEl = article.querySelector('time');
      if (!timeEl) return;
      
      const postTime = new Date(timeEl.getAttribute('datetime')).getTime();
      const age = now - postTime;
      
      // 只抓兩天內的帖子
      if (age > twoDaysMs) return;
      
      const usernameEl = article.querySelector('a[href^="/@"]');
      const contentEl = article.querySelector('[data-pressable-container="true"] span');
      const likesEl = article.querySelector('[role="button"]');
      
      results.push({
        username: usernameEl ? usernameEl.textContent.trim() : 'Unknown',
        content: contentEl ? contentEl.textContent.trim() : '',
        time: timeEl.getAttribute('datetime'),
        age: Math.floor(age / (1000 * 60 * 60)) + ' hours ago',
        link: usernameEl ? 'https://threads.net' + usernameEl.getAttribute('href') : ''
      });
    });
    
    return results;
  }, TWO_DAYS_MS);
  
  return posts;
}

(async () => {
  const browser = await chromium.launch({
    headless: false,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    userDataDir: '/Users/user/Library/Application Support/Google/Chrome'
  });
  
  const page = await browser.newPage();
  await page.goto('https://www.threads.net', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  
  const allResults = {};
  
  for (const feed of FEEDS) {
    try {
      const posts = await scrapeFeed(page, feed.name);
      allResults[feed.name] = posts;
      console.log(`✅ ${feed.name}: 找到 ${posts.length} 篇帖子`);
    } catch (e) {
      console.error(`❌ ${feed.name} 抓取失敗:`, e.message);
      allResults[feed.name] = [];
    }
    
    // 等待一下避免被 rate limit
    await page.waitForTimeout(3000);
  }
  
  // 儲存結果
  fs.writeFileSync('/tmp/threads-results.json', JSON.stringify(allResults, null, 2));
  
  await browser.close();
  console.log('\n✅ 全部抓取完成！');
})();
EOF

echo "✅ 腳本已建立: /tmp/threads-full-scraper.js"
echo "📊 預計抓取 9 個追蹤題目"
echo "⏰ 每天早上 8 點自動執行"
