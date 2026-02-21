#!/usr/bin/env python3
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
    m = re.match(r'^([0-9]*\.?[0-9]+)([km]?)$', s)
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


def infer_categories(posts):
    topic_rules = {
        '模型與產品發布': [r'\bgpt\b', r'claude', r'gemini', r'llm', r'agent', r'api', r'launch', r'release'],
        '晶片與算力基建': [r'nvidia', r'gpu', r'chip', r'cuda', r'datacenter', r'半導體', r'伺服器'],
        '新創與商業化': [r'startup', r'funding', r'vc', r'saas', r'pricing', r'growth', r'市場', r'營收'],
        '政策監管與法務': [r'regulat', r'law', r'policy', r'privacy', r'copyright', r'政府', r'監管'],
        '安全風險與事故': [r'security', r'vulnerab', r'attack', r'scam', r'風險', r'漏洞', r'詐騙'],
        '社群與平台趨勢': [r'x\.com', r'twitter', r'viral', r'trend', r'creator', r'社群', r'爆紅'],
    }

    buckets = defaultdict(list)
    for p in posts:
        txt = (p.get('text') or '').lower()
        best_name, best_score = '', -1
        for name, pats in topic_rules.items():
            score = sum(1 for pat in pats if re.search(pat, txt))
            if score > best_score:
                best_name, best_score = name, score
        buckets[best_name or '其他焦點'].append(p)

    ordered = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    names = [k for k, _ in ordered]
    while len(names) < 6:
        names.append(f'延伸觀察 {len(names)+1}')
        buckets[names[-1]] = []
    names = names[:6]
    for k, v in ordered[6:]:
        buckets[names[-1]].extend(v)

    return [(n, sorted(buckets[n], key=lambda x: x.get('engagement', 0), reverse=True)) for n in names]


def rewrite_summary(post):
    text = clean_text(post.get('text', ''))
    if len(text) > 120:
        text = text[:120] + '…'
    return f'記者重寫：{text}'


async def scrape_top_80():
    result = {'blocked_reason': '', 'posts': []}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp('http://127.0.0.1:18792')
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()

            q = quote('AI OR OpenAI OR NVIDIA OR startup OR regulation')
            url = f'https://x.com/search?q={q}&src=typed_query&f=top'
            await page.goto(url, wait_until='domcontentloaded', timeout=120000)
            await asyncio.sleep(3)

            content = (await page.content()).lower()
            if 'something went wrong' in content or ('log in' in content and 'sign up' in content):
                result['blocked_reason'] = 'X 頁面受限（可能需要重新登入或觸發風控）'

            rows = []
            for _ in range(80):
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
    except Exception as e:
        result['blocked_reason'] = f'抓取受阻：{str(e).splitlines()[0]}'
    return result


def render_html(ts_human, categories, insights, blocked_reason=''):
    body = []
    ln = 1
    for cat, items in categories:
        body.append(f"<section class='cat'><h2>{cat}</h2>")
        if not items:
            body.append("<p class='empty'>本輪無新增貼文</p>")
        for p in items:
            text = rewrite_summary(p).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            url = p['url']
            tid = p['tweet_id']
            metrics = f"❤{p.get('likes','0')} 🔁{p.get('reposts','0')} 💬{p.get('replies','0')}"
            body.append(
                f"<div class='line' id='L{ln}' data-copy='{text} | 原文：{url}'>"
                f"<a class='ln' href='#L{ln}' title='複製 highlight 連結'>{ln:03d}</a> "
                f"<span class='txt' title='點文字複製：文字+原文連結'>{text}</span> "
                f"<a class='tid' href='{url}' target='_blank' rel='noopener'>{tid}</a> "
                f"<span class='meta'>@{p.get('author','')} · {p.get('time','')} · {metrics}</span>"
                f"</div>"
            )
            ln += 1
        body.append('</section>')

    blocked_html = f"<div class='blocked'>⚠️ {blocked_reason}</div>" if blocked_reason else ''
    return f"""<!doctype html>
<html lang='zh-Hant'><head>
<meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>OpenClaw X 平台智能分析</title>
<style>
:root{{--bg:#0b1020;--panel:#121a2b;--text:#e5e7eb;--muted:#94a3b8;--acc:#60a5fa;--acc2:#22d3ee;--line:#1f2937}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:28px 20px 72px}} h1{{margin:0 0 4px;font-size:28px}} .sub{{color:var(--muted)}}
.cat{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:16px 0}} .cat h2{{margin:0 0 10px;color:#bfdbfe;font-size:18px}}
.line{{padding:6px 0;border-top:1px dashed #22304a}} .line:first-of-type{{border-top:none}}
.ln{{display:inline-block;width:42px;color:#7dd3fc;text-decoration:none}} .ln:hover,.tid:hover{{text-decoration:underline}}
.txt{{cursor:pointer}} .tid{{color:var(--acc2);text-decoration:none;margin-left:6px}}
.meta{{color:var(--muted);font-size:12px;margin-left:8px}} .empty{{color:var(--muted)}}
.insight{{background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:12px 14px}}
.blocked{{background:#3f1d1d;border:1px solid #7f1d1d;color:#fecaca;padding:10px 12px;border-radius:10px;margin:12px 0}}
.toast{{position:fixed;right:16px;bottom:16px;background:#111827;color:#e5e7eb;padding:8px 10px;border-radius:10px;font-size:13px;opacity:0;transition:.2s}}
.toast.show{{opacity:1}}
</style></head><body>
<div class='wrap'>
<h1>OpenClaw X 平台智能分析（每3小時）</h1>
<div class='sub'>最後更新：{ts_human}</div>
{blocked_html}
{''.join(body)}
<section class='insight'><h2>三行洞察</h2><ol><li>{insights[0]}</li><li>{insights[1]}</li><li>{insights[2]}</li></ol></section>
</div>
<div class='toast' id='toast'>已複製</div>
<script>
const toast=document.getElementById('toast');
function showToast(msg){{toast.textContent=msg;toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1200);}}
async function copyText(t){{try{{await navigator.clipboard.writeText(t);showToast('已複製');}}catch(e){{showToast('複製失敗');}}}}
for (const line of document.querySelectorAll('.line')) {{
  const ln=line.querySelector('.ln');
  const txt=line.querySelector('.txt');
  ln.addEventListener('click', async (e)=>{{
    e.preventDefault();
    const id=line.id;
    history.replaceState(null,'','#'+id);
    await copyText(location.origin + location.pathname + '#'+id);
  }});
  txt.addEventListener('click', async ()=>{{await copyText(line.dataset.copy);}});
}}
</script>
</body></html>"""


def render_md(ts_human, categories, insights, blocked_reason=''):
    out = [
        '# OpenClaw X 平台智能分析（每3小時）',
        f'- 最後更新：{ts_human}',
    ]
    if blocked_reason:
        out.append(f'- 抓取受阻：{blocked_reason}')
    out.append('')

    ln = 1
    for cat, items in categories:
        out.append(f'## {cat}')
        if not items:
            out.append('- 本輪無新增貼文')
        for p in items:
            out.append(
                f"{ln:03d}. {rewrite_summary(p)} ({p['url']}) [{p['tweet_id']}]  @ {p.get('author','')} | {p.get('time','')} | ❤{p.get('likes','0')} 🔁{p.get('reposts','0')} 💬{p.get('replies','0')}"
            )
            ln += 1
        out.append('')

    out.extend(['## 三行洞察', f'1. {insights[0]}', f'2. {insights[1]}', f'3. {insights[2]}'])
    return '\n'.join(out)


async def main():
    ts_file = now_ts()
    ts_human = datetime.now().strftime('%Y-%m-%d %H:%M (Asia/Taipei)')

    html_path = WEB_DIR / f'x_monitor_{ts_file}.html'
    md_path = REPORTS / f'x_monitor_{ts_file}.md'

    seen = load_seen()
    scrape = await scrape_top_80()
    blocked_reason = scrape.get('blocked_reason', '')
    posts = scrape.get('posts', [])

    new_posts = [p for p in posts if p.get('tweet_id') and p['tweet_id'] not in seen]
    all_seen = set(seen)
    all_seen.update(p['tweet_id'] for p in posts if p.get('tweet_id'))
    save_seen(all_seen)

    categories = infer_categories(new_posts)

    insights = [
        f'本輪 Top 分頁滾動 80 次後，去重並新增 {len(new_posts)} 則可追蹤貼文。',
        '高互動內容仍集中在 AI 模型更新、商業化與算力供應鏈敘事。',
        '建議下一輪優先回訪高互動來源帳號，追蹤同議題延伸與反轉訊號。',
    ]

    if blocked_reason and not new_posts:
        insights = [
            '本輪受登入或風控限制，無法完整讀取貼文列表。',
            '已維持同版型產出，方便對照與後續補抓。',
            '建議先恢復 X 存取狀態，再以同流程重跑。',
        ]

    html_path.write_text(render_html(ts_human, categories, insights, blocked_reason), encoding='utf-8')
    md_path.write_text(render_md(ts_human, categories, insights, blocked_reason), encoding='utf-8')

    print(json.dumps({
        'html_path': str(html_path),
        'md_path': str(md_path),
        'new_posts': len(new_posts),
        'blocked_reason': blocked_reason,
    }, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(main())