---
name: 每日 Reddit 摘要 (Daily Reddit Digest)/python
description: "Use Case #001 Python 方案: 每日 Reddit 摘要。使用 Python + PRAW + Claude API + Telegram Bot 建立每日自動摘要系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *), Bash(chmod *)
---

# Use Case #001: 每日 Reddit 摘要 — Python 方案

> 技術棧: Python 3.9+ / PRAW / Anthropic SDK / Telegram Bot HTTP API
> 難度: 初中級 | 時間: 30-45 分鐘

---

## 所需套件

```txt
praw==7.8.1              # Reddit API 存取 (官方 Python wrapper)
anthropic==0.43.0        # Claude AI 摘要
python-telegram-bot==21.9 # Telegram 推送
python-dotenv==1.0.1     # 環境變數管理
pytz==2024.2             # 時區處理
requests==2.32.3         # HTTP 請求
```

安裝指令:
```bash
python3 -m venv venv
source venv/bin/activate
pip install praw==7.8.1 anthropic==0.43.0 python-telegram-bot==21.9 python-dotenv==1.0.1 pytz==2024.2 requests==2.32.3
```

---

## 前置準備 Checklist

- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather)
- [ ] Telegram Chat ID
- [ ] Reddit API client_id + client_secret (reddit.com/prefs/apps → script 類型)

### Reddit API 申請步驟

1. 登入 reddit.com → 前往 reddit.com/prefs/apps
2. 點擊「create another app...」
3. 填寫：
   - name: `daily-digest-bot`
   - 選擇 **script**
   - redirect uri: `http://localhost:8000`
4. 記下 `client_id` (在 app 名稱下方的短字串) 和 `client_secret`

### Telegram Bot 建立步驟

1. 開啟 Telegram → 搜尋 `@BotFather`
2. 發送 `/newbot` → 取名 → 設定 username (結尾需為 `bot`)
3. 記下 Bot Token
4. 傳任意訊息給你的 bot
5. 訪問 `https://api.telegram.org/bot<TOKEN>/getUpdates` → 找到 `chat.id`

---

## 專案結構

```
daily-reddit-digest/
├── .env                          # 環境變數 (勿 commit)
├── requirements.txt              # Python 依賴
├── run_digest.py                 # 執行入口
├── test_components.py            # 逐模組測試
└── daily_reddit_digest/
    ├── __init__.py
    ├── config.py                 # 設定管理
    ├── reddit_fetcher.py         # Reddit 資料抓取
    ├── ai_summarizer.py          # Claude AI 摘要
    ├── telegram_sender.py        # Telegram 推送
    └── main.py                   # 主流程串接
```

---

## 實作流程 (Step by Step)

### Step 1: 建立專案與環境

```bash
mkdir -p daily-reddit-digest/daily_reddit_digest
cd daily-reddit-digest
python3 -m venv venv && source venv/bin/activate
```

建立 `requirements.txt` 並安裝。

### Step 2: 設定環境變數

建立 `.env`:
```bash
# Reddit
REDDIT_CLIENT_ID=你的_client_id
REDDIT_CLIENT_SECRET=你的_client_secret
REDDIT_USER_AGENT=daily-digest-bot/1.0

# Claude
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Telegram
TELEGRAM_BOT_TOKEN=7123456789:AAxxxxx
TELEGRAM_CHAT_ID=123456789

# 設定
SUBREDDITS=programming,ClaudeAI,MachineLearning,LocalLLaMA
POSTS_PER_SUBREDDIT=10
```

### Step 3: config.py — 設定管理

```python
"""Configuration management - loads from .env"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Reddit
    reddit_client_id: str = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_ID", ""))
    reddit_client_secret: str = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_SECRET", ""))
    reddit_user_agent: str = field(default_factory=lambda: os.getenv("REDDIT_USER_AGENT", "daily-digest-bot/1.0"))

    # Claude
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    # Telegram
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))

    # Settings
    subreddits: list = field(default_factory=lambda: os.getenv("SUBREDDITS", "programming").split(","))
    posts_per_subreddit: int = field(default_factory=lambda: int(os.getenv("POSTS_PER_SUBREDDIT", "10")))

    def validate(self):
        missing = []
        if not self.reddit_client_id: missing.append("REDDIT_CLIENT_ID")
        if not self.reddit_client_secret: missing.append("REDDIT_CLIENT_SECRET")
        if not self.anthropic_api_key: missing.append("ANTHROPIC_API_KEY")
        if not self.telegram_bot_token: missing.append("TELEGRAM_BOT_TOKEN")
        if not self.telegram_chat_id: missing.append("TELEGRAM_CHAT_ID")
        if missing:
            raise ValueError(f"Missing env vars: {', '.join(missing)}")
        return True
```

### Step 4: reddit_fetcher.py — Reddit 抓取

```python
"""Fetch top posts from Reddit using PRAW"""
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
    author: str

    def to_summary_text(self) -> str:
        body = self.selftext[:500] if self.selftext else "(no body)"
        return (
            f"### [{self.subreddit}] {self.title}\n"
            f"Score: {self.score} | Comments: {self.num_comments} | Author: u/{self.author}\n"
            f"URL: {self.permalink}\n"
            f"Content: {body}\n"
        )

def create_reddit_client(client_id, client_secret, user_agent):
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

def fetch_subreddit_posts(reddit, subreddit_name, limit=10):
    """Fetch top daily posts from a subreddit"""
    posts = []
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top(time_filter="day", limit=limit):
        posts.append(RedditPost(
            title=submission.title,
            url=submission.url,
            score=submission.score,
            num_comments=submission.num_comments,
            subreddit=subreddit_name,
            selftext=submission.selftext[:2000] if submission.selftext else "",
            permalink=f"https://reddit.com{submission.permalink}",
            author=str(submission.author) if submission.author else "[deleted]",
        ))
    return posts

def fetch_all_posts(reddit, subreddits, limit=10):
    """Fetch posts from all configured subreddits"""
    all_posts = []
    for sub in subreddits:
        sub = sub.strip()
        try:
            posts = fetch_subreddit_posts(reddit, sub, limit)
            all_posts.extend(posts)
            print(f"  ✓ r/{sub}: {len(posts)} posts")
        except Exception as e:
            print(f"  ✗ r/{sub}: {e}")
    return all_posts
```

### Step 5: ai_summarizer.py — Claude AI 摘要

```python
"""Generate digest summary using Claude API"""
import anthropic

SYSTEM_PROMPT = """你是 Reddit 每日摘要助手。請用繁體中文產生結構化的每日摘要報告。

格式要求：
1. 開頭用一句話總結今日重點趨勢
2. 依 subreddit 分類列出重點貼文
3. 每篇貼文用 2-3 句話摘要重點
4. 附上原文連結
5. 結尾列出今日關鍵字標籤"""

def summarize_posts(api_key, posts):
    """Send posts to Claude and get a structured summary"""
    client = anthropic.Anthropic(api_key=api_key)

    posts_text = "\n\n---\n\n".join([p.to_summary_text() for p in posts])

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"以下是今日 Reddit 熱門貼文，請產生每日摘要報告：\n\n{posts_text}"
        }]
    )

    summary = response.content[0].text
    tokens_used = response.usage.input_tokens + response.usage.output_tokens
    print(f"  ✓ Claude summary generated ({tokens_used} tokens used)")
    return summary
```

### Step 6: telegram_sender.py — Telegram 推送

```python
"""Send digest via Telegram Bot API"""
import requests

def send_message(bot_token, chat_id, text, parse_mode="Markdown"):
    """Send a message via Telegram Bot API, auto-split if too long"""
    max_len = 4096
    chunks = []

    # Split by paragraphs first, then by character limit
    if len(text) <= max_len:
        chunks = [text]
    else:
        current = ""
        for line in text.split("\n"):
            if len(current) + len(line) + 1 > max_len:
                if current:
                    chunks.append(current)
                current = line
            else:
                current = current + "\n" + line if current else line
        if current:
            chunks.append(current)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for i, chunk in enumerate(chunks):
        payload = {"chat_id": chat_id, "text": chunk, "parse_mode": parse_mode}
        resp = requests.post(url, json=payload, timeout=30)

        # Fallback: if Markdown parsing fails, send as plain text
        if not resp.ok and parse_mode == "Markdown":
            payload["parse_mode"] = ""
            resp = requests.post(url, json=payload, timeout=30)

        if resp.ok:
            print(f"  ✓ Telegram chunk {i+1}/{len(chunks)} sent")
        else:
            print(f"  ✗ Telegram error: {resp.text}")

def test_connection(bot_token, chat_id):
    """Send a test message to verify bot is working"""
    send_message(bot_token, chat_id, "✅ Reddit Digest Bot 連線測試成功！", parse_mode="")
```

### Step 7: main.py — 主程式串接

```python
"""Main orchestrator: fetch -> summarize -> save -> send"""
import os
from datetime import datetime
from .config import Config
from .reddit_fetcher import create_reddit_client, fetch_all_posts
from .ai_summarizer import summarize_posts
from .telegram_sender import send_message

def run():
    print("=" * 50)
    print(f"Reddit Daily Digest - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # 1. Load config
    print("\n[1/4] Loading config...")
    config = Config()
    config.validate()
    print(f"  ✓ Tracking {len(config.subreddits)} subreddits")

    # 2. Fetch Reddit posts
    print("\n[2/4] Fetching Reddit posts...")
    reddit = create_reddit_client(
        config.reddit_client_id,
        config.reddit_client_secret,
        config.reddit_user_agent,
    )
    posts = fetch_all_posts(reddit, config.subreddits, config.posts_per_subreddit)
    print(f"  Total: {len(posts)} posts fetched")

    if not posts:
        print("  ⚠ No posts found, skipping.")
        return

    # 3. Generate AI summary
    print("\n[3/4] Generating AI summary...")
    summary = summarize_posts(config.anthropic_api_key, posts)

    # Save to local file
    os.makedirs("output", exist_ok=True)
    filename = f"output/{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"  ✓ Saved to {filename}")

    # 4. Send via Telegram
    print("\n[4/4] Sending to Telegram...")
    header = f"📰 *Reddit 每日摘要* - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    send_message(config.telegram_bot_token, config.telegram_chat_id, header + summary)

    print("\n✅ Done!")
```

### Step 8: run_digest.py — 執行入口

```python
#!/usr/bin/env python3
"""Entry point for cron execution"""
from daily_reddit_digest.main import run

if __name__ == "__main__":
    run()
```

### Step 9: 設定 Cron 排程

```bash
# 編輯 crontab
crontab -e

# 每天下午 5 點執行
0 17 * * * cd /path/to/daily-reddit-digest && /path/to/venv/bin/python run_digest.py >> /tmp/reddit-digest.log 2>&1
```

---

## 測試步驟

| 階段 | 測試什麼 | 指令 | 預期結果 |
|------|---------|------|---------|
| 1 | 環境變數 | `python -c "from daily_reddit_digest.config import Config; Config().validate()"` | 無錯誤 |
| 2 | Reddit 抓取 | `python -c "..."` (見下方) | 回傳 10 篇貼文 |
| 3 | Claude 摘要 | 用 2-3 篇測試 | 產生繁中摘要 |
| 4 | Telegram | 傳送測試訊息 | 手機收到通知 |
| 5 | 完整流程 | `python run_digest.py` | 收到完整報告 |

---

## 常見陷阱

| 問題 | 原因 | 解法 |
|------|------|------|
| `prawcore.exceptions.ResponseException: 401` | client_id 或 secret 錯誤 | 重新確認 reddit.com/prefs/apps 的值 |
| `prawcore.exceptions.OAuthException` | user_agent 格式不對 | 用 `botname/1.0` 格式 |
| Telegram 訊息被截斷 | 超過 4096 字元 | 已內建分段傳送 |
| Telegram `parse_mode` 錯誤 | Markdown 特殊字元 | 已內建 fallback 純文字 |
| Claude `rate_limit_error` | 超過 API 限額 | 加 retry 或降低頻率 |
| Cron 沒觸發 | 路徑或環境變數問題 | 用絕對路徑，在 cron 中 source .env |

---

## 完整參考

詳細程式碼 (含錯誤處理、logging、進階擴充): `docs/usecase-tutorials/daily-reddit-digest/TUTORIAL.md`
