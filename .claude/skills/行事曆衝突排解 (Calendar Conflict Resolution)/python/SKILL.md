---
name: 行事曆衝突排解 (Calendar Conflict Resolution)/python
description: "Use Case #050 Python 方案: 行事曆衝突排解。使用 Python 實作 Calendar Conflict Resolution 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #050: 行事曆衝突排解 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 日历智能提醒

## 简介

传统的日历提醒只是简单地在事件前通知你。这个使用案例提供基于上下文的智能提醒，考虑你的当前状态、交通时间、准备需求，甚至天气情况。

**为什么重要**：不再错过重要事件，确保每次会议都有充分准备。

**真实例子**：一位顾问使用此代理后，不再因为准备不足而匆忙参加会议，代理会提前提醒他需要准备的材料并估算交通时间。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 访问日历 |
| `maps` | [ClawdHub](https://clawhub.com/skills/maps) | 计算交通时间 |
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 查找相关材料 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送提醒 |

---

## 设置步骤

### 1. 前置条件

- 日历访问权限
- 地图 API 密钥
- 常用位置（家、办公室）

### 2. 提示词模板

```markdown
## 日历智能提醒

你是我的智能助理。监控我的日历并提供上下文感知的提醒：

### 提醒类型

**1. 准备提醒（会议前 24 小时）**
- 会议目的和议程
- 需要准备的材料
- 相关邮件或文档链接
- 参与者背景信息

**2. 出发提醒（根据交通动态计算）**
- 当前位置到会议地点的时间
- 交通状况和替代路线
- 天气对交通的影响
- 建议出发时间

**3. 即时提醒（会议前 15 分钟）**
- 会议链接或地址
- 主要讨论要点
- 需要提出的问题

### 上下文考虑
- 当前位置
- 交通状况
- 天气条件
- 前一项会议的结束时间
- 准备时间需求

### 智能规则
- 如果会议需要出行，提前计算交通时间
- 如果是重要客户，额外准备背景研究
- 如果是首次会议，准备自我介绍要点
- 如果天气恶劣，建议提前出发
```

### 3. 配置

```
Schedule: */15 * * * *
Action: 监控日历 → 计算上下文 → 发送智能提醒
```

---

## 成功指标

- [ ] 从不迟到会议
- [ ] 每次会议都有充分准备
- [ ] 不再错过重要事件
- [ ] 减少会议焦虑

---

## 变体与扩展

### 变体 1：团队会议管理
协调团队会议，确保所有人都有空。

### 变体 2：旅行行程整合
整合航班、酒店和会议到统一提醒。

---

## 故障排除

### 问题：交通时间不准确
**解决方案**：检查地图 API 配置和实时交通数据。

### 问题：提醒过于频繁
**解决方案**：调整提醒频率和优先级规则。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🗓️ Smart Meeting Scheduler

> Schedule meetings in seconds. Timezone math done for you, conflicts detected, follow-ups automated.

---

## The Problem

Scheduling meetings across timezones is a nightmare. You're juggling Calendly links, checking five people's availability, doing timezone math in your head, and manually sending follow-up reminders. Half the meeting gets wasted because nobody sent an agenda, and action items disappear into the void after the call ends.

---

## The Solution

OpenClaw handles the entire meeting lifecycle: finds times that work across timezones, checks everyone's availability, sends calendar invites with context, reminds participants before the meeting, and automatically captures and distributes follow-up action items.

---

## Setup Guide

### Step 1: Install Calendar Skills

```bash
openclaw skill install calendar       # Google Calendar integration
openclaw skill install ical           # iCal/Apple Calendar support
openclaw skill install remind-me      # Smart reminders
openclaw skill install gmail          # Email invites
```

### Step 2: Configure Timezone Preferences

Create `~/openclaw/meetings/config.json`:

```json
{
  "myTimezone": "America/New_York",
  "workingHours": {
    "start": "09:00",
    "end": "18:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  },
  "bufferMinutes": 15,
  "defaultDuration": 30,
  "preferredTimes": ["10:00", "14:00", "16:00"],
  "avoidTimes": ["12:00-13:00"]
}
```

### Step 3: Set Up Contact Timezones

Create `~/openclaw/meetings/contacts.json`:

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
calendar-conflict-resolution/
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
mkdir -p calendar-conflict-resolution && cd calendar-conflict-resolution
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

根據 行事曆衝突排解 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Calendar Conflict Resolution"""
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
"""Main orchestrator for Calendar Conflict Resolution"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 行事曆衝突排解 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 行事曆衝突排解 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/calendar-conflict-resolution.log 2>&1
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
