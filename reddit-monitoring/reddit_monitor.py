#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit OpenClaw 監控系統
- 採集 Reddit 貼文 (使用 Tavily Search + 直接 API)
- 分析情緒與趨勢
- 生成繁體中文報告
- 歸檔並上傳 GitHub
"""

import json
import os
import sys
import glob
import time
import requests
import subprocess
from datetime import datetime
from collections import defaultdict
import re

# 設定
KEYWORDS = ['OpenClaw', 'openclaw', '龍蝦', 'Clawdbot', 'Moltbot']
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def search_tavily(query):
    """使用 Tavily API 搜尋 Reddit"""
    api_key = os.environ.get('TAVILY_API_KEY')
    if not api_key:
        log("⚠️  TAVILY_API_KEY 未設定，跳過 Tavily 搜尋")
        return []
    
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key": api_key,
                "query": f"{query} reddit",
                "search_depth": "advanced",
                "include_domains": ["reddit.com"],
                "max_results": 20
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            if 'reddit.com/r/' in item.get('url', ''):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0)
                })
        return results
    except Exception as e:
        log(f"❌ Tavily 搜尋失敗: {e}")
        return []

def fetch_reddit_api(subreddit=None, query=None):
    """直接從 Reddit JSON API 獲取資料"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        if subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&sort=new&limit=50"
        else:
            url = f"https://www.reddit.com/search.json?q={query}&sort=new&limit=50"
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 保存原始資料
        timestamp = int(time.time())
        filename = f"reddit_search_{query.replace(' ', '_').lower()}_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        
        log(f"✅ Reddit API 資料已保存: {filename}")
        return filepath
    except Exception as e:
        log(f"❌ Reddit API 請求失敗: {e}")
        return None

def extract_posts_from_file(filepath):
    """從 Reddit JSON 檔案提取貼文"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        posts = []
        children = data.get('data', {}).get('children', [])
        
        for child in children:
            p = child.get('data', {})
            if not p:
                continue
            
            title = p.get('title', '')
            selftext = p.get('selftext', '')
            combined_text = (title + ' ' + selftext).lower()
            
            # 檢查是否與關鍵字相關
            keywords_lower = [k.lower() for k in KEYWORDS]
            if not any(kw in combined_text for kw in keywords_lower):
                continue
            
            posts.append({
                'title': title,
                'url': 'https://reddit.com' + p.get('permalink', ''),
                'content': selftext[:1000] if selftext else '',
                'subreddit': p.get('subreddit', 'Unknown'),
                'author': p.get('author', 'Unknown'),
                'upvotes': p.get('ups', 0),
                'comments_count': p.get('num_comments', 0),
                'created_utc': p.get('created_utc', 0),
                'post_type': classify_post(title, selftext),
                'id': p.get('id', ''),
                'source_file': os.path.basename(filepath)
            })
        
        return posts
    except Exception as e:
        log(f"❌ 解析檔案失敗 {filepath}: {e}")
        return []

def classify_post(title, content):
    """分類貼文類型"""
    text = (title + ' ' + content).lower()
    
    if any(k in text for k in ['security', 'danger', 'warning', 'leaked', 'unsafe', 'vulnerability']):
        return '⚠️ 警告/安全'
    elif any(k in text for k in ['overhyped', 'problem', 'worse', 'burned', 'waste', 'disappointed', 'bad']):
        return '👎 負面評價'
    elif any(k in text for k in ['cool', 'awesome', 'love it', 'helpful', 'amazing', 'best', 'great']):
        return '👍 正面評價'
    elif any(k in text for k in ['guide', 'how to', 'tutorial', 'setup', 'tips']):
        return '📚 教學/指南'
    elif any(k in text for k in ['architecture', 'technical', 'deep dive', 'analysis']):
        return '🔬 技術分析'
    elif any(k in text for k in ['vs', 'compare', 'alternative', 'better than']):
                return '⚖️ 比較/對比'
    else:
        return '💬 討論/問答'

def collect_data():
    """採集資料"""
    log("🚀 開始採集 Reddit 資料...")
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. 從 Reddit API 搜尋
    queries = ['OpenClaw', 'clawdbot', 'moltbot', 'claude code assistant']
    for query in queries:
        fetch_reddit_api(query=query)
        time.sleep(1)  # 避免請求過快
    
    # 2. 從特定 subreddit 搜尋
    subreddits = ['LocalLLaMA', 'ClaudeAI', 'ArtificialInteligence', 'singularity']
    for sub in subreddits:
        fetch_reddit_api(subreddit=sub, query='openclaw OR clawdbot OR moltbot')
        time.sleep(1)
    
    log("✅ 資料採集完成")

def analyze_data():
    """分析資料"""
    log("📊 開始分析資料...")
    
    # 讀取所有搜尋檔案
    all_posts = []
    search_files = glob.glob(os.path.join(DATA_DIR, 'reddit_search_*.json'))
    
    log(f"找到 {len(search_files)} 個搜尋檔案")
    
    for filepath in search_files:
        posts = extract_posts_from_file(filepath)
        all_posts.extend(posts)
        if posts:
            log(f"  - {os.path.basename(filepath)}: {len(posts)} 則相關貼文")
    
    # 去重 (依 ID)
    seen_ids = set()
    unique_posts = []
    for post in all_posts:
        if post['id'] not in seen_ids:
            seen_ids.add(post['id'])
            unique_posts.append(post)
    
    # 依 upvotes 排序
    unique_posts.sort(key=lambda x: x['upvotes'], reverse=True)
    
    log(f"✅ 分析完成，共 {len(unique_posts)} 則唯一貼文")
    return unique_posts

def generate_report(posts):
    """生成繁體中文報告"""
    log("📝 生成報告...")
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # 統計
    subreddit_counts = defaultdict(int)
    type_counts = defaultdict(int)
    total_upvotes = 0
    total_comments = 0
    
    for post in posts:
        subreddit_counts[post['subreddit']] += 1
        type_counts[post['post_type']] += 1
        total_upvotes += post['upvotes']
        total_comments += post['comments_count']
    
    top_subreddits = sorted(subreddit_counts.items(), key=lambda x: -x[1])[:10]
    
    # 生成報告
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    timestamp_file = datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    report = f"""# 🦞 Reddit OpenClaw 監控報告（繁體中文）

> **產生時間**：{now} (Asia/Taipei)  
> **監控關鍵字**：OpenClaw、openclaw、龍蝦、Clawdbot、Moltbot  
> **採集貼文數**：{len(posts)}  
> **總 Upvotes**：{total_upvotes} ⬆️  
> **總留言數**：{total_comments} 💬

---

## 一、整體概況

### 📍 Subreddit 分佈

| Subreddit | 貼文數 |
|-----------|--------|
"""
    
    for sub, count in top_subreddits:
        report += f"| r/{sub} | {count} |\n"
    
    report += f"""
### 📊 貼文類型分佈

| 類型 | 數量 |
|------|------|
"""
    for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        report += f"| {ptype} | {count} |\n"
    
    # 重要貼文摘要
    report += """
---

## 二、重要貼文摘要

"""
    
    # 各類型貼文
    for ptype in ['⚠️ 警告/安全', '👍 正面評價', '👎 負面評價', '📚 教學/指南', '🔬 技術分析']:
        type_posts = [p for p in posts if p['post_type'] == ptype]
        if type_posts:
            report += f"### {ptype}\n\n"
            for post in type_posts[:5]:
                content_preview = post['content'][:200] if post['content'] else '無內容預覽'
                created_time = datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d') if post['created_utc'] else '未知'
                report += f"**[{post['upvotes']}⬆️] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
                report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | 發布: {created_time}\n"
                report += f"- {content_preview}...\n\n"
    
    # 熱門討論
    report += "### 💬 熱門討論（依 Upvotes 排序）\n\n"
    discussion_posts = [p for p in posts if p['post_type'] == '💬 討論/問答'][:10]
    for post in discussion_posts:
        created_time = datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d') if post['created_utc'] else '未知'
        report += f"**[{post['upvotes']}⬆️] r/{post['subreddit']}** | [{post['title']}]({post['url']})\n"
        report += f"- 作者: u/{post['author']} | 留言: {post['comments_count']} | 發布: {created_time}\n\n"
    
    # 關鍵詞分析
    report += """---

## 三、關鍵詞分析

"""
    keywords = ['security', 'token', 'local', 'self-hosted', 'claude', 'openai', 
                'kubernetes', 'docker', 'skill', 'memory', 'cost', 'price', 'mcp',
                'setup', 'guide', 'tutorial']
    keyword_counts = {}
    all_text = ' '.join([p['title'] + ' ' + p['content'] for p in posts]).lower()
    
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

### 1. 📈 社群熱度指標

- **總貼文數**: {len(posts)} 則
- **總 upvotes**: {total_upvotes} ⬆️
- **總留言數**: {total_comments} 💬
- **平均 upvotes**: {total_upvotes // len(posts) if posts else 0} ⬆️/貼文
- **最活躍 subreddit**: r/{top_subreddits[0][0] if top_subreddits else 'N/A'}

### 2. 😊 用戶情緒分佈

| 情緒類型 | 數量 |
|----------|------|
| 👍 正面評價 | {type_counts.get('👍 正面評價', 0)} 則 |
| 👎 負面評價 | {type_counts.get('👎 負面評價', 0)} 則 |
| ⚠️ 警告/安全 | {type_counts.get('⚠️ 警告/安全', 0)} 則 |
| 📚 教學/指南 | {type_counts.get('📚 教學/指南', 0)} 則 |
| 🔬 技術分析 | {type_counts.get('🔬 技術分析', 0)} 則 |
| 💬 討論/問答 | {type_counts.get('💬 討論/問答', 0)} 則 |

### 3. 🔍 關注焦點

"""
    
    if 'security' in keyword_counts:
        report += "- **🔒 安全議題**：用戶持續關注安全性和權限問題\n"
    if 'cost' in keyword_counts or 'price' in keyword_counts or 'token' in keyword_counts:
        report += "- **💰 成本效益**：token 消耗與實際效益的討論\n"
    if 'local' in keyword_counts or 'self-hosted' in keyword_counts:
        report += "- **🏠 本地部署**：M4 Mac Mini、Raspberry Pi 等本地運行方案受關注\n"
    if 'mcp' in keyword_counts or 'skill' in keyword_counts:
        report += "- **🧩 技能生態**：MCP 和技能擴充功能持續被討論\n"
    if 'claude' in keyword_counts:
        report += "- **🤖 Claude 整合**：與 Claude Code 的比較和整合討論\n"
    
    report += f"""
---

## 五、資料檔案歸檔

- **原始搜尋結果**：`reddit-monitoring/data/reddit_search_*.json`
- **本報告**：`reddit-monitoring/reports/reddit_openclaw_report_{timestamp_file}.md`
- **原始資料彙整**：`reddit-monitoring/data/reddit_openclaw_enhanced_{int(time.time())}.json`

---

## 附錄：完整貼文清單

| # | Subreddit | 類型 | Upvotes | 標題 |
|---|-----------|------|---------|------|
"""
    
    for i, post in enumerate(posts, 1):
        title_short = post['title'][:40] + '...' if len(post['title']) > 40 else post['title']
        report += f"| {i} | r/{post['subreddit']} | {post['post_type']} | {post['upvotes']} | {title_short} |\n"
    
    report += f"""
---

*本報告由 OpenClaw Reddit 監控系統自動生成*  
*監控時間：{now} (Asia/Taipei)*  
*任務 ID: reddit-openclaw-monitor*
"""
    
    # 寫入報告
    report_path = os.path.join(REPORTS_DIR, f'reddit_openclaw_report_{timestamp_file}.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存原始資料彙整
    raw_data = {
        'timestamp': now,
        'total_posts': len(posts),
        'total_upvotes': total_upvotes,
        'total_comments': total_comments,
        'posts': posts,
        'stats': {
            'subreddits': dict(subreddit_counts),
            'types': dict(type_counts),
            'keywords': keyword_counts
        }
    }
    
    raw_path = os.path.join(DATA_DIR, f'reddit_openclaw_enhanced_{int(time.time())}.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    
    log(f"✅ 報告已生成: {report_path}")
    log(f"✅ 資料已歸檔: {raw_path}")
    
    return report_path, raw_path

def push_to_github():
    """上傳到 GitHub"""
    log("🚀 上傳到 GitHub...")
    
    try:
        # 檢查是否在 git repo 中
        result = subprocess.run(
            ['git', '-C', os.path.dirname(__file__), 'status', '--porcelain'],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            log("⚠️  不是 git repository，跳過 GitHub 上傳")
            return False
        
        # 添加變更
        subprocess.run(
            ['git', '-C', os.path.dirname(__file__), 'add', 'data/', 'reports/'],
            capture_output=True
        )
        
        # 提交
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        result = subprocess.run(
            ['git', '-C', os.path.dirname(__file__), 'commit', '-m', f'Reddit OpenClaw 監控報告 - {now}'],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            # 推送
            subprocess.run(
                ['git', '-C', os.path.dirname(__file__), 'push'],
                capture_output=True
            )
            log("✅ GitHub 上傳完成")
            return True
        else:
            log("ℹ️  無新變更需要提交")
            return False
            
    except Exception as e:
        log(f"❌ GitHub 上傳失敗: {e}")
        return False

def main():
    log("="*60)
    log("🦞 Reddit OpenClaw 監控系統啟動")
    log("="*60)
    
    # 步驟 1: 採集
    collect_data()
    
    # 步驟 2: 分析
    posts = analyze_data()
    
    if not posts:
        log("⚠️  未找到相關貼文，嘗試從現有檔案分析...")
        # 嘗試從現有檔案分析
        all_posts = []
        for filepath in glob.glob(os.path.join(DATA_DIR, 'reddit_search_*.json')):
            all_posts.extend(extract_posts_from_file(filepath))
        
        # 去重
        seen_ids = set()
        posts = []
        for post in all_posts:
            if post['id'] not in seen_ids:
                seen_ids.add(post['id'])
                posts.append(post)
        posts.sort(key=lambda x: x['upvotes'], reverse=True)
        
        log(f"從現有檔案找到 {len(posts)} 則相關貼文")
    
    # 步驟 3: 生成報告
    if posts:
        report_path, raw_path = generate_report(posts)
    else:
        log("⚠️  無可用資料生成報告")
        report_path = None
    
    # 步驟 4: 上傳 GitHub
    push_to_github()
    
    log("="*60)
    log("✅ 監控任務完成")
    log("="*60)
    
    return report_path

if __name__ == '__main__':
    main()
