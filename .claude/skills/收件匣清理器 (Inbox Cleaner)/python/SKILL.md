---
name: 收件匣清理器 (Inbox Cleaner)/python
description: "Use Case #032 Python 方案: 收件匣清理器。使用 Python 實作 Inbox Cleaner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #032: 收件匣清理器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Inbox De-clutter

Newsletters can take up the inbox like nothing else. Often times they pile-up without being opened at all. 

## Skills you Need
[Gmail OAuth Setup](https://clawhub.ai/kai-jar/gmail-oauth).

## How to Set it Up
1. [optional] Create a new gmail specifically for OpenClaw.
2. [optional] Unsubscribe from all newsletters from your main email and subscribe to them using the OpenClaw email.
3. Install the skill and make sure it works. 
4. Instruct OpenClaw:
```txt
I want you to run a cron job everyday at 8 p.m. to read all the newsletter emails of the past 24 hours and give me a digest of the most important bits along with links to read more. Then ask for my feedback on whether you picked good bits, and update your memory based on my preferences for better digests in the future jobs.
```

---

# 收件箱分类与跟进

## 简介

自动分类邮件、起草回复、总结线程、建议下一步行动。适合创始人、销售、客户服务和客服人员。

**为什么重要**：减少邮件处理时间，确保重要邮件不被遗漏，提高响应效率。

**真实例子**：一位销售总监使用此代理管理每日 200+ 邮件，代理自动分类、起草回复，邮件处理时间从 3 小时减少到 30 分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 邮件处理 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `task_manager` | [ClawdHub](https://clawhub.com/skills/tasks) | 创建任务 |

---

## 使用方式

### 自动分类
- 客户邮件
- 内部通知
- 营销邮件
- 紧急事项

### 起草回复
代理根据邮件内容起草回复建议

### 跟进提醒
自动创建跟进任务

---

## 来源

- 来源：Quantum Byte


---

# 📧 Email Triage Autopilot

> Transform inbox chaos into organized action. Stop drowning in emails—let OpenClaw surface what matters.

---

## The Problem

The average professional receives 120+ emails daily, spending 2-3 hours just reading and sorting them. Most are noise (newsletters, notifications, CC chains), but buried in there are urgent requests, deadlines, and opportunities that get missed. You either live in your inbox anxiously or miss important things while trying to batch-check. Neither works.

---

## The Solution

OpenClaw continuously monitors your inbox, categorizes every email by urgency and importance, drafts responses to routine queries, extracts action items into your todo system, and delivers a concise morning briefing of what actually needs your attention. You check email once or twice a day, fully informed, and respond only to what matters.

**The magic:** OpenClaw learns YOUR priorities—who's important, what topics are urgent, which newsletters you actually read vs. ignore.

---

## Setup Guide

### Step 1: Install the Gmail Skill (5 minutes)

```bash
# Install the gmail skill
openclaw skill install gmail

# Authenticate (opens browser for OAuth)
openclaw skill gmail auth
```

For other providers:
- **Outlook:** `openclaw skill install outlook`
- **IMAP:** `openclaw skill install imap` (works with any provider)

### Step 2: Create Your Priority Rules File

Create `~/openclaw/email-rules.md`:

```markdown
# Email Priority Rules

## 🔴 URGENT (notify immediately)
- From: [boss@company.com, ceo@company.com, wife@family.com]
- Subject contains: "urgent", "asap", "emergency", 

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
inbox-cleaner/
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
mkdir -p inbox-cleaner && cd inbox-cleaner
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

根據 收件匣清理器 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Inbox Cleaner"""
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
"""Main orchestrator for Inbox Cleaner"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 收件匣清理器 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 收件匣清理器 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/inbox-cleaner.log 2>&1
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
