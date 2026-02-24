#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit OpenClaw 監控報告生成器
生成繁體中文報告
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import re

def extract_subreddit(url):
    """從 Reddit URL 提取 subreddit 名稱"""
    match = re.search(r'reddit\.com/r/([^/]+)', url)
    return f"r/{match.group(1)}" if match else "Unknown"

def parse_search_file(filepath):
    """解析 firecrawl 搜尋結果檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data.get('success') or 'data' not in data:
            return []
        
        posts = []
        for item in data['data'].get('web', []):
            url = item.get('url', '')
            # 只保留 Reddit 貼文
            if 'reddit.com/r/' in url and '/comments/' in url:
                posts.append({
                    'title': item.get('title', '').replace(' : ', ' | ').split(' | ')[0],
                    'url': url,
                    'description': item.get('description', ''),
                    'subreddit': extract_subreddit(url)
                })
        return posts
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return []

def classify_post(title, description):
    """分類貼文類型"""
    text = (title + " " + description).lower()
    
    if any(k in text for k in ['security', 'danger', 'do not use', 'warning', 'leaked', 'scary']):
        return '警告/安全'
    elif any(k in text for k in ['god-awful', 'overhyped', 'not useful', 'problem', 'worse']):
        return '負面評價'
    elif any(k in text for k in ['game changer', 'cool', 'awesome', 'love it', 'helpful']):
        return '正面評價'
    elif any(k in text for k in ['guide', 'how to', 'tutorial', 'setup']):
        return '教學/指南'
    elif any(k in text for k in ['architecture', 'technical', 'looked into', 'dig']):
        return '技術分析'
    else:
        return '討論/問答'

def generate_report(data_dir, output_dir):
    """生成監控報告"""
    
    # 讀取所有搜尋檔案
    all_posts = []
    search_files = [
        'search_openclaw_1.json',
        'search_openclaw_2.json', 
        'search_clawdbot.json'
    ]
    
    for filename in search_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            posts = parse_search_file(filepath)
            all_posts.extend(posts)
    
    # 去重 (依 URL)
    seen_urls = set()
    unique_posts = []
    for post in all_posts:
        if post['url'] not in seen_urls:
            seen_urls.add(post['url'])
            post['type'] = classify_post(post['title'], post['description'])
            unique_posts.append(post)
    
    # 統計
    subreddit_counts = defaultdict(int)
    type_counts = defaultdict(int)
    
    for post in unique_posts:
        subreddit_counts[post['subreddit']] += 1
        type_counts[post['type']] += 1
    
    # 排序
    top_subreddits = sorted(subreddit_counts.items(), key=lambda x: -x[1])
    
    # 生成報告
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    timestamp_file = datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    report = f"""# Reddit OpenClaw 監控報告（繁體中文）

- 產生時間：{now}
- 關鍵字：OpenClaw / openclaw / 龍蝦 / Clawdbot
- 採集貼文數：{len(unique_posts)}

## 一、整體概況

- 涵蓋 subreddit 數：{len(subreddit_counts)}
- Subreddit 分佈：
"""
    
    for sub, count in top_subreddits:
        report += f"  - {sub}: {count} 則\n"
    
    report += f"""
## 二、貼文類型分佈

"""
    for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        report += f"- {ptype}: {count} 則\n"
    
    # 依類型分組顯示
    report += """
## 三、重要貼文摘要

### 🔴 警告/安全類
"""
    for post in unique_posts:
        if post['type'] == '警告/安全':
            report += f"""
**{post['subreddit']}** | {post['title']}
- {post['description'][:120]}...
- 🔗 {post['url']}
"""
    
    report += """
### 🟢 正面評價
"""
    for post in unique_posts:
        if post['type'] == '正面評價':
            report += f"""
**{post['subreddit']}** | {post['title']}
- {post['description'][:120]}...
- 🔗 {post['url']}
"""
    
    report += """
### 🔵 技術分析/教學
"""
    for post in unique_posts:
        if post['type'] in ['技術分析', '教學/指南']:
            report += f"""
**{post['subreddit']}** | {post['title']}
- {post['description'][:120]}...
- 🔗 {post['url']}
"""
    
    report += """
### 🟡 討論/問答
"""
    count = 0
    for post in unique_posts:
        if post['type'] == '討論/問答' and count < 10:
            report += f"""
**{post['subreddit']}** | {post['title']}
- {post['description'][:100]}...
- 🔗 {post['url']}
"""
            count += 1
    
    # 關鍵詞統計
    report += """
## 四、關鍵詞分析

"""
    keywords = ['security', 'token', 'local', 'self-hosted', 'claude', 'openai', 
                'kubernetes', 'docker', 'skill', 'memory', 'cost', 'price']
    keyword_counts = {}
    all_text = ' '.join([p['title'] + ' ' + p['description'] for p in unique_posts]).lower()
    
    for kw in keywords:
        count = all_text.count(kw)
        if count > 0:
            keyword_counts[kw] = count
    
    for kw, count in sorted(keyword_counts.items(), key=lambda x: -x[1]):
        report += f"- {kw}: {count} 次\n"
    
    # 趨勢判讀
    report += """
## 五、趨勢判讀

1. **安全疑慮持續**：多篇貼文警告 OpenClaw 的安全風險，包括權限過大、潛在供應鏈攻擊
2. **成本討論升溫**：用戶關注 token 消耗與實際效益是否成正比
3. **本地部署熱度**：M4 Mac Mini、Raspberry Pi 等本地運行方案受關注
4. **社群技能生態**：700+ 社群技能但缺乏安全審查機制引發擔憂
5. **品牌認知轉移**：Clawdbot → Moltbot → OpenClaw 名稱演變仍在適應期

## 六、資料檔案

"""
    report += f"""
- 原始搜尋結果：
"""
    for f in search_files:
        report += f"  - `reddit-monitoring/data/{f}`\n"
    
    report += f"""
- 本報告：`reddit-monitoring/reports/reddit_openclaw_report_{timestamp_file}.md`

---

## 附錄：完整貼文清單

| # | Subreddit | 類型 | 標題 |
|---|-----------|------|------|
"""
    
    for i, post in enumerate(unique_posts, 1):
        title_short = post['title'][:50] + '...' if len(post['title']) > 50 else post['title']
        report += f"| {i} | {post['subreddit']} | {post['type']} | {title_short} |\n"
    
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
    
    print(f"報告已生成: {report_path}")
    print(f"原始資料: {raw_path}")
    print(f"共採集 {len(unique_posts)} 則貼文，來自 {len(subreddit_counts)} 個 subreddit")
    
    return report_path, raw_path

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    output_dir = os.path.join(os.path.dirname(__file__), 'reports')
    generate_report(data_dir, output_dir)
