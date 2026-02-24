#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit OpenClaw Monitor - Playwright 版本
使用瀏覽器自動化採集 Reddit 資料
"""

import asyncio
import json
import os
import time
from datetime import datetime, timezone, timedelta
from collections import Counter
from playwright.async_api import async_playwright

# 配置
KEYWORDS = ["OpenClaw", "openclaw", "龍蝦"]
DATA_DIR = "/Users/user/data/social_monitoring"
REPORT_DIR = "/Users/user/reports/social_monitoring/reddit"
ARCHIVE_DIR = f"{DATA_DIR}/archive/reddit"

async def fetch_reddit_search(page, keyword):
    """使用 Playwright 搜尋 Reddit"""
    results = []
    
    # 構建搜尋 URL
    search_url = f"https://www.reddit.com/search/?q={keyword}&type=posts"
    
    try:
        print(f"🔍 正在搜尋：'{keyword}'")
        await page.goto(search_url, wait_until="networkidle", timeout=60000)
        
        # 等待貼文載入
        await page.wait_for_selector("[data-testid='post-container'], shreddit-post, .Post", timeout=15000)
        
        # 滾動以載入更多內容
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1)
        
        # 嘗試多種選擇器來獲取貼文
        posts_data = await page.evaluate("""
            () => {
                const posts = [];
                
                // 嘗試多種選擇器
                const selectors = [
                    'shreddit-post',
                    '[data-testid="post-container"]',
                    'div[data-click-id="background"]',
                    '.Post',
                    '[data-testid="post"]'
                ];
                
                let elements = [];
                for (const selector of selectors) {
                    elements = document.querySelectorAll(selector);
                    if (elements.length > 0) break;
                }
                
                elements.forEach(post => {
                    try {
                        // 標題
                        const titleEl = post.querySelector('[data-testid="post-title-text"], h3 a, a[data-click-id="body"], h1, h2, h3');
                        const title = titleEl ? titleEl.textContent.trim() : '';
                        
                        // Subreddit
                        const subredditEl = post.querySelector('a[href^="/r/"], shreddit-subreddit-name');
                        let subreddit = '';
                        if (subredditEl) {
                            const match = subredditEl.textContent.match(/r\/([A-Za-z0-9_]+)/);
                            subreddit = match ? match[1] : subredditEl.textContent.trim().replace('r/', '');
                        }
                        
                        // Upvotes
                        const upvoteEl = post.querySelector('[data-testid="upvote-button"] + div, span[id^="vote-button"] + span, [data-click-id="upvote"] + div');
                        let upvotes = 0;
                        if (upvoteEl) {
                            const text = upvoteEl.textContent.trim();
                            if (text.includes('k')) {
                                upvotes = parseFloat(text.replace('k', '')) * 1000;
                            } else {
                                upvotes = parseInt(text.replace(/[^0-9]/g, '')) || 0;
                            }
                        }
                        
                        // 留言數
                        const commentEl = post.querySelector('[data-testid="comment-button"] span, a[href*="comments"] span, [data-click-id="comments"]');
                        let comments = 0;
                        if (commentEl) {
                            const text = commentEl.textContent.trim();
                            if (text.includes('k')) {
                                comments = parseFloat(text.replace('k', '')) * 1000;
                            } else {
                                comments = parseInt(text.replace(/[^0-9]/g, '')) || 0;
                            }
                        }
                        
                        // 連結
                        const linkEl = post.querySelector('a[href*="/comments/"], a[data-testid="post-title-text"]');
                        const url = linkEl ? linkEl.href : '';
                        
                        // 作者
                        const authorEl = post.querySelector('a[href^="/user/"], a[href^="/u/"]');
                        const author = authorEl ? authorEl.textContent.trim().replace('u/', '').replace('user/', '') : '[deleted]';
                        
                        // 時間
                        const timeEl = post.querySelector('faceplate-timeago, time, span[data-testid="post_timestamp"]');
                        const post_time = timeEl ? timeEl.textContent.trim() : '';
                        
                        if (title) {
                            posts.push({
                                title: title,
                                subreddit: subreddit,
                                upvotes: upvotes,
                                num_comments: comments,
                                url: url,
                                author: author,
                                post_time: post_time,
                                content: ''
                            });
                        }
                    } catch (e) {}
                });
                
                return posts;
            }
        """)
        
        results.extend(posts_data)
        print(f"   ✓ 找到 {len(posts_data)} 則貼文")
        
    except Exception as e:
        print(f"   ⚠️  搜尋 '{keyword}' 時發生錯誤: {e}")
    
    return results

async def fetch_subreddit_posts(page, subreddit_name):
    """獲取特定 subreddit 的貼文"""
    results = []
    url = f"https://www.reddit.com/r/{subreddit_name}/"
    
    try:
        print(f"🔍 正在獲取 r/{subreddit_name}")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # 等待貼文載入
        await page.wait_for_selector("[data-testid='post-container'], shreddit-post, .Post", timeout=15000)
        
        # 滾動
        for _ in range(2):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1)
        
        posts_data = await page.evaluate("""
            () => {
                const posts = [];
                const elements = document.querySelectorAll('shreddit-post, [data-testid="post-container"], div[data-click-id="background"]');
                
                elements.forEach(post => {
                    try {
                        const titleEl = post.querySelector('[data-testid="post-title-text"], h3 a, a[data-click-id="body"]');
                        const title = titleEl ? titleEl.textContent.trim() : '';
                        
                        const upvoteEl = post.querySelector('[data-testid="upvote-button"] + div, span[id^="vote-button"] + span');
                        let upvotes = 0;
                        if (upvoteEl) {
                            const text = upvoteEl.textContent.trim();
                            if (text.includes('k')) {
                                upvotes = parseFloat(text.replace('k', '')) * 1000;
                            } else {
                                upvotes = parseInt(text.replace(/[^0-9]/g, '')) || 0;
                            }
                        }
                        
                        const commentEl = post.querySelector('[data-testid="comment-button"] span, a[href*="comments"] span');
                        let comments = 0;
                        if (commentEl) {
                            const text = commentEl.textContent.trim();
                            if (text.includes('k')) {
                                comments = parseFloat(text.replace('k', '')) * 1000;
                            } else {
                                comments = parseInt(text.replace(/[^0-9]/g, '')) || 0;
                            }
                        }
                        
                        const linkEl = post.querySelector('a[href*="/comments/"]');
                        const url = linkEl ? linkEl.href : '';
                        
                        const authorEl = post.querySelector('a[href^="/user/"], a[href^="/u/"]');
                        const author = authorEl ? authorEl.textContent.trim().replace('u/', '') : '[deleted]';
                        
                        if (title) {
                            posts.push({
                                title: title,
                                subreddit: '%s',
                                upvotes: upvotes,
                                num_comments: comments,
                                url: url,
                                author: author,
                                post_time: '',
                                content: ''
                            });
                        }
                    } catch (e) {}
                });
                
                return posts;
            }
        """ % subreddit_name)
        
        results.extend(posts_data)
        print(f"   ✓ 找到 {len(posts_data)} 則貼文")
        
    except Exception as e:
        print(f"   ⚠️  獲取 r/{subreddit_name} 時發生錯誤: {e}")
    
    return results

def deduplicate_posts(posts):
    """根據 URL 去重"""
    seen = set()
    unique = []
    for post in posts:
        url = post.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(post)
    return unique

def analyze_data(all_posts):
    """分析資料並產生統計"""
    # Subreddit 分佈
    subreddit_counts = Counter([p.get("subreddit", "unknown") for p in all_posts])
    
    # 關鍵詞統計
    keyword_counts = Counter()
    text_to_check = ""
    for p in all_posts:
        text_to_check += (p.get("title", "") + " " + p.get("content", "")).lower()
    
    keyword_map = {
        "openclaw": ["openclaw"],
        "agent": ["agent"],
        "龍蝦": ["龍蝦"],
        "setup": ["setup", "install"],
        "lobster": ["lobster"],
        "error": ["error", "bug", "issue"],
        "security": ["security", "exposed", "vulnerability"],
        "openai": ["openai"],
        "claude": ["claude"],
        "ai": ["ai"]
    }
    
    for key, patterns in keyword_map.items():
        count = sum(text_to_check.count(p) for p in patterns)
        if count > 0:
            keyword_counts[key] = count
    
    # 熱門貼文（按 upvotes）
    top_posts = sorted(all_posts, key=lambda x: x.get("upvotes", 0), reverse=True)[:10]
    
    # 最新貼文
    recent_posts = sorted(all_posts, key=lambda x: x.get("created_utc", 0), reverse=True)[:10]
    
    return {
        "total_posts": len(all_posts),
        "subreddit_distribution": dict(subreddit_counts.most_common(20)),
        "keyword_counts": dict(keyword_counts.most_common(20)),
        "top_posts": top_posts,
        "recent_posts": recent_posts
    }

def generate_report(analysis, timestamp):
    """產生繁體中文報告"""
    taipei_time = datetime.now(timezone(timedelta(hours=8)))
    
    report = f"""# Reddit OpenClaw 監控報告（繁體中文）

- 產生時間：{taipei_time.strftime("%Y-%m-%d %H:%M:%S")}
- 關鍵字：OpenClaw / openclaw / 龍蝦
- 採集貼文數：{analysis['total_posts']}

## 一、整體概況
- 涵蓋 subreddit 數：{len(analysis['subreddit_distribution'])}
- Subreddit 分佈：
"""
    
    for sub, count in list(analysis['subreddit_distribution'].items())[:10]:
        report += f"  - r/{sub}: {count} 則\n"
    
    report += """
## 二、熱門貼文 Top 5（依 upvotes）
"""
    
    for i, post in enumerate(analysis['top_posts'][:5], 1):
        content_preview = post.get("content", "")[:200] if post.get("content") else "（無內文）"
        if len(content_preview) >= 200:
            content_preview += "..."
        
        report += f"""### Top {i}
- Subreddit：r/{post.get('subreddit', 'unknown')}
- 標題：{post.get('title', 'N/A')}
- Upvotes：{post.get('upvotes', 0)}
- 留言數：{post.get('num_comments', 0)}
- 內容摘要：{content_preview}
- 連結：{post.get('url', 'N/A')}

"""
    
    report += """## 三、討論趨勢
- 關鍵詞命中（title+content）：
"""
    
    for keyword, count in analysis['keyword_counts'].items():
        report += f"  - {keyword}: {count}\n"
    
    # 趨勢判讀
    trend_insight = "重點集中在"
    if analysis['keyword_counts'].get('security', 0) > 5:
        trend_insight += "資安暴露、"
    if analysis['keyword_counts'].get('setup', 0) > 5:
        trend_insight += "部署設定、"
    if analysis['keyword_counts'].get('error', 0) > 3:
        trend_insight += "錯誤問題、"
    if analysis['keyword_counts'].get('openai', 0) > 3:
        trend_insight += "OpenAI 相關、"
    if analysis['keyword_counts'].get('claude', 0) > 3:
        trend_insight += "Claude 相關、"
    trend_insight += "社群討論與應用落地。"
    
    report += f"- 趨勢判讀：{trend_insight}\n\n"
    
    report += """## 四、最新發現
"""
    
    for post in analysis['recent_posts'][:5]:
        report += f"- r/{post.get('subreddit', 'unknown')}｜{post.get('title', 'N/A')}（{post.get('upvotes', 0)}↑ / {post.get('num_comments', 0)}留言）\n"
    
    report += f"""
## 五、資料檔案
- 原始採集：{DATA_DIR}/reddit_openclaw_{timestamp}.json
- 增強資料：{REPORT_DIR}/reddit_openclaw_enhanced_{timestamp}.json
- 歸檔位置：{ARCHIVE_DIR}/reddit_openclaw_{timestamp}.json
"""
    
    return report

async def main():
    print("🦞 Reddit OpenClaw 監控啟動 (Playwright 版本)...")
    print(f"⏰ 執行時間：{datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')} (Asia/Taipei)")
    
    timestamp = int(time.time() * 1000)
    
    # 確保目錄存在
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    all_posts = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # 搜尋所有關鍵字
        for keyword in KEYWORDS:
            posts = await fetch_reddit_search(page, keyword)
            all_posts.extend(posts)
            await asyncio.sleep(2)
        
        # 也檢查相關 subreddit
        related_subreddits = ["OpenclawBot", "OpenAI", "ClaudeAI", "ArtificialIntelligence", "LocalLLaMA"]
        for subreddit in related_subreddits:
            posts = await fetch_subreddit_posts(page, subreddit)
            # 過濾包含關鍵字的貼文
            filtered = [p for p in posts if any(kw.lower() in p.get("title", "").lower() for kw in KEYWORDS)]
            all_posts.extend(filtered)
            await asyncio.sleep(2)
        
        await browser.close()
    
    # 去重
    unique_posts = deduplicate_posts(all_posts)
    print(f"\n📊 去重後總貼文數：{len(unique_posts)}")
    
    # 分析資料
    print("\n🔬 正在分析資料...")
    analysis = analyze_data(unique_posts)
    
    # 產生報告
    print("\n📝 正在產生報告...")
    report = generate_report(analysis, timestamp)
    
    # 儲存資料
    raw_file = f"{DATA_DIR}/reddit_openclaw_{timestamp}.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(unique_posts, f, ensure_ascii=False, indent=2)
    print(f"✓ 原始資料已儲存：{raw_file}")
    
    enhanced_file = f"{REPORT_DIR}/reddit_openclaw_enhanced_{timestamp}.json"
    with open(enhanced_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_posts": len(unique_posts),
            "posts": unique_posts,
            "analysis": analysis
        }, f, ensure_ascii=False, indent=2)
    print(f"✓ 增強資料已儲存：{enhanced_file}")
    
    date_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d_%H-%M")
    report_file = f"{REPORT_DIR}/reddit_openclaw_report_{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✓ 報告已儲存：{report_file}")
    
    archive_file = f"{ARCHIVE_DIR}/reddit_openclaw_{timestamp}.json"
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_posts": len(unique_posts),
            "posts": unique_posts,
            "analysis": analysis
        }, f, ensure_ascii=False, indent=2)
    print(f"✓ 歸檔資料已儲存：{archive_file}")
    
    # 輸出摘要
    print("\n" + "="*60)
    print("📋 監控摘要")
    print("="*60)
    print(f"總貼文數：{analysis['total_posts']}")
    print(f"涵蓋 subreddit：{len(analysis['subreddit_distribution'])}")
    print("\n熱門 subreddit：")
    for sub, count in list(analysis['subreddit_distribution'].items())[:5]:
        print(f"  - r/{sub}: {count} 則")
    
    print("\n✅ Reddit OpenClaw 監控完成！")
    
    return report, report_file, archive_file

if __name__ == "__main__":
    asyncio.run(main())
