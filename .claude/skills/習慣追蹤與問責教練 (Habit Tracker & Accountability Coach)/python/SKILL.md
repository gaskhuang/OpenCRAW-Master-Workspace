---
name: 習慣追蹤與問責教練 (Habit Tracker & Accountability Coach)/python
description: "Use Case #043 Python 方案: 習慣追蹤與問責教練。使用 Python 實作 Habit Tracker & Accountability Coach 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #043: 習慣追蹤與問責教練 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Habit Tracker & Accountability Coach

You've tried every habit tracker app out there. They all work for a week, then you stop opening them. The problem isn't the app — it's that tracking habits is passive. What if your agent actively reached out to you, asked how your day went, and adapted its approach based on whether you're on a streak or falling off?

This use case turns OpenClaw into a proactive accountability partner that checks in with you daily via Telegram or SMS.

## Pain Point

Habit apps rely on you remembering to open them. Push notifications are easy to ignore. What actually works for behavior change is **active accountability** — someone (or something) that asks you directly, celebrates your wins, and nudges you when you slip. This agent does exactly that, without the awkwardness of bugging a friend.

## What It Does

- **Daily check-ins** via Telegram or SMS at times you choose (e.g., 7 AM for morning routine, 9 PM for end-of-day review)
- **Tracks habits** you define — exercise, reading, meditation, water intake, coding, whatever matters to you
- **Streak tracking** — knows your current streak for each habit and references it in messages
- **Adaptive nudges** — adjusts tone based on your performance (encouraging when you're consistent, gently persistent when you miss days)
- **Weekly reports** — summarizes your week with completion rates, longest streaks, and patterns (e.g., "You tend to skip workouts on Wednesdays")

## Skills You Need

- Telegram or SMS integration (Twilio for SMS, or Telegram Bot API)
- Scheduling / cron for timed check-ins
- File system or database access for storing habit data
- Optional: Google Sheets integration for a visual habit dashboard

## How to Set It Up

1. Define your habits and check-in schedule:
```text
I want you to be my accountability coach. Track these daily habits for me:

1. Morning workout (check in at 7:30 AM)
2. Read for 30 minutes (check in at 8:00 PM)
3. No social media before noon (check in at 12:30 PM)
4. Drink 8 glasses of water (check in at 6:00 PM)

Send me a Telegram message at each check-in time asking if I completed
the habit. Keep track of my streaks in a local file.
```

2. Set up the tracking and tone:
```text
When I confirm a habit, respond with a short encouraging message and
mention my current streak. Example: "Day 12 of morning workouts. Solid."

When I miss a habit, don't guilt-trip me. Just acknowledge it and remind
me why I started. If I miss 3 days in a row, send a longer motivational
message and ask if I want to adjust the goal.

If I don't respond to a check-in within 2 hours, send one follow-up.
Don't spam me after that.
```

3. Add weekly reports:
```text
Every Sunday at 10 AM, send me a weekly summary:
- Completion rate for each habit
- Current streaks
- Best day and worst day
- One pattern you noticed (e.g., "You always skip reading on Fridays")
- One suggestion for next week

Store all data in ~/habits/log.json so I can review history anytime.
```

4. Option

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
habit-tracker-&-accountability-coach/
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
mkdir -p habit-tracker-&-accountability-coach && cd habit-tracker-&-accountability-coach
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

根據 習慣追蹤與問責教練 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Habit Tracker & Accountability Coach"""
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
"""Main orchestrator for Habit Tracker & Accountability Coach"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 習慣追蹤與問責教練 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 習慣追蹤與問責教練 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/habit-tracker-&-accountability-coach.log 2>&1
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
