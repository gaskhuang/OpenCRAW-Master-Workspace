#!/usr/bin/env python3
"""
搜索黃國昌 (KC Huang) 在 Threads 上的帖子
抓取過去兩週的留言並列出所有 Post 連結
"""
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from playwright.sync_api import sync_playwright, Page, BrowserContext

# 黃國昌的 Threads 帳號
TARGET_USERNAME = "kc_huang"  # 常見的帳號格式
TARGET_NAMES = ["黃國昌", "黃國昌", "KC Huang", "kc_huang"]

class KCThreadsScraper:
    """黃國昌 Threads 爬蟲"""
    
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
        user_data_dir = tempfile.mkdtemp(prefix="threads_kc_")
        
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
            like_match = re.search(r'(\d+(?:,\d+)*)\s*(?:likes?|讚)', text_content, re.IGNORECASE)
            if like_match:
                post['like_count'] = int(like_match.group(1).replace(',', ''))
            
            reply_match = re.search(r'(\d+(?:,\d+)*)\s*(?:replies?|留言)', text_content, re.IGNORECASE)
            if reply_match:
                post['comment_count'] = int(reply_match.group(1).replace(',', ''))
            
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
    
    def search_user_by_name(self, name: str) -> Optional[str]:
        """搜索用戶並返回用戶名"""
        print(f"[*] 搜索用戶: {name}")
        
        # 嘗試直接訪問常見的帳號
        possible_usernames = [
            "kc_huang",
            "huang.kc",
            "kc_huang_tw",
            "kc_huang_2024",
        ]
        
        # 先嘗試直接訪問 kc_huang
        for username in possible_usernames[:2]:
            try:
                url = f"{self.THREADS_BASE_URL}/@{username}"
                print(f"[*] 嘗試訪問: {url}")
                self.page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                
                # 檢查頁面是否存在
                page_text = self.page.locator('body').inner_text()
                if "Page Not Found" in page_text or "Sorry, this page" in page_text:
                    print(f"  [!] {username} 不存在")
                    continue
                
                # 檢查是否包含 "黃國昌"
                if "黃國昌" in page_text or "KC" in page_text or "國昌" in page_text:
                    print(f"  [✓] 找到用戶: @{username}")
                    return username
                    
            except Exception as e:
                print(f"  [!] 訪問失敗: {e}")
                continue
        
        return None
    
    def scrape_user_profile(self, username: str, max_scrolls: int = 50) -> List[Dict[str, Any]]:
        """抓取指定用戶的 Threads"""
        print(f"[*] 開始抓取 @{username} 的帖子...")
        
        url = f"{self.THREADS_BASE_URL}/@{username}"
        try:
            self.page.goto(url, wait_until="networkidle", timeout=60000)
            time.sleep(5)
        except Exception as e:
            print(f"[!] 頁面載入失敗: {e}")
            return []
        
        posts: List[Dict[str, Any]] = []
        
        # 滾動抓取
        for scroll_idx in range(max_scrolls):
            try:
                # 提取當前可見的貼文
                post_selectors = ['article', '[role="article"]', 'div[data-pressable-container="true"]']
                
                for selector in post_selectors:
                    try:
                        elements = self.page.locator(selector).all()
                        for elem in elements:
                            try:
                                html = elem.inner_html()
                                post = self._extract_post_from_element(html)
                                if post:
                                    # 確認是目標用戶的帖子
                                    author = post.get('author_username', '').lower()
                                    author_name = post.get('author_name', '')
                                    if (username.lower() in author or 
                                        any(name in author_name for name in TARGET_NAMES)):
                                        posts.append(post)
                            except:
                                continue
                    except:
                        continue
                
            except Exception as e:
                print(f"[!] 滾動 {scroll_idx} 錯誤: {e}")
            
            # 滾動
            self.page.mouse.wheel(0, 2000)
            time.sleep(2)
            
            if (scroll_idx + 1) % 10 == 0:
                print(f"[*] 已滾動 {scroll_idx + 1}/{max_scrolls}，收集到 {len(posts)} 篇貼文")
        
        print(f"[*] 共收集 {len(posts)} 篇貼文")
        return posts
    
    def search_by_keyword(self, keyword: str, max_scrolls: int = 50) -> List[Dict[str, Any]]:
        """使用關鍵字搜索相關帖子"""
        print(f"[*] 使用關鍵字搜索: {keyword}")
        
        # 訪問 Threads 並搜索
        url = f"{self.THREADS_BASE_URL}/search?q={keyword}"
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)
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
                                    # 檢查是否與黃國昌相關
                                    author = post.get('author_username', '').lower()
                                    author_name = post.get('author_name', '')
                                    text = post.get('text', '')
                                    
                                    if (any(name in author for name in ['kc', 'huang']) or
                                        any(name in author_name for name in TARGET_NAMES) or
                                        "黃國昌" in text or "國昌" in text):
                                        posts.append(post)
                            except:
                                continue
                    except:
                        continue
                
            except Exception as e:
                pass
            
            self.page.mouse.wheel(0, 2000)
            time.sleep(2)
            
            if (scroll_idx + 1) % 10 == 0:
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
            filename = f"kc_huang_threads_{timestamp}.json"
        
        output_path = Path("/Users/user/data") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts_clean, f, ensure_ascii=False, indent=2)
        
        print(f"[*] 結果已保存: {output_path}")
        return output_path


def main():
    """主函數"""
    print("=" * 60)
    print("🔍 黃國昌 Threads 帖子搜索工具")
    print("=" * 60)
    
    scraper = KCThreadsScraper(headless=True)
    
    try:
        scraper.start()
        
        all_posts = []
        
        # 方法 1: 嘗試直接訪問用戶主頁
        print("\n[方法 1] 嘗試直接訪問用戶主頁...")
        username = scraper.search_user_by_name("黃國昌")
        
        if username:
            posts = scraper.scrape_user_profile(username, max_scrolls=50)
            all_posts.extend(posts)
        
        # 方法 2: 搜索關鍵字
        print("\n[方法 2] 搜索關鍵字...")
        search_posts = scraper.search_by_keyword("黃國昌", max_scrolls=30)
        all_posts.extend(search_posts)
        
        # 去重
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            if post['id'] not in seen_ids:
                seen_ids.add(post['id'])
                unique_posts.append(post)
        
        print(f"\n[*] 共收集 {len(unique_posts)} 篇唯一貼文")
        
        # 過濾過去兩週
        recent_posts = scraper.filter_recent_posts(unique_posts, days=14)
        print(f"[*] 過去兩週的貼文: {len(recent_posts)} 篇")
        
        # 保存結果
        output_file = scraper.save_results(recent_posts)
        
        # 輸出結果
        print("\n" + "=" * 60)
        print("📋 黃國昌過去兩週的 Threads 帖子連結:")
        print("=" * 60)
        
        if recent_posts:
            for i, post in enumerate(recent_posts, 1):
                url = post.get('post_url', '')
                text = post.get('text', '')[:60]
                author = post.get('author_username') or post.get('author_name', 'Unknown')
                time_text = post.get('created_time', 'Unknown time')
                
                if url:
                    print(f"\n{i}. [{time_text}] @{author}")
                    print(f"   連結: {url}")
                    print(f"   內容: {text}...")
        else:
            print("\n⚠️ 未找到過去兩週的貼文")
            print("可能原因:")
            print("- 用戶帳號名稱不同")
            print("- 需要登入才能查看")
            print("- 用戶近期沒有發文")
        
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
