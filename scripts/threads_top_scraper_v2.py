#!/usr/bin/env python3
"""
Threads Top/For You Feed Scraper v2
使用 Playwright 連接到已登入的 Chrome 或啟動新瀏覽器
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
        self.blocked_reason: str = ""
        
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
    
    def _parse_number(self, val) -> Optional[int]:
        """解析數字（處理萬/千/K/M 單位）"""
        if val is None:
            return None
        try:
            s = str(val).strip().replace(',', '').lower()
            if not s:
                return None
            # 處理 萬/千
            if '萬' in s:
                return int(float(s.replace('萬', '')) * 10000)
            elif '千' in s:
                return int(float(s.replace('千', '')) * 1000)
            # 處理 k/m
            elif s.endswith('k'):
                return int(float(s[:-1]) * 1000)
            elif s.endswith('m'):
                return int(float(s[:-1]) * 1000000)
            elif s.isdigit():
                return int(s)
            return None
        except:
            return None
    
    async def scrape_with_cdp(self, scroll_times: int = 80) -> List[ThreadsPost]:
        """使用 CDP 連接到現有 Chrome"""
        print("🔌 嘗試連接到現有 Chrome (CDP port 18792)...")
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.connect_over_cdp('http://127.0.0.1:18792')
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                page = context.pages[0] if context.pages else await context.new_page()
                
                print("✅ 已連接到現有 Chrome")
                return await self._scrape_page(page, scroll_times)
                
            except Exception as e:
                print(f"⚠️ CDP 連接失敗: {e}")
                return []
    
    async def scrape_with_new_browser(self, scroll_times: int = 80, headless: bool = False) -> List[ThreadsPost]:
        """啟動新瀏覽器進行抓取"""
        print(f"🌐 啟動新瀏覽器 (headless={headless})...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=headless,
                executable_path=CHROME_PATH if Path(CHROME_PATH).exists() else None,
                args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # 注入腳本隱藏自動化標記
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            """)
            
            page = await context.new_page()
            
            try:
                result = await self._scrape_page(page, scroll_times)
            finally:
                await browser.close()
                
            return result
    
    async def _scrape_page(self, page: Page, scroll_times: int = 80) -> List[ThreadsPost]:
        """在給定頁面上執行抓取"""
        # 訪問 Threads 首頁
        print("🌐 訪問 Threads.net...")
        try:
            await page.goto("https://www.threads.net", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
        except Exception as e:
            self.blocked_reason = f"頁面載入失敗: {e}"
            print(f"❌ {self.blocked_reason}")
            return []
        
        current_url = page.url
        print(f"📍 當前頁面: {current_url}")
        
        # 檢查是否需要登入
        content = await page.content()
        content_lower = content.lower()
        
        if 'login' in current_url.lower() or 'accounts' in current_url.lower():
            self.blocked_reason = "Threads 需要登入"
            print(f"⚠️ {self.blocked_reason}")
            return []
        
        if 'something went wrong' in content_lower:
            self.blocked_reason = "Threads 頁面錯誤"
            print(f"⚠️ {self.blocked_reason}")
            return []
        
        # 嘗試切換到 For You 視圖
        print("🔍 尋找 For You / 為你推薦 視圖...")
        try:
            # 尋找 "為你推薦" 或 "For You" 按鈕
            selectors = [
                'text=為你推薦',
                'text=For you',
                'text=For You',
                '[role="tab"]:has-text("為你推薦")',
                '[role="tab"]:has-text("For you")',
            ]
            
            for sel in selectors:
                btn = await page.query_selector(sel)
                if btn:
                    await btn.click()
                    print(f"✅ 已點擊: {sel}")
                    await asyncio.sleep(2)
                    break
        except Exception as e:
            print(f"⚠️ 無法切換視圖: {e}")
        
        # 滾動並收集帖子
        print(f"📜 開始滾動 {scroll_times} 次...")
        all_rows = []
        
        for i in range(scroll_times):
            # 提取當前可見帖子
            posts = await self._extract_posts_js(page)
            all_rows.extend(posts)
            
            # 滾動
            await page.mouse.wheel(0, 1200)
            await asyncio.sleep(1.2)
            
            if (i + 1) % 20 == 0:
                print(f"  已滾動 {i + 1}/{scroll_times} 次，收集 {len(all_rows)} 條記錄")
        
        print(f"✅ 滾動完成，總共收集 {len(all_rows)} 條記錄")
        
        # 去重
        dedup = {}
        for r in all_rows:
            pid = r.get('post_id')
            if pid:
                dedup[pid] = r
        
        print(f"📝 去重後: {len(dedup)} 篇唯一帖子")
        
        # 轉換為對象
        threads_posts = []
        now = datetime.now(timezone.utc).isoformat()
        
        for pid, r in dedup.items():
            threads_posts.append(ThreadsPost(
                post_id=pid,
                author=r.get('author', ''),
                author_username=r.get('author_username', ''),
                created_at=r.get('created_at', ''),
                text=r.get('text', ''),
                like_count=self._parse_number(r.get('likes')),
                reply_count=self._parse_number(r.get('replies')),
                repost_count=self._parse_number(r.get('reposts')),
                url=r.get('url', ''),
                scraped_at=now
            ))
        
        return threads_posts
    
    async def _extract_posts_js(self, page: Page) -> List[Dict[str, Any]]:
        """使用 JavaScript 提取帖子"""
        return await page.evaluate("""
            () => {
                const results = [];
                
                // 尋找所有文章元素
                const articles = document.querySelectorAll('article, div[role="article"]');
                
                articles.forEach(article => {
                    try {
                        // 尋找作者連結
                        const authorLinks = article.querySelectorAll('a[href^="/@"]');
                        let username = '';
                        let displayName = '';
                        
                        for (const link of authorLinks) {
                            const href = link.getAttribute('href') || '';
                            const match = href.match(/@([^/]+)/);
                            if (match) {
                                username = match[1];
                                displayName = link.textContent?.trim() || username;
                                break;
                            }
                        }
                        
                        if (!username) return;
                        
                        // 尋找帖子連結
                        const postLinks = article.querySelectorAll('a[href*="/post/"]');
                        let postUrl = '';
                        let postId = '';
                        
                        for (const link of postLinks) {
                            const href = link.getAttribute('href') || '';
                            const match = href.match(/\/post\/([A-Za-z0-9_-]+)/);
                            if (match) {
                                postId = match[1];
                                postUrl = href.startsWith('http') ? href : 'https://www.threads.com' + href;
                                break;
                            }
                        }
                        
                        if (!postId) return;
                        
                        // 尋找時間
                        const timeEl = article.querySelector('time');
                        const createdAt = timeEl ? timeEl.getAttribute('datetime') : '';
                        
                        // 尋找內容 - 多種策略
                        let text = '';
                        
                        // 策略 1: 尋找 data-pressable-container 內的文本
                        const pressableSpans = article.querySelectorAll('[data-pressable-container="true"] span, [data-pressable-container="true"] div');
                        for (const el of pressableSpans) {
                            const txt = el.textContent?.trim() || '';
                            if (txt.length > text.length && !txt.includes('@' + username)) {
                                text = txt;
                            }
                        }
                        
                        // 策略 2: 尋找特定 class 的 div
                        if (!text) {
                            const contentDivs = article.querySelectorAll('div[dir="auto"], span[class*="text"], div[class*="content"]');
                            for (const el of contentDivs) {
                                const txt = el.textContent?.trim() || '';
                                if (txt.length > text.length && txt.length < 5000) {
                                    text = txt;
                                }
                            }
                        }
                        
                        // 尋找互動數
                        let likes = null;
                        let replies = null;
                        let reposts = null;
                        
                        // 尋找所有可能包含數字的元素
                        const allElements = article.querySelectorAll('button, span, div');
                        const numbers = [];
                        
                        for (const el of allElements) {
                            const txt = el.textContent?.trim() || '';
                            // 匹配純數字或帶單位的數字
                            if (/^[\\d,.]+[\\dkm萬千]?$/i.test(txt)) {
                                const parent = el.parentElement;
                                const parentText = parent?.textContent?.toLowerCase() || '';
                                const ariaLabel = parent?.getAttribute('aria-label')?.toLowerCase() || '';
                                
                                numbers.push({
                                    value: txt,
                                    context: parentText + ' ' + ariaLabel
                                });
                            }
                        }
                        
                        // 簡單啟發式：通常順序是 回覆、轉發、引用、讚
                        if (numbers.length >= 1) replies = numbers[0].value;
                        if (numbers.length >= 2) reposts = numbers[1].value;
                        if (numbers.length >= 3) likes = numbers[3]?.value || numbers[2]?.value;
                        
                        results.push({
                            post_id: postId,
                            author: displayName,
                            author_username: username,
                            created_at: createdAt,
                            text: text,
                            likes: likes,
                            replies: replies,
                            reposts: reposts,
                            url: postUrl
                        });
                    } catch (e) {
                        // 忽略單個帖子錯誤
                    }
                });
                
                return results;
            }
        """)
    
    async def run(self, scroll_times: int = 80):
        """執行完整爬取流程"""
        print("=" * 60)
        print("🚀 啟動 Threads Top Feed 爬蟲 v2")
        print(f"📅 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 滾動次數: {scroll_times}")
        print("=" * 60)
        print()
        
        # 首先嘗試 CDP 連接
        results = await self.scrape_with_cdp(scroll_times)
        
        # 如果失敗，嘗試新瀏覽器
        if not results and not self.blocked_reason:
            print("\n🔄 嘗試使用新瀏覽器...")
            results = await self.scrape_with_new_browser(scroll_times, headless=False)
        
        if not results and not self.blocked_reason:
            self.blocked_reason = "無法提取任何帖子"
        
        # 去重 - 只保留本輪新增的
        self.results = []
        for post in results:
            if post.post_id not in self.seen_ids:
                self.results.append(post)
                self.new_ids.add(post.post_id)
        
        print(f"\n🆕 本輪新增帖子: {len(self.results)}")
        
        # 保存已見 IDs
        self._save_seen_ids()
        
        return self.results
    
    def generate_report(self) -> str:
        """生成 Markdown 報告"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")
        time_display = now.strftime("%Y-%m-%d %H:%M")
        
        report = f"""# Threads 動態深度摘要（過去 3 小時）

> 任務時間：{time_display} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重

## 本輪採集結果
- 本輪新增貼文（去重後）：{len(self.results)}

"""
        
        if self.blocked_reason:
            report += f"""## ⚠️ 抓取受阻
{self.blocked_reason}

"""
        
        if self.results:
            # 依內容自動分類
            categories = self._categorize_posts(self.results)
            
            # 輸出各分類
            line_num = 1
            for cat_name, posts in categories.items():
                if not posts:
                    continue
                report += f"## {cat_name}\n"
                for post in posts:
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
        if len(text) > 100:
            text = text[:97] + "..."
        # 添加作者和互動信息
        author_part = f"@{post.author_username}" if post.author_username else post.author
        engagement = []
        if post.like_count:
            engagement.append(f"{post.like_count}讚")
        if post.reply_count:
            engagement.append(f"{post.reply_count}回")
        
        if engagement:
            return f"「{author_part} {' | '.join(engagement)}」{text}"
        return f"「{author_part}」{text}"
    
    def _generate_journalist_notes(self) -> str:
        """生成記者評註"""
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
        elif self.blocked_reason:
            notes += f"1. **抓取受阻**: {self.blocked_reason}\n"
            notes += "2. 建議檢查網絡連接或 Threads 登入狀態。\n"
            notes += "3. 可嘗試手動登入後再執行抓取。\n"
        else:
            notes += "1. 本輪新增內容較少，建議稍後重試。\n"
            notes += "2. Threads 演算法推送內容有限。\n"
            notes += "3. 建議擴大追蹤範圍或調整抓取策略。\n"
        
        return notes + "\n"
    
    def _extract_keywords(self) -> List[str]:
        """提取關鍵詞用於下一輪追蹤"""
        if not self.results:
            return ['AI', '開發', '產品', '設計', '創業']
        
        all_text = ' '.join(p.text for p in self.results)
        keywords = []
        tech_terms = ['AI', 'MCP', 'Claude', 'OpenAI', 'Cursor', '開發', '程式', '創業', '產品', '設計']
        for term in tech_terms:
            if term in all_text:
                keywords.append(term)
        return keywords[:6] if keywords else ['AI', '開發', '產品', '設計', '創業']


async def main():
    scraper = ThreadsTopScraper()
    
    # 執行爬取
    results = await scraper.run(scroll_times=80)
    
    # 生成報告
    report = scraper.generate_report()
    
    # 保存報告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = REPORTS_DIR / f"threads_top_news_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 報告已生成: {report_path}")
    print(f"📊 本輪新增: {len(results)} 篇帖子")
    
    if scraper.blocked_reason:
        print(f"⚠️ 阻塞原因: {scraper.blocked_reason}")
    
    # 輸出摘要
    print("\n" + "=" * 60)
    print(report[:2000] + "..." if len(report) > 2000 else report)


if __name__ == "__main__":
    asyncio.run(main())
