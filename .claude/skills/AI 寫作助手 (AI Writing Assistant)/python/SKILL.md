---
name: AI 寫作助手 (AI Writing Assistant)/python
description: "Use Case #016 Python 方案: AI 寫作助手。使用 Python 實作 AI Writing Assistant 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #016: AI 寫作助手 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# ✍️ Writing Assistant

> From blank page to published post. Your personal editor that never sleeps.

---

## The Problem

Writing quality blog content is exhausting: research, drafting, editing, SEO optimization, formatting, publishing. Most writers either spend 8+ hours per post or publish half-baked content. The editing loop alone kills momentum—you're too close to your own words to see what's wrong.

---

## The Solution

OpenClaw becomes your writing partner: helps research topics, generates first drafts, edits for clarity and style, optimizes for SEO, and handles the publishing workflow. You provide the ideas and voice; OpenClaw handles the heavy lifting.

---

## Setup Guide

### Step 1: Install Writing Skills

```bash
openclaw skill install gsc           # Google Search Console
openclaw skill install brave-search  # Research & SERP analysis
openclaw skill install web-fetch     # Reference gathering
openclaw skill install ghost         # Blog publishing (if using Ghost)
```

### Step 2: Create Writing Workspace

```bash
mkdir -p ~/openclaw/writing/{drafts,published,research}
```

Create `~/openclaw/writing/style-guide.md`:

```markdown
# My Writing Style Guide

## Voice
- Conversational but authoritative
- Use contractions (it's, you'll, don't)
- Second person ("you") to speak directly to reader

## Structure
- Short paragraphs (3-4 sentences max)
- Use subheadings every 200-300 words
- Include actionable takeaways

## Avoid
- Passive voice
- Jargon without explanation
- Walls of text

## SEO Requirements
- Target keyword in title
- Keyword in first 100 words
- Include 3-5 internal links
```

### Step 3: Set Up Blog Config

Create `~/openclaw/writing/blog-config.json`:

```json
{
  "platform": "ghost",
  "siteUrl": "https://yourblog.com",
  "author": "Your Name",
  "defaultCategory": "Tech",
  "wordCountTarget": "1500-2500",
  "publishDays": ["Tuesday", "Thursday"],
  "seoKeywords": ["main topic", "related topic"]
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `gsc` | Track keyword rankings and opportunities |
| `brave-search` | Research topics and analyze competition |
| `web-fetch` | Pull reference content and citations |
| `ghost` / `wordpress` | Direct blog publishing |
| `grammarly-api` | Grammar and style checking (optional) |

---

## Example Prompts

**Topic research:**
```
I want to write about [topic]. Research the top 10 ranking articles, identify gaps in their coverage, and suggest 5 unique angles I could take.
```

**Draft generation:**
```
Create a first draft for a blog post about [topic]. Target keyword: [keyword]. Follow my style guide in ~/openclaw/writing/style-guide.md. Aim for 1800 words.
```

**Editing pass:**
```
Edit this draft for clarity and flow. Remove fluff, strengthen weak sentences, and ensure it matches my voice. Be ruthless—cut anything that doesn't add value.
```

**SEO optimization:**
```
Optimize this post for SEO. Check keyword density, suggest meta description, add internal lin

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
ai-writing-assistant/
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
mkdir -p ai-writing-assistant && cd ai-writing-assistant
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

根據 AI 寫作助手 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for AI Writing Assistant"""
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
"""Main orchestrator for AI Writing Assistant"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== AI 寫作助手 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 AI 寫作助手 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/ai-writing-assistant.log 2>&1
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
