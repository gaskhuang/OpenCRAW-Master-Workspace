#!/usr/bin/env python3
"""
Threads 快速抓取腳本 - 使用 Playwright
"""
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set

from playwright.sync_api import sync_playwright

# 設定
REPORTS_DIR = Path("/Users/user/reports")
DATA_DIR = Path("/Users/user/threads-scraper-tool/data")
PROFILE_DIR = DATA_DIR / "threads_browser_profile"

def extract_post_data(element_html: str, seen_ids: Set[str]) -> Dict[str, Any]:
    """從 HTML 提取貼文資料"""
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(element_html, 'html.parser')
        post = {
            'id': '',
            'post_url': '',
            'author_name': '',
            'author_username': '',
            'text': '',
            'created_time': '',
            'like_count': 0,
            'comment_count': 0,
            'repost_count': 0,
            'scraped_at': datetime.utcnow().isoformat() + "Z"
        }
        
        # 提取文字內容
        text_elem = None
        text_selectors = [
            'span[dir="auto"]',
            'div[data-pressable-container="true"] span',
        ]
        
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
        
        # 提取貼文 URL
        link_elem = soup.find('a', href=lambda x: x and '/post/' in x)
        if link_elem:
            href = link_elem.get('href', '')
            if href:
                if not href.startswith('http'):
                    post['post_url'] = 'https://www.threads.net' + href
                else:
                    post['post_url'] = href
                
                id_match = re.search(r'/post/([^/?]+)', href)
                if id_match:
                    post['id'] = id_match.group(1)
        
        if not post['id']:
            import hashlib
            content_hash = hashlib.md5(post['text'][:100].encode()).hexdigest()[:16]
            post['id'] = f"threads_{content_hash}"
        
        if post['id'] in seen_ids:
            return None
        
        seen_ids.add(post['id'])
        return post
        
    except Exception as e:
        return None

def scrape_threads():
    """主爬取函數"""
    print("[*] 啟動 Threads 爬蟲...")
    
    posts = []
    seen_ids = set()
    
    with sync_playwright() as p:
        # 使用 persistent context 保持登入狀態
        PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(30000)
        
        try:
            print("[*] 正在開啟 Threads...")
            page.goto("https://www.threads.net", wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)
            
            # 檢查是否需要登入
            page_text = page.locator('body').inner_text().lower()
            if 'log in' in page_text and 'for you' not in page_text:
                print("[!] 可能需要登入，嘗試等待更多內容載入...")
                time.sleep(5)
            
            print("[*] 開始滾動採集 (80 次)...")
            
            for i in range(80):
                # 提取當前頁面的貼文
                post_selectors = ['article', '[role="article"]', 'div[data-pressable-container="true"]']
                
                for selector in post_selectors:
                    try:
                        elements = page.locator(selector).all()
                        for elem in elements:
                            try:
                                html = elem.inner_html()
                                post = extract_post_data(html, seen_ids)
                                if post:
                                    posts.append(post)
                            except:
                                continue
                    except:
                        continue
                
                # 滾動
                page.mouse.wheel(0, 2000)
                time.sleep(1.5)
                
                if (i + 1) % 10 == 0:
                    print(f"[*] 已滾動 {i+1}/80，收集到 {len(posts)} 篇貼文")
            
            print(f"[*] 採集完成，共 {len(posts)} 篇獨特貼文")
            
        except Exception as e:
            print(f"[!] 錯誤: {e}")
        
        finally:
            context.close()
    
    return posts

def categorize_posts(posts: List[Dict]) -> Dict[str, List[Dict]]:
    """依內容自動分類"""
    categories = {
        "🤖 AI 模型與工具": [],
        "🦞 OpenClaw 生態": [],
        "🎬 AI 影片與圖像": [],
        "🛠️ 開發者工具與實踐": [],
        "🏭 產業與市場動態": [],
        "💡 AI 觀點與趨勢": [],
        "💬 其他內容": [],
    }
    
    for post in posts:
        text = (post.get('text', '') + ' ' + post.get('author_username', '')).lower()
        categorized = False
        
        # AI 模型與工具
        if any(kw in text for kw in ['gpt', 'claude', 'llm', 'ai model', 'openai', 'anthropic', 'gemini', 'language model', '大模型', '模型', 'chatgpt']):
            categories["🤖 AI 模型與工具"].append(post)
            categorized = True
        
        # OpenClaw 生態
        if any(kw in text for kw in ['openclaw', 'lobster', '龍蝦', 'kimi', 'claw', 'openclaw', '開源']):
            categories["🦞 OpenClaw 生態"].append(post)
            categorized = True
        
        # AI 影片與圖像
        if any(kw in text for kw in ['video', 'image', 'sora', 'runway', 'pika', 'stable diffusion', 'midjourney', 'dall-e', '圖像', '影片', 'video']):
            categories["🎬 AI 影片與圖像"].append(post)
            categorized = True
        
        # 開發者工具
        if any(kw in text for kw in ['coding', 'developer', 'programming', 'code', 'github', 'api', 'sdk', '開發', '程式', 'coding']):
            categories["🛠️ 開發者工具與實踐"].append(post)
            categorized = True
        
        # 產業與市場
        if any(kw in text for kw in ['startup', 'funding', 'investment', 'market', 'business', '公司', '創業', '投資', '融資', 'startup']):
            categories["🏭 產業與市場動態"].append(post)
            categorized = True
        
        # AI 觀點與趨勢
        if any(kw in text for kw in ['trend', 'future', 'prediction', 'opinion', '觀點', '趨勢', '未來', '預測']):
            categories["💡 AI 觀點與趨勢"].append(post)
            categorized = True
        
        if not categorized:
            categories["💬 其他內容"].append(post)
    
    return {k: v for k, v in categories.items() if v}

def generate_report(posts: List[Dict]):
    """生成報告"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    filename_timestamp = now.strftime("%Y%m%d_%H%M")
    filename = f"threads_top_news_{filename_timestamp}.md"
    filepath = REPORTS_DIR / filename
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not posts:
        content = f"""# Threads 動態深度摘要（過去 3 小時）

> 任務時間：{timestamp} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重
> 本輪新增貼文（去重後）：0

## ⚠️ 抓取受阻

本輪未能提取到新帖子。可能原因：
- Threads 未登入狀態下內容有限
- 頁面載入問題
- 反爬機制

## 本輪最值得關注的 3 個議題（記者評註）

1. 本輪新增內容較少，建議稍後重試。
2. Threads 演算法推送內容有限。
3. 建議擴大追蹤範圍或調整抓取策略。

## 風險訊號
- 本輪貼文時間跨度依 Threads 演算法推送決定。
- 互動欄位（按讚/留言）結構化抽取可能有 null 缺值。
- 若 Threads 出現反爬機制，部分內容可能未被完整載入。

## 下一輪追蹤關鍵詞

- AI
- 開發
- 產品
- 設計
- 創業
- 科技新聞
"""
        filepath.write_text(content, encoding="utf-8")
        return filepath
    
    # 分類
    categories = categorize_posts(posts)
    
    lines = [
        "# Threads 動態深度摘要（過去 3 小時）",
        "",
        f"> 任務時間：{timestamp} (Asia/Taipei)",
        "> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重",
        f"> 本輪新增貼文（去重後）：{len(posts)}",
        "",
    ]
    
    # 各分類內容
    line_num = 1
    for cat_name, cat_posts in categories.items():
        if not cat_posts:
            continue
        lines.append(f"## {cat_name}")
        lines.append("")
        
        for post in cat_posts[:8]:  # 每類最多 8 則
            text = post.get('text', '')[:120]
            if len(post.get('text', '')) > 120:
                text += '...'
            
            text = text.replace('\n', ' ').strip()
            author = post.get('author_username') or post.get('author_name') or 'Unknown'
            post_id = post.get('id', '')[:20]
            url = post.get('post_url') or f"https://threads.net/@{author}"
            likes = post.get('like_count', 0)
            
            summary = f"[{line_num}] **@{author}**: {text} 👍{likes} [（{post_id}...）]({url})"
            lines.append(summary)
            line_num += 1
        
        lines.append("")
    
    # 記者評註
    lines.extend([
        "---",
        "",
        "## 本輪最值得關注的 3 個議題（記者評註）",
        "",
    ])
    
    top_posts = sorted(posts, key=lambda x: x.get('like_count', 0), reverse=True)[:3]
    for i, post in enumerate(top_posts, 1):
        text = post.get('text', '')[:80]
        author = post.get('author_username') or post.get('author_name') or 'Unknown'
        likes = post.get('like_count', 0)
        lines.append(f"{i}. **@{author}**（{likes} 讚）: {text}...")
    
    # 風險訊號
    lines.extend([
        "",
        "---",
        "",
        "## 風險訊號",
        "",
        "- 本輪貼文時間跨度依 Threads 演算法推送決定。",
        "- 互動欄位（按讚/留言）結構化抽取可能有 null 缺值。",
        "- 若 Threads 出現反爬機制，部分內容可能未被完整載入。",
        "",
    ])
    
    # 關鍵詞
    lines.extend([
        "---",
        "",
        "## 下一輪追蹤關鍵詞",
        "",
        "- AI",
        "- 開發",
        "- 產品",
        "- 設計",
        "- 創業",
        "- 科技新聞",
        "",
    ])
    
    content = "\n".join(lines)
    filepath.write_text(content, encoding="utf-8")
    
    return filepath

if __name__ == "__main__":
    posts = scrape_threads()
    filepath = generate_report(posts)
    print(f"\n✅ 報告已生成: {filepath}")
    print(f"   共收集 {len(posts)} 篇貼文")
