---
name: 食譜推薦與購物清單 (Recipe & Shopping List)/python
description: "Use Case #026 Python 方案: 食譜推薦與購物清單。使用 Python 實作 Recipe & Shopping List 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #026: 食譜推薦與購物清單 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 食谱推荐与购物清单

## 简介

每天想吃什么是一个永恒的难题。这个使用案例根据你的食材库存、饮食偏好和营养需求，推荐食谱并生成购物清单。

**为什么重要**：简化 meal planning，减少食物浪费，保持饮食健康。

**真实例子**：一位上班族使用此代理规划每周饮食，代理根据冰箱里的食材推荐食谱，生成购物清单，帮他节省了每周 5 小时的 meal planning 时间。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `recipe_api` | [ClawdHub](https://clawhub.com/skills/recipe) | 获取食谱 |
| `nutrition` | [ClawdHub](https://clawhub.com/skills/nutrition) | 营养分析 |
| `shopping` | [ClawdHub](https://clawhub.com/skills/shopping) | 生成清单 |

---

## 设置步骤

### 1. 前置条件

- 饮食偏好（素食、无麸质等）
- 过敏信息
- 厨具清单

### 2. 提示词模板

```markdown
## 食谱推荐与购物清单

你是我的营养顾问。帮我规划每日饮食：

### 推荐逻辑

**考虑因素**
- 现有食材
- 饮食偏好
- 营养平衡
- 烹饪时间
- 难度级别

**每日规划**
- 早餐：简单快捷
- 午餐：营养均衡
- 晚餐：丰富多样
- 零食：健康选择

### 食谱推荐

**输入**
- 可用食材
- 时间限制
- 人数

**输出**
```
🍽️ 今日推荐

🌅 早餐：牛油果吐司
⏱️ 时间：10 分钟
🥗 营养：350 卡，蛋白质 12g
📋 食材：
- 面包 2 片 ✓
- 牛油果 1 个 ✗
- 鸡蛋 1 个 ✓

🍳 步骤：
1. 烤面包
2. 捣牛油果
3. 煎鸡蛋
4. 组合
```

### 购物清单

**自动生成**
- 汇总所需食材
- 检查库存
- 分类整理
- 估算价格

**清单格式**
```
🛒 购物清单

🥬 蔬菜
- 西红柿 500g
- 菠菜 1 把
- 胡萝卜 3 根

🥩 肉类
- 鸡胸肉 500g
- 鸡蛋 12 个

🍚 主食
- 大米 1kg
- 意大利面 500g

💰 预估：$XX.XX
```

### 每周计划
- 生成周菜单
- 批量采购清单
-  meal prep 建议
- 剩菜利用方案
```

### 3. 配置

```
Schedule: 0 18 * * *
Action: 推荐食谱 → 生成清单 → 发送
```

---

## 成功指标

- [ ] 每日食谱推荐符合偏好
- [ ] 购物清单准确完整
- [ ] 食物浪费减少
- [ ] 饮食更加健康

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🛒 Grocery Optimizer

> Meal plan, shop smart, waste less.

---

## The Problem

Grocery shopping without a plan leads to impulse buys, forgotten items, and food waste. Meal planning is tedious. You buy ingredients for recipes you never make.

---

## The Solution

OpenClaw helps plan meals based on what's on sale, generates optimized grocery lists, tracks what you have, and ensures nothing goes to waste.

---

## Setup Guide

### Step 1: Install Shopping Skills

```bash
openclaw skill install bring-shopping
openclaw skill install recipe-to-list
openclaw skill install gurkerl  # or picnic, instacart
```

### Step 2: Configure Preferences

Create `~/openclaw/grocery/preferences.json`:

```json
{
  "dietaryRestrictions": [],
  "householdSize": 2,
  "cookingDays": ["Monday", "Wednesday", "Friday", "Sunday"],
  "budgetWeekly": 150,
  "stores": ["preferred store"]
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `bring-shopping` | Shopping list management |
| `recipe-to-list` | Recipe ingredient extraction |
| `gurkerl`/`picnic` | Online grocery ordering |

---

## Example Prompts

**Weekly planning:**
```
Plan meals for this week. Keep it under $150, use what's in season, and minimize waste.
```

**Recipe to list:**
```
I want to make [recipe]. Add ingredients to my shopping list, minus what I already have.
```

**What's for dinner:**
```
What can I make with chicken, rice, and the vegetables expiring soon?
```

---

## Cron Schedule

```
0 9 * * 0      # Sunday 9 AM - weekly meal planning
0 10 * * 3     # Wednesday - mid-week list check
```

---

## Expected Results

- 20% reduction in grocery spending
- Less food waste
- No more "what's for dinner?" 

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
recipe-&-shopping-list/
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
mkdir -p recipe-&-shopping-list && cd recipe-&-shopping-list
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

根據 食譜推薦與購物清單 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Recipe & Shopping List"""
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
"""Main orchestrator for Recipe & Shopping List"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 食譜推薦與購物清單 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 食譜推薦與購物清單 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/recipe-&-shopping-list.log 2>&1
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
