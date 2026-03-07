---
name: 旅遊行程規劃 (Travel Itinerary Planner)/python
description: "Use Case #020 Python 方案: 旅遊行程規劃。使用 Python 實作 Travel Itinerary Planner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #020: 旅遊行程規劃 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 旅行行程规划师

## 简介

规划旅行需要考虑目的地、交通、住宿、景点、预算等众多因素。这个使用案例根据你的偏好和预算，智能规划完整行程，预订服务，并生成详细的旅行指南。

**为什么重要**：节省规划时间，优化旅行体验，确保不遗漏重要景点。

**真实例子**：一对夫妇使用此代理规划日本 10 日游，代理根据他们的兴趣（美食、文化、自然）规划了详细行程，预订了餐厅和交通，使他们的旅行完美无缺。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `travel_api` | [ClawdHub](https://clawhub.com/skills/travel) | 获取旅行信息 |
| `booking` | [ClawdHub](https://clawhub.com/skills/booking) | 预订服务 |
| `maps` | [ClawdHub](https://clawhub.com/skills/maps) | 路线规划 |
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 天气信息 |

---

## 设置步骤

### 1. 前置条件

- 目的地和日期
- 预算范围
- 兴趣偏好
- 旅行人数

### 2. 提示词模板

```markdown
## 旅行行程规划师

你是我的旅行顾问。帮我规划完美的旅行：

### 信息收集

**基本信息**
- 目的地：[城市/国家]
- 日期：YYYY-MM-DD 到 YYYY-MM-DD
- 人数：X 人
- 预算：$XXXX

**偏好设置**
- 旅行风格：休闲/紧凑/冒险
- 兴趣：文化/美食/自然/购物
- 住宿偏好：酒店/民宿/青旅
- 交通偏好：公共交通/租车/打车

### 规划内容

**1. 交通安排**
- 往返机票/火车
- 当地交通（地铁、公交、租车）
- 机场接送

**2. 住宿预订**
- 根据位置选择
- 考虑预算和偏好
- 查看评价和设施

**3. 景点规划**
- 必去景点
- 每日路线优化
- 门票预订
- 开放时间检查

**4. 餐饮推荐**
- 当地特色美食
- 预订热门餐厅
- 备选方案

**5. 活动安排**
- 文化体验
- 户外活动
- 购物时间
- 自由活动

### 行程输出
```
🗾 [目的地] 行程 - X 日游

📅 Day 1 - 抵达日
🕐 上午
- 抵达机场
- 前往酒店
- 办理入住

🕐 下午
- 市区漫步
- [景点 1]

🕐 晚上
- 晚餐 @[餐厅名]
- 早点休息

📅 Day 2 - 文化探索
...

💰 预算明细
- 交通：$XXX
- 住宿：$XXX
- 餐饮：$XXX
- 门票：$XXX
- 其他：$XXX
总计：$XXXX

📋 打包清单
- [物品列表]

📱 实用信息
- 紧急电话
- 大使馆信息
- 常用 App
```

### 实时调整
- 根据天气调整行程
- 处理突发情况
- 推荐替代方案
- 更新预订信息
```

### 3. 配置

```
Trigger: 用户请求
Action: 收集偏好 → 搜索选项 → 规划行程 → 生成指南
```

---

## 成功指标

- [ ] 行程符合偏好和预算
- [ ] 预订成功率 100%
- [ ] 旅行满意度高
- [ ] 无遗漏重要景点

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# ✈️ Smart Travel Planner

> Plan trips in minutes, not hours. Get personalized itineraries that actually work.

---

## The Problem

Planning a trip means juggling 10 browser tabs: flights, hotels, activities, restaurants, transport. You spend hours comparing options and still worry you missed the best deals or made suboptimal choices. Last-minute changes throw everything off.

---

## The Solution

OpenClaw handles the entire trip planning process: finds flights, suggests accommodations matching your preferences, builds day-by-day itineraries, and adapts when plans change. All in one conversation.

---

## Setup Guide

### Step 1: Install Travel Skills

```bash
openclaw skill install flights
openclaw skill install flight-tracker
openclaw skill install weather
openclaw skill install spots  # For local recommendations
```

### Step 2: Set Your Preferences

Create `~/openclaw/travel/preferences.md`:

```markdown
# My Travel Preferences

## Flights
- Preferred airlines: [list]
- Seat preference: Window/Aisle
- Max layover: 3 hours
- Budget range: Economy, willing to upgrade for long hauls

## Accommodation
- Style: Boutique hotels > big chains
- Must have: WiFi, workspace, AC
- Nice to have: Gym, breakfast included
- Avoid: Hostels, shared bathrooms

## Activities
- Love: Local food, walking tours, museums, nature
- Avoid: Tourist traps, shopping malls
- Pace: Moderate (not exhausting)
- Morning person: Yes

## Food
- Dietary: None


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
travel-itinerary-planner/
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
mkdir -p travel-itinerary-planner && cd travel-itinerary-planner
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

根據 旅遊行程規劃 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Travel Itinerary Planner"""
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
"""Main orchestrator for Travel Itinerary Planner"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 旅遊行程規劃 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 旅遊行程規劃 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/travel-itinerary-planner.log 2>&1
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
