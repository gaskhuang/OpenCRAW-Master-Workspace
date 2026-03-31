---
name: 心理健康定期打卡 (Mental Health Check-In)/python
description: "Use Case #109 Python 方案: 心理健康定期打卡。使用 Python 實作 Mental Health Check-In 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #109: 心理健康定期打卡 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 🧠 Mental Health Check-In

> Know yourself better. Track moods, prep for therapy, spot patterns before they spiral.

---

## The Problem

Mental health is invisible until it's not. You feel "off" but can't explain why. Therapy sessions start with "how was your week?" and you draw a blank. Bad patterns sneak up because you're not tracking them.

---

## The Solution

OpenClaw provides gentle daily check-ins, logs moods without judgment, helps you prepare for therapy sessions with actual data, and identifies patterns before they become problems.

---

## Setup Guide

### Step 1: Install Mindfulness & Journaling Skills

```bash
openclaw skill install obsidian-conversation-backup  # or notion
openclaw skill install remind-me
openclaw skill install calendar
```

### Step 2: Configure Check-In Profile

Create `~/openclaw/mentalhealth/config.json`:

```json
{
  "checkInTimes": ["09:00", "21:00"],
  "therapyDay": "Thursday",
  "therapyTime": "14:00",
  "moodScale": "1-10",
  "trackingAreas": [
    "mood",
    "anxiety",
    "energy",
    "sleep_quality",
    "social_connection",
    "accomplishment"
  ],
  "triggerWarnings": {
    "lowMoodStreak": 3,
    "anxietyThreshold": 7,
    "isolationDays": 2
  },
  "storage": "~/openclaw/mentalhealth/entries/"
}
```

### Step 3: Set Up Check-In Questions

Create `~/openclaw/mentalhealth/questions.md`:

```markdown
# Morning Check-In (2 min)
- How are you feeling right now? (1-10)
- Any anxiety present? (1-10)
- How did you sleep?
- What's one thing you're looking forward to?

# Evening Check-In (3 min)
- Overall mood today (1-10)
- Energy level (1-10)
- Did you connect with anyone today?
- One thing that went well
- Anything weighing on you?

# Weekly Patterns to Watch
- Are mood scores trending down?
- More anxious days than calm?
- Social isolation increasing?
- Self-care being neglected?

# Therapy Prep Questions
- What's been on my mind this week?
- Any breakthrough moments?
- What am I avoiding?
- What do I want to work on next?
```

### Step 4: Create Entry Template

Create `~/openclaw/mentalhealth/template.json`:

```json
{
  "date": "",
  "morning": {
    "mood": null,
    "anxiety": null,
    "sleepQuality": null,
    "lookingForward": ""
  },
  "evening": {
    "mood": null,
    "energy": null,
    "socialConnection": false,
    "win": "",
    "concern": ""
  },
  "notes": "",
  "tags": []
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `obsidian-conversation-backup` | Secure entry storage |
| `notion` | Alternative storage |
| `remind-me` | Check-in reminders |
| `calendar` | Therapy scheduling |
| `reflect` | Pattern analysis |

---

## Example Prompts

**Morning check-in:**
```
Morning check-in. Mood is 6, anxiety 4, slept okay. Looking forward to lunch with a friend.
```

**Quick mood log:**
```
Feeling anxious right now - about a 7. Work deadline stress.
```

**Pattern analysis:**
```
How has my mood been this month? Any patterns with days of the week, sleep, or social time

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
mental-health-check-in/
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
mkdir -p mental-health-check-in && cd mental-health-check-in
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

根據 心理健康定期打卡 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Mental Health Check-In"""
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
"""Main orchestrator for Mental Health Check-In"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 心理健康定期打卡 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 心理健康定期打卡 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/mental-health-check-in.log 2>&1
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
