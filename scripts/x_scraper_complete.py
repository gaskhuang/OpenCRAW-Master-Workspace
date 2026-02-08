#!/usr/bin/env python3
"""
X/Twitter Scraper for G大
使用 Playwright 爬取 X 的 AI/自動化相關帖子
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
from playwright.async_api import async_playwright, Page

# 設定
OUTPUT_DIR = Path.home() / "memory" / "daily-reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 搜尋關鍵字
SEARCH_QUERIES = [
    "AI automation",
    "OpenClaw",
    "Google Apps Script",
    "LLM",
    "Claude AI",
    "GPT",
    "artificial intelligence"
]

class XScraper:
    def __init__(self):
        self.results = {}
        
    async def search_and_scrape(self, page: Page, query: str) -> List[Dict[str, Any]]:
        """搜尋並爬取帖子"""
        print(f"🔍 正在搜尋: {query}")
        
        try:
            # 訪問 X 搜尋頁面
            encoded_query = query.replace(" ", "%20")
            url = f"https://x.com/search?q={encoded_query}&src=typed_query&f=live"
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(5)
            
            # 滾動載入更多內容
            for _ in range(5):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(2)
            
            # 提取帖子
            posts = await page.evaluate("""
                () => {
                    const articles = document.querySelectorAll('article[data-testid="tweet"]');
                    const results = [];
                    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
                    
                    articles.forEach((article) => {
                        try {
                            const timeEl = article.querySelector('time');
                            if (!timeEl) return;
                            
                            const postTime = new Date(timeEl.getAttribute('datetime'));
                            if (postTime < oneDayAgo) return;
                            
                            const userEl = article.querySelector('a[href^="/"]');
                            const contentEl = article.querySelector('[data-testid="tweetText"]');
                            const linkEl = article.querySelector('a[href*="/status/"]');
                            
                            // 獲取互動數據
                            const stats = article.querySelectorAll('[data-testid$="count"]');
                            let likes = 0, replies = 0, reposts = 0;
                            
                            stats.forEach(stat => {
                                const text = stat.textContent || '';
                                if (stat.closest('[data-testid="like"]')) likes = text;
                                if (stat.closest('[data-testid="reply"]')) replies = text;
                                if (stat.closest('[data-testid="retweet"]')) reposts = text;
                            });
                            
                            if (userEl && contentEl) {
                                results.push({
                                    username: userEl.textContent.trim().replace('@', ''),
                                    content: contentEl.textContent.trim(),
                                    time: timeEl.getAttribute('datetime'),
                                    likes: likes,
                                    replies: replies,
                                    reposts: reposts,
                                    post_url: linkEl ? 'https://x.com' + linkEl.getAttribute('href') : ''
                                });
                            }
                        } catch (e) {}
                    });
                    
                    return results;
                }
            """)
            
            print(f"✅ {query}: 找到 {len(posts)} 篇24小時內的帖子")
            return posts
            
        except Exception as e:
            print(f"❌ {query} 爬取失敗: {e}")
            return []
    
    async def run(self):
        """執行完整爬取流程"""
        print("🚀 啟動 X/Twitter 爬蟲...")
        print(f"📅 抓取範圍: 過去 24 小時")
        print(f"📂 輸出目錄: {OUTPUT_DIR}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            
            page = await context.new_page()
            
            # 訪問 X 首頁確認登入狀態
            print("🔐 檢查 X 登入狀態...")
            await page.goto("https://x.com", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 檢查是否已登入
            current_url = page.url
            if "login" in current_url or "i/flow" in current_url:
                print("⚠️ 需要登入 X，請手動登入後重試")
                print("   已打開瀏覽器視窗，請完成登入")
                await asyncio.sleep(60)  # 等待用戶登入
            
            # 爬取每個搜尋關鍵字
            for query in SEARCH_QUERIES:
                posts = await self.search_and_scrape(page, query)
                self.results[query] = posts
                await asyncio.sleep(3)
            
            await browser.close()
        
        # 保存結果
        await self.save_results()
        
    async def save_results(self):
        """保存結果"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # JSON 格式
        json_path = OUTPUT_DIR / f"{timestamp}-x-raw.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # HTML 報告
        html_path = OUTPUT_DIR / f"{timestamp}-x-report.html"
        self.generate_html_report(html_path, timestamp)
        
        print(f"\n✅ X 爬取完成！")
        print(f"📄 JSON: {json_path}")
        print(f"🌐 HTML: {html_path}")
        
    def generate_html_report(self, path: Path, timestamp: str):
        """生成 HTML 報告"""
        html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X/Twitter 爬取報告 - {timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #1da1f2 0%, #14171a 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            padding: 20px;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .query-section {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .query-title {{
            font-size: 1.3em;
            color: #1da1f2;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #1da1f2;
        }}
        .post {{
            padding: 15px;
            margin-bottom: 15px;
            background: #f7f9fa;
            border-radius: 12px;
            border-left: 4px solid #1da1f2;
        }}
        .post-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        .username {{ font-weight: 600; color: #1da1f2; }}
        .time {{ color: #657786; }}
        .content {{
            color: #14171a;
            line-height: 1.6;
            white-space: pre-wrap;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            font-size: 0.85em;
            color: #657786;
        }}
        .stat {{ display: flex; align-items: center; gap: 5px; }}
        .no-posts {{
            text-align: center;
            color: #657786;
            padding: 30px;
            font-style: italic;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 X/Twitter 爬取報告</h1>
            <div>{timestamp} · AI/自動化/科技動態</div>
        </div>
"""
        
        for query, posts in self.results.items():
            post_count = len(posts)
            html += f"""
        <div class="query-section">
            <h2 class="query-title">🔍 {query} ({post_count} 篇)</h2>
"""
            if posts:
                for post in posts:
                    html += f"""
            <div class="post">
                <div class="post-header">
                    <span class="username">@{post.get('username', 'unknown')}</span>
                    <span class="time">{post.get('time', '')}</span>
                </div>
                <div class="content">{post.get('content', '')}</div>
                <div class="stats">
                    <span class="stat">💬 {post.get('replies', 0)}</span>
                    <span class="stat">🔄 {post.get('reposts', 0)}</span>
                    <span class="stat">❤️ {post.get('likes', 0)}</span>
                </div>
            </div>
"""
            else:
                html += '<div class="no-posts">暫無24小時內的新帖子</div>'
            
            html += '</div>'
        
        html += f"""
        <div class="footer">
            <p>由小龍蝦 🦞 自動生成 · OpenClaw</p>
            <p>生成時間: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

async def main():
    scraper = XScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
