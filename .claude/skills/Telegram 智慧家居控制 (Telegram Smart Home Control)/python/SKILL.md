---
name: Telegram 智慧家居控制 (Telegram Smart Home Control)/python
description: "Use Case #019 Python 方案: Telegram 智慧家居控制。使用 Python 實作 Telegram Smart Home Control 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #019: Telegram 智慧家居控制 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 智能家居 Telegram 控制器

## 简介

通过 Telegram 消息控制你的智能家居设备。这个使用案例让你可以发送自然语言命令来控制灯光、温度、安防系统等，无需打开多个应用。

**为什么重要**：统一控制界面，语音/文字控制，远程管理家居。

**真实例子**：一位用户下班路上通过 Telegram 发送"我快到家了"，代理自动打开空调、调整灯光、开始播放音乐，营造舒适的回家环境。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 接收命令 |
| `smart_home` | [ClawdHub](https://clawhub.com/skills/smart-home) | 控制设备 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 理解命令 |

---

## 设置步骤

### 1. 前置条件

- 智能家居设备（支持 HomeKit、Google Home 或 Alexa）
- Telegram Bot
- 智能家居 Hub

### 2. 提示词模板

```markdown
## 智能家居 Telegram 控制器

你是我的智能家居管家。通过 Telegram 接收命令并执行：

### 命令解析

**灯光控制**
- "打开客厅灯" → 开灯
- "调暗卧室灯到 50%" → 调整亮度
- "关闭所有灯" → 全关

**温度控制**
- "设置温度到 24 度" → 调整空调
- "有点热" → 降低 2 度
- "开启节能模式" → 节能设置

**场景模式**
- "我回家了" → 回家模式
- "我要睡觉了" → 睡眠模式
- "我要出门了" → 离家模式
- "看电影" → 影院模式

**安防系统**
- "开启安防" → 启动监控
- "查看门口" → 发送摄像头画面
- "谁在家" → 报告人员状态

### 场景定义

**回家模式**
- 开门灯
- 空调调至舒适温度
- 播放欢迎音乐
- 关闭安防

**睡眠模式**
- 关闭所有灯
- 空调调至睡眠温度
- 启动夜间安防
- 静音所有设备

**离家模式**
- 关闭所有电器
- 启动全屋安防
- 扫地机器人开始工作
- 模拟有人在家的灯光

### 状态报告
```
🏠 家居状态

💡 灯光：客厅开，卧室关，厨房开
🌡️ 温度：24°C (目标)
🔒 安防：已启动
👥 人员：2 人在家
💡 能耗：今日 12.5 kWh
```
```

### 3. 配置

```
Trigger: Telegram 消息
Action: 解析命令 → 执行操作 → 确认回复
```

---

## 成功指标

- [ ] 所有设备可通过 Telegram 控制
- [ ] 命令理解准确率 > 95%
- [ ] 响应时间 < 3 秒
- [ ] 场景模式正常运行

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🏠 Smart Home Orchestrator

> Your home, intelligently automated. Not just "lights on" but "perfect ambiance."

---

## The Problem

Smart home devices are dumb in isolation. You have 10 apps for 10 devices. Creating complex automations requires programming skills. And when something changes (guest visiting, working from home), you manually adjust everything.

---

## The Solution

OpenClaw becomes your home's brain: understands context (time, weather, who's home, your calendar), orchestrates devices together, and adapts to your life. Tell it what you want in natural language.

---

## Setup Guide

### Step 1: Install Smart Home Skills

```bash
openclaw skill install homeassistant
openclaw skill install homey-cli
openclaw skill install nest-devices
openclaw skill install netatmo
```

### Step 2: Define Scenes

Create `~/openclaw/home/scenes.md`:

```markdown
# Home Scenes

## Morning
- Lights: Gradual brighten 15 min before alarm
- Thermostat: 72°F
- Coffee maker: Start
- Blinds: Open

## Work Mode
- Office lights: Bright, cool white
- Other rooms: Off
- Thermostat: Comfortable
- Do Not Disturb: On

## Movie Night
- Living room: Dim to 20%
- TV backlighting: On, blue
- Thermostat: 70°F
- Blinds: Closed

## Goodnight
- All lights: Off
- Doors: Locked
- Thermostat: 68°F
- Security: Armed
```

### Step 3: Set Context Rules

Create `~/openclaw/home/rules.md`:

```markdown
# Automation Rules

## When I leave home
- Lights off (except security)
- Thermostat: Eco mode
- Security: Armed

## When I arrive home
- Lights: Based on time of day
- Thermostat: Comfort mode
- Security: Disarmed

## Gu

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
telegram-smart-home-control/
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
mkdir -p telegram-smart-home-control && cd telegram-smart-home-control
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

根據 Telegram 智慧家居控制 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Telegram Smart Home Control"""
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
"""Main orchestrator for Telegram Smart Home Control"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== Telegram 智慧家居控制 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 Telegram 智慧家居控制 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/telegram-smart-home-control.log 2>&1
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
