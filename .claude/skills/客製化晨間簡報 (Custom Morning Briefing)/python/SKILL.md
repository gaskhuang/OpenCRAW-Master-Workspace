---
name: 客製化晨間簡報 (Custom Morning Briefing)/python
description: "Use Case #041 Python 方案: 客製化晨間簡報。使用 Python 實作 Custom Morning Briefing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #041: 客製化晨間簡報 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Custom Morning Brief

You wake up and spend the first 30 minutes of your day catching up — scrolling news, checking your calendar, reviewing your to-do list, trying to figure out what matters today. What if all of that was already done and waiting for you as a text message?

This workflow has OpenClaw send you a fully customized morning briefing every day at a scheduled time, covering news, tasks, ideas, and proactive recommendations.

## What It Does

- Sends a structured morning report to Telegram, Discord, or iMessage at the same time every day (e.g., 8:00 AM)
- Researches overnight news relevant to your interests by browsing the web
- Reviews your to-do list and surfaces tasks for the day
- Generates creative output (full scripts, email drafts, business proposals — not just ideas) while you sleep
- Recommends tasks the AI can complete autonomously to help you that day

## Pain Point

You're spending your most productive morning hours just getting oriented. Meanwhile, your AI agent sits idle all night. The morning brief turns idle overnight hours into productive prep time — you wake up to work already done.

## Skills You Need

- Telegram, Discord, or iMessage integration
- Todoist / Apple Reminders / Asana integration (whichever you use for tasks)
- [x-research-v2](https://clawhub.ai) for social media trend research (optional)

## How to Set It Up

1. Connect OpenClaw to your messaging platform and task manager.

2. Prompt OpenClaw:
```text
I want to set up a regular morning brief. Every morning at 8:00 AM,
send me a report through Telegram.

I want this report to include:
1. News stories relevant to my interests (AI, startups, tech)
2. Ideas for content I can create today
3. Tasks I need to complete today (pull from my to-do list)
4. Recommendations for tasks you can complete for me today

For the content ideas, write full draft scripts/outlines — not just titles.
```

3. OpenClaw will schedule this automatically. Verify it's working by checking your messages the next morning.

4. Customize over time — just text your bot:
```text
Add weather forecast to my morning brief.
Stop including general news, focus only on AI.
Include a motivational quote each morning.
```

5. If you can't think of what to include, you don't have to — just say:
```text
I want this report to include things relevant to me.
Think of what would be most helpful to put in this report.
```

## Key Insights

- The AI-recommended tasks section is the most powerful part — it has the agent proactively think of ways to help you, rather than waiting for instructions.
- You can customize the brief just by texting. Say "Add stock prices to my morning brief" and it updates.
- Full drafts (not just ideas) are the key to saving time. Wake up to scripts, not suggestions.
- It doesn't matter what industry you're in — a morning brief with tasks, news, and proactive suggestions is universally useful.

## Based On

Inspired by [Alex Finn's video on life-changing OpenClaw use cases](https:

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
custom-morning-briefing/
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
mkdir -p custom-morning-briefing && cd custom-morning-briefing
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

根據 客製化晨間簡報 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Custom Morning Briefing"""
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
"""Main orchestrator for Custom Morning Briefing"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 客製化晨間簡報 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 客製化晨間簡報 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/custom-morning-briefing.log 2>&1
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
