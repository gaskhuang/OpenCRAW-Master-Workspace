---
name: 異步站會機器人 (Async Standup Bot)/python
description: "Use Case #053 Python 方案: 異步站會機器人。使用 Python 實作 Async Standup Bot 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #053: 異步站會機器人 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 🤖 Async Team Standup Bot

> Run standups without the meeting. Blockers surfaced, progress tracked, time saved.

---

## The Problem

Daily standups eat 15-30 minutes of everyone's time, often at the worst part of the morning. Half the team zones out during updates that don't affect them. Remote teams across timezones struggle to find a time that works. Real blockers get buried in routine updates, and nobody actually reads the notes afterward.

---

## The Solution

OpenClaw runs async standups: collects updates via DM at each person's preferred time, identifies blockers automatically, creates digestible summaries, and alerts the right people when action is needed. Your team gets focused time back while staying more informed than before.

---

## Setup Guide

### Step 1: Install Communication Skills

```bash
openclaw skill install slack          # Slack integration
openclaw skill install discord        # Discord support
openclaw skill install telegram       # Telegram bots
openclaw skill install linear         # Issue tracker integration
```

### Step 2: Define Team Structure

Create `~/openclaw/standups/team.json`:

```json
{
  "team": "Engineering",
  "members": [
    {"name": "Alice", "handle": "@alice", "timezone": "America/New_York", "promptTime": "09:00"},
    {"name": "Bob", "handle": "@bob", "timezone": "Europe/London", "promptTime": "09:30"},
    {"name": "Priya", "handle": "@priya", "timezone": "Asia/Kolkata", "promptTime": "10:00"}
  ],
  "summaryChannel": "#engineering-standups",
  "alertChannel": "#engineering-alerts",
  "manager": "@sarah"
}
```

### Step 3: Configure Standup Questions

Create `~/openclaw/standups/questions.md`:

```markdown
# Standup Questions

## Daily (Mon-Fri)
1. What did you accomplish yesterday?
2. What are you working on today?
3. Any blockers or need help with anything?

## Monday Addition
4. What's your main goal for this week?

## Friday Addition
4. What went well this week?
5. What could have gone better?

## Blocker Keywords
- stuck, blocked, waiting on, need help
- can't, unable to, delayed
- dependency, waiting for, blocked by
```

### Step 4: Set Up Blocker Detection

Create `~/openclaw/standups/alerts.md`:

```markdown
# Alert Rules

## Immediate Alert (DM manager)
- Blocker mentioned + "urgent" or "critical"
- Same blocker mentioned 2+ days in a row
- Team member hasn't responded in 48 hours

## Daily Summary Include
- All blockers with owner
- Cross-team dependencies
- Risks to sprint commitments

## Weekly Patterns to Flag
- Team member consistently blocked
- Recurring blocker themes
- Velocity drops
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `slack` | Slack DMs and channels |
| `discord` | Discord integration |
| `telegram` | Telegram bot support |
| `linear` | Link blockers to issues |

---

## Example Prompts

**Start standup collection:**
```
Send standup prompts to the engineering team. Use each person's preferred time.
```

**Generate summary:**
```
Create today's

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
async-standup-bot/
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
mkdir -p async-standup-bot && cd async-standup-bot
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

根據 異步站會機器人 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Async Standup Bot"""
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
"""Main orchestrator for Async Standup Bot"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 異步站會機器人 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 異步站會機器人 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/async-standup-bot.log 2>&1
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
