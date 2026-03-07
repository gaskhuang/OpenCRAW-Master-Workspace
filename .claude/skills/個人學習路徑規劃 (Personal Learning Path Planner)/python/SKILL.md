---
name: 個人學習路徑規劃 (Personal Learning Path Planner)/python
description: "Use Case #111 Python 方案: 個人學習路徑規劃。使用 Python 實作 Personal Learning Path Planner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #111: 個人學習路徑規劃 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 📚 Learning Path Creator

> Learn anything systematically. No more random YouTube binges.

---

## The Problem

Self-directed learning is chaotic. You want to learn [skill] but don't know where to start, what order to learn things, or when you've "finished." Most people bounce between resources without a plan.

---

## The Solution

OpenClaw creates personalized curricula: assesses your starting point, finds the best resources, creates a structured path, tracks progress, and adjusts when you struggle or excel.

---

## Setup Guide

### Step 1: Install Learning Skills

```bash
openclaw skill install context7
openclaw skill install literature-review
openclaw skill install youtube-summarizer
```

### Step 2: Define Learning Goals

Create `~/openclaw/learning/goals.json`:

```json
{
  "currentGoal": {
    "topic": "Machine Learning",
    "level": "beginner",
    "timeCommitment": "5 hours/week",
    "deadline": "3 months",
    "learningStyle": "video + hands-on projects"
  },
  "preferences": {
    "freeResourcesPreferred": true,
    "languages": ["English"],
    "formats": ["video", "interactive", "book"]
  }
}
```

### Step 3: Create Progress Tracker

Create `~/openclaw/learning/progress.md`:

```markdown
# Learning Progress

## Current: Machine Learning Fundamentals

### Completed
- [x] Module 1: Linear algebra basics
- [x] Module 2: Statistics refresher

### In Progress
- [ ] Module 3: Python for ML (60%)

### Up Next
- [ ] Module 4: Supervised learning

### Notes
- Struggling with: gradient descent intuition
- Should review: matrix multiplication
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `context7` | Library documentation |
| `literature-review` | Academic resources |
| `youtube-summarizer` | Video content |
| `brave-search` | Resource discovery |

---

## Example Prompts

**Create curriculum:**
```
I want to learn [topic] from scratch. I can commit 5 hours per week for 3 months. Create a learning path with the best free resources.
```

**Daily practice:**
```
I have 45 minutes to study. What should I work on today based on my learning plan?
```

**Stuck on concept:**
```
I don't understand [concept]. Explain it differently and find additional resources that explain it well.
```

**Progress check:**
```
Review my learning progress. Am I on track? What should I adjust?
```

---

## Cron Schedule

```
0 7 * * *      # 7 AM - daily learning reminder
0 20 * * 0     # 8 PM Sunday - weekly progress review
0 10 1 * *     # 1st of month - curriculum adjustment
```

---

## Expected Results

**Week 1:**
- Clear learning path created
- Know exactly what to study

**Month 1:**
- Steady progress visible
- Concepts building on each other
- No more resource paralysis

**Month 3:**
- Measurable skill acquisition
- Portfolio of completed projects
- Ready for next learning goal


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
personal-learning-path-planner/
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
mkdir -p personal-learning-path-planner && cd personal-learning-path-planner
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

根據 個人學習路徑規劃 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Personal Learning Path Planner"""
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
"""Main orchestrator for Personal Learning Path Planner"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 個人學習路徑規劃 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 個人學習路徑規劃 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/personal-learning-path-planner.log 2>&1
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
