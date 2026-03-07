---
name: 睡眠品質優化 (Sleep Quality Optimizer)/python
description: "Use Case #108 Python 方案: 睡眠品質優化。使用 Python 實作 Sleep Quality Optimizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #108: 睡眠品質優化 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 😴 Sleep Optimizer

> Wake up refreshed. Optimize your nights to own your days.

---

## The Problem

Poor sleep destroys everything—focus, mood, health. You track with Whoop or Oura but never act on the data. Bedtime routines are inconsistent. You know you should sleep better but don't know what's actually hurting your sleep.

---

## The Solution

OpenClaw connects to your sleep trackers, identifies what's tanking your sleep score, enforces your wind-down routine, and adapts recommendations based on what actually works for *you*.

---

## Setup Guide

### Step 1: Install Sleep & Recovery Skills

```bash
openclaw skill install whoop
openclaw skill install oura-ring  # alternative tracker
openclaw skill install calendar
openclaw skill install remind-me
```

### Step 2: Configure Sleep Profile

Create `~/openclaw/sleep/profile.json`:

```json
{
  "targetBedtime": "22:30",
  "targetWakeTime": "06:30",
  "minSleepHours": 7.5,
  "idealSleepScore": 85,
  "tracker": "whoop",
  "windDownMinutes": 60,
  "factors": {
    "caffeineCutoff": "14:00",
    "alcoholEffect": true,
    "exerciseEffect": true,
    "screensCutoff": "21:30"
  }
}
```

### Step 3: Define Wind-Down Routine

Create `~/openclaw/sleep/routine.md`:

```markdown
# Wind-Down Routine (60 min before bed)

## T-60 minutes
- [ ] Put away work
- [ ] Dim lights
- [ ] Start winding down

## T-30 minutes
- [ ] No more screens
- [ ] Prepare for tomorrow
- [ ] Light reading or journaling

## T-10 minutes
- [ ] Bedroom
- [ ] Breathing exercises
- [ ] Sleep mask on

## Disruptors to Track
- Late caffeine
- Alcohol
- Heavy meals after 8 PM
- Intense exercise after 7 PM
- Stressful conversations
- Blue light exposure
```

### Step 4: Create Sleep Log

Create `~/openclaw/sleep/log.json`:

```json
{
  "entries": [],
  "weeklyAverage": null,
  "trends": {
    "improving": false,
    "disruptors": [],
    "helpers": []
  }
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `whoop` | Recovery/strain/sleep data |
| `oura-ring` | Sleep stage tracking |
| `calendar` | Schedule awareness |
| `remind-me` | Bedtime reminders |
| `timer` | Wind-down routine timing |

---

## Example Prompts

**Morning check-in:**
```
How did I sleep last night? What does Whoop say about my recovery?
```

**Analyze patterns:**
```
Look at my sleep data for the past 2 weeks. What's helping and what's hurting my sleep quality?
```

**Start wind-down:**
```
Start my wind-down routine. What's my target bedtime tonight?
```

**Track disruptor:**
```
Log that I had coffee at 4 PM today. Flag it for sleep correlation.
```

**Optimize schedule:**
```
I have an important meeting at 9 AM tomorrow. What time should I go to bed to be at peak recovery?
```

**Weekly review:**
```
Give me my sleep report for this week. Am I trending better or worse?
```

---

## Cron Schedule

```
0 21 * * *     # 9 PM - wind-down reminder
30 22 * * *    # 10:30 PM - final bedtime warning
0 7 * * *      # 7 AM - sleep quality report
0 9 * * 0

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
sleep-quality-optimizer/
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
mkdir -p sleep-quality-optimizer && cd sleep-quality-optimizer
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

根據 睡眠品質優化 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Sleep Quality Optimizer"""
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
"""Main orchestrator for Sleep Quality Optimizer"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 睡眠品質優化 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 睡眠品質優化 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/sleep-quality-optimizer.log 2>&1
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
