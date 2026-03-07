---
name: 發票處理自動化 (Invoice Processing Automation)/python
description: "Use Case #106 Python 方案: 發票處理自動化。使用 Python 實作 Invoice Processing Automation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #106: 發票處理自動化 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# Invoice Chaser

> Automated invoice tracking and payment reminders for freelancers and small businesses

## The Problem

Chasing unpaid invoices is awkward, time-consuming, and easy to forget—leading to cash flow problems that kill otherwise healthy businesses. Freelancers especially struggle: you're busy doing actual work, and manually tracking who owes what, when it's due, and who needs a nudge feels like a second job. Meanwhile, that $3,000 invoice from 45 days ago quietly slips through the cracks.

## The Solution

OpenClaw becomes your accounts receivable assistant. It tracks invoices from email confirmations, manual input, or CSV imports, then automatically sends polite reminder emails at customizable intervals (7, 14, 30 days overdue). It learns which clients pay slow vs. fast, warns you about potential cash flow gaps, and keeps a running ledger you can query anytime with natural language ("Who owes me money?" / "What's my expected income this month?").

---

## Setup Guide

### Step 1: Create Your Invoice Tracker File

Create `invoices.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/data
cat > ~/openclaw/data/invoices.json << 'EOF'
{
  "invoices": [],
  "clients": {},
  "settings": {
    "reminder_days": [7, 14, 30],
    "currency": "USD",
    "your_name": "YOUR NAME",
    "your_email": "your@email.com",
    "payment_terms": "Net 30"
  }
}
EOF
```

### Step 2: Create the Invoice Template

Create `~/openclaw/templates/invoice-reminder.md`:

```markdown
Subject: Friendly Reminder: Invoice #{{invoice_id}} - {{days_overdue}} days overdue

Hi {{client_name}},

I hope you're doing well! I wanted to follow up on Invoice #{{invoice_id}} for {{amount}} {{currency}}, which was due on {{due_date}}.

**Invoice Details:**
- Invoice #: {{invoice_id}}
- Amount: {{amount}} {{currency}}
- Due Date: {{due_date}}
- Days Overdue: {{days_overdue}}
- Description: {{description}}

If payment has already been sent, please disregard this message—and thank you!

If you have any questions or need to discuss payment arrangements, I'm happy to chat.

Best regards,
{{your_name}}
```

### Step 3: Set Up Email Access

Ensure OpenClaw has email skills configured. Add to your `skills/` directory or verify existing email integration works:

```bash
# Test email access
openclaw run "Check my inbox for any emails containing 'invoice' or 'payment'"
```

### Step 4: Add Your First Invoice

Simply tell OpenClaw:

```
Add invoice: Client "Acme Corp", $2,500 for "Website Redesign", 
invoice #INV-2024-001, due date Jan 15 2025, 
contact email: billing@acmecorp.com
```

### Step 5: Configure Cron Jobs (see section below)

### Step 6: Test the System

```
Show me all outstanding invoices
```

---

## Skills Needed

| Skill | Purpose | Required? |
|-------|---------|-----------|
| **Email (Gmail/IMAP)** | Send reminder emails, scan for payment confirmations | ✅ Yes |
| **File System** | Store invoice data in JSON | ✅ Built-in |
| **Calendar** | Track due dates, sched

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
invoice-processing-automation/
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
mkdir -p invoice-processing-automation && cd invoice-processing-automation
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

根據 發票處理自動化 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Invoice Processing Automation"""
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
"""Main orchestrator for Invoice Processing Automation"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 發票處理自動化 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 發票處理自動化 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/invoice-processing-automation.log 2>&1
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
