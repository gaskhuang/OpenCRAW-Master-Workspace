---
name: 多通道 AI 客服 (Multi-Channel AI Customer Service)/python
description: "Use Case #030 Python 方案: 多通道 AI 客服。使用 Python 實作 Multi-Channel AI Customer Service 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #030: 多通道 AI 客服 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Multi-Channel AI Customer Service Platform

Small businesses juggle WhatsApp, Instagram DMs, emails, and Google Reviews across multiple apps. Customers expect instant responses 24/7, but hiring staff for round-the-clock coverage is expensive.

This use case consolidates all customer touchpoints into a single AI-powered inbox that responds intelligently on your behalf.

## What It Does

- **Unified inbox**: WhatsApp Business, Instagram DMs, Gmail, and Google Reviews in one place
- **AI auto-responses**: Handles FAQs, appointment requests, and common inquiries automatically
- **Human handoff**: Escalates complex issues or flags them for review
- **Test mode**: Demo the system to clients without affecting real customers
- **Business context**: Trained on your services, pricing, and policies

## Real Business Example

At Futurist Systems, we deploy this for local service businesses (restaurants, clinics, salons). One restaurant reduced response time from 4+ hours to under 2 minutes, handling 80% of inquiries automatically.

## Skills You Need

- WhatsApp Business API integration
- Instagram Graph API (via Meta Business)
- `gog` CLI for Gmail
- Google Business Profile API for reviews
- Message routing logic in AGENTS.md

## How to Set It Up

1. **Connect channels** via OpenClaw config:
   - WhatsApp Business API (through 360dialog or official API)
   - Instagram via Meta Business Suite
   - Gmail via `gog` OAuth
   - Google Business Profile API token

2. **Create business knowledge base**:
   - Services and pricing
   - Business hours and location
   - FAQ responses
   - Escalation triggers (e.g., complaints, refund requests)

3. **Configure AGENTS.md** with routing logic:

```text
## Customer Service Mode

When receiving customer messages:

1. Identify channel (WhatsApp/Instagram/Email/Review)
2. Check if test mode is enabled for this client
3. Classify intent:
   - FAQ → respond from knowledge base
   - Appointment → check availability, confirm booking
   - Complaint → flag for human review, acknowledge receipt
   - Review → thank for feedback, address concerns

Response style:
- Friendly, professional, concise
- Match the customer's language (ES/EN/UA)
- Never invent information not in knowledge base
- Sign off with business name

Test mode:
- Prefix responses with [TEST]
- Log but don't send to real channels
```

4. **Set up heartbeat checks** for response monitoring:

```text
## Heartbeat: Customer Service Check

Every 30 minutes:
- Check for unanswered messages > 5 min old
- Alert if response queue is backing up
- Log daily response metrics
```

## Key Insights

- **Language detection matters**: Auto-detect and respond in customer's language
- **Test mode is essential**: Clients need to see it work before going live
- **Handoff rules**: Define clear escalation triggers to avoid AI overreach
- **Response templates**: Pre-approved templates for sensitive topics (refunds, complaints)

## Related Links

- [WhatsApp Business API](https://developers

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
multi-channel-ai-customer-service/
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
mkdir -p multi-channel-ai-customer-service && cd multi-channel-ai-customer-service
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

根據 多通道 AI 客服 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Multi-Channel AI Customer Service"""
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
"""Main orchestrator for Multi-Channel AI Customer Service"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 多通道 AI 客服 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 多通道 AI 客服 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/multi-channel-ai-customer-service.log 2>&1
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
