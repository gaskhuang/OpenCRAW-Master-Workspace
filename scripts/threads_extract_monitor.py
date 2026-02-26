#!/usr/bin/env python3
"""
Threads Monitor - 使用 browser-use 會話提取內容
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

def extract_from_browser_use():
    """使用 browser-use 提取 Threads 內容"""
    import subprocess
    
    # 首先滾動頁面多次來加載內容
    print("📜 開始滾動頁面加載內容...")
    
    # 滾動 80 次
    for i in range(80):
        result = subprocess.run(
            ["browser-use", "scroll", "down", "--amount", "800"],
            capture_output=True, text=True
        )
        if i % 20 == 0:
            print(f"  已滾動 {i}/80 次")
        # 短暫等待
        import time
        time.sleep(0.5)
    
    print("✅ 滾動完成，開始提取內容...")
    
    # 使用 JavaScript 提取內容
    js_code = """
(() => {
    const results = [];
    const articles = document.querySelectorAll('article, div[role="article"]');
    
    articles.forEach(article => {
        try {
            // 尋找作者
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
            
            // 尋找帖子連結
            const postLinks = article.querySelectorAll('a[href*="/post/"]');
            let postUrl = '';
            let postId = '';
            
            for (const link of postLinks) {
                const href = link.getAttribute('href') || '';
                const match = href.match(/\\/post\\/([A-Za-z0-9_-]+)/);
                if (match) {
                    postId = match[1];
                    postUrl = href.startsWith('http') ? href : 'https://www.threads.com' + href;
                    break;
                }
            }
            
            if (!postId) return;
            
            // 尋找時間
            const timeEl = article.querySelector('time');
            const createdAt = timeEl ? timeEl.getAttribute('datetime') : '';
            const timeText = timeEl ? timeEl.textContent?.trim() : '';
            
            // 尋找內容
            let text = '';
            const allDivs = article.querySelectorAll('div[dir="auto"]');
            for (const el of allDivs) {
                const txt = el.textContent?.trim() || '';
                if (txt.length > text.length && txt.length < 5000 && !txt.includes('@' + username)) {
                    text = txt;
                }
            }
            
            // 尋找互動數 - 尋找所有數字
            let likes = null;
            let replies = null;
            const spans = article.querySelectorAll('span');
            const numbers = [];
            
            for (const span of spans) {
                const txt = span.textContent?.trim() || '';
                if (/^[\\d,.]+[\\dkm萬千]?$/i.test(txt)) {
                    numbers.push(txt);
                }
            }
            
            // 通常順序：回覆、轉發、引用、讚
            if (numbers.length >= 1) replies = numbers[0];
            if (numbers.length >= 2) likes = numbers[numbers.length - 1];
            
            results.push({
                post_id: postId,
                author: displayName,
                author_username: username,
                created_at: createdAt,
                time_text: timeText,
                text: text,
                likes: likes,
                replies: replies,
                url: postUrl
            });
        } catch (e) {}
    });
    
    return JSON.stringify(results);
})()
    """
    
    # 執行 JavaScript
    result = subprocess.run(
        ["browser-use", "eval", js_code],
        capture_output=True, text=True
    )
    
    output = result.stdout + result.stderr
    
    # 嘗試解析 JSON 結果
    try:
        # 尋找 JSON 部分
        json_match = re.search(r'result:\\s*(\\[.*?\\])', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # 直接解析整個輸出
        return json.loads(output)
    except Exception as e:
        print(f"解析錯誤: {e}")
        print(f"輸出: {output[:500]}")
        return []

def categorize_posts(posts):
    """依內容自動分類貼文"""
    categories = {
        "💻 科技資訊": [],
        "💰 財經金融": [],
        "🎬 娛樂影視": [],
        "⚽ 體育運動": [],
        "📰 政治時事": [],
        "🌍 國際社會": [],
        "🎨 創意設計": [],
        "💬 生活閒談": [],
    }
    
    tech_keywords = ['ai', '人工智能', '程式', 'coding', 'developer', 'app', '軟體', '科技', 'tech', 'startup', '創業', 'code', 'python', 'javascript']
    finance_keywords = ['股票', '投資', 'crypto', '比特幣', 'ethereum', '理財', '金融', '財經', 'market', '經濟']
    entertainment_keywords = ['電影', 'music', '歌曲', '演唱會', '明星', '韓劇', 'netflix', 'disney', '遊戲', 'game', '偶像', '粉絲']
    sports_keywords = ['nba', '足球', 'mlb', '奧運', '體育', '運動', '球賽', '冠軍']
    politics_keywords = ['政治', '選舉', '總統', '政府', '政策', '立法院', '議會', '黨團']
    international_keywords = ['usa', 'america', 'china', 'japan', '歐洲', '國際', 'global', 'war', '衝突']
    design_keywords = ['設計', 'design', '藝術', 'art', '攝影', 'photo', '插畫', 'illustration']
    
    for post in posts:
        text = (post.get('text', '') + ' ' + post.get('author_username', '')).lower()
        categorized = False
        
        if any(kw in text for kw in tech_keywords):
            categories["💻 科技資訊"].append(post)
            categorized = True
        if any(kw in text for kw in finance_keywords):
            categories["💰 財經金融"].append(post)
            categorized = True
        if any(kw in text for kw in entertainment_keywords):
            categories["🎬 娛樂影視"].append(post)
            categorized = True
        if any(kw in text for kw in sports_keywords):
            categories["⚽ 體育運動"].append(post)
            categorized = True
        if any(kw in text for kw in politics_keywords):
            categories["📰 政治時事"].append(post)
            categorized = True
        if any(kw in text for kw in international_keywords):
            categories["🌍 國際社會"].append(post)
            categorized = True
        if any(kw in text for kw in design_keywords):
            categories["🎨 創意設計"].append(post)
            categorized = True
        
        if not categorized:
            categories["💬 生活閒談"].append(post)
    
    # 過濾空類別
    return {k: v for k, v in categories.items() if v}

def extract_keywords(posts):
    """提取熱門關鍵詞"""
    from collections import Counter
    
    all_text = ' '.join([p.get('text', '') for p in posts]).lower()
    
    # 提取 hashtag 和常見詞
    hashtags = re.findall(r'#(\w+)', all_text)
    words = re.findall(r'\b[a-z]{4,}\b', all_text)
    
    # 計數
    counter = Counter(hashtags + words)
    
    # 過濾常見詞
    stopwords = {'this', 'that', 'with', 'from', 'they', 'have', 'will', 'been', 'their', 'what', 'when', 'where', 'which', 'while', 'about', 'after', 'before', 'being', 'https', 'thread', 'like', 'just', 'know', 'want', 'think', 'need'}
    keywords = [(kw, count) for kw, count in counter.most_common(30) if kw not in stopwords and len(kw) > 3]
    
    return [kw for kw, _ in keywords[:10]]

def generate_report(posts):
    """生成記者版深度摘要報告"""
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    filename_timestamp = now.strftime("%Y%m%d_%H%M")
    
    # 去重
    seen_ids = set()
    unique_posts = []
    for post in posts:
        if post.get('post_id') not in seen_ids:
            seen_ids.add(post.get('post_id'))
            unique_posts.append(post)
    
    # 載入已見 IDs
    seen_ids_file = Path("/Users/user/reports/.threads_monitor_seen_ids.json")
    if seen_ids_file.exists():
        with open(seen_ids_file, 'r') as f:
            seen_data = json.load(f)
    else:
        seen_data = {}
    
    # 只保留新的帖子
    new_posts = [p for p in unique_posts if p.get('post_id') not in seen_data]
    
    # 更新已見 IDs
    for post in new_posts:
        seen_data[post.get('post_id')] = now.isoformat()
    
    # 保存已見 IDs
    seen_ids_file.parent.mkdir(parents=True, exist_ok=True)
    with open(seen_ids_file, 'w') as f:
        json.dump(seen_data, f, ensure_ascii=False)
    
    print(f"📝 總共收集: {len(unique_posts)} 篇唯一帖子")
    print(f"🆕 本輪新增: {len(new_posts)} 篇帖子")
    
    # 分析貼文內容進行分類
    categories = categorize_posts(new_posts)
    
    # 生成報告內容
    lines = [
        "# Threads 動態深度摘要（過去 3 小時）",
        "",
        f"> 任務時間：{timestamp} (Asia/Taipei)",
        f"> 採集流程：Threads 首頁流 → 連續下滑 80 次 → 前後集合去重",
        f"> 本輪新增貼文（去重後）：{len(new_posts)}",
        "",
    ]
    
    if not new_posts:
        lines.extend([
            "## ⚠️ 抓取受阻",
            "",
            "本輪未能提取到新帖子。可能原因：",
            "- Threads 未登入狀態下內容有限",
            "- 頁面載入問題",
            "- 反爬機制",
            "",
        ])
    else:
        # 各分類內容
        line_num = 1
        for cat_name, cat_posts in categories.items():
            if not cat_posts:
                continue
            lines.append(f"## {cat_name}")
            lines.append("")
            
            for post in cat_posts[:15]:  # 每類最多 15 則
                text = post.get('text', '')[:120]  # 限制摘要長度
                if len(post.get('text', '')) > 120:
                    text += '...'
                
                # 清理文本用於顯示
                text = text.replace('\\n', ' ').strip()
                
                author = post.get('author_username') or post.get('author') or 'Unknown'
                post_id = post.get('post_id', '')
                url = post.get('url') or f"https://www.threads.net/@{author}"
                likes = post.get('likes', 0) or 0
                
                summary = f"[{line_num}] **@{author}**: {text} 👍{likes} [（{post_id[:15]}...）]({url})"
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
    
    if new_posts:
        # 按點讚數排序
        sorted_posts = sorted(new_posts, key=lambda x: int(str(x.get('likes', 0)).replace(',', '').replace('k', '000').replace('萬', '0000') or 0), reverse=True)[:3]
        for i, post in enumerate(sorted_posts, 1):
            text = post.get('text', '')[:80]
            if len(post.get('text', '')) > 80:
                text += '...'
            author = post.get('author_username') or post.get('author') or 'Unknown'
            likes = post.get('likes', 0) or 0
            lines.append(f"{i}. **@{author}** 的內容獲得 {likes} 讚：{text}")
    else:
        lines.extend([
            "1. 本輪未能成功抓取新內容",
            "2. Threads 未登入狀態下內容存取受限",
            "3. 建議檢查登入狀態或網路連接",
        ])
    
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
    
    # 下一輪追蹤關鍵詞
    if new_posts:
        keywords = extract_keywords(new_posts)
    else:
        keywords = ['AI', '科技', '娛樂', '設計', '生活']
    
    lines.extend([
        "---",
        "",
        "## 下一輪追蹤關鍵詞",
        "",
    ])
    for kw in keywords[:10]:
        lines.append(f"- {kw}")
    
    content = "\\n".join(lines)
    
    # 保存報告
    report_path = Path(f"/Users/user/reports/threads_top_news_{filename_timestamp}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    
    return str(report_path), len(new_posts)

def main():
    print("=" * 60)
    print("🚀 Threads OpenClaw 監控 - 記者版")
    print(f"📅 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 提取內容
    posts = extract_from_browser_use()
    
    print(f"\\n📊 提取到 {len(posts)} 篇帖子")
    
    # 生成報告
    report_path, count = generate_report(posts)
    
    print(f"\\n✅ 報告已生成: {report_path}")
    print(f"📊 本輪新增: {count} 篇帖子")

if __name__ == "__main__":
    main()
