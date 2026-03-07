---
name: 目標驅動自主任務 (Goal-Driven Autonomous Tasks)/python
description: "Use Case #010 Python 方案: 目標驅動自主任務。使用 Python 實作 Goal-Driven Autonomous Tasks 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #010: 目標驅動自主任務 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# 每日目标任务生成器

## 简介

将长期目标转化为每日可执行任务。代理根据你的目标自动生成每日任务列表，并帮助你追踪完成进度。

**为什么重要**：将大目标分解为小步骤，确保持续进展，避免目标遗忘。

**真实例子**：一位创业者使用此代理管理多个项目目标，代理每天早上生成 3-5 个推进目标的行动项，项目完成率提高了 60%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `task_manager` | [ClawdHub](https://clawhub.com/skills/tasks) | 任务管理 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 日程安排 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送任务 |

---

## 使用方式

### 设置目标
告诉代理你的长期目标（如"学习 Python"、"建立个人品牌"）

### 每日任务
每天早上代理生成推进目标的行动项

### 进度追踪
代理追踪任务完成情况，调整后续任务

---

## 来源

- 作者：Alex Finn
- 平台：YouTube


---

# Autonomous Project Management with Subagents

Managing complex projects with multiple parallel workstreams is exhausting. You end up context-switching constantly, tracking status across tools, and manually coordinating handoffs.

This use case implements a decentralized project management pattern where subagents work autonomously on tasks, coordinating through shared state files rather than a central orchestrator.

## Pain Point

Traditional orchestrator patterns create bottlenecks—the main agent becomes a traffic cop. For complex projects (multi-repo refactors, research sprints, content pipelines), you need agents that can work in parallel without constant supervision.

## What It Does

- **Decentralized coordination**: Agents read/write to a shared `STATE.yaml` file
- **Parallel execution**: Multiple subagents work on independent tasks simultaneously
- **No orchestrator overhead**: Main session stays thin (CEO pattern—strategy only)
- **Self-documenting**: All task state persists in version-controlled files

## Core Pattern: STATE.yaml

Each project maintains a `STATE.yaml` file that serves as the single source of truth:

```yaml
# STATE.yaml - Project coordination file
project: website-redesign
updated: 2026-02-10T14:30:00Z

tasks:
  - id: homepage-hero
    status: in_progress
    owner: pm-frontend
    started: 2026-02-10T12:00:00Z
    notes: "Working on responsive layout"
    
  - id: api-auth
    status: done
    owner: pm-backend
    completed: 2026-02-10T14:00:00Z
    output: "src/api/auth.ts"
    
  - id: content-migration
    status: blocked
    owner: pm-content
    blocked_by: api-auth
    notes: "Waiting for new endpoint schema"

next_actions:
  - "pm-content: Resume migration now that api-auth is done"
  - "pm-frontend: Review hero with design team"
```

## How It Works

1. **Main agent receives task** → spawns subagent with specific scope
2. **Subagent reads STATE.yaml** → finds its assigned tasks
3. **Subagent works autonomously** → updates STATE.yaml on progress
4. **Other agents poll STATE.yaml** → pick up unblocked work
5. **Main agent checks in periodically** → reviews state, adjusts priorities

## Skills You Need

- `sessions_spawn` / `sessions_send` for subagent management
- File system access for STATE.yaml
- Git for state versioning (optional but recommended)

## Setup: AGENTS.md Configuration

```text
## PM Delegation Pattern

M

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
goal-driven-autonomous-tasks/
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
mkdir -p goal-driven-autonomous-tasks && cd goal-driven-autonomous-tasks
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

根據 目標驅動自主任務 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Goal-Driven Autonomous Tasks"""
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
"""Main orchestrator for Goal-Driven Autonomous Tasks"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 目標驅動自主任務 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 目標驅動自主任務 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/goal-driven-autonomous-tasks.log 2>&1
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
