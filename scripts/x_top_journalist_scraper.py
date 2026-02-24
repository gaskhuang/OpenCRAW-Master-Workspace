#!/usr/bin/env python3
"""
X Top 新文記者版（滾動 80 次 / 六大類）
使用 CDP 連線到 Chrome 進行抓取
"""

import asyncio
import json
import re
import os
import sys
from datetime import datetime
from urllib.parse import urlencode
from typing import List, Dict, Any, Optional
import subprocess

# CDP endpoint
CDP_URL = "http://127.0.0.1:19222"
OUTPUT_DIR = "/Users/user/reports"
WEB_DIR = "/Users/user/reports/web"
SEEN_IDS_FILE = "/Users/user/reports/.x_top_seen_ids.json"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)


def check_cdp() -> tuple[bool, str]:
    """檢查 CDP 是否可用"""
    import urllib.request
    try:
        req = urllib.request.Request(f"{CDP_URL}/json/version", method="GET")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            if "Browser" in data:
                return True, f"CDP 就緒: {data.get('Browser', 'Unknown')}"
            return False, "CDP 回應格式異常"
    except Exception as e:
        return False, f"CDP 連線失敗: {str(e)}"


def get_websocket_url() -> Optional[str]:
    """取得 WebSocket debugger URL"""
    import urllib.request
    try:
        req = urllib.request.Request(f"{CDP_URL}/json/list", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            pages = json.loads(resp.read().decode())
            if pages:
                return pages[0].get("webSocketDebuggerUrl")
    except Exception as e:
        print(f"取得 WebSocket URL 失敗: {e}")
    return None


def create_new_tab(url: str = "about:blank") -> Optional[str]:
    """建立新分頁並返回 WebSocket URL"""
    import urllib.request
    try:
        req = urllib.request.Request(
            f"{CDP_URL}/json/new?{urlencode({'': url})[1:]}",
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("webSocketDebuggerUrl")
    except Exception as e:
        print(f"建立新分頁失敗: {e}")
    return None


async def scrape_x_top() -> Dict[str, Any]:
    """主要抓取邏輯 - 使用 Playwright CDP"""
    from playwright.async_api import async_playwright
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tweets": [],
        "blocked_reason": None
    }
    
    async with async_playwright() as p:
        try:
            # 連接到現有的 CDP
            browser = await p.chromium.connect_over_cdp(f"{CDP_URL}")
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            
            # 使用現有頁面或新建
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("🌐 正在開啟 X.com...")
            try:
                await page.goto("https://x.com", wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"⚠️ 頁面載入超時，繼續檢查...")
            await asyncio.sleep(5)
            
            current_url = page.url
            print(f"📍 當前頁面: {current_url}")
            
            # 檢查是否需要登入
            content = await page.content()
            content_lower = content.lower()
            
            # 多種登入/阻擋狀態檢查
            if 'login' in current_url.lower() or 'flow/login' in current_url.lower():
                # 嘗試 explore 頁面
                print("🔍 嘗試訪問 explore 頁面...")
                try:
                    await page.goto("https://x.com/explore", wait_until="domcontentloaded", timeout=30000)
                except:
                    pass
                await asyncio.sleep(5)
                
                content = await page.content()
                content_lower = content.lower()
                current_url = page.url
                print(f"📍 當前頁面: {current_url}")
                
                if 'login' in current_url.lower():
                    results["blocked_reason"] = "X 需要登入帳號才能查看內容"
                    await browser.close()
                    return results
            
            # 檢查是否有推文元素
            has_tweets = await page.evaluate('() => document.querySelectorAll("article[data-testid=tweet]").length > 0')
            
            # 檢查各種阻擋狀態
            if 'account is suspended' in content_lower or 'your account has been suspended' in content_lower:
                results["blocked_reason"] = "帳號已被暫停"
                await browser.close()
                return results
            
            if 'rate limit' in content_lower or 'rate_limit' in content_lower:
                results["blocked_reason"] = "已達速率限制 (Rate Limit)"
                await browser.close()
                return results
            
            # 如果沒有推文元素，表示需要登入
            if not has_tweets:
                results["blocked_reason"] = "X 需要登入帳號才能查看內容"
                await browser.close()
                return results
            
            # 嘗試尋找並點擊「為你推薦」/ "For You"
            print("🔍 尋找 For You / 為你推薦 視圖...")
            try:
                selectors = [
                    'text=For you',
                    'text=For You',
                    'text=為你推薦',
                    '[role="tab"]:has-text("For you")',
                    '[role="tab"]:has-text("For You")',
                    'a[href="/home"]',
                ]
                for sel in selectors:
                    btn = await page.query_selector(sel)
                    if btn:
                        await btn.click()
                        print(f"✅ 已點擊: {sel}")
                        await asyncio.sleep(2)
                        break
            except Exception as e:
                print(f"⚠️ 無法切換視圖: {e}")
            
            # 開始滾動抓取
            print("📜 開始滾動抓取...")
            seen_ids = set()
            tweets = []
            
            for i in range(80):
                # 滾動
                await page.mouse.wheel(0, 1200)
                await asyncio.sleep(1.0)
                
                # 提取推文資料
                new_tweets = await page.evaluate(r"""
                    () => {
                        const tweets = [];
                        const articles = document.querySelectorAll('article[data-testid="tweet"]');
                        articles.forEach(article => {
                            try {
                                // 取得 tweet ID
                                const links = article.querySelectorAll('a[href*="/status/"]');
                                let tweetId = null;
                                for (const link of links) {
                                    const href = link.getAttribute('href') || '';
                                    const match = href.match(/\/status\/(\d+)/);
                                    if (match) {
                                        tweetId = match[1];
                                        break;
                                    }
                                }
                                if (!tweetId) return;
                                
                                // 取得作者
                                let author = 'unknown';
                                const authorLinks = article.querySelectorAll('a[href^="/"]');
                                for (const link of authorLinks) {
                                    const href = link.getAttribute('href') || '';
                                    if (href.startsWith('/') && !href.includes('/status/')) {
                                        const parts = href.split('/').filter(p => p);
                                        if (parts.length > 0) {
                                            author = parts[0].split('?')[0];
                                            break;
                                        }
                                    }
                                }
                                
                                // 取得時間
                                const timeEl = article.querySelector('time');
                                const time = timeEl ? timeEl.getAttribute('datetime') : '';
                                
                                // 取得內文
                                const textEl = article.querySelector('[data-testid="tweetText"]');
                                const text = textEl ? textEl.innerText : '';
                                
                                // 取得互動數
                                const getCount = (testid) => {
                                    const el = article.querySelector(`[data-testid="${testid}"]`);
                                    if (!el) return 0;
                                    const text = el.innerText || el.textContent || '';
                                    const num = text.match(/([\d,.]+)(K|M|\u842c)?/i);
                                    if (!num) return 0;
                                    let val = parseFloat(num[1].replace(/,/g, ''));
                                    if (num[2]) {
                                        const unit = num[2].toUpperCase();
                                        if (unit === 'K') val *= 1000;
                                        if (unit === 'M') val *= 1000000;
                                        if (unit === '\u842c') val *= 10000;
                                    }
                                    return Math.floor(val);
                                };
                                
                                const likes = getCount('like');
                                const retweets = getCount('retweet');
                                const replies = getCount('reply');
                                
                                tweets.push({
                                    tweet_id: tweetId,
                                    author: '@' + author,
                                    time: time,
                                    text: text,
                                    likes: likes,
                                    retweets: retweets,
                                    replies: replies,
                                    url: `https://x.com/${author}/status/${tweetId}`
                                });
                            } catch (e) {}
                        });
                        return tweets;
                    }
                """)
                
                # 去重並加入新推文
                for tweet in new_tweets:
                    if tweet["tweet_id"] not in seen_ids:
                        seen_ids.add(tweet["tweet_id"])
                        tweets.append(tweet)
                
                if (i + 1) % 20 == 0:
                    print(f"  已滾動 {i+1}/80 次，收集 {len(tweets)} 則推文")
            
            results["tweets"] = tweets
            await browser.close()
            
        except Exception as e:
            results["blocked_reason"] = f"抓取異常: {str(e)}"
            print(f"❌ 抓取失敗: {e}")
    
    return results


def load_seen_ids() -> set:
    """載入已見過的 tweet IDs"""
    if os.path.exists(SEEN_IDS_FILE):
        try:
            with open(SEEN_IDS_FILE, 'r') as f:
                return set(json.load(f))
        except:
            pass
    return set()


def save_seen_ids(ids: set):
    """儲存已見過的 tweet IDs"""
    with open(SEEN_IDS_FILE, 'w') as f:
        json.dump(list(ids), f)


def classify_tweets(tweets: List[Dict]) -> Dict[str, List[Dict]]:
    """將推文分類為六大類"""
    categories = {
        "科技與 AI": [],
        "政治與時事": [],
        "財經與商業": [],
        "娛樂與文化": [],
        "社會與生活": [],
        "國際新聞": []
    }
    
    keywords = {
        "科技與 AI": ["ai", "artificial intelligence", "gpt", "llm", "model", "openai", "google", "anthropic", "tech", "software", "app", "startup", "coding", "programming", "developer", "科技", "人工智慧", "模型", "程式", "開發", "軟體"],
        "政治與時事": ["trump", "biden", "government", "policy", "election", "vote", "president", "congress", "senate", "law", "political", "政治", "選舉", "政府", "政策", "法律", "總統"],
        "財經與商業": ["stock", "market", "crypto", "bitcoin", "ethereum", "price", "money", "invest", "fund", "vc", "startup", "business", "economy", "trade", "tariff", "財經", "股票", "市場", "投資", "加密", "比特幣", "經濟", "貿易"],
        "娛樂與文化": ["movie", "film", "music", "song", "album", "actor", "actress", "celebrity", "sports", "game", "gaming", "entertainment", "netflix", "disney", "電影", "音樂", "遊戲", "娛樂", "明星", "運動"],
        "社會與生活": ["life", "lifestyle", "health", "food", "travel", "work", "job", "family", "relationship", "mental health", "生活", "健康", "美食", "旅遊", "工作", "家庭", "心理"],
        "國際新聞": ["war", "ukraine", "russia", "china", "europe", "israel", "gaza", "middle east", "asia", "conflict", "peace", "nato", "聯合國", "烏克蘭", "俄羅斯", "中國", "歐洲", "中東", "戰爭", "和平"]
    }
    
    for tweet in tweets:
        text_lower = tweet.get("text", "").lower()
        scores = {cat: 0 for cat in categories}
        
        for cat, words in keywords.items():
            for word in words:
                if word in text_lower:
                    scores[cat] += 1
        
        # 選擇最高分類
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] == 0:
            best_cat = "社會與生活"  # 預設分類
        
        categories[best_cat].append(tweet)
    
    # 各分類內排序（愛心 + 分享 + 留言 由高到低）
    for cat in categories:
        categories[cat].sort(
            key=lambda x: x.get("likes", 0) + x.get("retweets", 0) + x.get("replies", 0),
            reverse=True
        )
    
    return categories


def generate_summary(tweets: List[Dict]) -> List[str]:
    """生成三行洞察"""
    if not tweets:
        return ["本輪未抓取到任何推文。", "", ""]
    
    total = len(tweets)
    total_engagement = sum(t.get("likes", 0) + t.get("retweets", 0) + t.get("replies", 0) for t in tweets)
    avg_engagement = total_engagement // total if total > 0 else 0
    
    # 找出最高互動推文
    top_tweet = max(tweets, key=lambda x: x.get("likes", 0) + x.get("retweets", 0) + x.get("replies", 0))
    top_summary = top_tweet.get("text", "")[:50] + "..." if len(top_tweet.get("text", "")) > 50 else top_tweet.get("text", "")
    
    return [
        f"本輪 Top 分頁滾動 80 次後，共新增 {total} 則可追蹤貼文（去重後）。",
        f"總互動數 {total_engagement:,}，平均互動 {avg_engagement:,}。",
        f"熱門話題：{top_summary}"
    ]


def generate_html(categories: Dict[str, List[Dict]], insights: List[str], timestamp: str, blocked_reason: Optional[str] = None) -> str:
    """生成 HTML 報告"""
    
    lines_html = []
    line_num = 0
    
    for cat_name, tweets in categories.items():
        if not tweets and not blocked_reason:
            continue
        
        cat_lines = []
        for tweet in tweets:
            line_num += 1
            text = tweet.get("text", "").replace("'", "&#39;").replace('"', "&quot;")
            summary = text[:80] + "..." if len(text) > 80 else text
            author = tweet.get("author", "@unknown")
            time = tweet.get("time", "")[:10] if tweet.get("time") else ""
            likes = tweet.get("likes", 0)
            retweets = tweet.get("retweets", 0)
            replies = tweet.get("replies", 0)
            tweet_id = tweet.get("tweet_id", "")
            url = tweet.get("url", f"https://x.com/i/web/status/{tweet_id}")
            
            copy_text = f"{summary} | 原文：{url}"
            
            cat_lines.append(
                f"<div class='line' id='L{line_num}' data-line='{line_num}' data-copy='{copy_text}'>"
                f"<a class='ln' href='#L{line_num}' title='複製此行 highlight link'>{line_num:03d}</a> "
                f"<span class='txt' title='點文字複製：該行文字+原文連結'>{summary}</span> "
                f"<a class='tid' href='{url}' target='_blank' rel='noopener' title='開啟原貼文'>{tweet_id}</a> "
                f"<span class='meta'>{author} · {time} · ❤{likes:,} 🔁{retweets:,} 💬{replies:,}</span>"
                f"</div>"
            )
        
        if cat_lines or blocked_reason:
            lines_html.append(f"<section class='cat'><h2>{cat_name}</h2>{''.join(cat_lines) if cat_lines else '<div class="empty">本類別無新推文</div>'}</section>")
    
    if blocked_reason:
        lines_html.append(f"<section class='blocked'><strong>⚠️ 抓取受阻：</strong>{blocked_reason}</section>")
    
    insights_html = "<ol>" + "".join(f"<li>{i}</li>" for i in insights) + "</ol>"
    
    html = f"""<!doctype html>
<html lang='zh-Hant'>
<head>
<meta charset='utf-8' />
<meta name='viewport' content='width=device-width, initial-scale=1' />
<title>X Top 新文記者版</title>
<style>
:root{{--bg:#0b1020;--panel:#121a2b;--text:#e5e7eb;--muted:#94a3b8;--acc:#60a5fa;--acc2:#22d3ee;--line:#1f2937}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',sans-serif}}
.wrap{{max-width:1100px;margin:0 auto;padding:28px 20px 70px}}
h1{{font-size:28px;margin:0 0 6px}} .sub{{color:var(--muted)}}
.cat{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:16px 0}}
.cat h2{{margin:0 0 10px;color:#bfdbfe;font-size:18px}}
.line{{padding:6px 0;border-top:1px dashed #22304a}} .line:first-of-type{{border-top:none}}
.ln{{display:inline-block;width:42px;color:#7dd3fc;text-decoration:none}} .ln:hover{{text-decoration:underline}}
.txt{{cursor:pointer}} .tid{{color:var(--acc2);text-decoration:none;margin-left:6px}} .tid:hover{{text-decoration:underline}}
.meta{{color:var(--muted);font-size:12px;margin-left:8px}}
.insight{{background:#0f172a;border:1px solid #1e293b;padding:12px 14px;border-radius:12px}}
.blocked{{background:#3f1d1d;border:1px solid #7f1d1d;padding:10px 12px;border-radius:10px;margin:12px 0;color:#fecaca}}
.empty{{color:var(--muted)}}
.toast{{position:fixed;right:16px;bottom:16px;background:#111827;color:#e5e7eb;padding:8px 10px;border-radius:10px;font-size:13px;opacity:0;transition:.2s}}
.toast.show{{opacity:1}}
</style>
</head>
<body><div class='wrap'>
<h1>X Top 新文記者版（滾動 80 次 / 六大類）</h1>
<div class='sub'>最後更新：{timestamp} (Asia/Taipei)</div>

{''.join(lines_html)}

<section class='insight'><h2>三行洞察</h2>{insights_html}</section>
</div><div class='toast' id='toast'>已複製</div>
<script>
const toast = document.getElementById('toast');
function showToast(msg){{toast.textContent=msg;toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1200);}}
async function copyText(t){{try{{await navigator.clipboard.writeText(t);showToast('已複製');}}catch(e){{showToast('複製失敗');}}}}
for (const line of document.querySelectorAll('.line')) {{
  const ln = line.querySelector('.ln');
  const txt = line.querySelector('.txt');
  ln.addEventListener('click', async (e) => {{
    e.preventDefault();
    const id = line.id;
    history.replaceState(null,'','#'+id);
    await copyText(location.origin + location.pathname + '#'+id);
  }});
  txt.addEventListener('click', async () => {{
    await copyText(line.dataset.copy);
  }});
}}
</script></body></html>"""
    
    return html


def generate_md(categories: Dict[str, List[Dict]], insights: List[str], timestamp: str, blocked_reason: Optional[str] = None) -> str:
    """生成 Markdown 報告"""
    lines = [
        "# X Top 新文記者版（滾動 80 次 / 六大類）",
        f"",
        f"**最後更新：**{timestamp} (Asia/Taipei)",
        f"",
        "---",
        f""
    ]
    
    for cat_name, tweets in categories.items():
        if not tweets and not blocked_reason:
            continue
        
        lines.append(f"## {cat_name}")
        lines.append("")
        
        if tweets:
            for i, tweet in enumerate(tweets, 1):
                text = tweet.get("text", "")
                summary = text[:100] + "..." if len(text) > 100 else text
                author = tweet.get("author", "@unknown")
                time = tweet.get("time", "")[:10] if tweet.get("time") else ""
                likes = tweet.get("likes", 0)
                retweets = tweet.get("retweets", 0)
                replies = tweet.get("replies", 0)
                tweet_id = tweet.get("tweet_id", "")
                url = tweet.get("url", f"https://x.com/i/web/status/{tweet_id}")
                total = likes + retweets + replies
                
                lines.append(f"{i}. **{summary}**")
                lines.append(f"   - 作者：{author} | 時間：{time}")
                lines.append(f"   - ❤{likes:,} 🔁{retweets:,} 💬{replies:,} (總計：{total:,})")
                lines.append(f"   - [原文連結]({url})")
                lines.append("")
        else:
            lines.append("*本類別無新推文*")
            lines.append("")
    
    if blocked_reason:
        lines.append(f"## ⚠️ 抓取受阻")
        lines.append("")
        lines.append(f"**原因：**{blocked_reason}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## 三行洞察")
    lines.append("")
    for i, insight in enumerate(insights, 1):
        lines.append(f"{i}. {insight}")
    
    return "\n".join(lines)


def git_push_files(files: List[str], timestamp: str) -> str:
    """推送檔案到 GitHub"""
    try:
        # 切換到 git 目錄
        git_dir = "/Users/user"
        
        # 添加檔案
        for f in files:
            subprocess.run(["git", "-C", git_dir, "add", f], capture_output=True)
        
        # 提交
        commit_msg = f"X Top 新文記者版更新 - {timestamp}"
        result = subprocess.run(
            ["git", "-C", git_dir, "commit", "-m", commit_msg],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and "nothing to commit" not in result.stderr.lower():
            return f"Git commit 失敗: {result.stderr}"
        
        # 推送
        result = subprocess.run(
            ["git", "-C", git_dir, "push"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return f"Git push 失敗: {result.stderr}"
        
        # 取得 commit hash
        result = subprocess.run(
            ["git", "-C", git_dir, "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True
        )
        commit_hash = result.stdout.strip() if result.returncode == 0 else "unknown"
        
        return commit_hash
        
    except Exception as e:
        return f"Git 操作失敗: {str(e)}"


async def main():
    """主程式"""
    print("=" * 60)
    print("X Top 新文記者版（滾動 80 次 / 六大類）")
    print("=" * 60)
    
    # 檢查 CDP
    print("\n1️⃣ 檢查 CDP 連線...")
    ok, msg = check_cdp()
    print(f"   {msg}")
    
    if not ok:
        # 產生受阻報告
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename_ts = datetime.now().strftime("%Y%m%d_%H%M")
        blocked_reason = msg
        
        categories = {cat: [] for cat in ["科技與 AI", "政治與時事", "財經與商業", "娛樂與文化", "社會與生活", "國際新聞"]}
        insights = ["CDP 連線失敗，無法進行抓取。", "請檢查 Chrome 是否已啟動並啟用遠端偵錯。", ""]
        
        html = generate_html(categories, insights, timestamp, blocked_reason)
        md = generate_md(categories, insights, timestamp, blocked_reason)
        
        html_path = f"{WEB_DIR}/x_top_news_{filename_ts}.html"
        md_path = f"{OUTPUT_DIR}/x_top_news_{filename_ts}.md"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"\n✅ 受阻報告已產生：")
        print(f"   HTML: {html_path}")
        print(f"   MD: {md_path}")
        return
    
    # 載入已見過的 IDs
    seen_ids = load_seen_ids()
    print(f"   已載入 {len(seen_ids)} 筆歷史記錄")
    
    # 執行抓取
    print("\n2️⃣ 開始抓取 X Top...")
    results = await scrape_x_top()
    
    blocked_reason = results.get("blocked_reason")
    all_tweets = results.get("tweets", [])
    
    # 去重（本輪新增）
    new_tweets = [t for t in all_tweets if t["tweet_id"] not in seen_ids]
    print(f"   總計抓取 {len(all_tweets)} 則，本輪新增 {len(new_tweets)} 則")
    
    # 更新已見過的 IDs
    for t in all_tweets:
        seen_ids.add(t["tweet_id"])
    save_seen_ids(seen_ids)
    
    # 分類
    print("\n3️⃣ 分類推文...")
    categories = classify_tweets(new_tweets)
    for cat, tweets in categories.items():
        if tweets:
            print(f"   {cat}: {len(tweets)} 則")
    
    # 生成洞察
    insights = generate_summary(new_tweets)
    
    # 生成報告
    print("\n4️⃣ 產生報告...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename_ts = datetime.now().strftime("%Y%m%d_%H%M")
    
    html = generate_html(categories, insights, timestamp, blocked_reason)
    md = generate_md(categories, insights, timestamp, blocked_reason)
    
    html_path = f"{WEB_DIR}/x_top_news_{filename_ts}.html"
    md_path = f"{OUTPUT_DIR}/x_top_news_{filename_ts}.md"
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"   HTML: {html_path}")
    print(f"   MD: {md_path}")
    
    # Git 推送
    print("\n5️⃣ GitHub 推送...")
    commit_hash = git_push_files([html_path, md_path], timestamp)
    print(f"   Commit: {commit_hash}")
    
    # 輸出摘要
    print("\n" + "=" * 60)
    print("✅ 任務完成")
    print("=" * 60)
    print(f"\n📊 統計：")
    print(f"   - 新增推文：{len(new_tweets)} 則")
    print(f"   - 累積記錄：{len(seen_ids)} 則")
    if blocked_reason:
        print(f"   - 狀態：⚠️ {blocked_reason}")
    print(f"\n📁 檔案：")
    print(f"   - HTML: reports/web/x_top_news_{filename_ts}.html")
    print(f"   - MD: reports/x_top_news_{filename_ts}.md")
    print(f"\n🔗 Commit: {commit_hash}")


if __name__ == "__main__":
    asyncio.run(main())
