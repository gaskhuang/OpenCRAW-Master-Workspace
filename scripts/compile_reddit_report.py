#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
編譯 Reddit OpenClaw 監控報告
從 Firecrawl 搜尋結果生成繁體中文報告
"""

import json
import os
from datetime import datetime, timezone, timedelta
from collections import Counter
import re

# 配置
DATA_DIR = "/Users/user/data/social_monitoring"
REPORT_DIR = "/Users/user/reports/social_monitoring/reddit"
ARCHIVE_DIR = f"{DATA_DIR}/archive/reddit"
FIRECRAWL_DIR = "/Users/user/.firecrawl"

def extract_subreddit(url):
    """從 URL 提取 subreddit 名稱"""
    match = re.search(r'/r/([A-Za-z0-9_]+)/', url)
    return match.group(1) if match else "unknown"

def parse_search_results():
    """解析 Firecrawl 搜尋結果"""
    all_posts = []
    
    # 讀取所有搜尋結果檔案
    search_files = [
        f"{FIRECRAWL_DIR}/search_openclaw_reddit.json",
        f"{FIRECRAWL_DIR}/search_openclaw_security.json", 
        f"{FIRECRAWL_DIR}/search_openclaw_setup.json"
    ]
    
    seen_urls = set()
    
    for filepath in search_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'data' in data and 'web' in data['data']:
                    for item in data['data']['web']:
                        url = item.get('url', '')
                        if url in seen_urls or 'reddit.com' not in url:
                            continue
                        seen_urls.add(url)
                        
                        subreddit = extract_subreddit(url)
                        title = item.get('title', '').replace(' : r/', ' | r/').split(' | ')[0]
                        
                        # 從標題清理
                        title = re.sub(r'\s*:\s*r/[A-Za-z0-9_]+\s*-?\s*Reddit$', '', title)
                        
                        post = {
                            "title": title,
                            "subreddit": subreddit,
                            "url": url,
                            "description": item.get('description', ''),
                            "upvotes": 0,  # 無法從搜尋結果取得
                            "num_comments": 0  # 無法從搜尋結果取得
                        }
                        all_posts.append(post)
            except Exception as e:
                print(f"⚠️  讀取 {filepath} 失敗: {e}")
    
    return all_posts

def analyze_data(posts):
    """分析資料"""
    # Subreddit 分佈
    subreddit_counts = Counter([p.get("subreddit", "unknown") for p in posts])
    
    # 關鍵詞統計
    keyword_counts = Counter()
    text_to_check = ""
    for p in posts:
        text_to_check += (p.get("title", "") + " " + p.get("description", "")).lower()
    
    keyword_map = {
        "openclaw": ["openclaw"],
        "agent": ["agent"],
        "龍蝦": ["龍蝦"],
        "setup": ["setup", "install", "guide"],
        "lobster": ["lobster"],
        "error": ["error", "bug", "issue", "problem"],
        "security": ["security", "exposed", "vulnerability", "worse", "risk"],
        "openai": ["openai"],
        "claude": ["claude"],
        "ai": ["ai"],
        "overhyped": ["overhyped", "overrated"],
        "architecture": ["architecture"],
        "monitoring": ["monitoring"]
    }
    
    for key, patterns in keyword_map.items():
        count = sum(text_to_check.count(p) for p in patterns)
        if count > 0:
            keyword_counts[key] = count
    
    # 熱門貼文（這裡無法取得 upvotes，所以按關鍵詞相關度排序）
    # 使用描述長度作為「豐富度」指標
    sorted_posts = sorted(posts, key=lambda x: len(x.get("description", "")), reverse=True)[:10]
    
    return {
        "total_posts": len(posts),
        "subreddit_distribution": dict(subreddit_counts.most_common(20)),
        "keyword_counts": dict(keyword_counts.most_common(20)),
        "top_posts": sorted_posts[:10],
        "recent_posts": posts[:10]
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
## 二、熱門貼文 Top 5（依內容豐富度）
"""
    
    for i, post in enumerate(analysis['top_posts'][:5], 1):
        content_preview = post.get("description", "")[:250] if post.get("description") else "（無內文）"
        if len(content_preview) >= 250:
            content_preview += "..."
        
        report += f"""### Top {i}
- Subreddit：r/{post.get('subreddit', 'unknown')}
- 標題：{post.get('title', 'N/A')}
- 內容摘要：{content_preview}
- 連結：{post.get('url', 'N/A')}

"""
    
    report += """## 三、討論趨勢
- 關鍵詞命中（title+content）：
"""
    
    for keyword, count in analysis['keyword_counts'].items():
        report += f"  - {keyword}: {count}\n"
    
    # 趨勢判讀
    trends = []
    if analysis['keyword_counts'].get('security', 0) > 3:
        trends.append("資安風險")
    if analysis['keyword_counts'].get('setup', 0) > 3:
        trends.append("部署設定")
    if analysis['keyword_counts'].get('error', 0) > 2 or analysis['keyword_counts'].get('problem', 0) > 2:
        trends.append("問題回報")
    if analysis['keyword_counts'].get('overhyped', 0) > 2:
        trends.append("過度炒作疑慮")
    if analysis['keyword_counts'].get('architecture', 0) > 2:
        trends.append("架構討論")
    if analysis['keyword_counts'].get('openai', 0) > 2:
        trends.append("OpenAI 收購傳聞")
    
    if not trends:
        trends = ["一般性討論", "應用分享"]
    
    trend_insight = "、".join(trends) + "。"
    report += f"- 趨勢判讀：重點集中在{trend_insight}\n\n"
    
    report += """## 四、重要發現
"""
    
    # 篩選重要貼文
    important_keywords = ['security', 'worse', 'problem', 'overhyped', 'guide', 'ultimate']
    important_posts = []
    for post in analysis['top_posts']:
        desc_lower = post.get('description', '').lower()
        title_lower = post.get('title', '').lower()
        if any(kw in desc_lower or kw in title_lower for kw in important_keywords):
            important_posts.append(post)
    
    if important_posts:
        for post in important_posts[:5]:
            report += f"- r/{post.get('subreddit', 'unknown')}｜{post.get('title', 'N/A')}\n"
    else:
        for post in analysis['top_posts'][:5]:
            report += f"- r/{post.get('subreddit', 'unknown')}｜{post.get('title', 'N/A')}\n"
    
    report += f"""
## 五、資料檔案
- 原始搜尋結果：{FIRECRAWL_DIR}/search_openclaw_*.json
- 增強資料：{REPORT_DIR}/reddit_openclaw_enhanced_{timestamp}.json
- 歸檔位置：{ARCHIVE_DIR}/reddit_openclaw_{timestamp}.json
- 本報告：{REPORT_DIR}/reddit_openclaw_report_{taipei_time.strftime("%Y-%m-%d_%H-%M")}.md

---
*本報告由 OpenClaw Reddit 監控系統自動生成*
"""
    
    return report

def main():
    print("🦞 Reddit OpenClaw 監控報告編譯中...")
    print(f"⏰ 執行時間：{datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')} (Asia/Taipei)")
    
    timestamp = int(datetime.now().timestamp() * 1000)
    
    # 確保目錄存在
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    # 解析搜尋結果
    print("\n🔍 正在解析搜尋結果...")
    posts = parse_search_results()
    print(f"   ✓ 解析到 {len(posts)} 則貼文")
    
    if not posts:
        print("⚠️  沒有找到任何貼文，請先執行 Firecrawl 搜尋")
        return
    
    # 分析資料
    print("\n🔬 正在分析資料...")
    analysis = analyze_data(posts)
    
    # 產生報告
    print("\n📝 正在產生報告...")
    report = generate_report(analysis, timestamp)
    
    # 儲存資料
    enhanced_file = f"{REPORT_DIR}/reddit_openclaw_enhanced_{timestamp}.json"
    with open(enhanced_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_posts": len(posts),
            "posts": posts,
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
            "total_posts": len(posts),
            "posts": posts,
            "analysis": analysis
        }, f, ensure_ascii=False, indent=2)
    print(f"✓ 歸檔資料已儲存：{archive_file}")
    
    # 同時儲存一個副本到 data/social_monitoring
    data_file = f"{DATA_DIR}/reddit_openclaw_{timestamp}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"✓ 原始資料已儲存：{data_file}")
    
    # 輸出摘要
    print("\n" + "="*60)
    print("📋 監控摘要")
    print("="*60)
    print(f"總貼文數：{analysis['total_posts']}")
    print(f"涵蓋 subreddit：{len(analysis['subreddit_distribution'])}")
    print("\n熱門 subreddit：")
    for sub, count in list(analysis['subreddit_distribution'].items())[:5]:
        print(f"  - r/{sub}: {count} 則")
    print("\n熱門關鍵詞：")
    for kw, count in list(analysis['keyword_counts'].items())[:5]:
        print(f"  - {kw}: {count}")
    
    print("\n✅ Reddit OpenClaw 監控完成！")
    print(f"\n📄 報告位置：{report_file}")
    
    return report, report_file, archive_file

if __name__ == "__main__":
    main()
