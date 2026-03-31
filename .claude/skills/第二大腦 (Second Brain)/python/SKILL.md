---
name: 第二大腦 (Second Brain)/python
description: "Use Case #044 Python 方案: 第二大腦。使用 Python 實作 Second Brain 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #044: 第二大腦 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Second Brain

You come up with ideas, find interesting links, hear about books to read — but you never have a good system for capturing them. Notion gets complex, Apple Notes becomes a graveyard of 10,000 unread entries. You need something as simple as texting a friend.

This workflow turns OpenClaw into a memory-capture system you interact with via text message, backed by a custom searchable UI you can browse anytime.

## What It Does

- Text anything to your OpenClaw via Telegram, iMessage, or Discord — "Remind me to read a book about local LLMs" — and it remembers it instantly
- OpenClaw's built-in memory system stores everything you tell it permanently
- A custom Next.js dashboard lets you search through every memory, conversation, and note
- Global search (Cmd+K) across all memories, documents, and tasks
- No folders, no tags, no complex organization — just text and search

## Pain Point

Every note-taking app eventually becomes a chore. You stop using it because the friction of organizing is higher than the friction of forgetting. The key insight is: **capture should be as easy as texting, and retrieval should be as easy as searching**.

## Skills You Need

- Telegram, iMessage, or Discord integration (for text-based capture)
- Next.js (OpenClaw builds this for you — no coding needed)

## How to Set It Up

1. Make sure your OpenClaw is connected to your preferred messaging platform (Telegram, Discord, etc.).

2. Start using it immediately — just text your bot anything you want to remember:
```text
Hey, remind me to read "Designing Data-Intensive Applications"
Save this link: https://example.com/interesting-article
Remember: John recommended the restaurant on 5th street
```

3. Build the searchable UI by prompting OpenClaw:
```text
I want to build a second brain system where I can review all our notes,
conversations, and memories. Please build that out with Next.js.

Include:
- A searchable list of all memories and conversations
- Global search (Cmd+K) across everything
- Ability to filter by date and type
- Clean, minimal UI
```

4. OpenClaw will build and deploy the entire Next.js app for you. Navigate to the URL it provides and you have your second brain dashboard.

5. From now on, whenever you think of something — on the road, in a meeting, before bed — just text your bot. Come back to the dashboard whenever you need to find something.

## Key Insights

- The power is in the **zero-friction capture**. You don't need to open an app, pick a folder, or add tags. Just text.
- OpenClaw's memory system is cumulative — it remembers *everything* you've ever told it, making it more powerful over time.
- You can text your bot from your phone and it builds things on your computer. The interface is the conversation.

## Based On

Inspired by [Alex Finn's video on life-changing OpenClaw use cases](https://www.youtube.com/watch?v=41_TNGDDnfQ).

## Related Links

- [OpenClaw Memory System](https://github.com/openclaw/openclaw)
- [Building a Second Br

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
second-brain/
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
mkdir -p second-brain && cd second-brain
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

根據 第二大腦 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Second Brain"""
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
"""Main orchestrator for Second Brain"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 第二大腦 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 第二大腦 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/second-brain.log 2>&1
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
