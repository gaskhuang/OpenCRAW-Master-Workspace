---
name: 自由工作者案源開發 (Freelancer Lead Generation)/python
description: "Use Case #064 Python 方案: 自由工作者案源開發。使用 Python 實作 Freelancer Lead Generation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #064: 自由工作者案源開發 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# Freelancer Lead Pipeline

> Automate job discovery, lead qualification, proposal drafting, and follow-ups — so you can focus on actual client work.

---

## The Problem

Finding quality freelance gigs is a full-time job on top of your actual work. You spend hours scrolling Upwork, LinkedIn, and niche job boards, only to find most postings don't match your skills, budget, or timeline. By the time you craft a personalized proposal, the best opportunities are already flooded with applicants. Meanwhile, promising leads go cold because you forgot to follow up.

---

## The Solution

OpenClaw monitors job boards on your schedule, filters opportunities against your criteria, drafts personalized proposals using context from each posting, and tracks your entire pipeline in a simple markdown file. It sends you only qualified leads, reminds you to follow up, and can even help generate invoices when you close deals.

**What you get:**
- Morning digest of qualified leads matching your criteria
- Pre-drafted proposals ready to customize and send
- Automatic pipeline tracking with follow-up reminders
- No more missed opportunities or forgotten leads

---

## Setup Guide

### Step 1: Create Your Freelancer Profile (5 minutes)

Create `~/openclaw/freelance/PROFILE.md`:

```markdown
# Freelancer Profile

## Identity
- **Name:** [Your Name]
- **Title:** Senior Full-Stack Developer
- **Specialties:** React, Node.js, Python, AWS
- **Experience:** 8 years

## Ideal Client Criteria
- **Budget minimum:** $50/hour or $2,000+ fixed projects
- **Project length:** 1 week to 3 months
- **Industries:** SaaS, fintech, healthtech, e-commerce
- **Red flags:** "equity only", "exposure", "quick test project", budget under $500

## Availability
- **Hours/week:** 20-30
- **Timezone:** EST (UTC-5)
- **Start date:** Can start within 1 week

## Portfolio Links
- GitHub: https://github.com/yourname
- Portfolio: https://yoursite.com
- LinkedIn: https://linkedin.com/in/yourname

## Proposal Style
- Tone: Professional but personable
- Length: 150-250 words
- Always include: Relevant experience, specific approach, timeline estimate
- Avoid: Generic templates, desperation, undercutting
```

### Step 2: Set Up Pipeline Tracking (3 minutes)

Create `~/openclaw/freelance/PIPELINE.md`:

```markdown
# Lead Pipeline

## 🔥 Hot Leads (respond today)
<!-- Leads scored 8+/10, posted <24h ago -->

## 📋 Qualified Leads (respond this week)
<!-- Leads scored 6-7/10, good fit but not urgent -->

## ✉️ Proposals Sent
| Date | Client | Project | Amount | Status | Follow-up |
|------|--------|---------|--------|--------|-----------|

## 🤝 Active Projects
| Client | Project | Start | End | Rate | Invoiced |
|--------|---------|-------|-----|------|----------|

## ❌ Rejected/Passed
<!-- Quick notes on why, for pattern learning -->
```

### Step 3: Create Job Board URLs File (5 minutes)

Create `~/openclaw/freelance/JOB_SOURCES.md`:

```markdown
# Job Sources to Monitor

## Upwork
- https://www.upwork.com/nx/f

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
freelancer-lead-generation/
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
mkdir -p freelancer-lead-generation && cd freelancer-lead-generation
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

根據 自由工作者案源開發 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Freelancer Lead Generation"""
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
"""Main orchestrator for Freelancer Lead Generation"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 自由工作者案源開發 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 自由工作者案源開發 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/freelancer-lead-generation.log 2>&1
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
