---
name: 投資組合監控 (Portfolio Monitor)/python
description: "Use Case #104 Python 方案: 投資組合監控。使用 Python 實作 Portfolio Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #104: 投資組合監控 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# 投资组合监控

## 简介

自动监控被投公司的关键指标、新闻动态、里程碑事件，生成投资组合报告。

**为什么重要**：及时了解被投公司状况，主动提供支持，优化投后管理。

**真实例子**：一家 VC 使用此代理监控 30+ 被投公司，代理自动收集指标和新闻，每周生成投资组合健康报告。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |
| `news` | [ClawdHub](https://clawhub.com/skills/news) | 新闻监控 |
| `reporting` | [ClawdHub](https://clawhub.com/skills/reporting) | 报告生成 |

---

## 使用方式

### 数据收集
- 财务指标
- 用户增长
- 新闻动态
- 社交媒体

### 异常检测
识别需要关注的变化

### 生成报告
投资组合健康度评估

---

## 来源

- 来源：Data Driven VC


---

# 📈 Stock Portfolio Tracker

> Stay informed on your investments. Without checking every hour.

---

## The Problem

Portfolio tracking apps show prices but miss context. What earnings are coming? What news affects your holdings? Most investors either check obsessively (stress) or ignore completely (risk).

---

## The Solution

OpenClaw monitors your portfolio with context: tracks prices, alerts on significant moves, summarizes relevant news, and reminds you of earnings dates. Informed without obsessed.

---

## Setup Guide

### Step 1: Install Finance Skills

```bash
openclaw skill install stock-analysis
openclaw skill install yahoo-finance
openclaw skill install portfolio-watcher
```

### Step 2: Enter Your Holdings

Create `~/openclaw/portfolio/holdings.json`:

```json
{
  "holdings": [
    {
      "symbol": "AAPL",
      "shares": 50,
      "costBasis": 145.00
    },
    {
      "symbol": "GOOGL",
      "shares": 20,
      "costBasis": 125.00
    },
    {
      "symbol": "VTI",
      "shares": 100,
      "costBasis": 220.00
    }
  ],
  "watchlist": ["MSFT", "AMZN", "NVDA"]
}
```

### Step 3: Set Alert Thresholds

Create `~/openclaw/portfolio/alerts.md`:

```markdown
# Portfolio Alerts

## Price Alerts
- Position up/down > 5% in a day
- Hit target price (set per stock)
- 52-week high/low

## News Alerts
- Earnings announcement
- Major news (M&A, leadership, product)
- Analyst rating changes

## Regular Updates
- Daily: Portfolio summary
- Weekly: Performance review
- Quarterly: Rebalancing check
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `stock-analysis` | Stock analysis and metrics |
| `yahoo-finance` | Price and fundamental data |
| `portfolio-watcher` | Portfolio tracking |

---

## Example Prompts

**Morning briefing:**
```
How's my portfolio doing? Any pre-market movers? What earnings are coming this week?
```

**Deep dive:**
```
Analyze AAPL. How's it valued vs peers? What are analysts saying? Any concerns?
```

**Rebalancing:**
```
My tech allocation is 60% of portfolio now. Suggest trades to get back to my 40% target.
```

**Tax planning:**
```
Which positions have losses I could harvest? What's my overall tax situation this year?
```

---

## Cron Schedule

```
0 6 * * 1-5    # 6 AM weekdays - pre-market briefing
0 16 * * 1-5   # 4 PM weekdays - market close summary
0 9 * * 0      # Sunday 9 AM - weekly performance review
0 0 1 */3 *    # Quarterly - rebalancing check
`

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
portfolio-monitor/
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
mkdir -p portfolio-monitor && cd portfolio-monitor
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

根據 投資組合監控 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Portfolio Monitor"""
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
"""Main orchestrator for Portfolio Monitor"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 投資組合監控 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 投資組合監控 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/portfolio-monitor.log 2>&1
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
