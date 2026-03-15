---
name: X Twitter 自動化 (X Twitter Automation)/python
description: "Use Case #121 Python 方案: X Twitter 自動化。使用 Python 實作 X Twitter Automation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #121: X Twitter 自動化 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 社群媒體自動化

---

## 原始需求 (來自 Source Repos)

# X/Twitter Automation from Chat

Full X/Twitter automation through natural language — post tweets, reply, like, retweet, follow, DM, search, extract data, run giveaways, and monitor accounts, all from your OpenClaw chat.

## Pain Point

Managing an X/Twitter presence requires jumping between the app, third-party dashboards, and analytics tools. Running giveaways means manual winner picking. Extracting followers, likers, or retweeters requires scraping scripts. There is no single interface that lets you do all of this conversationally.

## What It Does

TweetClaw is an OpenClaw plugin that connects your agent to the X/Twitter API. You interact entirely through chat:

- **Post & engage** — Compose tweets, reply to threads, like, retweet, follow/unfollow, send DMs
- **Search & extract** — Search tweets and users, extract followers, likers, retweeters, quote tweeters, list members
- **Giveaways** — Pick random winners from tweet engagements with configurable filters (minimum followers, account age, keyword requirements)
- **Monitors** — Watch accounts for new tweets or follower changes and get notified

All actions go through a managed API — no browser cookies, no scraping, no credential exposure.

## Prompts

**Install the plugin:**
```text
openclaw plugins install @xquik/tweetclaw
```

**Post a tweet:**
```text
Post a tweet: "Just shipped a new feature — try it out!"
```

**Run a giveaway:**
```text
Pick 3 random winners from the retweeters of this tweet: https://x.com/username/status/123456789. Exclude accounts with fewer than 50 followers.
```

**Extract data:**
```text
Extract all users who liked this tweet and export as CSV: https://x.com/username/status/123456789
```

**Monitor an account:**
```text
Monitor @elonmusk and notify me whenever he posts a new tweet.
```

## Skills Needed

- [@xquik/tweetclaw](https://www.npmjs.com/package/@xquik/tweetclaw) — Install via `openclaw plugins install @xquik/tweetclaw`

## Related Links

- [GitHub Repository](https://github.com/Xquik-dev/tweetclaw)
- [npm Package](https://www.npmjs.com/package/@xquik/tweetclaw)


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/x-twitter-automation
cd ~/x-twitter-automation
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `main.py`，實作 X Twitter 自動化 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_x_twitter_automation():
    """執行 X Twitter 自動化 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 X Twitter 自動化 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_x_twitter_automation()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/x-twitter-automation && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
