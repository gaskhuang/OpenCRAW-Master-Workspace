---
name: 廣告創意 AB 測試 (Ad Creative AB Testing)/python
description: "Use Case #068 Python 方案: 廣告創意 A/B 測試。使用 Python 實作 Ad Creative A/B Testing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #068: 廣告創意 A/B 測試 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 🎨 Design Feedback Assistant

> Get instant UI/UX reviews without waiting for stakeholders. Ship better designs, faster.

---

## The Problem

Designers often work in isolation—you finish a design, share it, and wait days for feedback. When feedback comes, it's scattered across Slack, email, and Figma comments. Accessibility issues get caught in QA (too late). Design systems grow inconsistent because documentation is tedious.

---

## The Solution

OpenClaw provides instant, structured design feedback: reviews UI screenshots for usability issues, audits accessibility compliance, compares against your design system, and helps document components. Get a fresh perspective anytime, not just during review meetings.

---

## Setup Guide

### Step 1: Install Design Skills

```bash
openclaw skill install browser     # Screenshot and visual analysis
openclaw skill install web-fetch   # Reference design patterns
openclaw skill install image       # Image analysis capabilities
```

### Step 2: Create Design Workspace

```bash
mkdir -p ~/openclaw/design/{reviews,components,accessibility}
```

Create `~/openclaw/design/design-system.md`:

```markdown
# Design System Reference

## Colors
- Primary: #2563EB (Blue 600)
- Secondary: #7C3AED (Violet 600)
- Success: #059669 (Green 600)
- Warning: #D97706 (Amber 600)
- Error: #DC2626 (Red 600)

## Typography
- Headings: Inter, semi-bold
- Body: Inter, regular, 16px base
- Line height: 1.5 for body text

## Spacing
- Base unit: 4px
- Common: 8, 16, 24, 32, 48px

## Components
- Buttons: rounded-lg, min-height 44px
- Cards: rounded-xl, shadow-sm
- Inputs: border-gray-300, focus:ring-2
```

### Step 3: Set Up Review Checklist

Create `~/openclaw/design/review-checklist.md`:

```markdown
# UI/UX Review Checklist

## Usability
- [ ] Clear visual hierarchy
- [ ] Obvious primary action
- [ ] Consistent alignment
- [ ] Adequate white space
- [ ] Readable text contrast

## Accessibility
- [ ] Color contrast ≥ 4.5:1 (text)
- [ ] Touch targets ≥ 44x44px
- [ ] Focus states visible
- [ ] Alt text for images
- [ ] Screen reader friendly

## Consistency
- [ ] Matches design system colors
- [ ] Correct typography scale
- [ ] Standard component patterns
- [ ] Consistent iconography
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `browser` | Capture screenshots, inspect live sites |
| `image` | Analyze design screenshots |
| `web-fetch` | Pull design pattern references |
| `figma-api` | Connect to Figma files (optional) |

---

## Example Prompts

**UI review:**
```
Review this screenshot of my dashboard design. Check for visual hierarchy, alignment issues, and usability problems. Be specific about what to fix.
[attach screenshot]
```

**Accessibility audit:**
```
Audit this design for WCAG 2.1 AA compliance. Check color contrast, touch targets, and focus states. List all issues with severity ratings.
[attach screenshot]
```

**Design system check:**
```
Compare this component against my design system in ~/open

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
ad-creative-a/b-testing/
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
mkdir -p ad-creative-a/b-testing && cd ad-creative-a/b-testing
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

根據 廣告創意 A/B 測試 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Ad Creative A/B Testing"""
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
"""Main orchestrator for Ad Creative A/B Testing"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 廣告創意 A/B 測試 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 廣告創意 A/B 測試 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/ad-creative-a/b-testing.log 2>&1
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
