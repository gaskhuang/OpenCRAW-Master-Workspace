---
name: YouTube 內容產線 (YouTube Content Pipeline)/python
description: "Use Case #011 Python 方案: YouTube 內容產線。使用 Python 實作 YouTube Content Pipeline 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #011: YouTube 內容產線 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# YouTube Content Pipeline

As a daily YouTube creator, finding fresh, timely video ideas across the web and X/Twitter is time-consuming. Tracking what you've already covered prevents duplicates and helps you stay ahead of trends.

This workflow automates the entire content scouting and research pipeline:

• Hourly cron job scans breaking AI news (web + X/Twitter) and pitches video ideas to Telegram
• Maintains a 90-day video catalog with view counts and topic analysis to avoid re-covering topics
• Stores all pitches in a SQLite database with vector embeddings for semantic dedup (so you never get pitched the same idea twice)
• When you share a link in Slack, OpenClaw researches the topic, searches X for related posts, queries your knowledge base, and creates an Asana card with a full outline

## Skills you Need

- `web_search` (built-in)
- [x-research-v2](https://clawhub.ai) or custom X/Twitter search skill
- [knowledge-base](https://clawhub.ai) skill for RAG
- Asana integration (or Todoist)
- `gog` CLI for YouTube Analytics
- Telegram topic for receiving pitches

## How to Set it Up

1. Set up a Telegram topic for video ideas and configure it in OpenClaw.
2. Install the knowledge-base skill and x-research skill.
3. Create a SQLite database for pitch tracking:
```sql
CREATE TABLE pitches (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  topic TEXT,
  embedding BLOB,
  sources TEXT
);
```
4. Prompt OpenClaw:
```text
Run an hourly cron job to:
1. Search web and X/Twitter for breaking AI news
2. Check against my 90-day YouTube catalog (fetch from YouTube Analytics via gog)
3. Check semantic similarity against all past pitches in the database
4. If novel, pitch the idea to my Telegram "video ideas" topic with sources

Also: when I share a link in Slack #ai_trends, automatically:
1. Research the topic
2. Search X for related posts
3. Query my knowledge base
4. Create an Asana card in Video Pipeline with a full outline
```


---

# YouTube 分析数据拉取

## 简介

每日自动拉取 YouTube 分析数据，生成报告，追踪视频表现和频道增长。

**为什么重要**：了解内容表现，优化创作策略，追踪增长趋势。

**真实例子**：一位 YouTuber 使用此代理每日获取分析数据，代理生成趋势报告，帮助他识别最受欢迎的内容类型。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `youtube_api` | [ClawdHub](https://clawhub.com/skills/youtube) | 获取数据 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送报告 |

---

## 使用方式

### 每日拉取
定时拉取 YouTube 分析数据

### 生成报告
- 观看次数
- 订阅增长
- 收入统计
- 热门视频

### 趋势分析
分析数据趋势，提供优化建议

---

## 来源

- 来源：Stack Junkie


---

# 🎬 Video Content Pipeline

> From idea to upload-ready. Script, optimize, dominate the algorithm.

---

## The Problem

YouTube success requires more than good videos—it demands optimized titles, thumbnails that pop, SEO-rich descriptions, strategic tags, and engaging scripts. Creators spend hours on metadata that could go into content. Most never nail the algorithm because they're guessing, not analyzing.

---

## The Solution

OpenClaw handles the YouTube grind: 

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
youtube-content-pipeline/
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
mkdir -p youtube-content-pipeline && cd youtube-content-pipeline
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

根據 YouTube 內容產線 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for YouTube Content Pipeline"""
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
"""Main orchestrator for YouTube Content Pipeline"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== YouTube 內容產線 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 YouTube 內容產線 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/youtube-content-pipeline.log 2>&1
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
