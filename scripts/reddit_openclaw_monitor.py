#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit OpenClaw Monitor
採集 Reddit 上關於 OpenClaw、龍蝦、openclaw 的貼文與留言
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta
from collections import Counter
import time

# 配置
KEYWORDS = ["OpenClaw", "openclaw", "龍蝦"]
DATA_DIR = "/Users/user/data/social_monitoring"
REPORT_DIR = "/Users/user/reports/social_monitoring/reddit"
ARCHIVE_DIR = f"{DATA_DIR}/archive/reddit"

# Pushshift API 端點
PUSHSHIFT_SUBMISSION_URL = "https://api.pushshift.io/reddit/search/submission"
PUSHSHIFT_COMMENT_URL = "https://api.pushshift.io/reddit/search/comment"

def fetch_reddit_data(keyword, limit=100):
    """使用 Pushshift API 獲取 Reddit 資料"""
    results = {
        "submissions": [],
        "comments": [],
        "keyword": keyword
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    # 獲取貼文 (submissions)
    try:
        params = {
            "q": keyword,
            "size": limit,
            "sort": "desc",
            "sort_type": "created_utc"
        }
        resp = requests.get(PUSHSHIFT_SUBMISSION_URL, params=params, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            results["submissions"] = data.get("data", [])
        else:
            print(f"⚠️  獲取貼文失敗 (keyword={keyword}): HTTP {resp.status_code}")
    except Exception as e:
        print(f"⚠️  獲取貼文錯誤 (keyword={keyword}): {e}")
    
    time.sleep(0.5)  # 禮貌性延遲
    
    # 獲取留言 (comments)
    try:
        params = {
            "q": keyword,
            "size": limit,
            "sort": "desc", 
            "sort_type": "created_utc"
        }
        resp = requests.get(PUSHSHIFT_COMMENT_URL, params=params, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            results["comments"] = data.get("data", [])
        else:
            print(f"⚠️  獲取留言失敗 (keyword={keyword}): HTTP {resp.status_code}")
    except Exception as e:
        print(f"⚠️  獲取留言錯誤 (keyword={keyword}): {e}")
    
    return results

def deduplicate_posts(posts):
    """根據 ID 去重"""
    seen = set()
    unique = []
    for post in posts:
        pid = post.get("id")
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(post)
    return unique

def convert_to_standard_format(post):
    """轉換為標準格式"""
    created_utc = post.get("created_utc", 0)
    date_str = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "id": post.get("id"),
        "title": post.get("title", ""),
        "author": post.get("author", "[deleted]"),
        "subreddit": post.get("subreddit", ""),
        "content": post.get("selftext", "") or post.get("body", ""),
        "url": f"https://reddit.com{post.get('permalink', '')}" if post.get('permalink') else post.get("url", ""),
        "upvotes": post.get("score", 0) or 0,
        "num_comments": post.get("num_comments", 0) or 0,
        "created_utc": created_utc,
        "created_date": date_str,
        "is_comment": "body" in post and "title" not in post
    }

def analyze_data(all_posts):
    """分析資料並產生統計"""
    submissions = [p for p in all_posts if not p.get("is_comment", False)]
    comments = [p for p in all_posts if p.get("is_comment", False)]
    
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
        "openai": ["openai"]
    }
    
    for key, patterns in keyword_map.items():
        count = sum(text_to_check.count(p) for p in patterns)
        if count > 0:
            keyword_counts[key] = count
    
    # 熱門貼文（按 upvotes）
    top_posts = sorted(submissions, key=lambda x: x.get("upvotes", 0), reverse=True)[:10]
    
    # 最新貼文
    recent_posts = sorted(submissions, key=lambda x: x.get("created_utc", 0), reverse=True)[:10]
    
    return {
        "total_posts": len(all_posts),
        "total_submissions": len(submissions),
        "total_comments": len(comments),
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

def main():
    print("🦞 Reddit OpenClaw 監控啟動...")
    print(f"⏰ 執行時間：{datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')} (Asia/Taipei)")
    
    timestamp = int(time.time() * 1000)
    
    # 確保目錄存在
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    # 收集所有關鍵字的資料
    all_raw_data = []
    all_standard_posts = []
    
    for keyword in KEYWORDS:
        print(f"\n🔍 正在搜尋關鍵字：'{keyword}'")
        data = fetch_reddit_data(keyword, limit=100)
        
        for submission in data["submissions"]:
            all_raw_data.append(submission)
            all_standard_posts.append(convert_to_standard_format(submission))
        
        for comment in data["comments"]:
            all_raw_data.append(comment)
            all_standard_posts.append(convert_to_standard_format(comment))
        
        print(f"   ✓ 貼文：{len(data['submissions'])} 則")
        print(f"   ✓ 留言：{len(data['comments'])} 則")
    
    # 去重
    unique_posts = deduplicate_posts(all_standard_posts)
    print(f"\n📊 去重後總貼文數：{len(unique_posts)}")
    
    # 分析資料
    print("\n🔬 正在分析資料...")
    analysis = analyze_data(unique_posts)
    
    # 產生報告
    print("\n📝 正在產生報告...")
    report = generate_report(analysis, timestamp)
    
    # 儲存原始資料
    raw_file = f"{DATA_DIR}/reddit_openclaw_{timestamp}.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(all_raw_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 原始資料已儲存：{raw_file}")
    
    # 儲存標準化資料
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
    
    # 儲存報告
    date_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d_%H-%M")
    report_file = f"{REPORT_DIR}/reddit_openclaw_report_{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✓ 報告已儲存：{report_file}")
    
    # 歸檔
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
    
    # 輸出報告摘要
    print("\n" + "="*60)
    print("📋 監控摘要")
    print("="*60)
    print(f"總貼文數：{analysis['total_posts']}")
    print(f"貼文數：{analysis['total_submissions']}")
    print(f"留言數：{analysis['total_comments']}")
    print(f"涵蓋 subreddit：{len(analysis['subreddit_distribution'])}")
    print("\n熱門 subreddit：")
    for sub, count in list(analysis['subreddit_distribution'].items())[:5]:
        print(f"  - r/{sub}: {count} 則")
    
    print("\n✅ Reddit OpenClaw 監控完成！")
    
    return report, report_file, archive_file

if __name__ == "__main__":
    main()
