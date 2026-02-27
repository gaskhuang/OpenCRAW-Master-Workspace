#!/usr/bin/env python3
"""
自動按 Threads 貼文愛心的腳本
"""
import asyncio
import json
from playwright.async_api import async_playwright

# Threads 貼文連結 (13篇)
POST_URLS = [
    "https://www.threads.net/@fullmoonary2fafa/post/DVOaU8Xj7Ih",
    "https://www.threads.net/@cangyuecai/post/DVPddgqElBK",
    "https://www.threads.net/@evonne_zuan1015/post/DVOAovIktin",
    "https://www.threads.net/@chuchutrainchen/post/DVOZvWckdFv",
    "https://www.threads.net/@wwwss614/post/DVOpoImk2Ah",
    "https://www.threads.net/@darrell_tw_/post/DVNWRHbkbQa",
    "https://www.threads.net/@automoney_n8n/post/DVP0OufEYGR",
    "https://www.threads.net/@zaious0618/post/DVN-SPUge3p",
    "https://www.threads.net/@brainness.ai/post/DVN1vf8kzO0",
    "https://www.threads.net/@ipurpleu__330/post/DVO59drk20q",
    "https://www.threads.net/@jung_i_seul/post/DVPi_Ovkvxe",
    "https://www.threads.net/@mona_luna_shop/post/DVPg2EtDBLi",
    "https://www.threads.net/@s.j_yu.02/post/DVOFq6Yk3oO"
]

# Chrome profile 路徑
CHROME_PROFILE_PATH = "/Users/user/.tmp_threads_profile/Default"

async def like_post(page, url):
    """在單一貼文按愛心"""
    try:
        print(f"\n🔄 正在處理: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)  # 等待頁面載入
        
        # 尋找愛心按鈕（使用多種選擇器）
        like_button_selectors = [
            'svg[aria-label="讚"]',  # 中文
            'svg[aria-label="Like"]',  # 英文
            'svg[aria-label="不讚"]',  # 已按過
            'svg[aria-label="Unlike"]',  # 已按過（英文）
        ]
        
        for selector in like_button_selectors:
            try:
                button = await page.wait_for_selector(selector, timeout=5000)
                if button:
                    # 檢查是否已經按過愛心
                    aria_label = await button.get_attribute('aria-label')
                    if aria_label in ['不讚', 'Unlike']:
                        print(f"  ✅ 已經按過愛心了: {aria_label}")
                        return True
                    
                    # 點擊愛心按鈕
                    await button.click()
                    await asyncio.sleep(2)
                    print(f"  ❤️ 成功按愛心！")
                    return True
            except:
                continue
        
        print(f"  ⚠️ 找不到愛心按鈕")
        return False
        
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")
        return False

async def main():
    """主程式"""
    print("=" * 50)
    print("🦞 Threads 自動按愛心腳本")
    print("=" * 50)
    
    async with async_playwright() as p:
        # 啟動瀏覽器（使用現有 profile）
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE_PATH,
            headless=False,  # 顯示視窗以便確認登入狀態
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = await browser.new_page()
        
        # 先檢查是否已登入
        print("\n🔍 檢查登入狀態...")
        await page.goto("https://www.threads.net/", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # 檢查是否在登入頁面
        if "/login" in page.url or await page.query_selector('input[name="username"]'):
            print("⚠️ 尚未登入 Threads，請先登入！")
            await asyncio.sleep(10)  # 給時間手動登入
        else:
            print("✅ 已登入 Threads")
        
        # 逐一按愛心
        results = []
        for url in POST_URLS:
            success = await like_post(page, url)
            results.append({"url": url, "success": success})
            await asyncio.sleep(2)
        
        # 總結
        print("\n" + "=" * 50)
        print("📊 執行結果")
        print("=" * 50)
        success_count = sum(1 for r in results if r["success"])
        print(f"成功: {success_count}/{len(POST_URLS)}")
        
        for r in results:
            status = "✅" if r["success"] else "❌"
            print(f"{status} {r['url']}")
        
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
