#!/usr/bin/env python3
"""
Threads Scraper for G大
使用 Playwright 爬取 Threads 多個主題的帖子
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

# 要爬取的主題
FEEDS = [
    "MCP",
    "ClaudeAI", 
    "AI程式開發",
    "v0",
    "資安",
    "為你推薦",
    "追蹤中"
]

class ThreadsScraper:
    def __init__(self):
        self.results = {}
        
    async def scrape_feed(self, page: Page, feed_name: str) -> List[Dict[str, Any]]:
        """爬取單個主題的帖子"""
        print(f"🔍 正在搜尋: {feed_name}")
        
        try:
            # 直接訪問搜尋頁面
            encoded_query = feed_name.replace(" ", "%20")
            url = f"https://www.threads.com/search?q={encoded_query}&serp_type=default&filter=recent"
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 滾動載入更多內容
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, 800)")
                await asyncio.sleep(2)
            
            # 提取帖子
            posts = await page.evaluate("""
                () => {
                    const articles = document.querySelectorAll('article');
                    const results = [];
                    const twoDaysAgo = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000);
                    
                    articles.forEach((article) => {
                        const timeEl = article.querySelector('time');
                        if (!timeEl) return;
                        
                        const postTime = new Date(timeEl.getAttribute('datetime'));
                        if (postTime < twoDaysAgo) return;
                        
                        const usernameEl = article.querySelector('a[href^="/@"]');
                        const contentEl = article.querySelector('[data-pressable-container="true"] span');
                        const linkEl = article.querySelector('a[href*="/post/"]');
                        
                        if (usernameEl && contentEl) {
                            results.push({
                                username: usernameEl.textContent.trim(),
                                content: contentEl.textContent.trim(),
                                time: timeEl.getAttribute('datetime'),
                                post_url: linkEl ? 'https://threads.com' + linkEl.getAttribute('href') : ''
                            });
                        }
                    });
                    
                    return results;
                }
            """)
            
            print(f"✅ {feed_name}: 找到 {len(posts)} 篇兩天內的帖子")
            return posts
            
        except Exception as e:
            print(f"❌ {feed_name} 爬取失敗: {e}")
            return []
    
    async def run(self):
        """執行完整爬取流程"""
        print("🚀 啟動 Threads 爬蟲...")
        print(f"📅 抓取範圍: 過去 48 小時")
        print(f"📂 輸出目錄: {OUTPUT_DIR}")
        
        async with async_playwright() as p:
            # 使用 Chrome 設定
            browser = await p.chromium.launch(
                headless=False,  # 設為 True 可隱藏瀏覽器
                args=['--profile-directory=Default'],
                executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800}
            )
            
            page = await context.new_page()
            
            # 先訪問首頁確認登入狀態
            print("🔐 檢查登入狀態...")
            await page.goto("https://threads.net", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 爬取每個主題
            for feed in FEEDS:
                posts = await self.scrape_feed(page, feed)
                self.results[feed] = posts
                await asyncio.sleep(2)  # 避免請求過快
            
            await browser.close()
        
        # 保存結果
        await self.save_results()
        
    async def save_results(self):
        """保存結果為 JSON 和 HTML 報告"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # JSON 格式
        json_path = OUTPUT_DIR / f"{timestamp}-threads-raw.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # HTML 報告
        html_path = OUTPUT_DIR / f"{timestamp}-threads-report.html"
        self.generate_html_report(html_path, timestamp)
        
        print(f"\n✅ 爬取完成！")
        print(f"📄 JSON: {json_path}")
        print(f"🌐 HTML: {html_path}")
        
    def generate_html_report(self, path: Path, timestamp: str):
        """生成 HTML 報告"""
        html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Threads 爬取報告 - {timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        .header .meta {{ opacity: 0.9; }}
        .feed-section {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .feed-title {{
            font-size: 1.5em;
            color: #1a1a2e;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .post {{
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }}
        .post-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        .username {{ font-weight: 600; color: #667eea; }}
        .time {{ color: #888; }}
        .content {{
            color: #333;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        .post-link {{
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-size: 0.85em;
        }}
        .post-link:hover {{ text-decoration: underline; }}
        .no-posts {{
            text-align: center;
            color: #888;
            padding: 30px;
            font-style: italic;
        }}
        .summary {{
            background: rgba(255,255,255,0.1);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .summary h2 {{ margin-bottom: 10px; }}
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
            <h1>🧵 Threads 爬取報告</h1>
            <div class="meta">{timestamp} · G大的科技動態追蹤</div>
        </div>
        
        <div class="summary">
            <h2>📊 爬取摘要</h2>
            <p>總共爬取了 {len(self.results)} 個主題，涵蓋 AI、程式開發、資安等領域。</p>
        </div>
"""
        
        for feed, posts in self.results.items():
            post_count = len(posts)
            html += f"""
        <div class="feed-section">
            <h2 class="feed-title">📌 {feed} ({post_count} 篇)</h2>
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
                {f'<a href="{post.get("post_url", "")}" class="post-link" target="_blank">查看原文 →</a>' if post.get('post_url') else ''}
            </div>
"""
            else:
                html += '<div class="no-posts">暫無兩天內的新帖子</div>'
            
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
    scraper = ThreadsScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
