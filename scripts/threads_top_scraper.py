#!/usr/bin/env python3
"""
Threads Top/For You Feed Scraper
爬取 Threads 首頁熱門/為你推薦內容
使用已登入會話 (Chrome Profile)
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, asdict

# Playwright
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# 設定
REPORTS_DIR = Path.home() / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 去重記錄檔
SEEN_IDS_FILE = Path.home() / "reports" / ".threads_monitor_seen_ids.json"

# Chrome 路徑 (macOS)
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


@dataclass
class ThreadsPost:
    post_id: str
    author: str
    author_username: str
    created_at: str
    text: str
    like_count: Optional[int]
    reply_count: Optional[int]
    repost_count: Optional[int]
    url: str
    scraped_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ThreadsTopScraper:
    def __init__(self):
        self.results: List[ThreadsPost] = []
        self.seen_ids: Set[str] = self._load_seen_ids()
        self.new_ids: Set[str] = set()
        
    def _load_seen_ids(self) -> Set[str]:
        """載入已見過的 post_id"""
        if SEEN_IDS_FILE.exists():
            try:
                with open(SEEN_IDS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 只保留最近 7 天的記錄
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return set(pid for pid, ts in data.items() if ts > cutoff)
            except Exception:
                pass
        return set()
    
    def _save_seen_ids(self):
        """保存已見過的 post_id"""
        data = {}
        now = datetime.now().isoformat()
        # 合併舊的和新的
        for pid in self.seen_ids | self.new_ids:
            data[pid] = now
        SEEN_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SEEN_IDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    
    def _extract_post_id_from_url(self, url: str) -> Optional[str]:
        """從 URL 提取 post_id"""
        # 格式: https://www.threads.com/@username/post/ABCD1234
        match = re.search(r'/post/([A-Za-z0-9_-]+)', url)
        return match.group(1) if match else None
    
    async def scroll_page(self, page: Page, times: int = 80, delay: float = 1.5):
        """連續滾動頁面"""
        print(f"📜 開始滾動 {times} 次...")
        for i in range(times):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(delay)
            if (i + 1) % 20 == 0:
                print(f"  已滾動 {i + 1}/{times} 次")
        print(f"✅ 滾動完成 ({times} 次)")
    
    async def extract_posts(self, page: Page) -> List[ThreadsPost]:
        """提取頁面上的所有帖子"""
        print("🔍 提取帖子數據...")
        
        posts = await page.evaluate("""
            () => {
                const results = [];
                const articles = document.querySelectorAll('article, div[role="article"]');
                
                articles.forEach(article => {
                    try {
                        // 提取作者信息
                        const authorLink = article.querySelector('a[href^="/@"]');
                        if (!authorLink) return;
                        
                        const href = authorLink.getAttribute('href');
                        const usernameMatch = href.match(/@([^/]+)/);
                        const username = usernameMatch ? usernameMatch[1] : '';
                        const displayName = authorLink.textContent?.trim() || username;
                        
                        // 提取帖子連結和ID
                        const postLink = article.querySelector('a[href*="/post/"]');
                        if (!postLink) return;
                        
                        const postUrl = postLink.href.startsWith('http') 
                            ? postLink.href 
                            : 'https://www.threads.com' + postLink.getAttribute('href');
                        
                        const postIdMatch = postUrl.match(/\/post\/([A-Za-z0-9_-]+)/);
                        const postId = postIdMatch ? postIdMatch[1] : '';
                        if (!postId) return;
                        
                        // 提取時間
                        const timeEl = article.querySelector('time');
                        const createdAt = timeEl ? timeEl.getAttribute('datetime') : '';
                        
                        // 提取內容 - 多種可能的选择器
                        let text = '';
                        const textSelectors = [
                            '[data-pressable-container="true"] span',
                            'div[class*="text"] span',
                            'div[dir="auto"] span',
                            'span[class*="content"]',
                            'div[role="button"] span'
                        ];
                        
                        for (const selector of textSelectors) {
                            const el = article.querySelector(selector);
                            if (el && el.textContent.trim().length > text.length) {
                                text = el.textContent.trim();
                            }
                        }
                        
                        // 提取互動數據
                        let likes = null;
                        let replies = null;
                        let reposts = null;
                        
                        // 尋找包含數字的按鈕或文本
                        const buttons = article.querySelectorAll('button, span, div');
                        buttons.forEach(btn => {
                            const txt = btn.textContent?.trim() || '';
                            const numMatch = txt.match(/^(\d+[\d,]*(?:\.\d+)?(?:萬|千)?)\s*$/);
                            if (numMatch) {
                                const num = numMatch[1];
                                // 根據上下文判斷是什麼類型
                                const parent = btn.parentElement;
                                const parentText = parent?.textContent?.toLowerCase() || '';
                                
                                if (parentText.includes('讚') || parentText.includes('like')) {
                                    likes = num;
                                } else if (parentText.includes('回覆') || parentText.includes('reply')) {
                                    replies = num;
                                } else if (parentText.includes('轉發') || parentText.includes('repost')) {
                                    reposts = num;
                                }
                            }
                        });
                        
                        results.push({
                            post_id: postId,
                            author: displayName,
                            author_username: username,
                            created_at: createdAt,
                            text: text,
                            like_count: likes,
                            reply_count: replies,
                            repost_count: reposts,
                            url: postUrl
                        });
                    } catch (e) {
                        // 忽略單個帖子的錯誤
                    }
                });
                
                return results;
            }
        """)
        
        # 轉換為對象
        threads_posts = []
        now = datetime.now(timezone.utc).isoformat()
        for p in posts:
            if p.get('post_id'):
                threads_posts.append(ThreadsPost(
                    post_id=p['post_id'],
                    author=p.get('author', ''),
                    author_username=p.get('author_username', ''),
                    created_at=p.get('created_at', ''),
                    text=p.get('text', ''),
                    like_count=self._parse_number(p.get('like_count')),
                    reply_count=self._parse_number(p.get('reply_count')),
                    repost_count=self._parse_number(p.get('repost_count')),
                    url=p.get('url', ''),
                    scraped_at=now
                ))
        
        print(f"✅ 提取到 {len(threads_posts)} 篇帖子")
        return threads_posts
    
    def _parse_number(self, val) -> Optional[int]:
        """解析數字（處理萬/千單位）"""
        if val is None:
            return None
        try:
            s = str(val).strip().replace(',', '')
            if '萬' in s:
                return int(float(s.replace('萬', '')) * 10000)
            elif '千' in s:
                return int(float(s.replace('千', '')) * 1000)
            elif s.isdigit():
                return int(s)
            return None
        except:
            return None
    
    async def run(self, use_logged_in: bool = True, scroll_times: int = 80):
        """執行完整爬取流程"""
        print("🚀 啟動 Threads Top Feed 爬蟲")
        print(f"📅 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 滾動次數: {scroll_times}")
        print(f"🔐 使用登入會話: {use_logged_in}")
        print()
        
        async with async_playwright() as p:
            browser: Optional[Browser] = None
            context: Optional[BrowserContext] = None
            
            try:
                if use_logged_in and Path(CHROME_PATH).exists():
                    # 使用已登入的 Chrome
                    print("🔐 啟動 Chrome (使用 Default profile)...")
                    browser = await p.chromium.launch(
                        headless=False,  # 必須有頭才能使用 profile
                        executable_path=CHROME_PATH,
                        args=[
                            '--profile-directory=Default',
                            '--no-first-run',
                            '--no-default-browser-check'
                        ]
                    )
                    context = browser.contexts[0] if browser.contexts else await browser.new_context()
                else:
                    # 使用無頭瀏覽器（無登入）
                    print("🌐 啟動無頭瀏覽器...")
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        viewport={'width': 1280, 'height': 800},
                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    )
                
                page = await context.new_page()
                
                # 訪問 Threads 首頁
                print("🌐 訪問 Threads.net...")
                await page.goto("https://www.threads.net", wait_until="networkidle")
                await asyncio.sleep(3)
                
                # 檢查是否需要登入
                current_url = page.url
                print(f"📍 當前頁面: {current_url}")
                
                if "login" in current_url.lower() or "accounts" in current_url.lower():
                    print("⚠️ 需要登入。請先手動登入 Threads，或提供 cookies。")
                    # 嘗試無登入模式訪問公開內容
                    print("🔄 嘗試訪問公開內容...")
                    await page.goto("https://www.threads.com/discover", wait_until="networkidle")
                    await asyncio.sleep(3)
                
                # 嘗試切換到 For You / Top 視圖
                print("🔍 尋找 For You / Top 視圖...")
                
                # 尋找並點擊 "為你推薦" 或 "For You"
                try:
                    # 先尋找 "為你推薦" 按鈕
                    for_you_btn = await page.query_selector('text=為你推薦')
                    if not for_you_btn:
                        for_you_btn = await page.query_selector('text=For you')
                    if not for_you_btn:
                        for_you_btn = await page.query_selector('text=For You')
                    
                    if for_you_btn:
                        await for_you_btn.click()
                        print("✅ 已切換到 For You 視圖")
                        await asyncio.sleep(2)
                except Exception as e:
                    print(f"⚠️ 無法切換視圖: {e}")
                
                # 記錄初始帖子
                print("📝 記錄初始帖子...")
                initial_posts = await self.extract_posts(page)
                print(f"   初始帖子數: {len(initial_posts)}")
                
                # 滾動頁面
                await self.scroll_page(page, times=scroll_times, delay=1.5)
                
                # 再次提取所有帖子
                print("📝 提取所有帖子...")
                all_posts = await self.extract_posts(page)
                print(f"   總帖子數: {len(all_posts)}")
                
                # 去重 - 只保留本輪新增的
                new_posts = []
                for post in all_posts:
                    if post.post_id not in self.seen_ids:
                        new_posts.append(post)
                        self.new_ids.add(post.post_id)
                
                print(f"🆕 本輪新增帖子: {len(new_posts)}")
                self.results = new_posts
                
                # 保存已見 IDs
                self._save_seen_ids()
                
            finally:
                if browser:
                    await browser.close()
                    print("🔒 瀏覽器已關閉")
        
        return self.results
    
    def generate_report(self) -> str:
        """生成 Markdown 報告"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")
        time_display = now.strftime("%Y-%m-%d %H:%M")
        
        # 依內容自動分類
        categories = self._categorize_posts(self.results)
        
        report = f"""# Threads 動態深度摘要（過去 3 小時）

> 任務時間：{time_display} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重

## 本輪採集結果
- 本輪新增貼文（去重後）：{len(self.results)}

---

"""
        
        # 輸出各分類
        line_num = 1
        for cat_name, posts in categories.items():
            if not posts:
                continue
            report += f"## {cat_name}\n"
            for post in posts:
                # 生成摘要
                summary = self._generate_summary(post)
                report += f"[{line_num}] {summary} [({post.post_id})]({post.url})\n"
                line_num += 1
            report += "\n"
        
        # 記者評註
        report += self._generate_journalist_notes()
        
        # 風險訊號
        report += """## 風險訊號
- 本輪貼文時間跨度依 Threads 演算法推送決定。
- 互動欄位（按讚/留言）結構化抽取可能有 null 缺值。
- 若 Threads 出現反爬機制，部分內容可能未被完整載入。

"""
        
        # 下一輪追蹤關鍵詞
        keywords = self._extract_keywords()
        report += f"## 下一輪追蹤關鍵詞\n"
        for kw in keywords:
            report += f"- {kw}\n"
        
        return report
    
    def _categorize_posts(self, posts: List[ThreadsPost]) -> Dict[str, List[ThreadsPost]]:
        """自動分類帖子"""
        categories = {
            "科技與開發": [],
            "設計與創意": [],
            "商業與職場": [],
            "生活與娛樂": [],
            "社會與文化": [],
            "其他": []
        }
        
        tech_keywords = ['AI', '程式', '開發', 'code', '工程師', 'app', '軟體', '技術', 'python', 'javascript', 'API', 'MCP', 'LLM', 'GPT', 'Claude', 'Cursor', 'IDE', 'bug', 'debug']
        design_keywords = ['設計', 'UI', 'UX', 'Figma', '設計師', '視覺', '介面', '排版', '配色', 'logo', 'brand']
        business_keywords = ['創業', '產品', 'PM', '管理', '職涯', '面試', '工作', '加薪', '轉職', '副業', '營收', '用戶', '增長']
        life_keywords = ['電影', '劇', '音樂', '遊戲', '美食', '旅行', '運動', 'NBA', '健身', '生活', '日常', '心情', '感情']
        social_keywords = ['政治', '政策', '社會', '教育', '環保', '人權', '平等', '民主', '選舉', '新聞']
        
        for post in posts:
            text_lower = post.text.lower()
            text_zh = post.text
            
            scores = {
                "科技與開發": sum(1 for k in tech_keywords if k.lower() in text_lower or k in text_zh),
                "設計與創意": sum(1 for k in design_keywords if k.lower() in text_lower or k in text_zh),
                "商業與職場": sum(1 for k in business_keywords if k.lower() in text_lower or k in text_zh),
                "生活與娛樂": sum(1 for k in life_keywords if k.lower() in text_lower or k in text_zh),
                "社會與文化": sum(1 for k in social_keywords if k.lower() in text_lower or k in text_zh),
            }
            
            best_cat = max(scores, key=scores.get)
            if scores[best_cat] == 0:
                best_cat = "其他"
            
            categories[best_cat].append(post)
        
        # 移除空類別
        return {k: v for k, v in categories.items() if v}
    
    def _generate_summary(self, post: ThreadsPost) -> str:
        """生成帖子摘要"""
        text = post.text.replace('\n', ' ').strip()
        # 限制長度
        if len(text) > 80:
            text = text[:77] + "..."
        # 添加作者和互動信息
        author_part = f"@{post.author_username}" if post.author_username else post.author
        engagement = []
        if post.like_count:
            engagement.append(f"{post.like_count}讚")
        if post.reply_count:
            engagement.append(f"{post.reply_count}回")
        
        if engagement:
            return f"[{author_part} {' | '.join(engagement)}] {text}"
        return f"[{author_part}] {text}"
    
    def _generate_journalist_notes(self) -> str:
        """生成記者評註"""
        # 根據結果生成評註
        notes = """## 本輪最值得關注的 3 個議題（記者評註）
"""
        if len(self.results) >= 3:
            # 按互動數排序
            sorted_posts = sorted(
                [p for p in self.results if p.like_count],
                key=lambda x: x.like_count or 0,
                reverse=True
            )[:3]
            
            for i, post in enumerate(sorted_posts, 1):
                snippet = post.text[:50] + "..." if len(post.text) > 50 else post.text
                notes += f"{i}. **@{post.author_username}**: {snippet}\n"
        else:
            notes += "1. 本輪新增內容較少，建議稍後重試。\n"
            notes += "2. Threads 演算法推送內容有限。\n"
            notes += "3. 建議擴大追蹤範圍或調整抓取策略。\n"
        
        return notes + "\n"
    
    def _extract_keywords(self) -> List[str]:
        """提取關鍵詞用於下一輪追蹤"""
        # 簡單的關鍵詞提取
        all_text = ' '.join(p.text for p in self.results)
        # 常見科技關鍵詞
        keywords = []
        tech_terms = ['AI', 'MCP', 'Claude', 'OpenAI', 'Cursor', '開發', '程式', '創業', '產品', '設計']
        for term in tech_terms:
            if term in all_text:
                keywords.append(term)
        return keywords[:6] if keywords else ['AI', '開發', '產品', '設計', '創業']


async def main():
    scraper = ThreadsTopScraper()
    
    # 執行爬取
    results = await scraper.run(
        use_logged_in=True,
        scroll_times=80
    )
    
    if not results:
        print("⚠️ 未採集到任何新帖子")
        # 仍然生成報告（空報告）
    
    # 生成報告
    report = scraper.generate_report()
    
    # 保存報告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = REPORTS_DIR / f"threads_top_news_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 報告已生成: {report_path}")
    print(f"📊 本輪新增: {len(results)} 篇帖子")
    
    # 同時輸出到 stdout
    print("\n" + "="*50)
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
