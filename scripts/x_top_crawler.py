#!/usr/bin/env python3
import asyncio
import json
import re
import os
import sys
from datetime import datetime, timezone, timedelta
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:19222"
TARGET_URL = "https://x.com/explore/tabs/top"

TAIPEI_TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TAIPEI_TZ)
TIMESTAMP = NOW.strftime("%Y%m%d_%H%M")
DATE_STR = NOW.strftime("%Y-%m-%d")

HTML_PATH = f"reports/web/x_top_news_{TIMESTAMP}.html"
MD_PATH = f"reports/x_top_news_{TIMESTAMP}.md"
DEDUP_FILE = "reports/x_top_crawled_ids.json"

CATEGORY_KEYWORDS = {
    "政治與國際": ["政治", "總統", "選舉", "政府", "國會", "外交", "國際", "戰爭", "衝突", "談判", "制裁", "大選", "政黨", "總理", "首相", "領導人", "biden", "trump", "putin", "zelensky", "烏克蘭", "俄羅斯", "中國", "美國", "台灣", "日本", "韓國", "北韓", "以色列", "巴勒斯坦", "中東", "歐盟", "北約", "聯合國"],
    "科技與AI": ["科技", "AI", "人工智慧", "機器學習", "deepseek", "openai", "chatgpt", "nvidia", "apple", "google", "microsoft", "meta", "tesla", "spacex", "半導體", "晶片", "輝達", "台積電", "intel", "amd", "雲端", "區塊鏈", "crypto", "比特幣", "ethereum", "程式", "軟體", "硬體", "iphone", "android", "5g", "6g", "電動車", "自駕車", "機器人", "quantum", "量子"],
    "財經與市場": ["財經", "股市", "股票", "道瓊", "nasdaq", "s&p", "指數", "大盤", "台股", "美股", "日股", "匯率", "利率", "央行", "fed", "通膨", "cpi", "gdp", "經濟", "貿易", "關稅", "投資", "基金", "債券", "ETF", "期貨", "選擇權", "加密貨幣", "虛擬貨幣", "黃金", "石油", "能源", "銀行", "金融"],
    "社會與生活": ["社會", "生活", "健康", "醫療", "疫情", "疫苗", "教育", "學校", "大學", "就業", "工作", "勞工", "薪資", "健保", "長照", "食品安全", "交通", "地震", "颱風", "天氣", "氣候", "環保", "再生能源", "污染", "災害", "事故", "犯罪", "警方", "法院", "司法", "人權", "性平"],
    "娛樂與文化": ["娛樂", "電影", "電視", "影集", "netflix", "disney", "串流", "音樂", "演唱會", "藝人", "明星", "網紅", "kpop", "jpop", "遊戲", "電玩", "nintendo", "sony", "playstation", "xbox", "動漫", "漫畫", "小說", "書籍", "藝術", "展覽", "博物館", "時尚", "潮流", "美食", "旅遊", "運動", "奧運", "世界盃", "nba", "mlb", "體育"],
    "科學與探索": ["科學", "太空", "nasa", "spacex", "mars", "火星", "月球", "衛星", "火箭", "天文", "物理", "化學", "生物", "醫學", "研究", "發現", "考古", "恐龍", "化石", "基因", "dna", "氣候變遷", "永續", "環境", "生態", "自然", "動物", "植物", "海洋", "極地"]
}

def load_crawled_ids():
    if os.path.exists(DEDUP_FILE):
        try:
            with open(DEDUP_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_crawled_ids(ids):
    os.makedirs(os.path.dirname(DEDUP_FILE), exist_ok=True)
    with open(DEDUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(ids), f, ensure_ascii=False, indent=2)

def parse_count(text):
    if not text:
        return 0
    text = text.strip().replace(',', '').lower()
    try:
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        elif text.replace('.', '').replace('-', '').isdigit():
            return int(float(text))
    except:
        pass
    return 0

def categorize_tweet(tweet):
    text = (tweet.get('text', '') + ' ' + tweet.get('author_handle', '')).lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[category] = score
    if scores:
        return max(scores, key=scores.get)
    return "其他"

def format_time(time_str):
    return time_str.strip() if time_str else ""

def escape_js_string(s):
    if not s:
        return ""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

def generate_html(tweets_by_category, blocked_reason=None):
    total_tweets = sum(len(tweets) for tweets in tweets_by_category.values())
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X Top 新聞 - {DATE_STR}</title>
    <style>
        :root {{ --bg-primary: #0f0f0f; --bg-secondary: #16181c; --bg-card: #1e2028; --text-primary: #e7e9ea; --text-secondary: #71767b; --accent: #1d9bf0; --border: #2f3336; --love: #f91880; --retweet: #00ba7c; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", sans-serif; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        header {{ background: var(--bg-secondary); border-bottom: 1px solid var(--border); padding: 20px; margin: -20px -20px 20px -20px; position: sticky; top: 0; z-index: 100; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 8px; }}
        .meta {{ color: var(--text-secondary); font-size: 0.875rem; }}
        .blocked-banner {{ background: #ff4444; color: white; padding: 12px 20px; margin: 0 -20px 20px -20px; font-weight: bold; text-align: center; }}
        .category {{ background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 16px; overflow: hidden; }}
        .category-header {{ background: var(--bg-card); padding: 12px 16px; font-weight: bold; font-size: 1.1rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        .tweet-count {{ background: var(--accent); color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.875rem; }}
        .tweet {{ padding: 16px; border-bottom: 1px solid var(--border); transition: background 0.2s; }}
        .tweet:hover {{ background: rgba(255,255,255,0.03); }}
        .tweet:last-child {{ border-bottom: none; }}
        .tweet-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
        .author {{ font-weight: bold; color: var(--text-primary); text-decoration: none; }}
        .author:hover {{ text-decoration: underline; }}
        .time {{ color: var(--text-secondary); font-size: 0.875rem; }}
        .tweet-text {{ margin-bottom: 12px; white-space: pre-wrap; word-wrap: break-word; cursor: pointer; padding: 8px; border-radius: 8px; transition: background 0.2s; }}
        .tweet-text:hover {{ background: rgba(29, 155, 240, 0.1); }}
        .tweet-text.copied {{ background: rgba(0, 186, 124, 0.2); }}
        .tweet-actions {{ display: flex; gap: 20px; color: var(--text-secondary); font-size: 0.875rem; }}
        .action {{ display: flex; align-items: center; gap: 6px; }}
        .action.love {{ color: var(--love); }}
        .action.retweet {{ color: var(--retweet); }}
        .tweet-id {{ font-family: monospace; font-size: 0.75rem; color: var(--text-secondary); margin-top: 8px; cursor: pointer; display: inline-block; padding: 2px 6px; border-radius: 4px; transition: background 0.2s; }}
        .tweet-id:hover {{ background: rgba(29, 155, 240, 0.2); color: var(--accent); }}
        .tweet-id.copied {{ background: rgba(0, 186, 124, 0.3); color: var(--retweet); }}
        .empty {{ padding: 40px; text-align: center; color: var(--text-secondary); }}
        .toast {{ position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); background: var(--accent); color: white; padding: 12px 24px; border-radius: 24px; font-weight: bold; opacity: 0; transition: all 0.3s ease; z-index: 1000; }}
        .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐦 X Top 新聞</h1>
            <div class="meta">產生時間：{NOW.strftime("%Y-%m-%d %H:%M")} (台北時間)｜共 {total_tweets} 則新推文</div>
        </header>
        {f'<div class="blocked-banner">⚠️ 受阻原因：{blocked_reason}</div>' if blocked_reason else ''}
"""
    if blocked_reason and total_tweets == 0:
        html += '<div class="empty">因受阻無法取得新推文，請稍後再試</div>'
    
    line_num = 0
    for category in list(CATEGORY_KEYWORDS.keys()) + ["其他"]:
        tweets = tweets_by_category.get(category, [])
        if not tweets and category != "其他" and not blocked_reason:
            continue
        html += f'''
        <div class="category">
            <div class="category-header">
                <span>{category}</span>
                <span class="tweet-count">{len(tweets)}</span>
            </div>
'''
        if not tweets:
            html += '<div class="empty">本類別暫無新推文</div>'
        else:
            for tweet in tweets:
                line_num += 1
                total_engagement = tweet.get('likes', 0) + tweet.get('retweets', 0) + tweet.get('replies', 0)
                html += f'''
            <div class="tweet">
                <div class="tweet-header">
                    <a href="https://x.com/{tweet.get('author_handle', '')}" target="_blank" class="author">@{tweet.get('author_handle', 'unknown')}</a>
                    <span class="time">{format_time(tweet.get('time'))}</span>
                </div>
                <div class="tweet-text" onclick="copyText(this, '{tweet.get('url', '')}')">{tweet.get('text', '')}</div>
                <div class="tweet-actions">
                    <span class="action love">❤ {tweet.get('likes_fmt', 0)}</span>
                    <span class="action retweet">🔄 {tweet.get('retweets_fmt', 0)}</span>
                    <span class="action reply">💬 {tweet.get('replies_fmt', 0)}</span>
                    <span style="margin-left:auto;color:var(--text-secondary)">Σ {total_engagement:,}</span>
                </div>
                <span class="tweet-id" onclick="copyId(this, '{tweet.get('tweet_id', '')}')">#{tweet.get('tweet_id', '')} ・ L{line_num}</span>
            </div>
'''
        html += '</div>'
    
    html += '''
    </div>
    <div class="toast" id="toast">已複製！</div>
    <script>
        function showToast(msg) { const t = document.getElementById("toast"); t.textContent = msg; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 2000); }
        function copyText(el, url) { navigator.clipboard.writeText(el.textContent + "\\n" + url).then(() => { el.classList.add("copied"); setTimeout(() => el.classList.remove("copied"), 500); showToast("已複製推文文字+連結"); }); }
        function copyId(el, id) { navigator.clipboard.writeText("https://x.com/i/status/" + id).then(() => { el.classList.add("copied"); setTimeout(() => el.classList.remove("copied"), 500); showToast("已複製推文連結"); }); }
    </script>
</body>
</html>'''
    return html

def generate_md(tweets_by_category, blocked_reason=None):
    total_tweets = sum(len(tweets) for tweets in tweets_by_category.values())
    md = f"# X Top 新聞 - {DATE_STR}\n\n**產生時間**：{NOW.strftime("%Y-%m-%d %H:%M")} (台北時間)  \n**總推文數**：{total_tweets} 則\n\n"
    if blocked_reason:
        md += f"> ⚠️ **受阻原因**：{blocked_reason}\n\n"
    line_num = 0
    for category in list(CATEGORY_KEYWORDS.keys()) + ["其他"]:
        tweets = tweets_by_category.get(category, [])
        md += f"## {category} ({len(tweets)} 則)\n\n"
        if not tweets:
            md += "*本類別暫無新推文*\n\n"
            continue
        for tweet in tweets:
            line_num += 1
            total_engagement = tweet.get('likes', 0) + tweet.get('retweets', 0) + tweet.get('replies', 0)
            md += f"### L{line_num} @{tweet.get('author_handle', 'unknown')}\n\n"
            md += f"{tweet.get('text', '')}\n\n"
            md += f"- 時間：{format_time(tweet.get('time'))}\n"
            md += f"- 愛心：{tweet.get('likes_fmt', 0)} | 分享：{tweet.get('retweets_fmt', 0)} | 留言：{tweet.get('replies_fmt', 0)} | **總互動：{total_engagement:,}**\n"
            md += f"- 連結：{tweet.get('url', '')}\n\n---\n\n"
    return md

async def crawl_x_top():
    blocked_reason = None
    
    try:
        import urllib.request
        req = urllib.request.Request(f"{CDP_URL}/json/version", method='GET')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                blocked_reason = f"CDP 回應異常: HTTP {resp.status}"
                return generate_html({}), generate_md({}), blocked_reason
    except Exception as e:
        blocked_reason = f"CDP 連線失敗: {str(e)}"
        return generate_html({}), generate_md({}), blocked_reason
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await context.new_page()
            
            print(f"正在開啟 {TARGET_URL}...")
            # 使用 domcontentloaded 而非 networkidle
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            
            print("等待內容載入...")
            await asyncio.sleep(10)  # 給足夠時間讓 JS 載入
            
            # 檢查頁面狀態
            page_content = await page.content()
            
            if "sign in" in page_content.lower() and "password" in page_content.lower():
                blocked_reason = "X 要求登入才能查看內容"
                await browser.close()
                return generate_html({}), generate_md({}), blocked_reason
            
            if "something went wrong" in page_content.lower():
                blocked_reason = "X 頁面載入錯誤"
                await browser.close()
                return generate_html({}), generate_md({}), blocked_reason
            
            if "rate limit" in page_content.lower():
                blocked_reason = "觸發 X 速率限制"
                await browser.close()
                return generate_html({}), generate_md({}), blocked_reason
            
            # 嘗試等待文章出現
            try:
                await page.wait_for_selector('article', timeout=15000)
                print("找到文章元素")
            except:
                print("等待文章超時，繼續嘗試...")
            
            # 滾動 80 次
            print("開始滾動頁面...")
            for i in range(80):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(0.6)
                if i % 20 == 0:
                    print(f"  已滾動 {i}/80 次")
            
            print("滾動完成，解析推文...")
            await asyncio.sleep(3)
            
            # 提取推文資料
            tweet_data = await page.evaluate("""() => {
                const tweets = [];
                const articles = document.querySelectorAll('article');
                
                articles.forEach(article => {
                    try {
                        const links = article.querySelectorAll('a[href^="/"]');
                        let authorHandle = '';
                        for (const link of links) {
                            const href = link.getAttribute('href') || '';
                            const parts = href.split('/');
                            if (parts.length === 2 && parts[1] && !['i','explore','home','messages','notifications','search','settings'].includes(parts[1])) {
                                authorHandle = parts[1];
                                break;
                            }
                        }
                        
                        const timeEl = article.querySelector('time');
                        const time = timeEl ? timeEl.textContent : '';
                        
                        let textEl = article.querySelector('[data-testid="tweetText"]');
                        if (!textEl) {
                            const divs = article.querySelectorAll('div[dir="auto"]');
                            for (const div of divs) {
                                if (div.textContent.length > 10) {
                                    textEl = div;
                                    break;
                                }
                            }
                        }
                        const text = textEl ? textEl.textContent : '';
                        
                        const getCount = (testid) => {
                            const el = article.querySelector('[data-testid="' + testid + '"]');
                            if (!el) return '0';
                            const span = el.querySelector('span');
                            return span ? span.textContent : (el.textContent || '0');
                        };
                        
                        const likes = getCount('like');
                        const retweets = getCount('retweet');
                        const replies = getCount('reply');
                        
                        let url = '';
                        let tweetId = '';
                        const statusLinks = article.querySelectorAll('a[href*="/status/"]');
                        for (const link of statusLinks) {
                            const href = link.getAttribute('href') || '';
                            const match = href.match(/status\\/(\\d+)/);
                            if (match) {
                                tweetId = match[1];
                                url = 'https://x.com' + href.split('?')[0];
                                break;
                            }
                        }
                        
                        if (tweetId && text) {
                            tweets.push({
                                author_handle: authorHandle,
                                time: time,
                                text: text,
                                likes_fmt: likes,
                                retweets_fmt: retweets,
                                replies_fmt: replies,
                                url: url,
                                tweet_id: tweetId
                            });
                        }
                    } catch (e) {}
                });
                
                return tweets;
            }""")
            
            await browser.close()
            
            print(f"從頁面提取到 {len(tweet_data)} 則推文")
            
            # 處理資料
            crawled_ids = load_crawled_ids()
            new_tweets = []
            
            for t in tweet_data:
                tid = t.get('tweet_id')
                if not tid or tid in crawled_ids:
                    continue
                crawled_ids.add(tid)
                t['likes'] = parse_count(t.get('likes_fmt', '0'))
                t['retweets'] = parse_count(t.get('retweets_fmt', '0'))
                t['replies'] = parse_count(t.get('replies_fmt', '0'))
                new_tweets.append(t)
            
            save_crawled_ids(crawled_ids)
            print(f"本輪新增 {len(new_tweets)} 則推文")
            
            if len(new_tweets) == 0:
                if len(tweet_data) == 0:
                    blocked_reason = "X 頁面無法取得推文資料（未登入或頁面結構變更）"
                else:
                    blocked_reason = "無新推文（全部已抓取過）"
            
            # 分類並排序
            tweets_by_category = {cat: [] for cat in list(CATEGORY_KEYWORDS.keys()) + ["其他"]}
            for tweet in new_tweets:
                cat = categorize_tweet(tweet)
                tweets_by_category[cat].append(tweet)
            
            for cat in tweets_by_category:
                tweets_by_category[cat].sort(
                    key=lambda x: x.get('likes', 0) + x.get('retweets', 0) + x.get('replies', 0),
                    reverse=True
                )
            
            html = generate_html(tweets_by_category, blocked_reason)
            md = generate_md(tweets_by_category, blocked_reason)
            
            return html, md, blocked_reason
            
        except Exception as e:
            blocked_reason = f"抓取過程出錯: {str(e)}"
            return generate_html({}), generate_md({}), blocked_reason

async def main():
    html_content, md_content, blocked_reason = await crawl_x_top()
    
    os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"已儲存 HTML: {HTML_PATH}")
    
    with open(MD_PATH, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"已儲存 MD: {MD_PATH}")
    
    if blocked_reason:
        print(f"⚠️ {blocked_reason}")

if __name__ == "__main__":
    asyncio.run(main())
