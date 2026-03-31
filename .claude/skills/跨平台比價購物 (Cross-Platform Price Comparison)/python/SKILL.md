---
name: 跨平台比價購物 (Cross-Platform Price Comparison)/python
description: "Use Case #021 Python 方案: 跨平台比價購物。使用 Python 實作 Cross-Platform Price Comparison 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #021: 跨平台比價購物 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 价格比较购物助手

## 简介

想买的商品在不同平台价格不同？这个使用案例自动追踪你关注的商品价格，比较多个平台，在价格下降时通知你，并预测最佳购买时机。

**为什么重要**：省钱，确保买到最优价格，避免错过促销。

**真实例子**：一位用户想购买一台相机，代理追踪了 5 个平台的价格，在 Prime Day 时通知他最低价格，帮他节省了 300 美元。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `web_scraping` | [ClawdHub](https://clawhub.com/skills/scraping) | 抓取价格 |
| `price_api` | [ClawdHub](https://clawhub.com/skills/price) | 获取价格 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送通知 |

---

## 设置步骤

### 1. 前置条件

- 购物清单
- 目标价格（可选）
- 通知渠道

### 2. 提示词模板

```markdown
## 价格比较购物助手

你是我的购物助手。追踪价格并推荐最佳购买时机：

### 功能

**价格追踪**
- 监控多个电商平台
- 记录历史价格
- 识别价格趋势
- 检测促销活动

**价格比较**
- 比较同款商品不同平台
- 考虑运费和税费
- 计算总成本
- 推荐最佳选项

**智能提醒**
- 价格达到目标时通知
- 促销活动开始时通知
- 价格异常下降时通知
- 库存紧张时通知

**购买建议**
- 预测价格趋势
- 建议等待或立即购买
- 估算最佳购买时间
- 提供替代选项

### 通知格式
```
💰 价格提醒

📦 商品：[名称]
💵 当前价格：$XX.XX
📉 历史最低：$XX.XX
📊 价格趋势：下降/上升/稳定

🏪 各平台价格：
- 平台 A：$XX.XX
- 平台 B：$XX.XX
- 平台 C：$XX.XX

💡 建议：[等待/立即购买]
理由：[原因]
```

### 价格历史
```
📈 价格历史 - [商品名]

30 天趋势：📉
平均价格：$XX.XX
最低价格：$XX.XX (日期)
最高价格：$XX.XX (日期)

预测：未来 7 天可能 [上涨/下降/稳定]
```
```

### 3. 配置

```
Schedule: */6 * * * *
Action: 检查价格 → 分析 → 发送通知
```

---

## 成功指标

- [ ] 价格监控覆盖目标商品
- [ ] 及时收到降价通知
- [ ] 平均节省 > 15%
- [ ] 不错过重要促销

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 💰 Price Drop Alerter

> Never pay full price again. Get alerted the moment prices drop.

---

## The Problem

You want to buy something but it's too expensive. You check periodically, forget, then buy at full price right before a sale. Or you set alerts that spam you with 1% changes. Neither works.

---

## The Solution

OpenClaw monitors products across multiple retailers, tracks price history, predicts good buying times, and alerts you only when prices hit YOUR target or drop significantly.

---

## Setup Guide

### Step 1: Install Shopping Skills

```bash
openclaw skill install camelcamelcamel-alerts  # Amazon price tracking
openclaw skill install marktplaats  # Dutch marketplace
openclaw skill install whcli  # Austrian Willhaben
```

### Step 2: Create Watchlist

Create `~/openclaw/shopping/watchlist.json`:

```json
{
  "items": [
    {
      "name": "Sony WH-1000XM5",
      "url": "https://amazon.com/dp/...",
      "targetPrice": 280,
      "currentPrice": 350,
      "addedDate": "2026-01-15",
      "priority": "high"
    },
    {
      "name": "Standing Desk",
      "url": "https://...",
      "targetPrice": 400,
      "currentPrice": 599,
      "addedDate": "2026-01-20",
      "priority": "medium"
    }
  ],
  "priceHistory": {}
}
```

### Step 3: Set Alert Preferences

Create `~/openclaw/shopping/preferences.md`:

```markdown
# Alert Preferences

## Notify me when:
- Price drops below my target
- Price drops 20%+ from recent high
- Lowest price in 30 days
- Lightning deals on watchlist items

## Don't notify for:
- Price changes < 5%
- Items I marked "not urgent"
- Out of stock alerts

## Check frequency:
- High priority: Every 2 hours
- Medium priority: Every 6 hours
- Low priority: Daily
```

---

#

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
cross-platform-price-comparison/
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
mkdir -p cross-platform-price-comparison && cd cross-platform-price-comparison
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

根據 跨平台比價購物 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Cross-Platform Price Comparison"""
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
"""Main orchestrator for Cross-Platform Price Comparison"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 跨平台比價購物 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 跨平台比價購物 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/cross-platform-price-comparison.log 2>&1
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
