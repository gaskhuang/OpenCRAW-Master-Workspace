---
name: Reddit 產品聲量追蹤 (Reddit Product Buzz Tracking)/python
description: "Use Case #008 Python 方案: Reddit 產品聲量追蹤。使用 Python 實作 Reddit Product Buzz Tracking 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #008: Reddit 產品聲量追蹤 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# Daily Reddit Digest
Run a daily digest everyday to give you the top performing posts from your favourite subreddits.

What to use it for:

• Browsing subreddits (hot/new/top posts)
• Searching posts by topic
• Pulling comment threads for context
• Building shortlists of posts to manually review/reply to later

> It's read-only. No posting, voting, or commenting.

## Skills you Need
[reddit-readonly](https://clawhub.ai/buksan1950/reddit-readonly) skill. It doesn't need auth. 

## How to Set it Up
After installing the skill, prompt your OpenClaw:
```text
I want you to give me the top performing posts from the following subreddits.
<paste the list here>
Create a separate memory for the reddit processes, about the type of posts I like to see and every day ask me if I liked the list you provided. Save my preference as rules in the memory to use for a better digest curation. (e.g. do not include memes.)
Every day at 5pm, run this process and give me the digest.
```

---

# 客户信号扫描器

## 简介

扫描客户行为信号，识别 upsell 机会、流失风险、满意度变化。

**为什么重要**：主动客户管理，提高留存率，发现增长机会。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `crm` | [ClawdHub](https://clawhub.com/skills/crm) | 客户数据 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 行为分析 |

---

## 使用方式

连接客户数据源，设置信号规则

---

## 来源

- 作者：OpenClaw 社区


---

# Competitor Radar 🎯

> Automated competitive intelligence that keeps you one step ahead

## The Problem

You're building a product but have no idea what competitors are doing until customers tell you they switched. Manually checking competitor websites, blogs, and social media is a time sink that falls off your radar within a week. By the time you notice a competitor launched a killer feature or slashed prices, you've already lost deals.

## The Solution

OpenClaw becomes your always-on competitive intelligence analyst. It monitors competitor websites for pricing changes, scans their blogs for product announcements, tracks their social media activity, and delivers a weekly digest with strategic recommendations. When something big happens (major price drop, new feature launch), you get an instant alert.

---

## Setup Guide

### Step 1: Create Your Competitor Config File

Create `competitors.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/competitor-radar
```

```json
// ~/openclaw/competitor-radar/competitors.json
{
  "competitors": [
    {
      "name": "Acme Corp",
      "website": "https://acme.com",
      "pricing_page": "https://acme.com/pricing",
      "blog": "https://acme.com/blog",
      "twitter": "acmecorp",
      "linkedin": "company/acme-corp"
    },
    {
      "name": "BigCo",
      "website": "https://bigco.io",
      "pricing_page": "https://bigco.io/pricing",
      "blog": "https://bigco.io/resources/blog",
      "twitter": "bigco_io"
    },
    {
      "name": "StartupX",
      "website": "https://startupx.com",
      "pricing_page": "https://startupx.com/plans",
      "changelog": "https://startupx.com/changelog"

---

## 所需套件

```txt
anthropic>=0.43.0        # Claude AI 核心
python-dotenv>=1.0.1     # 環境變數管理
requests>=2.32.3         # HTTP 請求
python-telegram-bot>=21.9 # Telegram 推送 (可選)
pytz>=2024.2             # 時區處理
schedule>=1.2.0          # 排程管理 (可選)
```

---

## 前置準備 Checklist

- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather) — 如需推送
- [ ] 相關第三方 API Key — 視 use case 需求

---

## 專案結構

```
reddit-product-buzz-tracking/
├── .env                    # 環境變數
├── requirements.txt        # Python 依賴
├── config.py              # 設定管理
├── main.py                # 主程式
├── core.py                # 核心業務邏輯
├── notifier.py            # 通知推送
└── output/                # 輸出資料夾
```

---

## 實作流程 (Step by Step)

### Step 1: 環境準備

```bash
mkdir -p reddit-product-buzz-tracking && cd reddit-product-buzz-tracking
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests python-telegram-bot pytz
```

### Step 2: 設定環境變數 (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
# 其他必要的 API keys
```

### Step 3: config.py — 設定管理

```python
"""Configuration management"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.ANTHROPIC_API_KEY: missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"Missing: {', '.join(missing)}")
```

### Step 4: core.py — 核心業務邏輯

根據 Reddit 產品聲量追蹤 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Reddit Product Buzz Tracking"""
import anthropic
from config import Config

def collect_data():
    """Collect data from relevant sources"""
    # TODO: Implement data collection
    # This depends on the specific use case
    pass

def analyze_with_ai(data):
    """Use Claude to analyze/process collected data"""
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"請分析以下資料並產生繁體中文報告：\n\n{data}"
        }]
    )
    return response.content[0].text
```

### Step 5: notifier.py — 通知推送

```python
"""Send notifications via Telegram"""
import requests
from config import Config

def send_telegram(text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    max_len = 4096
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        requests.post(url, json={
            "chat_id": Config.TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        })
```

### Step 6: main.py — 主程式

```python
"""Main orchestrator for Reddit Product Buzz Tracking"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== Reddit 產品聲量追蹤 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 Reddit 產品聲量追蹤 報告\n\n{result}")
        print("✅ Done!")
    else:
        print("⚠ No data collected")

if __name__ == "__main__":
    run()
```

### Step 7: 排程

```bash
# 每天執行
crontab -e
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/reddit-product-buzz-tracking.log 2>&1
```

---

## 測試步驟

| 階段 | 測試 | 預期結果 |
|------|------|---------|
| 1 | 環境變數 | Config.validate() 無錯誤 |
| 2 | 資料收集 | collect_data() 回傳資料 |
| 3 | AI 分析 | analyze_with_ai() 產生繁中報告 |
| 4 | 通知推送 | Telegram 收到訊息 |
| 5 | 完整流程 | python main.py 成功 |

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| API rate limit | 加入 retry + exponential backoff |
| Token 超過上限 | 分段處理，限制輸入長度 |
| Telegram 格式錯誤 | Markdown fallback 為純文字 |
| Cron 環境變數遺失 | 使用絕對路徑 + source .env |
