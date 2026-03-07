---
name: 一文多平台內容複製 (Cross-Platform Content Repurposing)/python
description: "Use Case #017 Python 方案: 一文多平台內容複製。使用 Python 實作 Cross-Platform Content Repurposing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #017: 一文多平台內容複製 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# Content Multiplication Engine

> Turn one piece of content into 10+ platform-specific posts automatically.

## The Problem

Creating content for one platform is hard enough—repurposing it for Twitter, LinkedIn, Instagram, newsletters, and Reddit is a time sink that kills consistency. Most creators either post the same thing everywhere (which performs poorly) or spend hours manually reformatting, losing momentum and burning out. The result? Great content stuck on one platform while your audience waits elsewhere.

## The Solution

OpenClaw acts as your always-on content repurposing assistant. Drop a blog post URL, paste a video transcript, or share podcast notes—OpenClaw transforms it into platform-native content for every channel you care about. It understands each platform's style: Twitter threads with hooks, LinkedIn thought-leadership angles, Instagram carousel concepts, punchy newsletter snippets, and Reddit-appropriate discussion starters. Set it up once, and your content multiplies while you sleep.

## Setup Guide

### Step 1: Create Your Content Workspace (2 minutes)

```bash
mkdir -p ~/content-engine/{input,output,templates}
```

Create a simple input structure in `~/content-engine/input/`:
- Drop source files here (`.md`, `.txt`, or just URLs)

### Step 2: Create Platform Templates (5 minutes)

Create `~/content-engine/templates/platforms.md`:

```markdown
# Platform Guidelines

## Twitter/X Thread
- Hook in first tweet (curiosity gap or bold statement)
- 5-10 tweets max, each standalone valuable
- End with CTA or callback to first tweet
- Use line breaks for readability
- No hashtags in thread, maybe 1-2 at end

## LinkedIn Post
- First line is the hook (before "see more")
- Personal angle or story lead-in
- Insights with white space between points
- End with question to drive comments
- 1300-1500 chars ideal
- 3-5 relevant hashtags at bottom

## Instagram Caption
- Hook in first line (emoji optional)
- Story or value in 2-3 short paragraphs  
- CTA: save, share, comment prompt
- Hashtags: 20-30 relevant ones in first comment (provide separately)
- Carousel slide concepts if applicable

## Newsletter Snippet
- TL;DR in 2-3 sentences
- Key insight or quote pullout
- "Read more" hook with link placeholder
- Keep under 150 words

## Reddit Post
- Title: Question or discussion-starter format
- No self-promotion tone
- Add genuine value first
- Mention source naturally at end
- Adapt to subreddit culture (specify which sub)
```

### Step 3: Add to TOOLS.md (1 minute)

Add this to your `~/openclaw/TOOLS.md`:

```markdown
### Content Engine
- Input folder: ~/content-engine/input/
- Output folder: ~/content-engine/output/
- Templates: ~/content-engine/templates/platforms.md
- Default platforms: Twitter, LinkedIn, Newsletter
```

### Step 4: Configure HEARTBEAT.md (2 minutes)

Add this section to your `~/openclaw/HEARTBEAT.md`:

```markdown
### Content Multiplication Check
- [ ] Check ~/content-engine/input/ for new files
- [ ] If found: Proces

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
cross-platform-content-repurposing/
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
mkdir -p cross-platform-content-repurposing && cd cross-platform-content-repurposing
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

根據 一文多平台內容複製 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Cross-Platform Content Repurposing"""
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
"""Main orchestrator for Cross-Platform Content Repurposing"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 一文多平台內容複製 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 一文多平台內容複製 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/cross-platform-content-repurposing.log 2>&1
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
