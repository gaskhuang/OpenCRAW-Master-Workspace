#!/usr/bin/env python3
"""簡單測試 - 驗證 Playwright 和瀏覽器環境"""

import asyncio
from playwright.async_api import async_playwright

async def test_browser():
    print("🧪 測試 Playwright 環境...")
    
    async with async_playwright() as p:
        print("✅ Playwright 載入成功")
        
        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=True)
        print("✅ Chromium 啟動成功")
        
        page = await browser.new_page()
        print("✅ 新頁面建立成功")
        
        # 訪問 Threads
        print("🔍 訪問 Threads.net...")
        await page.goto("https://threads.net", wait_until="networkidle")
        title = await page.title()
        print(f"📄 頁面標題: {title}")
        
        # 檢查是否登入
        content = await page.content()
        if "登入" in content or "log in" in content.lower():
            print("⚠️  需要登入 Threads")
        else:
            print("✅ 似乎已登入 Threads")
        
        await browser.close()
        print("✅ 測試完成！環境正常")

if __name__ == "__main__":
    asyncio.run(test_browser())
