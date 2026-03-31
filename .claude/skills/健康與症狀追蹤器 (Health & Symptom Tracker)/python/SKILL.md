---
name: 健康與症狀追蹤器 (Health & Symptom Tracker)/python
description: "Use Case #034 Python 方案: 健康與症狀追蹤器。使用 Python 實作 Health & Symptom Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #034: 健康與症狀追蹤器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Health & Symptom Tracker

Identifying food sensitivities requires consistent logging over time, which is tedious to maintain. You need reminders to log and analysis to spot patterns.

This workflow tracks food and symptoms automatically:

• Message your food and symptoms in a dedicated Telegram topic and OpenClaw logs everything with timestamps
• 3x daily reminders (morning, midday, evening) prompt you to log meals
• Over time, analyzes patterns to identify potential triggers

## Skills you Need

- Cron jobs for reminders
- Telegram topic for logging
- File storage (markdown log file)

## How to Set it Up

1. Create a Telegram topic called "health-tracker" (or similar).
2. Create a log file: `~/clawd/memory/health-log.md`
3. Prompt OpenClaw:
```text
When I message in the "health-tracker" topic:
1. Parse the message for food items and symptoms
2. Log to ~/clawd/memory/health-log.md with timestamp
3. Confirm what was logged

Set up 3 daily reminders:
- 8 AM: "🍳 Log your breakfast"
- 1 PM: "🥗 Log your lunch"
- 7 PM: "🍽️ Log your dinner and any symptoms"

Every Sunday, analyze the past week's log and identify patterns:
- Which foods correlate with symptoms?
- Are there time-of-day patterns?
- Any clear triggers?

Post the analysis to the health-tracker topic.
```

4. Optional: Add a memory file for OpenClaw to track known triggers and update it as patterns emerge.


---

# 健康习惯养成助手

## 简介

养成健康习惯需要持续追踪和提醒。这个使用案例帮助你建立和维持健康习惯，追踪进度，提供激励，并生成健康报告。

**为什么重要**：改善健康，建立良好习惯，提高生活质量。

**真实例子**：一位用户想养成每天运动的习惯，代理每天提醒、追踪进度、提供鼓励，三个月后他成功养成了每天运动 30 分钟的习惯。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `health` | [ClawdHub](https://clawhub.com/skills/health) | 健康数据 |
| `wearable` | [ClawdHub](https://clawhub.com/skills/wearable) | 穿戴设备 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送提醒 |

---

## 设置步骤

### 1. 前置条件

- 健康目标
- 可穿戴设备（可选）
- 习惯列表

### 2. 提示词模板

```markdown
## 健康习惯养成助手

你是我的健康教练。帮助我建立和维持健康习惯：

### 习惯追踪

**每日习惯**
- 喝水 8 杯
- 运动 30 分钟
- 睡眠 8 小时
- 冥想 10 分钟
- 吃水果蔬菜

**每周习惯**
- 运动 5 天
- 社交活动
- 学习新技能
- 整理环境

### 提醒策略

**早上**
- 7:00：起床，喝水
- 7:30：冥想
- 8:00：健康早餐

**白天**
- 每小时：起身活动
- 12:00：午餐提醒
- 15:00：喝水提醒

**晚上**
- 18:00：运动时间
- 21:00：准备睡觉
- 22:00：睡觉时间

### 进度追踪

**每日检查**
```
🌟 今日习惯打卡

✅ 喝水 8 杯 - 完成！
✅ 运动 30 分钟 - 完成！
⏳ 睡眠 8 小时 - 进行中
✅ 冥想 10 分钟 - 完成！

📊 今日得分：4/5
🔥 连续打卡：12 天
```

**每周报告**
- 习惯完成率
- 趋势分析
- 改进建议
- 庆祝成就

### 激励机制
- 连续打卡奖励
- 里程碑庆祝
- 好友挑战
- 进度可视化
```

### 3. 配置

```
Schedule: 0 7,12,18,21 * * *
Action: 发送提醒 → 追踪进度 → 生成报告
```

---

## 成功指标

- [ ] 习惯完成率 > 80%
- [ ] 连续打卡天数增加
- [ ] 健康指标改善
- [ ] 生活质量提升

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


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
health-&-symptom-tracker/
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
mkdir -p health-&-symptom-tracker && cd health-&-symptom-tracker
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

根據 健康與症狀追蹤器 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Health & Symptom Tracker"""
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
"""Main orchestrator for Health & Symptom Tracker"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 健康與症狀追蹤器 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 健康與症狀追蹤器 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/health-&-symptom-tracker.log 2>&1
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
