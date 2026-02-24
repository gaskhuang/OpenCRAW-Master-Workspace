#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit OpenClaw 監控報告生成器 (從 Reddit API 資料)
生成繁體中文報告
"""

import json
import os
import glob
from datetime import datetime
from collections import defaultdict
import re

def extract_posts_from_file(filepath):
    """從 Reddit API JSON 檔案提取貼文"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        posts = []
        children = data.get('data', {}).get('children', [])
        
        for child in children:
            p = child.get('data', {})
            if not p:
                continue
                
            # 只保留符合條件的貼文
            title = p.get('title', '')
            selftext = p.get('selftext', '')
            
            # 檢查是否與 OpenClaw/龍蝦相關
            combined_text = (title + ' ' + selftext).lower()
            keywords = ['openclaw', 'clawdbot', 'moltbot', '龍蝦', 'lobster ai', 'claude code']
            
            if not any(kw in combined_text for kw in keywords):
                continue
            
            post_data = {
                'title': title,
                'url': 'https://reddit.com' + p.get('permalink', ''),
                'content': selftext[:500] if selftext else '',
                'subreddit': p.get('subreddit', 'Unknown'),
                'author': p.get('author', 'Unknown'),
                'upvotes': p.get('ups', 0),
                'comments_count': p.get('num_comments', 0),
                'created_utc': p.get('created_utc', 0),
                'post_type': classify_post(title, selftext),
                'id': p.get('id', '')
            }
            posts.append(post_data)
        
        return posts
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return []

def classify_post(title, content):
    """分類貼文類型"""
    text = (title + ' ' + content).lower()
    
    if any(k in text for k in ['security', 'danger', 'do not use', 'warning', 'leaked', 'scary', 'unsafe']):
        return '警告/安全'
    elif any(k in text for k in ['overhyped', 'not useful', 'problem', 'worse', 'burned', 'waste', 'disappointed']):
        return '負面評價'
    elif any(k in text for k in ['game changer', 'cool', 'awesome', 'love it', 'helpful', 'amazing', 'best']):
        return '正面評價'
    elif any(k in text for k in ['guide', 'how to', 'tutorial', 'setup', 'tips', 'tricks']):
        return '教學/指南'
    elif any(k in text for k in ['architecture', 'technical', 'looked into', 'dig', 'deep dive']):
        return '技術分析'
    elif any(k in text for k in ['vs', 'compare', 'better than', 'alternative']):
        return '比較/對比'
    else:
        return '討論/問答'

def format_timestamp(utc_timestamp):
    """將 UTC timestamp 轉換為可讀格式"""
    try:
        dt = datetime.fromtimestamp(utc_timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return 'Unknown'

def generate_report(data_dir, output_dir):
    """生成監控報告"""
    
    # 讀取所有搜尋檔案
    all_posts = []
    search_files = glob.glob(os.path.join(data_dir, 'reddit_search_*.json'))
    
    print(f"找到 {len(search_files)} 個搜尋檔案")
    
    for filepath in search_files:
        posts = extract_posts_from_file(filepath)
        all_posts.extend(posts)
        print(f"  - {os.path.basename(filepath)}: {len(posts)} 則相關貼文")
    
    # 去重 (依 ID)
    seen_ids = set()
    unique_posts = []
    for post in all_posts:
        if post['id'] not in seen_ids:
            seen_ids.add(post['id'])
            unique_posts.append(post)
    
    # 依 upvotes 排序
    unique_posts.sort(key=lambda x: x['upvotes'], reverse=True)
    
    # 統計
    subreddit_counts = defaultdict(int)
    type_counts = defaultdict(int)
    total_upvotes = 0
    total_comments = 0
    
    for post in unique_posts:
        subreddit_counts[post['subreddit']] += 1
        type_counts[post['post_type']] += 1
        total_upvotes += post['upvotes']
        total_comments += post['comments_count']
    
    # 排序 subreddit
    top_subreddits = sorted(subreddit_counts.items(), key=lambda x: -x[1])
    
    # 生成報告
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    timestamp_file = datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    report = f"""# 🦞 Reddit OpenClaw 監控報告（繁體中文）

> 產生時間：{now} (Asia/Taipei)  
> 關鍵字：OpenClaw、openclaw、龍蝦、Clawdbot、Claude Code  
> 採集貼文數：{len(unique_posts)}  
> 總 Upvotes：{total_upvotes}  
> 總留言數：{total_comments}

---

## 一、整體概況

### Subreddit 分佈
| Subreddit | 貼文數 |
|-----------|--------|
"""
    
    for sub, count in top_subreddits[:10]:
        report += f"| r/{sub} | {count} |\n"
    
    report += f"""
### 貼文類型分佈
| 類型 | 數量 |
|------|------|
"""
    for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        report += f"| {ptype} | {count} |\n"
    
    # 依類型分組顯示重要貼文
    report += """
---

## 二、重要貼文摘要

### 🔴 警告/安全類
"""
    warning_posts = [p for p in unique_posts if p['post_type'] == '警告/安全']
    if warning_posts:
        for post in warning_posts[:5]:
            content_preview = post['content'][:150] if post['content'] else '無內容預覽'
            report += f"\n**[{post['upvotes']}\u2191] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
            report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | {format_timestamp(post['created_utc'])}\n"
            report += f"- {content_preview}...\n"
    else:
        report += "\n暫無相關貼文\n"
    
    report += """
### 🟢 正面評價
"""
    positive_posts = [p for p in unique_posts if p['post_type'] == '正面評價']
    if positive_posts:
        for post in positive_posts[:5]:
            content_preview = post['content'][:150] if post['content'] else '無內容預覽'
            report += f"\n**[{post['upvotes']}\u2191] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
            report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | {format_timestamp(post['created_utc'])}\n"
            report += f"- {content_preview}...\n"
    else:
        report += "\n暫無相關貼文\n"
    
    report += """
### 🔵 技術分析 / 教學指南
"""
    tech_posts = [p for p in unique_posts if p['post_type'] in ['技術分析', '教學/指南']]
    if tech_posts:
        for post in tech_posts[:5]:
            content_preview = post['content'][:150] if post['content'] else '無內容預覽'
            report += f"\n**[{post['upvotes']}\u2191] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
            report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | {format_timestamp(post['created_utc'])}\n"
            report += f"- {content_preview}...\n"
    else:
        report += "\n暫無相關貼文\n"
    
    report += """
### 🟡 熱門討論（依 Upvotes 排序）
"""
    discussion_posts = [p for p in unique_posts if p['post_type'] in ['討論/問答', '比較/對比']][:8]
    for post in discussion_posts:
        report += f"\n**[{post['upvotes']}\u2191] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
        report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | {format_timestamp(post['created_utc'])}\n"
    
    # 關鍵詞統計
    report += """
---

## 三、關鍵詞分析

"""
    keywords = ['security', 'token', 'local', 'self-hosted', 'claude', 'openai', 
                'kubernetes', 'docker', 'skill', 'memory', 'cost', 'price', 'mcp',
                'setup', 'guide', 'tutorial', 'vs', 'compare']
    keyword_counts = {}
    all_text = ' '.join([p['title'] + ' ' + p['content'] for p in unique_posts]).lower()
    
    for kw in keywords:
        count = all_text.count(kw)
        if count > 0:
            keyword_counts[kw] = count
    
    for kw, count in sorted(keyword_counts.items(), key=lambda x: -x[1]):
        report += f"- **{kw}**: {count} 次\n"
    
    # 趨勢判讀
    report += f"""
---

## 四、趨勢判讀與分析

### 1. 社群熱度
- 本次採集共 {len(unique_posts)} 則相關貼文
- 總 upvotes: {total_upvotes}
- 總留言數: {total_comments}
- 最活躍 subreddit: r/{top_subreddits[0][0] if top_subreddits else 'N/A'}

### 2. 用戶情緒
- 正面評價: {type_counts.get('正面評價', 0)} 則
- 負面評價: {type_counts.get('負面評價', 0)} 則
- 警告/安全: {type_counts.get('警告/安全', 0)} 則
- 教學/技術: {type_counts.get('教學/指南', 0) + type_counts.get('技術分析', 0)} 則

### 3. 關注焦點
"""
    
    if 'security' in keyword_counts or 'cost' in keyword_counts or 'price' in keyword_counts:
        report += "- **安全與成本**：用戶持續關注安全性和 token 消耗問題\n"
    if 'local' in keyword_counts or 'self-hosted' in keyword_counts:
        report += "- **本地部署**：M4 Mac Mini、Raspberry Pi 等本地運行方案受關注\n"
    if 'mcp' in keyword_counts or 'skill' in keyword_counts:
        report += "- **技能生態**：MCP 和技能擴充功能持續被討論\n"
    if 'claude' in keyword_counts:
        report += "- **Claude 整合**：與 Claude Code 的比較和整合討論\n"
    
    report += f"""
---

## 五、資料檔案

- 原始搜尋結果：`{data_dir}/reddit_search_*.json`
- 本報告：`reddit-monitoring/reports/reddit_openclaw_report_{timestamp_file}.md`
- 原始資料彙整：`reddit-monitoring/data/reddit_openclaw_raw_{int(datetime.now().timestamp())}.json`

---

## 附錄：完整貼文清單

| # | Subreddit | 類型 | Upvotes | 標題 |
|---|-----------|------|---------|------|
"""
    
    for i, post in enumerate(unique_posts, 1):
        title_short = post['title'][:45] + '...' if len(post['title']) > 45 else post['title']
        report += f"| {i} | r/{post['subreddit']} | {post['post_type']} | {post['upvotes']} | {title_short} |\n"
    
    report += f"""
---

*本報告由 OpenClaw Reddit 監控系統自動生成*  
*監控時間：{now} (Asia/Taipei)*
"""
    
    # 寫入報告
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f'reddit_openclaw_report_{timestamp_file}.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 同時保存原始資料
    raw_data = {
        'timestamp': now,
        'total_posts': len(unique_posts),
        'total_upvotes': total_upvotes,
        'total_comments': total_comments,
        'posts': unique_posts,
        'stats': {
            'subreddits': dict(subreddit_counts),
            'types': dict(type_counts)
        }
    }
    
    import time
    raw_path = os.path.join(data_dir, f'reddit_openclaw_raw_{int(time.time())}.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 報告已生成: {report_path}")
    print(f"✅ 原始資料: {raw_path}")
    print(f"📊 共採集 {len(unique_posts)} 則貼文，來自 {len(subreddit_counts)} 個 subreddit")
    
    return report_path, raw_path

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    output_dir = os.path.join(os.path.dirname(__file__), 'reports')
    generate_report(data_dir, output_dir)
