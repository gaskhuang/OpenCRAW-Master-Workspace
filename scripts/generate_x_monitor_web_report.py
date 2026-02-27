#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
ROOT = Path("/Users/user")
MEM_DIR = ROOT / "memory"
OUT_WEB_DIR = ROOT / "reports" / "web"
OUT_MD_DIR = ROOT / "reports"


def latest_source_json() -> Path | None:
    files = sorted(MEM_DIR.glob("openclaw_x_top_*.json"))
    return files[-1] if files else None


def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def detect_categories(posts: list[dict], errors: list[dict]) -> list[str]:
    keyword_buckets = {
        "產品與發布": ["launch", "release", "model", "feature", "更新", "發布"],
        "技術與工程": ["api", "code", "agent", "sdk", "script", "debug", "工程", "技術"],
        "商業與營運": ["pricing", "revenue", "business", "market", "客戶", "變現", "營收"],
        "生態與社群": ["community", "thread", "reply", "creator", "社群", "討論"],
        "實戰案例": ["case", "deploy", "install", "實作", "案例", "導入"],
        "風險與阻礙": ["blocked", "error", "login", "anti", "限制", "阻擋", "失敗"],
    }
    scores = {k: 0 for k in keyword_buckets}
    corpus = "\n".join([clean_text((p.get("text") or "")) for p in posts]) + "\n" + "\n".join(clean_text(e.get("message", "")) for e in errors)
    lc = corpus.lower()
    for k, kws in keyword_buckets.items():
        for kw in kws:
            if kw.lower() in lc:
                scores[k] += 1
    ranked = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    chosen = [k for k, _ in ranked[:6]]
    if len(chosen) < 6:
        for k in keyword_buckets:
            if k not in chosen:
                chosen.append(k)
            if len(chosen) == 6:
                break
    return chosen


def make_insights(status: str, post_count: int, errors: list[dict], blocked_reason: str) -> list[str]:
    e = "；".join(clean_text(x.get("message", "")) for x in errors[:2]) if errors else "無"
    reason = blocked_reason or (e if e and e != "無" else "無明確阻礙")
    return [
        f"資料可用性：本輪狀態為「{status}」，可分析貼文 {post_count} 則。",
        f"阻礙焦點：{reason}。",
        "下一步：優先恢復可抓取來源（已登入 X + Relay tab），再執行 3 小時追蹤可得到完整趨勢。",
    ]


def render(data: dict, out_html: Path, out_md: Path) -> None:
    crawl = data.get("crawl", {})
    analysis = data.get("analysis", {})
    status = crawl.get("status", "unknown")
    posts = crawl.get("posts", []) or []
    errors = crawl.get("errors", []) or []
    summary = clean_text(analysis.get("summary", ""))

    blocked_reason = ""
    if errors:
        blocked_reason = "；".join(clean_text(e.get("message", "")) for e in errors[:2] if clean_text(e.get("message", "")))
    if not blocked_reason and not posts:
        blocked_reason = "找不到可用來源資料（memory/openclaw_x_top_*.json）或本輪未抓到貼文。"

    cats = detect_categories(posts, errors)
    insights = make_insights(status, len(posts), errors, blocked_reason)

    lines = []
    ln = 1

    def add_line(text: str, link: str = "", tweet_id: str = ""):
        nonlocal ln
        lines.append({"line": ln, "text": text, "link": link, "tweet_id": tweet_id})
        ln += 1

    if posts:
        for p in posts:
            txt = clean_text(p.get("text") or "")
            url = p.get("url") or ""
            tid = str(p.get("tweet_id") or "")
            if txt:
                add_line(txt, url, tid)
    else:
        for e in errors:
            msg = clean_text(e.get("message", ""))
            src = clean_text(e.get("source", ""))
            url = e.get("url", "")
            add_line(f"[{src}] {msg}", url, "")

    generated_at = datetime.now(TZ)
    gen_str = generated_at.strftime("%Y-%m-%d %H:%M")

    html_lines = []
    for item in lines:
        line = item["line"]
        text = item["text"].replace("<", "&lt;").replace(">", "&gt;")
        link = item["link"]
        tid = item["tweet_id"]
        tid_html = f"<a class='tid' href='https://x.com/i/web/status/{tid}' target='_blank' rel='noopener'>{tid}</a>" if tid else ""
        html_lines.append(
            f"<div class='line' id='L{line}'><a class='ln' href='#L{line}' data-line='{line}'>{line:02d}</a>"
            f"<span class='txt' data-text='{text}' data-link='{link}'>{text}</span> {tid_html}</div>"
        )

    blocked_html = f"<div class='card'><h2>⚠️ 資料阻擋</h2><p>{blocked_reason}</p></div>" if blocked_reason else ""

    html = f"""<!doctype html>
<html lang='zh-Hant'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <title>X Monitor Web Report</title>
  <style>
    :root {{ --bg:#0b1220; --card:#111a2f; --text:#dbe7ff; --muted:#90a4c2; --acc:#5eead4; --line:#20314f; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:Inter,'Noto Sans TC',system-ui; }}
    .wrap {{ max-width:1120px; margin:28px auto; padding:0 16px; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; margin-bottom:14px; }}
    h1,h2 {{ margin:.2rem 0 .6rem 0; }}
    .muted {{ color:var(--muted); font-size:14px; }}
    .line {{ display:grid; grid-template-columns:48px 1fr auto; gap:10px; border-bottom:1px dashed #1a2944; padding:8px 0; }}
    .ln {{ color:#7aa2ff; text-decoration:none; font-variant-numeric:tabular-nums; }}
    .txt {{ cursor:pointer; }}
    .txt:hover {{ color:var(--acc); }}
    .tid {{ color:#fca5a5; text-decoration:none; font-family:ui-monospace,monospace; }}
    .pill {{ display:inline-block; border:1px solid #31507f; border-radius:999px; padding:4px 10px; margin:4px 6px 0 0; color:#b9d0ff; font-size:13px; }}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1>OpenClaw X 平台智能分析（網站版）</h1>
      <div class='muted'>Generated: {gen_str} (Asia/Taipei) ｜ Source: {latest_source_json().name if latest_source_json() else 'N/A'}</div>
      <p>記者摘要：{summary if summary else '本輪未取得可供重寫的貼文內容。'}</p>
    </div>
    {blocked_html}
    <div class='card'><h2>六類自動歸納</h2>{''.join([f"<span class='pill'>{c}</span>" for c in cats])}</div>
    <div class='card'><h2>三行洞察</h2><ol>{''.join([f'<li>{x}</li>' for x in insights])}</ol></div>
    <div class='card'>
      <h2>明細（互動）</h2>
      <div class='muted'>點文字：複製「文字 + 原文連結」｜點行號：複製 #Lxx 連結｜點 tweet_id：開原貼文</div>
      {''.join(html_lines) if html_lines else '<div class="muted">本輪無可顯示內容。</div>'}
    </div>
  </div>
  <script>
    async function cpy(t) {{ try {{ await navigator.clipboard.writeText(t); }} catch(e){{}} }}
    document.querySelectorAll('.txt').forEach(el => el.addEventListener('click', () => {{
      const text = el.dataset.text || '';
      const link = el.dataset.link || '';
      cpy(link ? `${{text}}\n${{link}}` : text);
    }}));
    document.querySelectorAll('.ln').forEach(el => el.addEventListener('click', (ev) => {{
      ev.preventDefault();
      const line = el.dataset.line;
      const url = `${{location.origin}}${{location.pathname}}#L${{line}}`;
      history.replaceState(null, '', `#L${{line}}`);
      cpy(url);
    }}));
  </script>
</body>
</html>
"""

    md_lines = [
        "# OpenClaw X 平台智能分析（網站版）",
        "",
        f"- 生成時間：{gen_str} (Asia/Taipei)",
        f"- 資料來源：{latest_source_json().name if latest_source_json() else 'N/A'}",
        f"- 狀態：{status}",
        "",
        "## 記者摘要",
        summary if summary else "本輪未取得可供重寫的貼文內容。",
        "",
    ]

    if blocked_reason:
        md_lines.extend([
            "## ⚠️ 資料阻擋",
            f"- {blocked_reason}",
            "",
        ])

    md_lines.extend([
        "## 六類自動歸納",
        *[f"- {c}" for c in cats],
        "",
        "## 三行洞察",
        *[f"1. {insights[0]}", f"2. {insights[1]}", f"3. {insights[2]}"],
        "",
        "## 明細",
    ])
    if lines:
        for item in lines:
            tid = f" `{item['tweet_id']}`" if item["tweet_id"] else ""
            src = f" ({item['link']})" if item["link"] else ""
            md_lines.append(f"- L{item['line']:02d} {item['text']}{tid}{src}")
    else:
        md_lines.append("- 無")

    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main():
    src = latest_source_json()
    data = {}
    if src and src.exists():
        data = json.loads(src.read_text(encoding="utf-8"))
    now = datetime.now(TZ)
    stamp = now.strftime("%Y%m%d_%H%M")
    out_html = OUT_WEB_DIR / f"x_monitor_{stamp}.html"
    out_md = OUT_MD_DIR / f"x_monitor_{stamp}.md"
    render(data, out_html, out_md)
    print(out_html)
    print(out_md)


if __name__ == "__main__":
    main()
