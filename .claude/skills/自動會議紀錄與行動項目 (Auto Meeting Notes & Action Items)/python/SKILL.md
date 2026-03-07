---
name: 自動會議紀錄與行動項目 (Auto Meeting Notes & Action Items)/python
description: "Use Case #042 Python 方案: 自動會議紀錄與行動項目。使用 Python 實作 Auto Meeting Notes & Action Items 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #042: 自動會議紀錄與行動項目 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Automated Meeting Notes & Action Items

You just finished a 45-minute team call. Now you need to write up the summary, pull out action items, and distribute them to Jira, Linear, or Todoist — manually. By the time you're done, the next meeting is starting. What if your agent handled all of that the moment the transcript lands?

This use case turns any meeting transcript into structured notes and automatically creates tasks in your project management tool.

## Pain Point

Meeting notes are tedious but critical. Most people either skip them (and lose context) or spend 20+ minutes writing them up. Action items get forgotten because they live in someone's head or buried in a chat thread. This agent eliminates the gap between "we discussed it" and "it's tracked and assigned."

## What It Does

- **Watches** for new meeting transcripts (via Otter.ai export, Google Meet transcript, Zoom recording summary, or a simple paste into chat)
- **Extracts** key decisions, discussion topics, and action items with owners and deadlines
- **Creates tasks** in Jira, Linear, Todoist, or Notion — assigned to the right person with context from the meeting
- **Posts a summary** to Slack or Discord so the whole team has a record
- **Follows up** — optionally pings assignees before deadlines via scheduled reminders

## Skills You Need

- Jira, Linear, Todoist, or Notion integration (for task creation)
- Slack or Discord integration (for posting summaries)
- File system access (for reading transcript files)
- Scheduling / cron (for follow-up reminders)
- Optional: Otter.ai, Fireflies.ai, or Google Meet API for automatic transcript retrieval

## How to Set It Up

1. Choose your transcript source. The simplest approach is pasting the transcript directly into chat. For automation, set up a folder watch or API integration.

2. Prompt OpenClaw:
```text
I just finished a meeting. Here's the transcript:

[paste transcript or point to file]

Please:
1. Write a concise summary (max 5 bullet points) covering key decisions and topics.
2. Extract ALL action items. For each one, identify:
   - What needs to be done
   - Who is responsible (match names to my team)
   - Deadline (if mentioned, otherwise mark as "TBD")
3. Create a Jira ticket for each action item, assigned to the right person.
4. Post the full summary to #meeting-notes in Slack.
```

3. For fully automated pipeline (transcript folder watch):
```text
Set up a recurring task: every 30 minutes, check ~/meeting-transcripts/ for
new .txt or .vtt files. When you find one:

1. Parse the transcript into a structured summary with action items.
2. Create tasks in Linear for each action item.
3. Post the summary to #team-updates in Slack.
4. Move the processed file to ~/meeting-transcripts/processed/.

For each action item with a deadline, set a reminder to ping the assignee
in Slack one day before it's due.
```

4. Customize the output format:
```text
When writing meeting summaries, always use this structure:
- **Date & Attendees*

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
auto-meeting-notes-&-action-items/
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
mkdir -p auto-meeting-notes-&-action-items && cd auto-meeting-notes-&-action-items
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

根據 自動會議紀錄與行動項目 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Auto Meeting Notes & Action Items"""
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
"""Main orchestrator for Auto Meeting Notes & Action Items"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 自動會議紀錄與行動項目 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 自動會議紀錄與行動項目 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/auto-meeting-notes-&-action-items.log 2>&1
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
