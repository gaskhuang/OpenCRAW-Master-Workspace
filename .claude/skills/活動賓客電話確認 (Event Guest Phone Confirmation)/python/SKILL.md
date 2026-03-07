---
name: 活動賓客電話確認 (Event Guest Phone Confirmation)/python
description: "Use Case #045 Python 方案: 活動賓客電話確認。使用 Python 實作 Event Guest Phone Confirmation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #045: 活動賓客電話確認 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Event Guest Confirmation

You're hosting an event — a dinner party, a wedding, a company offsite — and you need to confirm attendance from a list of guests. Manually calling 20+ people is tedious: you play phone tag, forget who said what, and lose track of dietary restrictions or plus-ones. Texting works sometimes, but people ignore messages. A real phone call gets a much higher response rate.

This use case has OpenClaw call each guest on your list using the [SuperCall](https://clawhub.ai/xonder/supercall) plugin, confirm whether they're attending, collect any notes, and compile everything into a summary for you.

## What It Does

- Iterates through a guest list (names + phone numbers) and calls each one
- The AI introduces itself as your event coordinator with a friendly persona
- Confirms the event date, time, and location with the guest
- Asks if they're attending, and collects any notes (dietary needs, plus-ones, arrival time, etc.)
- After all calls are complete, compiles a summary: who confirmed, who declined, who didn't pick up, and any notes

## Why SuperCall

This use case works with the [SuperCall](https://clawhub.ai/xonder/supercall) plugin specifically — not the built-in `voice_call` plugin. The key difference: SuperCall is a fully standalone voice agent. The AI persona on the call **only has access to the context you provide** (the persona name, the goal, and the opening line). It cannot access your gateway agent, your files, your other tools, or anything else.

This matters for guest confirmation because:

- **Safety**: The person on the other end of the call can't manipulate or access your agent through the conversation. There's no risk of prompt injection or data leakage.
- **Better conversations**: Because the AI is scoped to a single focused task (confirm attendance), it stays on-topic and handles the call more naturally than a general-purpose voice agent would.
- **Batch-friendly**: You're making many calls to different people. A sandboxed persona that resets per call is exactly what you want — no bleed-over between conversations.

## Skills You Need

- [SuperCall](https://clawhub.ai/xonder/supercall) — install via `openclaw plugins install @xonder/supercall`
- A Twilio account with a phone number (for making outbound calls)
- An OpenAI API key (for the GPT-4o Realtime voice AI)
- ngrok (for webhook tunneling — free tier works)

See the [SuperCall README](https://github.com/xonder/supercall) for full configuration instructions.

## How to Set It Up

1. Install and configure SuperCall following the [setup guide](https://github.com/xonder/supercall#configuration). Make sure hooks are enabled in your OpenClaw config.

2. Prepare your guest list. You can paste it directly in chat or keep it in a file:

```text
Guest List — Summer BBQ, Saturday June 14th, 4 PM, 23 Oak Street

- Sarah Johnson: +15551234567
- Mike Chen: +15559876543
- Rachel Torres: +15555551234
- David Kim: +15558887777
```

3. Prompt OpenClaw:

```text
I need you

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
event-guest-phone-confirmation/
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
mkdir -p event-guest-phone-confirmation && cd event-guest-phone-confirmation
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

根據 活動賓客電話確認 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Event Guest Phone Confirmation"""
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
"""Main orchestrator for Event Guest Phone Confirmation"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 活動賓客電話確認 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 活動賓客電話確認 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/event-guest-phone-confirmation.log 2>&1
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
