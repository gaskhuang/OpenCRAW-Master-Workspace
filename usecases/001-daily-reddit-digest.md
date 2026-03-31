# Use Case #001: 每日 Reddit 摘要 (Daily Reddit Digest)

> **分類**: 社群媒體
> **難度**: 初中級
> **預估時間**: 30-45 分鐘
> **Use Case 編號**: 001 / 118

---

## 一句話描述

根據個人偏好，自動整理並摘要喜愛的 subreddit 內容，每日產出精選報告推送到 Telegram。

---

## 功能需求

1. **設定階段**: 設定感興趣的 subreddit 與關鍵字偏好
2. **排程配置**: 配置每日排程（cron）
3. **抓取處理**: 自動抓取、過濾並摘要 Reddit 內容
4. **推送通知**: 透過 Telegram 推送每日摘要報告

---

## 兩方案比較

本 Use Case 由兩位 AI Agent 分別獨立設計，以下為比較：

| 比較項目 | 方案 A: Python + PRAW | 方案 B: Node.js + .json API |
|---------|----------------------|---------------------------|
| **語言** | Python 3.9+ | Node.js 18+ |
| **Reddit 存取** | PRAW (官方 API Wrapper) | 公開 .json 端點 (免註冊) |
| **AI 引擎** | Anthropic Claude SDK | Anthropic Claude SDK |
| **推送方式** | Telegram Bot HTTP API | node-telegram-bot-api |
| **排程** | 系統 cron | node-cron + pm2 |
| **需要 Reddit 帳號** | 是 (OAuth client_id/secret) | 否 (免註冊) |
| **Rate Limit** | 60-100 req/min (認證後) | ~10 req/min (無認證) |
| **程式碼行數** | ~714 行 (5 模組) | ~600 行 (6 模組) |
| **特色** | 穩定、官方支援、可存取更多資料 | 零門檻、新手友善、快速上手 |
| **適合對象** | 想要穩定長期運行的進階用戶 | 想要快速試用的初學者 |

### 結論

- **初學者推薦**: 方案 B (Node.js) -- 零 Reddit API 註冊，5 分鐘內可以開始
- **正式環境推薦**: 方案 A (Python) -- 更高的 Rate Limit，官方 API 更穩定

---

## 所需套件總覽

### 方案 A: Python

```
praw==7.8.1              # Reddit API 存取
anthropic==0.43.0        # Claude AI 摘要
python-telegram-bot==21.9 # Telegram 推送
python-dotenv==1.0.1     # 環境變數管理
pytz==2024.2             # 時區處理
requests==2.32.3         # HTTP 請求
```

### 方案 B: Node.js

```json
{
  "@anthropic-ai/sdk": "^0.39.0",
  "node-telegram-bot-api": "^0.66.0",
  "node-cron": "^3.0.3",
  "dotenv": "^16.4.7",
  "winston": "^3.17.0"
}
```

---

## 前置準備 Checklist

- [ ] Claude API Key (從 [console.anthropic.com](https://console.anthropic.com) 取得)
- [ ] Telegram Bot Token (透過 @BotFather 建立)
- [ ] Telegram Chat ID (傳訊息給 bot 後從 API 取得)
- [ ] (僅方案 A) Reddit API client_id + client_secret

---

## 實作流程 (Step by Step)

### Step 1: 環境準備

**方案 A (Python):**
```bash
mkdir daily-reddit-digest && cd daily-reddit-digest
python3 -m venv venv
source venv/bin/activate
pip install praw anthropic python-telegram-bot python-dotenv pytz requests
```

**方案 B (Node.js):**
```bash
mkdir daily-reddit-digest && cd daily-reddit-digest
npm init -y
npm install @anthropic-ai/sdk node-telegram-bot-api node-cron dotenv winston
```

### Step 2: 設定環境變數

建立 `.env` 檔案：

```bash
# === Claude API ===
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# === Telegram ===
TELEGRAM_BOT_TOKEN=7123456789:AAH1Bcd2EfGhIjKlMnOpQrStUvWxYz
TELEGRAM_CHAT_ID=123456789

# === Reddit (方案 A 才需要) ===
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret

# === 自訂設定 ===
SUBREDDITS=programming,ClaudeAI,MachineLearning,LocalLLaMA
POSTS_PER_SUBREDDIT=10
```

### Step 3: 建立 Reddit 資料抓取模組

**核心邏輯**: 從指定 subreddit 抓取今日熱門貼文

**方案 A (PRAW):**
```python
import praw
from dataclasses import dataclass

@dataclass
class RedditPost:
    title: str
    url: str
    score: int
    num_comments: int
    subreddit: str
    selftext: str
    permalink: str

def fetch_posts(reddit, subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.top(time_filter="day", limit=limit):
        posts.append(RedditPost(
            title=post.title,
            url=post.url,
            score=post.score,
            num_comments=post.num_comments,
            subreddit=subreddit_name,
            selftext=post.selftext[:2000],
            permalink=f"https://reddit.com{post.permalink}"
        ))
    return posts
```

**方案 B (.json API):**
```javascript
async function fetchPosts(subreddit, limit = 10) {
  const url = `https://www.reddit.com/r/${subreddit}/top.json?t=day&limit=${limit}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'daily-reddit-digest/1.0' }
  });
  const data = await res.json();
  return data.data.children.map(({ data: post }) => ({
    title: post.title,
    url: post.url,
    score: post.score,
    numComments: post.num_comments,
    subreddit,
    selftext: (post.selftext || '').slice(0, 2000),
    permalink: `https://reddit.com${post.permalink}`
  }));
}
```

### Step 4: 建立 AI 摘要模組

**核心邏輯**: 將抓取的貼文送給 Claude 產生繁中摘要

**方案 A (Python):**
```python
import anthropic

def summarize(posts):
    client = anthropic.Anthropic()
    posts_text = "\n\n".join([
        f"### [{p.subreddit}] {p.title}\n"
        f"Score: {p.score} | Comments: {p.num_comments}\n"
        f"URL: {p.permalink}\n"
        f"Content: {p.selftext[:500]}"
        for p in posts
    ])

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="你是 Reddit 每日摘要助手。請用繁體中文產生結構化摘要。",
        messages=[{
            "role": "user",
            "content": f"請摘要以下 Reddit 貼文：\n\n{posts_text}"
        }]
    )
    return response.content[0].text
```

**方案 B (Node.js):**
```javascript
import Anthropic from '@anthropic-ai/sdk';

async function summarize(posts) {
  const client = new Anthropic();
  const postsText = posts.map(p =>
    `### [${p.subreddit}] ${p.title}\n` +
    `Score: ${p.score} | Comments: ${p.numComments}\n` +
    `URL: ${p.permalink}\n` +
    `Content: ${p.selftext.slice(0, 500)}`
  ).join('\n\n');

  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4096,
    system: '你是 Reddit 每日摘要助手。請用繁體中文產生結構化摘要。',
    messages: [{
      role: 'user',
      content: `請摘要以下 Reddit 貼文：\n\n${postsText}`
    }]
  });
  return response.content[0].text;
}
```

### Step 5: 建立 Telegram 推送模組

**核心邏輯**: 將摘要傳送到 Telegram（注意 4096 字元上限）

**方案 A (Python):**
```python
import requests

def send_telegram(bot_token, chat_id, text):
    # Telegram 有 4096 字元限制，需要分段傳送
    max_len = 4096
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown"
        })
```

**方案 B (Node.js):**
```javascript
import TelegramBot from 'node-telegram-bot-api';

async function sendDigest(botToken, chatId, text) {
  const bot = new TelegramBot(botToken);
  const maxLen = 4096;
  for (let i = 0; i < text.length; i += maxLen) {
    const chunk = text.slice(i, i + maxLen);
    await bot.sendMessage(chatId, chunk, { parse_mode: 'Markdown' })
      .catch(() => bot.sendMessage(chatId, chunk)); // Markdown 失敗改純文字
  }
}
```

### Step 6: 主程式 -- 串接所有模組

**方案 A (Python):**
```python
# run_digest.py
from daily_reddit_digest.main import run
run()
```

**方案 B (Node.js):**
```bash
node src/index.js --run-once
```

### Step 7: 設定排程

**系統 cron (兩方案通用):**
```bash
# 每天下午 5 點執行
crontab -e
0 17 * * * cd /path/to/daily-reddit-digest && /path/to/python run_digest.py >> /tmp/digest.log 2>&1
```

**Node.js 內建排程 (方案 B):**
```javascript
import cron from 'node-cron';
// 每天 17:00 執行
cron.schedule('0 17 * * *', () => { runDigest(); });
```

---

## 測試步驟

| 階段 | 測試什麼 | 指令 | 預期結果 |
|------|---------|------|---------|
| 1 | 環境變數載入 | 跑 config 測試 | 所有 key 正確載入 |
| 2 | Reddit 抓取 | 抓取 1 個 subreddit | 回傳 10 篇貼文 |
| 3 | Claude 摘要 | 用 2-3 篇測試 | 產生繁中摘要 |
| 4 | Telegram 傳送 | 傳送測試訊息 | 手機收到通知 |
| 5 | 完整流程 | 執行主程式 | 收到完整摘要報告 |

---

## 常見陷阱

| 問題 | 原因 | 解決方案 |
|------|------|---------|
| Reddit 429 Too Many Requests | 未設定 User-Agent 或超過 Rate Limit | 設定 User-Agent header；方案 A 用 PRAW 自動處理 |
| Telegram 訊息被截斷 | 超過 4096 字元限制 | 分段傳送 |
| Telegram Markdown 解析失敗 | 特殊字元未跳脫 | 加 fallback 改送純文字 |
| Claude API 費用過高 | 送太多內容進去 | 限制每篇 selftext 長度；用 claude-haiku 降成本 |
| Cron 沒執行 | 路徑不對或環境變數沒載入 | 用絕對路徑；在 cron 中 source .env |

---

## 成本估算

| 項目 | 費用 |
|------|------|
| Reddit API | 免費 |
| Claude API (每日一次，~5000 tokens) | ~$0.50-2.00/月 |
| Telegram Bot | 免費 |
| **總計** | **~$0.50-2.00/月** |

---

## 進階擴充方向

1. **多通道推送**: 同時推送到 Slack、Discord、Email
2. **關鍵字過濾**: 依興趣自動篩選相關貼文
3. **歷史比較**: 與昨日摘要比較，標示新趨勢
4. **評論分析**: 抓取熱門評論一起摘要
5. **偏好學習**: 根據用戶回饋調整推薦
6. **多語言**: 自動翻譯非英文貼文

---

## 詳細教學文件

完整程式碼與詳細步驟說明請參考：

- **方案 A (Python)**: [`docs/usecase-tutorials/daily-reddit-digest/TUTORIAL.md`](../docs/usecase-tutorials/daily-reddit-digest/TUTORIAL.md)
- **方案 B (Node.js)**: [`docs/daily-reddit-digest-nodejs-tutorial.md`](../docs/daily-reddit-digest-nodejs-tutorial.md)

---

## 參考資源

- [PRAW 官方文件](https://praw.readthedocs.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [ni5arga/DailyDigestBot](https://github.com/ni5arga/DailyDigestBot)
- [seandearnaley/reddit-gpt-summarizer](https://github.com/seandearnaley/reddit-gpt-summarizer)
- [hesamsheikh/awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)

---

> 本教學由兩位 AI Agent 獨立設計，比較後整合為統一文件。
> 適用於 OpenClaw 118 Use Cases 課程教學系列。
