#!/usr/bin/env python3
"""
搜索台積電 (TSMC) 在 Threads 上的熱門帖子 - 快速版本
過濾條件：愛心 500+，轉貼 100+，最近兩週
"""
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from playwright.sync_api import sync_playwright, Page, BrowserContext

# 台積電相關關鍵詞
TSMC_KEYWORDS = ["台積電", "TSMC", "tsmc", "台積", "晶圓", "半導體", "2330"]

class TSMCTreadsScraper:
    """台積電 Threads 爬蟲 - 快速版本"""
    
    THREADS_BASE_URL = "https://www.threads.net"
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.seen_posts: Set[str] = set()
        self.posts_data: List[Dict[str, Any]] = []
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def start(self):
        """啟動瀏覽器"""
        print("[*] 啟動瀏覽器...")
        self.playwright = sync_playwright().start()
        
        # 使用臨時目錄
        import tempfile
        user_data_dir = tempfile.mkdtemp(prefix="threads_tsmc_")
        
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=self.headless,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="zh-TW",
            timezone_id="Asia/Taipei",
            args=[
                "--disable-blink-features=AutomationControlled",
            ]
        )
        
        # 注入反檢測腳本
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """)
        
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(30000)
        print("[*] 瀏覽器已啟動")
    
    def stop(self):
        """關閉瀏覽器"""
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
    
    def _extract_post_from_element(self, element_html: str) -> Optional[Dict[str, Any]]:
        """從 HTML 提取貼文資料"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(element_html, 'html.parser')
            
            post = {
                'id': '',
                'post_url': '',
                'author_name': '',
                'author_username': '',
                'text': '',
                'created_time': '',
                'created_timestamp': None,
                'like_count': 0,
                'comment_count': 0,
                'repost_count': 0,
                'scraped_at': datetime.now(timezone.utc).isoformat()
            }
            
            # 提取文字內容
            text_elem = None
            text_selectors = ['span[dir="auto"]', 'div[data-pressable-container="true"] span']
            
            for selector in text_selectors:
                elems = soup.select(selector)
                for elem in elems:
                    text = elem.get_text(strip=True)
                    if len(text) > 15 and not any(x in text.lower() for x in ['like', 'reply', 'repost', '·']):
                        post['text'] = text
                        break
                if post['text']:
                    break
            
            if not post['text']:
                all_text = soup.get_text(separator=' ', strip=True)
                lines = [l.strip() for l in all_text.split('\n') if len(l.strip()) > 15]
                if lines:
                    post['text'] = lines[0][:500]
            
            if not post['text']:
                return None
            
            # 檢查是否與台積電相關
            text_lower = post['text'].lower()
            if not any(kw.lower() in text_lower for kw in TSMC_KEYWORDS):
                return None
            
            # 提取作者
            author_selectors = ['a[href^="/@"]', 'a[href*="/@"] span']
            for selector in author_selectors:
                elem = soup.select_one(selector)
                if elem:
                    href = elem.get('href', '')
                    if href and '/@' in href:
                        match = re.search(r'/@([^/]+)', href)
                        if match:
                            post['author_username'] = match.group(1)
                            post['author_name'] = elem.get_text(strip=True) or post['author_username']
                            break
            
            # 提取互動數
            text_content = soup.get_text()
            
            # Like / 愛心 / 讚
            like_match = re.search(r'(\d+(?:,\d+)*)\s*(?:likes?|讚|like)', text_content, re.IGNORECASE)
            if like_match:
                post['like_count'] = int(like_match.group(1).replace(',', ''))
            
            # Reply / 留言
            reply_match = re.search(r'(\d+(?:,\d+)*)\s*(?:replies?|留言|reply)', text_content, re.IGNORECASE)
            if reply_match:
                post['comment_count'] = int(reply_match.group(1).replace(',', ''))
            
            # Repost / 轉貼
            repost_match = re.search(r'(\d+(?:,\d+)*)\s*(?:reposts?|轉貼|轉發|repost)', text_content, re.IGNORECASE)
            if repost_match:
                post['repost_count'] = int(repost_match.group(1).replace(',', ''))
            
            # 提取貼文 URL 和 ID
            link_elem = soup.find('a', href=lambda x: x and '/post/' in x)
            if link_elem:
                href = link_elem.get('href', '')
                if href:
                    if not href.startswith('http'):
                        post['post_url'] = self.THREADS_BASE_URL + href.split('?')[0]
                    else:
                        post['post_url'] = href.split('?')[0]
                    
                    id_match = re.search(r'/post/([^/?]+)', href)
                    if id_match:
                        post['id'] = id_match.group(1)
            
            # 提取時間
            time_elem = soup.find('time')
            if time_elem:
                post['created_time'] = time_elem.get_text(strip=True) or time_elem.get('datetime', '')
                datetime_attr = time_elem.get('datetime')
                if datetime_attr:
                    try:
                        dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                        post['created_timestamp'] = dt.replace(tzinfo=None)
                    except:
                        pass
            
            if not post['id']:
                import hashlib
                content_hash = hashlib.md5(post['text'][:100].encode()).hexdigest()[:16]
                post['id'] = f"threads_{content_hash}"
            
            if post['id'] in self.seen_posts:
                return None
            
            self.seen_posts.add(post['id'])
            return post
            
        except Exception as e:
            return None
    
    def search_by_keyword(self, keyword: str, max_scrolls: int = 15) -> List[Dict[str, Any]]:
        """使用關鍵字搜索相關帖子 - 快速版本，較少滾動"""
        print(f"[*] 搜索關鍵字: {keyword}")
        
        # 訪問 Threads 並搜索
        url = f"{self.THREADS_BASE_URL}/search?q={keyword}"
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)
        except Exception as e:
            print(f"[!] 搜索頁面載入失敗: {e}")
            return []
        
        posts: List[Dict[str, Any]] = []
        
        for scroll_idx in range(max_scrolls):
            try:
                post_selectors = ['article', '[role="article"]', 'div[data-pressable-container="true"]']
                
                for selector in post_selectors:
                    try:
                        elements = self.page.locator(selector).all()
                        for elem in elements:
                            try:
                                html = elem.inner_html()
                                post = self._extract_post_from_element(html)
                                if post:
                                    posts.append(post)
                                    print(f"  [+] 找到相關貼文: @{post.get('author_username')} | ❤️{post.get('like_count')} | 🔄{post.get('repost_count')} | {post.get('text', '')[:40]}...")
                            except:
                                continue
                    except:
                        continue
                
            except Exception as e:
                pass
            
            self.page.mouse.wheel(0, 2000)
            time.sleep(1.5)
            
            if (scroll_idx + 1) % 5 == 0:
                print(f"[*] 已滾動 {scroll_idx + 1}/{max_scrolls}，收集到 {len(posts)} 篇相關貼文")
        
        return posts
    
    def filter_recent_posts(self, posts: List[Dict], days: int = 14) -> List[Dict]:
        """過濾過去 N 天的帖子"""
        cutoff_date = datetime.now().replace(tzinfo=None) - timedelta(days=days)
        recent_posts = []
        
        for post in posts:
            created_time = post.get('created_time', '')
            timestamp = post.get('created_timestamp')
            
            # 如果有時間戳，使用時間戳
            if timestamp and isinstance(timestamp, datetime):
                if timestamp >= cutoff_date:
                    recent_posts.append(post)
                continue
            
            # 否則使用時間文字判斷
            if created_time:
                # 檢查是否包含 "d" (天)、"w" (週)、"mo" (月) 等
                if any(unit in created_time.lower() for unit in ['mo', 'year', '年']):
                    continue  # 超過一個月，跳過
                if 'w' in created_time.lower():
                    # 檢查週數
                    week_match = re.search(r'(\d+)\s*w', created_time.lower())
                    if week_match:
                        weeks = int(week_match.group(1))
                        if weeks > 2:
                            continue
                recent_posts.append(post)
            else:
                # 沒有時間信息，默認保留
                recent_posts.append(post)
        
        return recent_posts
    
    def filter_by_engagement(self, posts: List[Dict], min_likes: int = 500, min_reposts: int = 100) -> List[Dict]:
        """根據互動數過濾帖子"""
        filtered = []
        for post in posts:
            likes = post.get('like_count', 0)
            reposts = post.get('repost_count', 0)
            
            if likes >= min_likes and reposts >= min_reposts:
                filtered.append(post)
        
        return filtered
    
    def save_results(self, posts: List[Dict], filename: str = None):
        """保存結果到 JSON 文件 - 將 datetime 轉換為字符串"""
        # 處理 datetime 對象
        import copy
        posts_clean = copy.deepcopy(posts)
        for post in posts_clean:
            if isinstance(post.get('created_timestamp'), datetime):
                post['created_timestamp'] = post['created_timestamp'].isoformat()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tsmc_threads_{timestamp}.json"
        
        output_path = Path("/Users/user/data") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts_clean, f, ensure_ascii=False, indent=2)
        
        print(f"[*] 結果已保存: {output_path}")
        return output_path


def main():
    """主函數"""
    print("=" * 70)
    print("🔍 台積電 Threads 熱門帖子搜索工具 - 快速版本")
    print("=" * 70)
    print("篩選條件：")
    print("  - 愛心 (Likes) >= 500")
    print("  - 轉貼 (Reposts) >= 100")
    print("  - 時間：過去兩週")
    print("=" * 70)
    
    scraper = TSMCTreadsScraper(headless=True)
    
    try:
        scraper.start()
        
        all_posts = []
        
        # 使用多個關鍵字搜索 - 減少滾動次數以加快速度
        keywords = ["台積電", "TSMC"]
        
        for keyword in keywords:
            print(f"\n[搜索] 關鍵字: {keyword}")
            posts = scraper.search_by_keyword(keyword, max_scrolls=15)  # 減少到15次滾動
            all_posts.extend(posts)
            time.sleep(2)
        
        # 去重
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            if post['id'] not in seen_ids:
                seen_ids.add(post['id'])
                unique_posts.append(post)
        
        print(f"\n[*] 共收集 {len(unique_posts)} 篇唯一貼文（相關）")
        
        # 過濾過去兩週
        recent_posts = scraper.filter_recent_posts(unique_posts, days=14)
        print(f"[*] 過去兩週的貼文: {len(recent_posts)} 篇")
        
        # 過濾互動數（愛心 500+，轉貼 100+）
        hot_posts = scraper.filter_by_engagement(recent_posts, min_likes=500, min_reposts=100)
        print(f"[*] 符合熱門條件（❤️500+，🔄100+）: {len(hot_posts)} 篇")
        
        # 按愛心數排序
        hot_posts_sorted = sorted(hot_posts, key=lambda x: x.get('like_count', 0), reverse=True)
        
        # 保存結果
        output_file = scraper.save_results(hot_posts_sorted)
        
        # 輸出結果
        print("\n" + "=" * 70)
        print("📋 台積電熱門 Threads 帖子清單（過去兩週）")
        print("=" * 70)
        
        if hot_posts_sorted:
            for i, post in enumerate(hot_posts_sorted, 1):
                url = post.get('post_url', '')
                text = post.get('text', '')[:80]
                author = post.get('author_username') or post.get('author_name', 'Unknown')
                time_text = post.get('created_time', 'Unknown time')
                likes = post.get('like_count', 0)
                reposts = post.get('repost_count', 0)
                comments = post.get('comment_count', 0)
                
                print(f"\n{i}. @{author} | ❤️ {likes:,} | 🔄 {reposts:,} | 💬 {comments:,}")
                print(f"   🕐 {time_text}")
                print(f"   📝 {text}...")
                if url:
                    print(f"   🔗 {url}")
        else:
            print("\n⚠️ 未找到符合條件的熱門貼文")
            print("可能原因:")
            print("- Threads 搜索結果有限")
            print("- 需要登入才能查看更多內容")
            print("- 近期台積電相關熱門討論較少")
        
        print(f"\n[*] 詳細結果已保存: {output_file}")
        
    except KeyboardInterrupt:
        print("\n[!] 用戶中斷")
    except Exception as e:
        print(f"\n[!] 錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.stop()


if __name__ == "__main__":
    main()
