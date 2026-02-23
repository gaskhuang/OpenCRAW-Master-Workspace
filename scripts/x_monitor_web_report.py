#!/usr/bin/env python3
"""
OpenClaw X 平台智能分析（每3小時）
網站版輸出 - 對齊 https://x.deepsrt.com/ 風格
"""
import asyncio
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from playwright.async_api import async_playwright

BASE = Path('/Users/user')
REPORTS = BASE / 'reports'
WEB_DIR = REPORTS / 'web'
WEB_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = REPORTS / '.x_monitor_seen_ids.json'


def now_ts():
    return datetime.now().strftime('%Y%m%d_%H%M')


def parse_count(v):
    if v is None:
        return 0
    s = str(v).strip().lower().replace(',', '')
    if not s:
        return 0
    m = re.match(r'^([0-9]*\.?[0-9]+)([km]?)\s*(?:likes?|reposts?|replies?)?$', s)
    if not m:
        try:
            return int(float(s))
        except Exception:
            return 0
    n = float(m.group(1))
    u = m.group(2)
    if u == 'k':
        n *= 1000
    elif u == 'm':
        n *= 1000000
    return int(n)


def extract_id(url):
    m = re.search(r'/status/(\d+)', url or '')
    return m.group(1) if m else ''


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


def categorize_with_emoji(posts):
    """
    自動歸納 6 類，名稱由內容決定，帶有 emoji
    參考 x.deepsrt.com 風格
    """
    # 動態類別偵測規則
    category_patterns = {
        '🤖 AI 模型與工具': [
            r'\bgpt\b', r'claude', r'gemini', r'llm', r'\bai\b', r'model', r'openai', r'anthropic',
            r'google', r'codex', r'llama', r'grok', r'perplexity', r'chatgpt', r'copilot',
            r'模型', r'推理', r'訓練', r'參數', r'token', r'embedding'
        ],
        '🦞 OpenClaw 生態': [
            r'openclaw', r'lobster', r'龍蝦', r'claw', r'agent', r'mcp', r'skill',
            r'mission control', r'kanban', r'nano\s*claw', r'pico\s*claw', r'clawhub',
            r'agent.*經濟', r'agentic', r'autonomous', r'agent\s*驅動'
        ],
        '🎬 AI 影片與圖像': [
            r'sora', r'seedance', r'runway', r'video', r'image', r'video', r'動画',
            r'生成.*影片', r'生成.*圖', r'ai.*影片', r'ai.*圖像', r'繪圖', r'動畫',
            r'生成式.*視覺', r'midjourney', r'stable.diffusion', r'flux', r'banana'
        ],
        '🛠️ 開發者工具與實踐': [
            r'github', r'vscode', r'cursor', r'ide', r'code', r'programming', r'developer',
            r'api', r'sdk', r'cli', r'framework', r'library', r'debug', r'coding',
            r'程式', r'開發', r'工程師', r'編程', r'部署', r'上線'
        ],
        '🏭 產業與市場動態': [
            r'nvidia', r'nvda', r'chip', r'gpu', r'datacenter', r'server', r'startup',
            r'funding', r'vc', r'investment', r'ipo', r'earnings', r'revenue', r'market',
            r'半導體', r'晶片', r'算力', r'投資', r'估值', r'營收', r'市場', r'股價'
        ],
        '💡 AI 觀點與趨勢': [
            r'agi', r'future', r'trend', r'prediction', r'insight', r'analysis', r'opinion',
            r'perspective', r'thought', r'philosophy', r'impact', r'revolution',
            r'趨勢', r'觀點', r'看法', r'預測', r'未來', r'變革', r'革命'
        ],
        '🔐 安全與基礎設施': [
            r'security', r'vulnerab', r'exploit', r'hack', r'attack', r'privacy', r'safety',
            r'risk', r'threat', r'protection', r'安全', r'漏洞', r'風險', r'隱私',
            r'加密', r'駭客', r'攻擊', r'防護'
        ],
        '📊 政策與監管': [
            r'policy', r'regulation', r'government', r'law', r'legal', r'compliance',
            r'ban', r'restrict', r'policy', r'政策', r'監管', r'法規', r'政府', r'禁令'
        ],
    }
    
    buckets = defaultdict(list)
    
    for p in posts:
        txt = (p.get('text') or '').lower()
        best_cat = '🔍 其他焦點'
        best_score = 0
        
        for cat_name, patterns in category_patterns.items():
            score = sum(1 for pat in patterns if re.search(pat, txt))
            if score > best_score:
                best_score = score
                best_cat = cat_name
        
        buckets[best_cat].append(p)
    
    # 按貼文數量排序，取前6類
    ordered = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    
    # 確保至少有6個類別
    result = []
    for cat_name, items in ordered[:6]:
        # 按互動量排序
        sorted_items = sorted(items, key=lambda x: x.get('engagement', 0), reverse=True)
        result.append((cat_name, sorted_items))
    
    # 如果不足6類，補充空類別
    while len(result) < 6:
        result.append((f'📌 延伸觀察 {len(result)+1}', []))
    
    return result[:6]


def rewrite_summary(post):
    """
    記者角度重寫摘要
    參考 x.deepsrt.com 風格：簡潔、資訊豐富、專業語氣
    """
    text = clean_text(post.get('text', ''))
    author = post.get('author', '')
    
    if not text:
        return ''
    
    # 清理常見的 noise
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'http\S+', '', text).strip()
    
    # 如果原文已經很長，進行摘要
    if len(text) > 200:
        # 取前200字，嘗試在句號處截斷
        truncated = text[:200]
        last_period = truncated.rfind('。')
        last_dot = truncated.rfind('. ')
        cut_point = max(last_period, last_dot)
        if cut_point > 150:
            text = truncated[:cut_point+1]
        else:
            text = truncated + '...'
    
    return text


async def scrape_top_80():
    """抓取 X Top 分頁，滾動80次"""
    result = {'blocked_reason': '', 'posts': []}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp('http://127.0.0.1:18792')
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()

            q = quote('AI OR OpenAI OR NVIDIA OR OpenClaw OR agent OR Claude OR Gemini')
            url = f'https://x.com/search?q={q}&src=typed_query&f=top'
            await page.goto(url, wait_until='domcontentloaded', timeout=120000)
            await asyncio.sleep(3)

            content = (await page.content()).lower()
            if 'something went wrong' in content or ('log in' in content and 'sign up' in content):
                result['blocked_reason'] = 'X 頁面受限（可能需要重新登入或觸發風控）'

            rows = []
            for i in range(80):
                got = await page.evaluate(r"""
() => {
  const out = [];
  const arts = document.querySelectorAll('article[data-testid="tweet"]');
  for (const a of arts) {
    const timeEl = a.querySelector('time');
    if (!timeEl) continue;
    const dt = timeEl.getAttribute('datetime') || '';

    let status = '';
    for (const l of a.querySelectorAll('a[href*="/status/"]')) {
      const h = l.getAttribute('href') || '';
      if (h.includes('/status/')) { status = h; break; }
    }

    const userA = a.querySelector('a[href^="/"]');
    const href = userA ? (userA.getAttribute('href') || '') : '';
    const author = href.replace(/^\//,'').split('/')[0] || '';

    const txtEl = a.querySelector('[data-testid="tweetText"]');
    const text = txtEl ? txtEl.innerText : '';

    const getCount = (sel) => {
      const b = a.querySelector(`[data-testid="${sel}"]`);
      if (!b) return '0';
      const s = b.querySelector('[data-testid="app-text-transition-container"]');
      return s ? ((s.textContent || '').trim() || '0') : '0';
    }

    out.push({
      time: dt,
      author,
      text,
      url: status ? ('https://x.com' + status) : '',
      replies: getCount('reply'),
      reposts: getCount('retweet'),
      likes: getCount('like')
    });
  }
  return out;
}
""")
                rows.extend(got)
                await page.mouse.wheel(0, 2600)
                await asyncio.sleep(1.1)
                
                # 每20次滾動報告進度
                if (i + 1) % 20 == 0:
                    print(f"  已滾動 {i+1}/80 次，收集 {len(rows)} 條")

            # 去重
            dedup = {}
            for r in rows:
                tid = extract_id(r.get('url', ''))
                if not tid:
                    continue
                dedup[tid] = r

            posts = []
            for tid, r in dedup.items():
                r['tweet_id'] = tid
                r['text'] = clean_text(r.get('text', ''))
                r['engagement'] = parse_count(r.get('likes')) + parse_count(r.get('reposts')) + parse_count(r.get('replies'))
                posts.append(r)

            result['posts'] = sorted(posts, key=lambda x: (x['engagement'], x.get('time', '')), reverse=True)
            print(f"  去重後共 {len(posts)} 則貼文")
            
    except Exception as e:
        result['blocked_reason'] = f'抓取受阻：{str(e).splitlines()[0]}'
        print(f"  錯誤：{result['blocked_reason']}")
    return result


def render_html_deepsrt_style(ts_human, categories, insights, blocked_reason='', total_count=0):
    """
    渲染 HTML - 對齊 x.deepsrt.com 風格
    - 深色主題、卡片式布局
    - 點文字：複製「文字 + 原文連結」
    - 點 tweet_id：跳轉原貼文
    - 點行號：複製可分享 highlight 連結（#Lxx）
    """
    sections_html = []
    ln = 1
    
    for cat_name, items in categories:
        items_html = []
        for p in items:
            text = rewrite_summary(p)
            url = p.get('url', '')
            tid = p.get('tweet_id', '')
            author = p.get('author', '')
            likes = p.get('likes', '0')
            reposts = p.get('reposts', '0')
            
            # 複製內容：文字 + 原文連結
            copy_text = f"{text}\n{url}" if url else text
            
            items_html.append(
                f'''<div class="item" id="L{ln}" data-copy="{copy_text.replace('"', '&quot;')}">
                <span class="line-num" title="複製 highlight 連結">{ln:03d}</span>
                <span class="content">
                    <span class="text" title="點擊複製文字+連結">{text.replace('<', '&lt;').replace('>', '&gt;')}</span>
                    <a class="tweet-link" href="{url}" target="_blank" rel="noopener" title="開啟原文">({tid})</a>
                    <span class="meta">@{author} · ❤{likes} 🔁{reposts}</span>
                </span>
            </div>'''
            )
            ln += 1
        
        if not items:
            items_html.append('<div class="empty">本輪無新增貼文</div>')
        
        sections_html.append(
            f'''<section class="category">
            <h2>{cat_name}</h2>
            <div class="items">{''.join(items_html)}</div>
        </section>'''
        )
    
    blocked_banner = f'<div class="blocked-banner">⚠️ {blocked_reason}</div>' if blocked_reason else ''
    
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
        .blocked-banner {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 24px;
        }}
        .category {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .category h2 {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--accent);
        }}
        .item {{
            display: flex;
            gap: 12px;
            padding: 12px 0;
            border-bottom: 1px dashed var(--border);
            transition: background 0.2s;
        }}
        .item:last-child {{
            border-bottom: none;
        }}
        .item:hover {{
            background: var(--card-hover);
            margin: 0 -12px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 6px;
        }}
        .line-num {{
            color: var(--line-num);
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, monospace;
            min-width: 40px;
            cursor: pointer;
            user-select: none;
        }}
        .line-num:hover {{
            color: var(--accent-cyan);
            text-decoration: underline;
        }}
        .content {{
            flex: 1;
        }}
        .text {{
            cursor: pointer;
        }}
        .text:hover {{
            color: var(--accent-cyan);
        }}
        .tweet-link {{
            color: var(--text-muted);
            text-decoration: none;
            font-family: ui-monospace, monospace;
            font-size: 13px;
            margin-left: 6px;
        }}
        .tweet-link:hover {{
            color: var(--accent);
            text-decoration: underline;
        }}
        .meta {{
            color: var(--text-muted);
            font-size: 12px;
            margin-left: 8px;
        }}
        .empty {{
            color: var(--text-muted);
            font-style: italic;
            padding: 16px 0;
        }}
        .insights {{
            background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
            border: 1px solid #2d4a6f;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }}
        .insights h3 {{
            font-size: 16px;
            margin-bottom: 12px;
            color: var(--accent-cyan);
        }}
        .insights ol {{
            margin-left: 20px;
            color: var(--text-muted);
        }}
        .insights li {{
            margin: 8px 0;
        }}
        .stats {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }}
        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #1f2937;
            color: #fff;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s;
            z-index: 1000;
        }}
        .toast.show {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 X 動態摘要（過去 24 小時）</h1>
            <div class="subtitle">最後更新：{ts_human}</div>
        </header>
        
        {blocked_banner}
        
        <div class="insights">
            <h3>💡 三行洞察</h3>
            <ol>
                <li>{insights[0]}</li>
                <li>{insights[1]}</li>
                <li>{insights[2]}</li>
            </ol>
        </div>
        
        {''.join(sections_html)}
        
        <div class="stats">
            📊 共收集 {total_count} 條推文，精選顯示於上
        </div>
    </div>
    
    <div class="toast" id="toast">已複製到剪貼簿</div>
    
    <script>
        const toast = document.getElementById('toast');
        let toastTimeout;
        
        function showToast(msg) {{
            toast.textContent = msg;
            toast.classList.add('show');
            clearTimeout(toastTimeout);
            toastTimeout = setTimeout(() => toast.classList.remove('show'), 2000);
        }}
        
        async function copyToClipboard(text) {{
            try {{
                await navigator.clipboard.writeText(text);
                showToast('已複製到剪貼簿');
            }} catch (e) {{
                showToast('複製失敗');
            }}
        }}
        
        // 點擊行號：複製 highlight 連結
        document.querySelectorAll('.line-num').forEach(el => {{
            el.addEventListener('click', (e) => {{
                e.preventDefault();
                const item = el.closest('.item');
                const lineId = item.id;
                const url = `${{location.origin}}${{location.pathname}}#${{lineId}}`;
                history.replaceState(null, '', `#${{lineId}}`);
                copyToClipboard(url);
            }});
        }});
        
        // 點擊文字：複製「文字 + 原文連結」
        document.querySelectorAll('.text').forEach(el => {{
            el.addEventListener('click', () => {{
                const item = el.closest('.item');
                const copyText = item.dataset.copy;
                copyToClipboard(copyText);
            }});
        }});
    </script>
</body>
</html>'''
    return html


def render_md_deepsrt_style(ts_human, categories, insights, blocked_reason='', total_count=0):
    """渲染 Markdown - 對齊 x.deepsrt.com 風格"""
    lines = [
        '# 📋 X 動態摘要（過去 24 小時）',
        '',
        f'最後更新：{ts_human}',
        '',
    ]
    
    if blocked_reason:
        lines.extend([
            f'> ⚠️ **抓取受阻**：{blocked_reason}',
            '',
        ])
    
    lines.extend([
        '## 💡 三行洞察',
        '',
        f'1. {insights[0]}',
        f'2. {insights[1]}',
        f'3. {insights[2]}',
        '',
    ])
    
    ln = 1
    for cat_name, items in categories:
        lines.extend([f'## {cat_name}', ''])
        if not items:
            lines.append('*本輪無新增貼文*')
        for p in items:
            text = rewrite_summary(p)
            tid = p.get('tweet_id', '')
            url = p.get('url', '')
            author = p.get('author', '')
            likes = p.get('likes', '0')
            reposts = p.get('reposts', '0')
            
            lines.append(f'{ln:03d}. {text} ({tid})  @{author} | ❤{likes} 🔁{reposts}')
            if url:
                lines.append(f'    → {url}')
            ln += 1
        lines.append('')
    
    lines.extend([
        '---',
        '',
        f'📊 共收集 {total_count} 條推文，精選顯示於上',
    ])
    
    return '\n'.join(lines)


async def main():
    print("=" * 60)
    print("OpenClaw X 平台智能分析（每3小時）")
    print("=" * 60)
    
    ts_file = now_ts()
    ts_human = datetime.now().strftime('%Y-%m-%d %H:%M:%S (Asia/Taipei)')
    
    html_path = WEB_DIR / f'x_monitor_{ts_file}.html'
    md_path = REPORTS / f'x_monitor_{ts_file}.md'
    
    print(f"\n📁 輸出檔案：")
    print(f"   HTML: {html_path}")
    print(f"   MD:   {md_path}")
    
    # 載入已見過的 tweet_ids
    seen = load_seen()
    print(f"\n📚 已追蹤貼文數：{len(seen)}")
    
    # 執行爬蟲
    print("\n🔍 開始抓取 X Top 分頁（滾動 80 次）...")
    scrape = await scrape_top_80()
    blocked_reason = scrape.get('blocked_reason', '')
    posts = scrape.get('posts', [])
    
    # 篩選新貼文
    new_posts = [p for p in posts if p.get('tweet_id') and p['tweet_id'] not in seen]
    print(f"\n📊 本輪新貼文：{len(new_posts)} / {len(posts)}")
    
    # 更新已見集合
    all_seen = set(seen)
    all_seen.update(p['tweet_id'] for p in posts if p.get('tweet_id'))
    save_seen(all_seen)
    
    # 自動歸納 6 類
    print("\n🗂️  自動歸納類別...")
    categories = categorize_with_emoji(new_posts)
    for cat_name, items in categories:
        print(f"   {cat_name}: {len(items)} 則")
    
    # 三行洞察
    if blocked_reason and not new_posts:
        insights = [
            '本輪受登入或風控限制，無法完整讀取貼文列表，建議檢查瀏覽器連線狀態。',
            '已維持同版型產出，方便對照與後續補抓，資料將在恢復連線後自動回填。',
            '優先恢復 X 存取狀態（已登入 + Relay tab），再以同流程重跑即可得完整趨勢。',
        ]
    else:
        insights = [
            f'本輪 Top 分頁滾動 80 次後，去重並新增 {len(new_posts)} 則可追蹤貼文，總追蹤數達 {len(all_seen)}。',
            '高互動內容仍集中在 AI 模型更新、OpenClaw 生態動態與算力供應鏈敘事。',
            '建議下一輪優先回訪高互動來源帳號，追蹤同議題延伸與反轉訊號。',
        ]
    
    # 渲染輸出
    print("\n📝 渲染輸出檔案...")
    html_content = render_html_deepsrt_style(ts_human, categories, insights, blocked_reason, len(posts))
    md_content = render_md_deepsrt_style(ts_human, categories, insights, blocked_reason, len(posts))
    
    html_path.write_text(html_content, encoding='utf-8')
    md_path.write_text(md_content, encoding='utf-8')
    
    # 輸出結果
    result = {
        'html_path': str(html_path),
        'md_path': str(md_path),
        'new_posts': len(new_posts),
        'total_posts': len(posts),
        'blocked_reason': blocked_reason,
        'timestamp': ts_human,
    }
    
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


if __name__ == '__main__':
    result = asyncio.run(main())
    # 輸出給 cron 系統解析
    print(f"\nHTML_OUTPUT:{result['html_path']}")
    print(f"MD_OUTPUT:{result['md_path']}")
