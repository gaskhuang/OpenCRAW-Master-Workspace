#!/usr/bin/env python3
"""
台積電 (TSMC) Threads 熱門帖子快速爬蟲
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
TSMC_KEYWORDS = ["台積電", "TSMC", "tsmc", "台積", "晶圓", "半導體", "2330", "張忠謀", "魏哲家"]

class TSMCTreadsScraperFast:
    """台積電 Threads 快速爬蟲"""
    
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
        
        import tempfile
        user_data_dir = tempfile.mkdtemp(prefix="threads_tsmc_")
        
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=self.headless,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="zh-TW",
            timezone_id="Asia/Taipei",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
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
            
            # 提取圖片
            images = []
            img_elems = soup.find_all('img')
            for img in img_elems:
                src = img.get('src', '')
                if src and not src.startswith('data:'):
                    images.append(src)
            post['images'] = images[:5]  # 最多保存5張圖片
            
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
    
    def search_by_keyword(self, keyword: str, max_scrolls: int = 25) -> List[Dict[str, Any]]:
        """使用關鍵字搜索相關帖子（快速版）"""
        print(f"[*] 搜索關鍵字: {keyword}")
        
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
                                    print(f"  [+] @{post.get('author_username')} | ❤️{post.get('like_count')} | 🔄{post.get('repost_count')} | {post.get('text', '')[:40]}...")
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
            
            if timestamp and isinstance(timestamp, datetime):
                if timestamp >= cutoff_date:
                    recent_posts.append(post)
                continue
            
            if created_time:
                if any(unit in created_time.lower() for unit in ['mo', 'year', '年']):
                    continue
                if 'w' in created_time.lower():
                    week_match = re.search(r'(\d+)\s*w', created_time.lower())
                    if week_match:
                        weeks = int(week_match.group(1))
                        if weeks > 2:
                            continue
                recent_posts.append(post)
            else:
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
        """保存結果到 JSON 文件"""
        import copy
        posts_clean = copy.deepcopy(posts)
        for post in posts_clean:
            if isinstance(post.get('created_timestamp'), datetime):
                post['created_timestamp'] = post['created_timestamp'].isoformat()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tsmc_threads_hot_{timestamp}.json"
        
        output_path = Path("/Users/user/data") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts_clean, f, ensure_ascii=False, indent=2)
        
        print(f"[*] 結果已保存: {output_path}")
        return output_path


def generate_analysis_report(posts: List[Dict]) -> str:
    """生成分析報告"""
    if not posts:
        return "未找到符合條件的熱門貼文"
    
    report_lines = [
        "# 📊 台積電 Threads 熱門貼文分析報告",
        "",
        f"**分析時間**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**符合條件貼文數**: {len(posts)} 篇",
        f"**篩選條件**: ❤️ 愛心 500+ | 🔄 轉貼 100+ | 📅 過去兩週",
        "",
        "---",
        "",
    ]
    
    # 統計數據
    total_likes = sum(p.get('like_count', 0) for p in posts)
    total_reposts = sum(p.get('repost_count', 0) for p in posts)
    total_comments = sum(p.get('comment_count', 0) for p in posts)
    
    report_lines.extend([
        "## 📈 整體統計",
        "",
        f"- **總愛心數**: {total_likes:,}",
        f"- **總轉貼數**: {total_reposts:,}",
        f"- **總留言數**: {total_comments:,}",
        f"- **平均愛心數**: {total_likes // len(posts):,}",
        f"- **平均轉貼數**: {total_reposts // len(posts):,}",
        "",
        "---",
        "",
    ])
    
    # 熱門貼文列表
    report_lines.extend([
        "## 🔥 熱門貼文清單",
        "",
    ])
    
    for i, post in enumerate(posts, 1):
        url = post.get('post_url', '')
        text = post.get('text', '')
        author = post.get('author_username') or post.get('author_name', 'Unknown')
        time_text = post.get('created_time', 'Unknown time')
        likes = post.get('like_count', 0)
        reposts = post.get('repost_count', 0)
        comments = post.get('comment_count', 0)
        images = post.get('images', [])
        
        report_lines.extend([
            f"### {i}. @{author}",
            "",
            f"📊 **互動數據**: ❤️ {likes:,} | 🔄 {reposts:,} | 💬 {comments:,}",
            f"🕐 **發布時間**: {time_text}",
            "",
            f"📝 **貼文內容**:",
            f"> {text}",
            "",
        ])
        
        if images:
            report_lines.append(f"🖼️ **圖片數量**: {len(images)} 張")
            report_lines.append("")
        
        if url:
            report_lines.append(f"🔗 **貼文連結**: {url}")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
    
    # 摘要分析
    report_lines.extend([
        "## 🧠 主要內容摘要分析",
        "",
    ])
    
    # 分析主題
    topics = []
    for post in posts:
        text = post.get('text', '').lower()
        if any(k in text for k in ['股價', '股票', '漲', '跌', '投資', '股市', 'market', 'stock']):
            topics.append('股價與投資')
        if any(k in text for k in ['晶片', '晶圓', '製程', '奈米', 'nm', 'chip', 'wafer']):
            topics.append('晶片技術')
        if any(k in text for k in ['美國', '亞利桑那', '日本', '熊本', '德國', '廠']):
            topics.append('海外擴廠')
        if any(k in text for k in ['ai', '輝達', 'nvidia', 'gpu', '人工智慧']):
            topics.append('AI 相關')
        if any(k in text for k in ['徵才', '招聘', '工作', '工程師', '人才', 'hiring']):
            topics.append('人才徵聘')
    
    from collections import Counter
    topic_counts = Counter(topics)
    
    report_lines.append("### 熱門討論主題")
    report_lines.append("")
    for topic, count in topic_counts.most_common():
        report_lines.append(f"- **{topic}**: {count} 篇相關貼文")
    report_lines.append("")
    
    # 摘要內容
    all_text = " ".join([p.get('text', '') for p in posts])
    report_lines.extend([
        "### 內容摘要",
        "",
        f"從 {len(posts)} 篇熱門貼文可以看出，台積電近期在 Threads 上的討論主要集中在以下幾個面向：",
        "",
    ])
    
    if '股價與投資' in topic_counts:
        report_lines.append("- **投資人關注**：股價走勢與投資價值是熱門話題")
    if '海外擴廠' in topic_counts:
        report_lines.append("- **全球布局**：海外設廠進度與地緣政治影響備受關注")
    if 'AI 相關' in topic_counts:
        report_lines.append("- **AI 熱潮**：AI 晶片需求帶動台積電業務成長")
    if '晶片技術' in topic_counts:
        report_lines.append("- **技術領先**：先進製程技術持續引領產業")
    if '人才徵聘' in topic_counts:
        report_lines.append("- **人才競爭**：徵才與人才培育是重要議題")
    
    report_lines.extend([
        "",
        "---",
        "",
    ])
    
    # 留言建議
    report_lines.extend([
        "## 💬 正向留言建議（可直接複製使用）",
        "",
    ])
    
    suggestions = [
        "台積電真的是台灣的驕傲！技術領先全球，為台灣經濟貢獻良多 💪🇹🇼",
        
        "看好台積電的長期發展，先進製程技術持續領先同業，未來成長可期 📈",
        
        "台積電的企業文化與技術創新能力真的很讓人敬佩，全球科技業都仰賴他們的晶片 ✨",
        
        "身為台灣人，看到台積電在世界舞台發光發熱，感到無比自豪！台灣No.1 🏆",
        
        "AI時代來臨，台積電的先進製程技術將扮演更關鍵的角色，投資價值持續看漲 🤖",
        
        "台積電不只是在製造晶片，更是在推動全球科技進步，改變世界的力量 💡",
        
        "從張忠謀創立到現在，台積電一直堅持技術創新，這種企業精神值得學習 🎯",
        
        "台積電的員工都很專業，能夠在那裡工作真的是夢寐以求的機會！加油 💼",
        
        "全球最先進的晶片都出自台積電，這就是台灣的軟實力！支持台積電 🌟",
        
        "無論是3奈米還是未來的2奈米，台積電總是能帶給市場驚喜，期待未來發展！🔬",
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        report_lines.append(f"{i}. {suggestion}")
        report_lines.append("")
    
    return "\n".join(report_lines)


def main():
    """主函數"""
    print("=" * 70)
    print("🔍 台積電 Threads 熱門帖子快速搜索")
    print("=" * 70)
    print("篩選條件：")
    print("  - 愛心 (Likes) >= 500")
    print("  - 轉貼 (Reposts) >= 100")
    print("  - 時間：過去兩週")
    print("=" * 70)
    
    scraper = TSMCTreadsScraperFast(headless=True)
    
    try:
        scraper.start()
        
        all_posts = []
        
        # 使用多個關鍵字搜索（減少數量以加快搜索）
        keywords = ["台積電", "TSMC"]
        
        for keyword in keywords:
            print(f"\n[搜索] 關鍵字: {keyword}")
            posts = scraper.search_by_keyword(keyword, max_scrolls=25)
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
        
        # 生成分析報告
        report = generate_analysis_report(hot_posts_sorted)
        report_path = Path("/Users/user/reports") / f"tsmc_threads_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding='utf-8')
        
        print(f"\n[*] 分析報告已保存: {report_path}")
        
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
        print(f"[*] 分析報告: {report_path}")
        
        # 顯示報告內容
        print("\n" + "=" * 70)
        print(report)
        
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
