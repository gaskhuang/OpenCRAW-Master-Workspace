#!/usr/bin/env python3
"""
Threads Quick Scraper - 使用現有 Chrome CDP
"""

import asyncio
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from playwright.async_api import async_playwright, Page

REPORTS_DIR = Path.home() / "reports"
SEEN_IDS_FILE = REPORTS_DIR / ".threads_monitor_seen_ids.json"

def load_seen_ids() -> Dict[str, str]:
    if SEEN_IDS_FILE.exists():
        try:
            with open(SEEN_IDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_seen_ids(seen_ids: Dict[str, str]):
    SEEN_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_IDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(seen_ids, f, ensure_ascii=False)

def parse_number(val) -> Optional[int]:
    if val is None:
        return None
    try:
        s = str(val).strip().replace(',', '').lower()
        if not s:
            return None
        if '萬' in s:
            return int(float(s.replace('萬', '')) * 10000)
        elif '千' in s:
            return int(float(s.replace('千', '')) * 1000)
        elif s.endswith('k'):
            return int(float(s[:-1]) * 1000)
        elif s.endswith('m'):
            return int(float(s[:-1]) * 1000000)
        elif s.isdigit():
            return int(s)
        return None
    except:
        return None

async def extract_posts(page: Page) -> List[Dict[str, Any]]:
    """提取帖子數據"""
    return await page.evaluate("""
        () => {
            const results = [];
            const articles = document.querySelectorAll('article, div[role="article"]');
            
            articles.forEach(article => {
                try {
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
                    
                    const postLinks = article.querySelectorAll('a[href*="/post/"]');
                    let postUrl = '';
                    let postId = '';
                    
                    for (const link of postLinks) {
                        const href = link.getAttribute('href') || '';
                        const match = href.match(/\\/post\\/([A-Za-z0-9_-]+)/);
                        if (match) {
                            postId = match[1];
                            postUrl = href.startsWith('http') ? href : 'https://www.threads.net' + href;
                            break;
                        }
                    }
                    
                    if (!postId) return;
                    
                    const timeEl = article.querySelector('time');
                    const createdAt = timeEl ? timeEl.getAttribute('datetime') : '';
                    
                    let text = '';
                    const pressableSpans = article.querySelectorAll('[data-pressable-container="true"] span, [data-pressable-container="true"] div');
                    for (const el of pressableSpans) {
                        const txt = el.textContent?.trim() || '';
                        if (txt.length > text.length && !txt.includes('@' + username)) {
                            text = txt;
                        }
                    }
                    
                    if (!text) {
                        const contentDivs = article.querySelectorAll('div[dir="auto"], span[class*="text"], div[class*="content"]');
                        for (const el of contentDivs) {
                            const txt = el.textContent?.trim() || '';
                            if (txt.length > text.length && txt.length < 5000) {
                                text = txt;
                            }
                        }
                    }
                    
                    let likes = null;
                    let replies = null;
                    let reposts = null;
                    
                    const allElements = article.querySelectorAll('button, span, div');
                    const numbers = [];
                    
                    for (const el of allElements) {
                        const txt = el.textContent?.trim() || '';
                        if (/^[\\d,.]+[\\dkm萬千]?$/i.test(txt)) {
                            const parent = el.parentElement;
                            const parentText = parent?.textContent?.toLowerCase() || '';
                            const ariaLabel = parent?.getAttribute('aria-label')?.toLowerCase() || '';
                            numbers.push({value: txt, context: parentText + ' ' + ariaLabel});
                        }
                    }
                    
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
                } catch (e) {}
            });
            
            return results;
        }
    """)

async def scrape_threads():
    print("=" * 60)
    print("🚀 啟動 Threads Top Feed 爬蟲 (CDP)")
    print(f"📅 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    seen_ids = load_seen_ids()
    print(f"📋 已載入 {len(seen_ids)} 個歷史 post_id")
    
    async with async_playwright() as p:
        try:
            print("🔌 連接到 Chrome CDP (port 18792)...")
            browser = await p.chromium.connect_over_cdp('http://127.0.0.1:18792')
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()
            print("✅ 已連接到 Chrome")
            
            # 訪問 Threads
            print("🌐 訪問 Threads.net...")
            await page.goto("https://www.threads.net", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
            
            current_url = page.url
            print(f"📍 當前頁面: {current_url}")
            
            # 檢查登入狀態
            if 'login' in current_url.lower() or 'accounts' in current_url.lower():
                print("⚠️ Threads 需要登入")
                return []
            
            # 滾動並收集
            print("📜 開始滾動 80 次...")
            all_posts = []
            
            for i in range(80):
                posts = await extract_posts(page)
                all_posts.extend(posts)
                
                await page.mouse.wheel(0, 1200)
                await asyncio.sleep(0.8)
                
                if (i + 1) % 20 == 0:
                    print(f"  已滾動 {i + 1}/80 次，收集 {len(all_posts)} 條記錄")
            
            print(f"✅ 滾動完成，總共收集 {len(all_posts)} 條記錄")
            
            # 去重
            dedup = {}
            for post in all_posts:
                pid = post.get('post_id')
                if pid:
                    dedup[pid] = post
            
            print(f"📝 去重後: {len(dedup)} 篇唯一帖子")
            
            # 只保留新帖子
            new_posts = []
            now_str = datetime.now().isoformat()
            for pid, post in dedup.items():
                if pid not in seen_ids:
                    new_posts.append(post)
                    seen_ids[pid] = now_str
            
            print(f"🆕 本輪新增帖子: {len(new_posts)}")
            
            # 保存已見 IDs
            save_seen_ids(seen_ids)
            
            return new_posts
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            import traceback
            traceback.print_exc()
            return []

def categorize_posts(posts: List[Dict]) -> Dict[str, List[Dict]]:
    """自動分類帖子"""
    categories = {}
    
    for post in posts:
        text = post.get('text', '').lower()
        text_zh = post.get('text', '')
        
        # 動態分類 - 根據內容關鍵詞
        cat_scores = {}
        
        # 檢查各種類別
        tech_kw = ['ai', '程式', '開發', 'code', '工程師', 'app', '軟體', '技術', 'python', 'javascript', 'api', 'mcp', 'llm', 'gpt', 'claude', 'cursor', 'ide', 'bug', 'debug']
        design_kw = ['設計', 'ui', 'ux', 'figma', '設計師', '視覺', '介面', '排版', '配色', 'logo']
        business_kw = ['創業', '產品', 'pm', '管理', '職涯', '面試', '工作', '加薪', '轉職', '副業']
        life_kw = ['電影', '劇', '音樂', '遊戲', '美食', '旅行', '運動', 'nba', '健身', '生活']
        social_kw = ['政治', '政策', '社會', '教育', '環保', '人權', '平等', '民主']
        
        cat_scores['科技與開發'] = sum(1 for k in tech_kw if k in text or k in text_zh)
        cat_scores['設計與創意'] = sum(1 for k in design_kw if k in text or k in text_zh)
        cat_scores['商業與職場'] = sum(1 for k in business_kw if k in text or k in text_zh)
        cat_scores['生活與娛樂'] = sum(1 for k in life_kw if k in text or k in text_zh)
        cat_scores['社會與文化'] = sum(1 for k in social_kw if k in text or k in text_zh)
        
        best_cat = max(cat_scores, key=cat_scores.get)
        if cat_scores[best_cat] == 0:
            best_cat = '其他熱門內容'
        
        if best_cat not in categories:
            categories[best_cat] = []
        categories[best_cat].append(post)
    
    # 按互動數排序每個類別
    for cat in categories:
        categories[cat].sort(key=lambda x: parse_number(x.get('likes')) or 0, reverse=True)
    
    return categories

def generate_report(posts: List[Dict]) -> str:
    """生成 Markdown 報告"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M")
    time_display = now.strftime("%Y-%m-%d %H:%M")
    
    report = f"""# Threads 動態深度摘要（過去 3 小時）

> 任務時間：{time_display} (Asia/Taipei)
> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重
> 本輪新增貼文（去重後）：{len(posts)}

"""
    
    if not posts:
        report += """## ⚠️ 抓取受阻

本輪未能提取到新帖子。可能原因：
- Threads 未登入狀態下內容有限
- 頁面載入問題
- 反爬機制

"""
    else:
        # 分類輸出
        categories = categorize_posts(posts)
        
        line_num = 1
        for cat_name, cat_posts in categories.items():
            if not cat_posts:
                continue
            report += f"## {cat_name}\n\n"
            for post in cat_posts:
                text = post.get('text', '').replace('\n', ' ').strip()
                if len(text) > 100:
                    text = text[:97] + "..."
                
                username = post.get('author_username', post.get('author', ''))
                post_id = post.get('post_id', '')
                url = post.get('url', f"https://www.threads.net/@{username}/post/{post_id}")
                
                engagement = []
                likes = parse_number(post.get('likes'))
                replies = parse_number(post.get('replies'))
                if likes:
                    engagement.append(f"{likes}讚")
                if replies:
                    engagement.append(f"{replies}回")
                
                eng_str = f" {' | '.join(engagement)}" if engagement else ""
                report += f"[{line_num}] 「@{username}{eng_str}」{text} [({post_id})]({url})\n"
                line_num += 1
            report += "\n"
    
    # 記者評註
    report += "## 本輪最值得關注的 3 個議題（記者評註）\n\n"
    
    if len(posts) >= 3:
        sorted_posts = sorted([p for p in posts if parse_number(p.get('likes'))], 
                              key=lambda x: parse_number(x.get('likes')) or 0, reverse=True)[:3]
        for i, post in enumerate(sorted_posts, 1):
            snippet = post.get('text', '')[:50] + "..." if len(post.get('text', '')) > 50 else post.get('text', '')
            username = post.get('author_username', '')
            likes = parse_number(post.get('likes'))
            report += f"{i}. **@{username}** ({likes}讚): {snippet}\n"
    else:
        report += "1. 本輪新增內容較少，建議稍後重試。\n"
        report += "2. Threads 演算法推送內容有限。\n"
        report += "3. 建議擴大追蹤範圍或調整抓取策略。\n"
    
    report += """
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
    
    return report, timestamp

async def main():
    posts = await scrape_threads()
    report, timestamp = generate_report(posts)
    
    # 保存報告
    report_path = REPORTS_DIR / f"threads_top_news_{timestamp}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 報告已生成: {report_path}")
    print(f"📊 本輪新增: {len(posts)} 篇帖子")
    
    # 輸出摘要
    print("\n" + "=" * 60)
    print(report[:2000] if len(report) > 2000 else report)
    
    return report_path, len(posts)

if __name__ == "__main__":
    asyncio.run(main())
