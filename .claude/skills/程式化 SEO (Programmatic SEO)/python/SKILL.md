---
name: 程式化 SEO (Programmatic SEO)/python
description: "Use Case #058 Python 方案: 程式化 SEO。使用 Python 實作 Programmatic SEO 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #058: 程式化 SEO — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 🔍 SEO Content Pipeline

> Rank higher with less effort. Data-driven content that Google loves.

---

## The Problem

Creating SEO content is time-consuming: keyword research, competitor analysis, outline creation, writing, optimization. Most content either ignores SEO (no traffic) or over-optimizes (robotic reading). Finding the balance takes expertise and hours.

---

## The Solution

OpenClaw handles the entire SEO content workflow: finds keyword opportunities, analyzes what's ranking, creates optimized outlines, and helps you write content that ranks AND reads well.

---

## Setup Guide

### Step 1: Install SEO Skills

```bash
openclaw skill install gsc  # Google Search Console
openclaw skill install brave-search
openclaw skill install web-fetch
```

### Step 2: Configure Your Site

Create `~/openclaw/seo/site-config.json`:

```json
{
  "domain": "yourdomain.com",
  "gscPropertyId": "sc-domain:yourdomain.com",
  "targetKeywords": ["main topic", "secondary topic"],
  "competitors": ["competitor1.com", "competitor2.com"],
  "contentGoals": {
    "monthlyPosts": 8,
    "targetWordCount": "1500-2500"
  }
}
```

### Step 3: Create Content Brief Template

Create `~/openclaw/seo/brief-template.md`:

```markdown
# Content Brief: {keyword}

## Keyword Data
- Search volume:
- Difficulty:
- Current ranking:

## Top 5 Ranking Pages
1. [URL] - Word count, key points
2. ...

## Content Gaps
- Topics competitors miss:
- Questions not answered:

## Recommended Outline
1. H2:
   - H3:
2. ...

## Optimization Checklist
- [ ] Keyword in title
- [ ] Keyword in first 100 words
- [ ] Related keywords included
- [ ] Internal links
- [ ] External authoritative links
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `gsc` | Google Search Console data |
| `brave-search` | SERP analysis |
| `web-fetch` | Competitor content analysis |

---

## Example Prompts

**Keyword research:**
```
Find 10 keyword opportunities for [topic]. Look for low competition, decent volume, and topics I can write authoritatively about.
```

**Content brief:**
```
Create a content brief for the keyword "[keyword]". Analyze top 5 ranking pages and find gaps I can fill.
```

**Outline review:**
```
Here's my outline for [topic]. Is it comprehensive enough to outrank the current top results?
```

**Post-publish optimization:**
```
My post on [topic] has been live for a month. Check GSC for impressions without clicks - what queries should I better optimize for?
```

---

## Cron Schedule

```
0 8 * * 1      # Monday 8 AM - weekly content planning
0 9 * * *      # Daily - check GSC for quick wins
0 10 * * 5     # Friday - performance review
```

---

## Expected Results

**Month 1:**
- Content calendar with keyword-targeted posts
- 50% reduction in research time per post

**Month 3:**
- New posts ranking within 4-6 weeks
- 30%+ increase in organic traffic

**Month 6:**
- Consistent content production
- Clear ROI from SEO efforts


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
programmatic-seo/
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
mkdir -p programmatic-seo && cd programmatic-seo
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

根據 程式化 SEO 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Programmatic SEO"""
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
"""Main orchestrator for Programmatic SEO"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 程式化 SEO - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 程式化 SEO 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/programmatic-seo.log 2>&1
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
