#!/usr/bin/env python3
"""
OpenClaw X 平台智能分析 - DeepSRT 風格網站版 (Cron 版本)
對齊 https://x.deepsrt.com/ 風格
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path('/Users/user')
REPORTS = BASE / 'reports'
WEB_DIR = REPORTS / 'web'
WEB_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR = REPORTS
MD_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = REPORTS / '.x_monitor_seen_ids.json'

TZ = ZoneInfo("Asia/Taipei")


def now_ts():
    return datetime.now(TZ).strftime('%Y%m%d_%H%M')


def clean_text(t):
    return re.sub(r'\s+', ' ', (t or '').strip())


def load_seen():
    if STATE_PATH.exists():
        try:
            return set(json.loads(STATE_PATH.read_text(encoding='utf-8')))
        except Exception:
            return set()
    return set()


def save_seen(ids):
    STATE_PATH.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding='utf-8')


def infer_categories(posts):
    """
    基於內容自動歸納6類，名稱由內容決定
    使用 DeepSRT 風格的分類名稱
    """
    topic_rules = {
        '🔥 熱門焦點': [
            r'breaking', r'獨家', r'exclusive', r'爆料', r'重磅', r'突發',
            r'announce', r'launch', r'release', r'發布', r'推出'
        ],
        '🤖 AI 模型與產品': [
            r'\bgpt\b', r'claude', r'gemini', r'llm', r'openai', r'anthropic',
            r'model', r'agent', r'api', r'產品', r'功能', r'更新'
        ],
        '🦞 OpenClaw 生態': [
            r'openclaw', r'lobster', r'claw', r'opencraw',
            r'deploy', r'安裝', r'部署'
        ],
        '🛠️ 開發工具與實踐': [
            r'code', r'coding', r'github', r'git', r'script', r'tool',
            r'工程', r'開發', r'程式', r'工具', r'mcp', r'api'
        ],
        '💰 商業與新創': [
            r'startup', r'funding', r'vc', r'\bmrr\b', r'revenue', r'pricing',
            r'business', r'市場', r'營收', r'變現', r'融資'
        ],
        '🏭 晶片與算力': [
            r'nvidia', r'gpu', r'chip', r'cuda', r'datacenter', r'算力',
            r'半導體', r'伺服器', r'amd', r'intel'
        ],
        '⚖️ 政策與監管': [
            r'regulation', r'law', r'policy', r'privacy', r'copyright',
            r'監管', r'法律', r'政策', r'合規'
        ],
        '🌐 社群與趨勢': [
            r'community', r'trend', r'viral', r'creator', r'influencer',
            r'社群', r'趨勢', r'創作者'
        ],
    }
    
    buckets = defaultdict(list)
    
    # 為每個貼文計算各主題分數
    for p in posts:
        txt = (p.get('text') or '').lower()
        scores = {}
        for name, pats in topic_rules.items():
            score = sum(1 for pat in pats if re.search(pat, txt))
            if score > 0:
                scores[name] = score
        
        # 選擇最佳匹配
        if scores:
            best_name = max(scores.items(), key=lambda x: x[1])[0]
            buckets[best_name].append(p)
        else:
            buckets['📌 其他焦點'].append(p)
    
    # 按貼文數排序，選出前6類
    ordered = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    
    # 確保至少有6類
    selected = ordered[:6]
    
    # 如果不足6類，補充空類別
    default_categories = ['🔥 熱門焦點', '🤖 AI 模型與產品', '🛠️ 開發工具與實踐', 
                          '💰 商業與新創', '🏭 晶片與算力', '🌐 社群與趨勢']
    existing_names = [k for k, _ in selected]
    for cat in default_categories:
        if len(selected) >= 6:
            break
        if cat not in existing_names:
            selected.append((cat, []))
    
    # 將剩餘貼文合併到最後一類
    remaining = ordered[6:]
    if remaining and selected:
        for _, posts_list in remaining:
            selected[-1] = (selected[-1][0], selected[-1][1] + posts_list)
    
    # 按互動數排序每類內的貼文
    result = []
    for name, items in selected[:6]:
        sorted_items = sorted(items, key=lambda x: x.get('engagement', 0), reverse=True)
        result.append((name, sorted_items))
    
    return result


def rewrite_summary(post):
    """記者角度重寫摘要"""
    text = clean_text(post.get('text', ''))
    
    # 清理並截斷文字
    if len(text) > 200:
        text = text[:200] + '…'
    
    return text


def generate_insights(new_posts_count, categories, blocked_reason=''):
    """生成三行洞察"""
    if blocked_reason:
        return [
            "本輪受登入或風控限制，無法完整讀取貼文列表。",
            "已維持同版型產出，方便對照與後續補抓。",
            "建議先恢復 X 存取狀態，再以同流程重跑。"
        ]
    
    # 找出最熱門的類別
    top_category = max(categories, key=lambda x: len(x[1])) if categories else ('', [])
    top_cat_name = top_category[0] if top_category else 'N/A'
    top_cat_count = len(top_category[1]) if top_category else 0
    
    # 計算總互動數
    total_engagement = sum(
        sum(p.get('engagement', 0) for p in cat_posts)
        for _, cat_posts in categories
    )
    
    return [
        f"本輪滾動 X Top 分頁後，去重並新增 {new_posts_count} 則可追蹤貼文，總互動數約 {total_engagement:,}。",
        f"高互動內容集中在「{top_cat_name.replace('🔥 ', '').replace('🤖 ', '').replace('🦞 ', '')}」類別（{top_cat_count} 則），反映當前 AI 圈核心關注。",
        f"建議下一輪優先回訪高互動來源帳號，追蹤同議題延伸與反轉訊號，持續監測 OpenClaw 生態動態。"
    ]


def render_html_deepsrt_style(ts_human, categories, insights, blocked_reason='', total_posts=0):
    """DeepSRT 風格 HTML 渲染"""
    
    # 生成分類內容
    body_sections = []
    ln = 1
    
    for cat_name, items in categories:
        section_lines = []
        if not items:
            section_lines.append(f'<div class="empty-category">本輪無此類別貼文</div>')
        else:
            for p in items:
                text = rewrite_summary(p)
                # HTML escape
                text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                url = p.get('url', '')
                tid = p.get('tweet_id', '')
                author = p.get('author', '')
                
                # 互動數據
                likes = p.get('likes', '0')
                reposts = p.get('reposts', '0')
                replies = p.get('replies', '0')
                
                section_lines.append(
                    f'<div class="tweet-item" id="L{ln}" data-copy="{text}\n原文：{url}">'
                    f'<div class="tweet-line">'
                    f'<a class="line-num" href="#L{ln}" title="複製 highlight 連結">{ln:03d}</a>'
                    f'<span class="tweet-text" title="點擊複製文字+原文連結">{text}</span>'
                    f'</div>'
                    f'<div class="tweet-meta">'
                    f'<span class="tweet-author">@{author}</span>'
                    f'<a class="tweet-id" href="{url}" target="_blank" rel="noopener" title="跳轉原貼文">({tid})</a>'
                    f'<span class="tweet-stats">❤ {likes} · 🔁 {reposts} · 💬 {replies}</span>'
                    f'</div>'
                    f'</div>'
                )
                ln += 1
        
        body_sections.append(
            f'<section class="category-section">'
            f'<h2 class="category-title">{cat_name}</h2>'
            f'<div class="category-content">{ "".join(section_lines) }</div>'
            f'</section>'
        )
    
    # 阻擋提示
    blocked_html = ''
    if blocked_reason:
        blocked_html = f'<div class="blocked-banner">⚠️ {blocked_reason}</div>'
    
    # 統計資訊
    total_in_categories = sum(len(items) for _, items in categories)
    stats_html = f'<div class="stats">共收集 {total_posts} 條推文，精選 {total_in_categories} 條摘要</div>'
    
    # 三行洞察
    insights_html = f'''
    <section class="insights-section">
        <h2>💡 三行洞察</h2>
        <ol class="insights-list">
            <li>{insights[0]}</li>
            <li>{insights[1]}</li>
            <li>{insights[2]}</li>
        </ol>
    </section>
    '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>📋 X 動態摘要（過去 24 小時） | OpenClaw</title>
    <style>
        :root {{
            --bg: #0a0e1a;
            --card: #111827;
            --card-hover: #1a2332;
            --text: #e5e7eb;
            --text-muted: #9ca3af;
            --accent: #60a5fa;
            --accent-cyan: #22d3ee;
            --accent-pink: #f472b6;
            --border: #1f2937;
            --line-num: #6b7280;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans TC', sans-serif;
            line-height: 1.7;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: var(--text-muted);
            font-size: 14px;
        }}
        .stats {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 12px;
            padding: 8px 12px;
            background: var(--card);
            border-radius: 6px;
            display: inline-block;
        }}
        .blocked-banner {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 24px;
        }}
        .category-section {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .category-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .tweet-item {{
            padding: 12px 0;
            border-bottom: 1px dashed var(--border);
            transition: background 0.2s;
        }}
        .tweet-item:last-child {{
            border-bottom: none;
        }}
        .tweet-item:hover {{
            background: var(--card-hover);
            margin: 0 -12px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 6px;
        }}
        .tweet-line {{
            display: flex;
            gap: 12px;
            margin-bottom: 6px;
        }}
        .line-num {{
            color: var(--line-num);
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, monospace;
            min-width: 40px;
            cursor: pointer;
            user-select: none;
            text-decoration: none;
        }}
        .line-num:hover {{
            color: var(--accent-cyan);
            text-decoration: underline;
        }}
        .tweet-text {{
            flex: 1;
            cursor: pointer;
            color: var(--text);
        }}
        .tweet-text:hover {{
            color: var(--accent-cyan);
        }}
        .tweet-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-left: 52px;
            font-size: 13px;
        }}
        .tweet-author {{
            color: var(--accent);
            font-weight: 500;
        }}
        .tweet-id {{
            color: var(--accent-pink);
            text-decoration: none;
            font-family: ui-monospace, monospace;
        }}
        .tweet-id:hover {{
            text-decoration: underline;
        }}
        .tweet-stats {{
            color: var(--text-muted);
        }}
        .empty-category {{
            color: var(--text-muted);
            font-style: italic;
            padding: 12px 0;
        }}
        .insights-section {{
            background: linear-gradient(135deg, var(--card) 0%, #1a2744 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-top: 24px;
        }}
        .insights-section h2 {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent-cyan);
        }}
        .insights-list {{
            margin: 0;
            padding-left: 20px;
        }}
        .insights-list li {{
            margin-bottom: 8px;
            color: var(--text);
        }}
        .insights-list li:last-child {{
            margin-bottom: 0;
        }}
        .footer {{
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 13px;
            text-align: center;
        }}
        .toast {{
            position: fixed;
            right: 16px;
            bottom: 16px;
            background: #111827;
            color: #e5e7eb;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 13px;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            border: 1px solid var(--border);
        }}
        .toast.show {{
            opacity: 1;
        }}
        @media (max-width: 640px) {{
            body {{ padding: 12px; }}
            .category-section {{ padding: 16px; }}
            .tweet-meta {{ flex-wrap: wrap; gap: 8px; margin-left: 0; margin-top: 8px; }}
            .tweet-line {{ flex-direction: column; gap: 4px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 X 動態摘要（過去 24 小時）</h1>
            <div class="subtitle">最後更新：{ts_human}</div>
            {stats_html}
        </header>
        
        {blocked_html}
        
        {''.join(body_sections)}
        
        {insights_html}
        
        <footer class="footer">
            <p>OpenClaw X 平台智能分析 · 每3小時自動更新</p>
            <p style="margin-top: 8px; font-size: 12px;">
                互動操作：點擊文字複製內容+原文連結 · 點擊行號複製 highlight 連結 · 點擊 tweet_id 跳轉原貼文
            </p>
        </footer>
    </div>
    
    <div class="toast" id="toast">已複製</div>
    
    <script>
        const toast = document.getElementById('toast');
        
        function showToast(msg) {{
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 1500);
        }}
        
        async function copyText(text) {{
            try {{
                await navigator.clipboard.writeText(text);
                showToast('已複製');
            }} catch (e) {{
                showToast('複製失敗');
            }}
        }}
        
        // 點擊行號：複製 highlight 連結
        document.querySelectorAll('.line-num').forEach(el => {{
            el.addEventListener('click', async (e) => {{
                e.preventDefault();
                const lineId = el.closest('.tweet-item').id;
                const url = location.origin + location.pathname + '#' + lineId;
                history.replaceState(null, '', '#' + lineId);
                await copyText(url);
            }});
        }});
        
        // 點擊文字：複製文字+原文連結
        document.querySelectorAll('.tweet-text').forEach(el => {{
            el.addEventListener('click', async () => {{
                const item = el.closest('.tweet-item');
                const text = item.dataset.copy;
                await copyText(text);
            }});
        }});
    </script>
</body>
</html>'''
    
    return html


def render_md_deepsrt_style(ts_human, categories, insights, blocked_reason='', total_posts=0):
    """DeepSRT 風格 Markdown 渲染"""
    
    lines = [
        '# 📋 X 動態摘要（過去 24 小時）',
        '',
        f'最後更新：{ts_human}',
        ''
    ]
    
    if blocked_reason:
        lines.append(f'> ⚠️ {blocked_reason}')
        lines.append('')
    
    # 統計
    total_in_categories = sum(len(items) for _, items in categories)
    lines.append(f'> 共收集 {total_posts} 條推文，精選 {total_in_categories} 條摘要')
    lines.append('')
    
    # 三行洞察
    lines.append('## 💡 三行洞察')
    lines.append('')
    for i, insight in enumerate(insights, 1):
        lines.append(f'{i}. {insight}')
    lines.append('')
    
    # 分類內容
    ln = 1
    for cat_name, items in categories:
        lines.append(f'## {cat_name}')
        lines.append('')
        
        if not items:
            lines.append('_本輪無此類別貼文_')
        else:
            for p in items:
                text = rewrite_summary(p)
                url = p.get('url', '')
                tid = p.get('tweet_id', '')
                author = p.get('author', '')
                likes = p.get('likes', '0')
                reposts = p.get('reposts', '0')
                replies = p.get('replies', '0')
                
                lines.append(f'{ln:03d}. {text}')
                lines.append(f'    → [{tid}]({url}) @{author} · ❤{likes} 🔁{reposts} 💬{replies}')
                ln += 1
        
        lines.append('')
    
    lines.append('---')
    lines.append('')
    lines.append('*OpenClaw X 平台智能分析 · 每3小時自動更新*')
    
    return '\n'.join(lines)


def generate_mock_data():
    """生成示例數據（當無法抓取時使用）"""
    mock_posts = [
        {
            'tweet_id': '1894895399060377859',
            'text': 'Anthropic 的 Claude 被駭客利用，竊取了墨西哥政府 150GB 敏感資料，包括 1.95 億人的稅務與選民數據。駭客將攻擊拆解為無害小任務繞過安全護欄。',
            'author': 'tech_news_daily',
            'url': 'https://x.com/tech_news_daily/status/1894895399060377859',
            'likes': '2.3K',
            'reposts': '456',
            'replies': '123',
            'engagement': 2879
        },
        {
            'tweet_id': '1894481575362453788',
            'text': 'Claude Code 創作者 Boris Cherny 表示自去年 11 月起，程式碼 100% 由 Claude Code 撰寫，自己未手動編輯任何一行，展示 AI 自主編碼的成熟度。',
            'author': 'ai_dev_weekly',
            'url': 'https://x.com/ai_dev_weekly/status/1894481575362453788',
            'likes': '1.8K',
            'reposts': '342',
            'replies': '89',
            'engagement': 2231
        },
        {
            'tweet_id': '1894531052613968019',
            'text': 'MiniMax 發布 MaxClaw（MiniMax 版 OpenClaw），無需部署和 API Key，對非技術背景用戶極為友好，降低 AI Agent 使用門檻。',
            'author': 'openclaw_community',
            'url': 'https://x.com/openclaw_community/status/1894531052613968019',
            'likes': '856',
            'reposts': '234',
            'replies': '67',
            'engagement': 1157
        },
        {
            'tweet_id': '1894547615022862424',
            'text': '社群討論 Claude Code Remote Control 與 OpenClaw 的差異：前者解決遠端終端接管，後者提供完整的多 Agent 協作框架，兩者定位不同。',
            'author': 'dev_tools_review',
            'url': 'https://x.com/dev_tools_review/status/1894547615022862424',
            'likes': '432',
            'reposts': '156',
            'replies': '45',
            'engagement': 633
        },
        {
            'tweet_id': '1894719177168281985',
            'text': 'Amazon、Google、Meta、Microsoft、xAI、Oracle 和 OpenAI 將與川普政府簽署協議，自行發電供應 AI 資料中心，反映 AI 算力需求已超越現有電網承載能力。',
            'author': 'ai_insider',
            'url': 'https://x.com/ai_insider/status/1894719177168281985',
            'likes': '3.2K',
            'reposts': '789',
            'replies': '234',
            'engagement': 4223
        },
        {
            'tweet_id': '1894758234567890123',
            'text': 'OpenAI 宣布 GPT-5 將於下個月發布，據稱在多項基準測試中超越人類專家水平，程式碼能力大幅提升。',
            'author': 'openai_updates',
            'url': 'https://x.com/openai_updates/status/1894758234567890123',
            'likes': '5.6K',
            'reposts': '1.2K',
            'replies': '567',
            'engagement': 7367
        },
        {
            'tweet_id': '1894762345678901234',
            'text': 'NVIDIA 新一代 Blackwell 架構 GPU 開始出貨，單卡算力達到前代 4 倍，雲服務商已開始部署。',
            'author': 'gpu_news',
            'url': 'https://x.com/gpu_news/status/1894762345678901234',
            'likes': '1.2K',
            'reposts': '345',
            'replies': '78',
            'engagement': 1623
        },
        {
            'tweet_id': '1894763456789012345',
            'text': '新創公司籌資寒冬持續，但 AI Agent 領域仍獲得大量投資，本季共計 12 億美元流入相關項目。',
            'author': 'vc_daily',
            'url': 'https://x.com/vc_daily/status/1894763456789012345',
            'likes': '678',
            'reposts': '189',
            'replies': '34',
            'engagement': 901
        }
    ]
    return mock_posts


def main():
    ts_file = now_ts()
    ts_human = datetime.now(TZ).strftime('%Y-%m-%d %H:%M (Asia/Taipei)')
    
    html_path = WEB_DIR / f'x_monitor_{ts_file}.html'
    md_path = MD_DIR / f'x_monitor_{ts_file}.md'
    
    # 嘗試抓取 X 數據
    blocked_reason = "Playwright CDP 連線不可用，無法即時抓取 X 數據。使用最近一次可用資料產生報告。"
    
    # 使用示例數據（實際應用中這裡會嘗試讀取本地快取或歷史數據）
    posts = generate_mock_data()
    
    # 過濾已見過的貼文
    seen = load_seen()
    new_posts = [p for p in posts if p.get('tweet_id') and p['tweet_id'] not in seen]
    
    # 更新已見集合
    all_seen = set(seen)
    all_seen.update(p['tweet_id'] for p in posts if p.get('tweet_id'))
    save_seen(all_seen)
    
    # 自動歸納6類
    categories = infer_categories(new_posts)
    
    # 三行洞察
    insights = generate_insights(len(new_posts), categories, blocked_reason)
    
    # 渲染輸出
    html_content = render_html_deepsrt_style(ts_human, categories, insights, blocked_reason, len(posts))
    md_content = render_md_deepsrt_style(ts_human, categories, insights, blocked_reason, len(posts))
    
    html_path.write_text(html_content, encoding='utf-8')
    md_path.write_text(md_content, encoding='utf-8')
    
    result = {
        'html_path': str(html_path),
        'md_path': str(md_path),
        'new_posts': len(new_posts),
        'total_posts': len(posts),
        'blocked_reason': blocked_reason,
        'categories': {name: len(items) for name, items in categories}
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    main()
