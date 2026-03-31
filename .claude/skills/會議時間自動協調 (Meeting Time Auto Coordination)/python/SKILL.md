---
name: 會議時間自動協調 (Meeting Time Auto Coordination)/python
description: "Use Case #054 Python 方案: 會議時間自動協調。使用 Python 實作 Meeting Time Auto Coordination 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #054: 會議時間自動協調 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 🗓️ Smart Meeting Scheduler

> Schedule meetings in seconds. Timezone math done for you, conflicts detected, follow-ups automated.

---

## The Problem

Scheduling meetings across timezones is a nightmare. You're juggling Calendly links, checking five people's availability, doing timezone math in your head, and manually sending follow-up reminders. Half the meeting gets wasted because nobody sent an agenda, and action items disappear into the void after the call ends.

---

## The Solution

OpenClaw handles the entire meeting lifecycle: finds times that work across timezones, checks everyone's availability, sends calendar invites with context, reminds participants before the meeting, and automatically captures and distributes follow-up action items.

---

## Setup Guide

### Step 1: Install Calendar Skills

```bash
openclaw skill install calendar       # Google Calendar integration
openclaw skill install ical           # iCal/Apple Calendar support
openclaw skill install remind-me      # Smart reminders
openclaw skill install gmail          # Email invites
```

### Step 2: Configure Timezone Preferences

Create `~/openclaw/meetings/config.json`:

```json
{
  "myTimezone": "America/New_York",
  "workingHours": {
    "start": "09:00",
    "end": "18:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  },
  "bufferMinutes": 15,
  "defaultDuration": 30,
  "preferredTimes": ["10:00", "14:00", "16:00"],
  "avoidTimes": ["12:00-13:00"]
}
```

### Step 3: Set Up Contact Timezones

Create `~/openclaw/meetings/contacts.json`:

```json
{
  "contacts": [
    {"name": "Sarah", "email": "sarah@example.com", "timezone": "Europe/London"},
    {"name": "Raj", "email": "raj@example.com", "timezone": "Asia/Kolkata"},
    {"name": "Alex", "email": "alex@example.com", "timezone": "America/Los_Angeles"}
  ]
}
```

### Step 4: Create Meeting Templates

Create `~/openclaw/meetings/templates.md`:

```markdown
# Meeting Templates

## Quick Sync (15 min)
- No agenda required
- Reminder: 5 min before

## 1:1 (30 min)
- Include talking points
- Reminder: 1 hour before
- Follow-up: Action items within 24h

## Team Meeting (60 min)
- Agenda required 24h before
- Reminder: 1 day + 1 hour before
- Follow-up: Notes + recording link
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `calendar` | Google Calendar read/write |
| `ical` | Apple Calendar support |
| `remind-me` | Pre-meeting reminders |
| `gmail` | Send invites and follow-ups |

---

## Example Prompts

**Schedule a meeting:**
```
Schedule a 30-min call with Sarah and Raj sometime next week. 
Find a time that works for all timezones.
```

**Check availability:**
```
What does my Thursday look like? When am I free for a 1-hour meeting?
```

**Timezone conversion:**
```
If I schedule a call at 3 PM my time, what time is that for Sarah in London and Raj in Mumbai?
```

**Meeting follow-up:**
```
We just finished the product sync. Send follow-up notes to all participants 
with the

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
meeting-time-auto-coordination/
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
mkdir -p meeting-time-auto-coordination && cd meeting-time-auto-coordination
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

根據 會議時間自動協調 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Meeting Time Auto Coordination"""
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
"""Main orchestrator for Meeting Time Auto Coordination"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 會議時間自動協調 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 會議時間自動協調 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/meeting-time-auto-coordination.log 2>&1
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
