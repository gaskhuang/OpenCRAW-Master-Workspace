---
name: 冷外聯自動化 (Cold Outreach Automation)/python
description: "Use Case #061 Python 方案: 冷外聯自動化。使用 Python 實作 Cold Outreach Automation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #061: 冷外聯自動化 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# ✉️ Cold Outreach Automation

> Personalized at scale. Not spray-and-pray, but thoughtful outreach multiplied.

---

## The Problem

Cold outreach works when it's personal. But personalization doesn't scale—researching each prospect takes 15 minutes. So you either send generic emails (ignored) or limit your outreach (slow growth).

---

## The Solution

OpenClaw researches prospects automatically, finds personalization hooks, generates custom messages, and manages follow-up sequences. You review and send—personal touch at scale.

---

## Setup Guide

### Step 1: Install Outreach Skills

```bash
openclaw skill install apollo
openclaw skill install linkedin
openclaw skill install gmail
openclaw skill install web-fetch
```

### Step 2: Define Ideal Customer Profile

Create `~/openclaw/outreach/icp.md`:

```markdown
# Ideal Customer Profile

## Company
- Size: 50-500 employees
- Industry: SaaS, Tech, E-commerce
- Growth stage: Series A-C
- Tech stack: Uses [relevant tools]

## Persona
- Title: VP/Director of [department]
- Responsibility: [specific area]
- Pain points: [list]

## Disqualifiers
- Less than 10 employees
- Non-English speaking
- Already using competitor
```

### Step 3: Create Message Templates

Create `~/openclaw/outreach/templates.md`:

```markdown
# Outreach Templates

## First Touch
Subject: {personalization_hook}

Hi {first_name},

{personalized_opener_based_on_research}

[Value prop in 1 sentence]

Would it make sense to chat for 15 minutes?

## Follow-up 1 (Day 3)
Subject: Re: {original_subject}

{name}, wanted to bump this up...

## Follow-up 2 (Day 7)
Subject: Quick question, {name}

Different angle/value prop...

## Break-up (Day 14)
Subject: Should I close your file?

Last attempt, remove friction...
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `apollo` | Prospect research |
| `linkedin` | Profile insights |
| `gmail` | Email sending |
| `web-fetch` | Company research |

---

## Example Prompts

**Research prospect:**
```
Research [person] at [company]. Find personalization hooks: recent news, common connections, content they've shared.
```

**Generate sequence:**
```
Create a 4-email sequence for [persona] at [company type]. Focus on [pain point].
```

**Review and send:**
```
Show me today's outreach queue with draft messages. Let me approve or edit before sending.
```

**Optimize:**
```
Which subject lines and openers got the best response rates? Update my templates.
```

---

## Cron Schedule

```
0 7 * * 1-5    # 7 AM weekdays - prepare daily outreach
0 9 * * 1-5    # 9 AM - send first touch emails
0 14 * * 1-5   # 2 PM - send follow-ups
0 10 * * 1     # Monday - weekly metrics review
```

---

## Expected Results

**Week 1:**
- 5x outreach volume with same effort
- Personalized messages for every prospect

**Month 1:**
- Higher response rates than generic outreach
- Clear data on what messaging works

**Month 3:**
- Predictable meeting pipeline
- Continuously optimized messaging
- Scalable pros

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
cold-outreach-automation/
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
mkdir -p cold-outreach-automation && cd cold-outreach-automation
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

根據 冷外聯自動化 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Cold Outreach Automation"""
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
"""Main orchestrator for Cold Outreach Automation"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 冷外聯自動化 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 冷外聯自動化 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/cold-outreach-automation.log 2>&1
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
