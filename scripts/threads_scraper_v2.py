#!/usr/bin/env python3
"""
Threads Scraper - 使用現有 Chrome Profile
這個版本會使用你已登入的 Chrome 來爬取
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path.home() / "memory" / "daily-reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEEDS = ["MCP", "ClaudeAI", "AI程式開發", "v0", "資安"]

async def scrape_feed(page, feed_name):
    """爬取單個主題"""
    print(f"🔍 爬取: {feed_name}")
    
    try:
        # 訪問搜尋頁面
        query = feed_name.replace(" ", "%20")
        url = f"https://www.threads.com/search?q={query}&serp_type=default&filter=recent"
        
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)
        
        # 滾動載入更多
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(2)
        
        # 提取帖子
        posts = await page.evaluate("""
            () => {
                const articles = document.querySelectorAll('article');
                const results = [];
                const twoDaysAgo = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000);
                
                articles.forEach(article => {
                    const timeEl = article.querySelector('time');
                    if (!timeEl) return;
                    
                    const postTime = new Date(timeEl.getAttribute('datetime'));
                    if (postTime < twoDaysAgo) return;
                    
                    const usernameEl = article.querySelector('a[href^="/@"]');
                    const contentEl = article.querySelector('[data-pressable-container="true"] span');
                    
                    if (usernameEl && contentEl) {
                        results.push({
                            username: usernameEl.textContent.trim(),
                            content: contentEl.textContent.trim(),
                            time: timeEl.getAttribute('datetime'),
                            feed: 'FEED_NAME'
                        });
                    }
                });
                
                return results;
            }
        """.replace('FEED_NAME', feed_name))
        
        print(f"✅ {feed_name}: {len(posts)} 篇")
        return posts
        
    except Exception as e:
        print(f"❌ {feed_name} 失敗: {e}")
        return []

async def main():
    print("🚀 啟動 Threads 爬蟲")
    print(f"📂 輸出: {OUTPUT_DIR}")
    print("")
    
    async with async_playwright() as p:
        # 使用現有 Chrome Profile (這樣就能保持登入狀態)
        browser = await p.chromium.launch_persistent_context(
            user_data_dir='/Users/user/Library/Application Support/Google/Chrome',
            headless=False,  # 設 True 就看不到視窗
            args=['--profile-directory=Default']
        )
        
        page = await browser.new_page()
        
        # 先確認登入狀態
        print("🔐 檢查登入狀態...")
        await page.goto("https://threads.net", wait_until="networkidle")
        await asyncio.sleep(2)
        
        all_posts = []
        
        # 爬取每個主題
        for feed in FEEDS:
            posts = await scrape_feed(page, feed)
            all_posts.extend(posts)
            await asyncio.sleep(2)
        
        await browser.close()
        
        # 保存結果
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        
        # JSON
        json_path = OUTPUT_DIR / f"threads_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 完成！")
        print(f"📄 共 {len(all_posts)} 篇帖子")
        print(f"💾 保存至: {json_path}")

if __name__ == "__main__":
    asyncio.run(main())
