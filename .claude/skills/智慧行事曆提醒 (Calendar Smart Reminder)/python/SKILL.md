---
name: 智慧行事曆提醒 (Calendar Smart Reminder)/python
description: "Use Case #173 Python 方案: 智慧行事曆提醒。使用 Python 實作 Calendar Smart Reminder 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #173: 智慧行事曆提醒 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# 55. Smart Calendar Reminder

## Introduction

Standard calendar reminders are dumb — they just beep 15 minutes before an event. Your AI agent can do much better: it checks your calendar, reminds you 2 hours ahead with context, suggests preparation steps, and even warns you about travel time.

This use case turns your agent into a proactive calendar assistant that understands your schedule, anticipates what you need, and sends smart reminders via Telegram with actionable context.

Never walk into a meeting unprepared again.

## Skills You Need

- [Calendar Access](https://clawhub.ai/skills/calendar) — Google Calendar or Outlook integration
- Weather — For outdoor event preparation

## How to Setup

### Prerequisites
- Google Calendar or Outlook connected to OpenClaw
- Telegram bot for notifications

### Prompt Template
```
You are my smart calendar assistant. Check my calendar every 30 minutes during waking hours (8 AM - 10 PM).

For each upcoming event in the next 2 hours:

1. **Context**: What is this meeting about? Who's attending?
2. **Preparation**: What should I review or bring?
   - If it's a client meeting → remind me of last interaction
   - If it's a doctor appointment → remind me to bring insurance card
   - If it's a dinner → check the restaurant and suggest what to wear
3. **Logistics**: 
   - How long to get there? (check traffic if it's in-person)
   - Is it raining? Should I bring an umbrella?
4. **Conflicts**: Flag if two events overlap

Send reminders via Telegram. Format:
📅 [Event] in 2 hours
📍 [Location/Link]
📋 [Prep notes]
⏱️ [Leave by X:XX to arrive on time]
```

### Configuration
- Heartbeat check: Every 30 minutes during 8 AM - 10 PM
- Send reminder: 2 hours before each event

## Success Metrics
- Zero missed appointments
- Always prepared with context before meetings
- Travel time warnings prevent being late


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/calendar-smart-reminder
cd ~/calendar-smart-reminder
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

建立 `main.py`，實作 智慧行事曆提醒 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_calendar_smart_reminder():
    """執行 智慧行事曆提醒 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 智慧行事曆提醒 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_calendar_smart_reminder()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/calendar-smart-reminder && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
