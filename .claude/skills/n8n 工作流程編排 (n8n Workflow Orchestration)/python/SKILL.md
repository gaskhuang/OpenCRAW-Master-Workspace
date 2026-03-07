---
name: n8n 工作流程編排 (n8n Workflow Orchestration)/python
description: "Use Case #069 Python 方案: n8n 工作流程編排。使用 Python 實作 n8n Workflow Orchestration 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #069: n8n 工作流程編排 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# OpenClaw + n8n Workflow Orchestration

Letting your AI agent directly manage API keys and call external services is a recipe for security incidents. Every new integration means another credential in `.env.local`, another surface for the agent to accidentally leak or misuse.

This use case describes a pattern where OpenClaw delegates all external API interactions to n8n workflows via webhooks — the agent never touches credentials, and every integration is visually inspectable and lockable.

## Pain Point

When OpenClaw handles everything directly, you get three compounding problems:

- **No visibility**: It's hard to inspect what the agent actually built when it's buried in JavaScript skill files or shell scripts
- **Credential sprawl**: Every API key lives in the agent's environment, one bad commit away from exposure
- **Wasted tokens**: Deterministic sub-tasks (send an email, update a spreadsheet) burn LLM reasoning tokens when they could run as simple workflows

## What It Does

- **Proxy pattern**: OpenClaw writes n8n workflows with incoming webhooks, then calls those webhooks for all future API interactions
- **Credential isolation**: API keys live in n8n's credential store — the agent only knows the webhook URL
- **Visual debugging**: Every workflow is inspectable in n8n's drag-and-drop UI
- **Lockable workflows**: Once a workflow is built and tested, you lock it so the agent can't modify how it interacts with the API
- **Safeguard steps**: You can add validation, rate limiting, and approval gates in n8n before any external call executes

## How It Works

1. **Agent designs the workflow**: Tell OpenClaw what you need (e.g., "create a workflow that sends a Slack message when a new GitHub issue is labeled `urgent`")
2. **Agent builds it in n8n**: OpenClaw creates the workflow via n8n's API, including an incoming webhook trigger
3. **You add credentials**: Open n8n's UI, add your Slack token / GitHub token manually
4. **You lock the workflow**: Prevent further modifications by the agent
5. **Agent calls the webhook**: From now on, OpenClaw calls `http://n8n:5678/webhook/my-workflow` with a JSON payload — it never sees the API key

```text
┌──────────────┐     webhook call      ┌─────────────────┐     API call     ┌──────────────┐
│   OpenClaw   │ ───────────────────→  │   n8n Workflow   │ ─────────────→  │  External    │
│   (agent)    │   (no credentials)    │  (locked, with   │  (credentials   │  Service     │
│              │                       │   API keys)      │   stay here)    │  (Slack, etc)│
└──────────────┘                       └─────────────────┘                  └──────────────┘
```

## Skills You Need

- `n8n` API access (for creating/triggering workflows)
- `fetch` or `curl` for webhook calls
- Docker (if using the pre-configured stack)
- n8n credential management (manual, one-time setup per integration)

## How to Set It Up

### Option 1: Pre-configured Docker Stack

A community-maintained Docker Compose setup ([openclaw-n8

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
n8n-workflow-orchestration/
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
mkdir -p n8n-workflow-orchestration && cd n8n-workflow-orchestration
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

根據 n8n 工作流程編排 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for n8n Workflow Orchestration"""
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
"""Main orchestrator for n8n Workflow Orchestration"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== n8n 工作流程編排 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 n8n 工作流程編排 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/n8n-workflow-orchestration.log 2>&1
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
