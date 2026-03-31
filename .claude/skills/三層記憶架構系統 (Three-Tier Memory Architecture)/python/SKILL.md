---
name: 三層記憶架構系統 (Three-Tier Memory Architecture)/python
description: "Use Case #114 Python 方案: 三層記憶架構系統。使用 Python 實作 Three-Tier Memory Architecture 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #114: 三層記憶架構系統 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 高級 | 分類: AI 記憶與代理架構

---

## 原始需求 (來自 Source Repos)

# 三层记忆系统

## 简介

代理需要有效的记忆管理来保持上下文。这个使用案例实现三层记忆系统：长期核心原则、每日事件日志和项目特定追踪，平衡速度和持久性。

**为什么重要**：确保重要信息持久化，避免 Token 膨胀，保持上下文连贯。

**真实例子**：一位开发者使用此系统管理代理记忆，代理能够记住项目目标、每日决策和当前状态，工作效率提高了 3 倍。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `filesystem` | 内置 | 文件读写 |
| `memory_search` | [ClawdHub](https://clawhub.com/skills/memory) | 语义搜索 |

---

## 设置步骤

### 1. 目录结构

```
workspace/
├── MEMORY.md              # 长期：原则、锚点、目标
├── PROJECTS.md            # 项目：状态、阻塞、下一步
└── memory/
    ├── 2026-02-19.md      # 每日：事件、决策、上下文
    ├── 2026-02-18.md
    └── heartbeat-state.json
```

### 2. 提示词模板

```markdown
## 三层记忆系统

### MEMORY.md - 长期记忆

```markdown
# 长期记忆

## 核心原则
- 效率优于冗长
- 主动 > 被动
- 用理由记录决策

## 关键锚点
- 用户：[姓名]
- 风格：直接，无废话
- 偏好：具体例子 > 一般陈述

## 目标
- [ ] 构建 50 个 OpenClaw 案例
- [ ] 发布 GitHub 仓库
```

### 每日记忆

```markdown
# 记忆 - YYYY-MM-DD

## 今日事件
- [时间]：[事件描述]
- [时间]：[事件描述]

## 决策
- [决策]：[理由]

## 上下文
- 当前项目：[项目名]
- 阻塞项：[描述]
- 下一步：[描述]
```

### PROJECTS.md

```markdown
# 项目追踪

## 活跃项目

### [项目名]
**状态**：进行中
**进度**：70%
**阻塞**：[阻塞项]
**下一步**：[行动项]
```

### 记忆管理

**写入规则**
- 核心原则 → MEMORY.md
- 每日事件 → memory/YYYY-MM-DD.md
- 项目状态 → PROJECTS.md

**读取规则**
- 启动时读取 MEMORY.md
- 读取最近 7 天每日记忆
- 读取活跃项目状态

**归档规则**
- 30 天前的每日记忆归档
- 已完成项目移动到归档
```

### 3. 配置

```
Trigger: 代理启动 / 每日结束
Action: 读取记忆 → 更新记忆 → 存储
```

---

## 成功指标

- [ ] 重要信息持久化
- [ ] 上下文保持连贯
- [ ] Token 使用优化
- [ ] 代理响应准确

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
three-tier-memory-architecture/
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
mkdir -p three-tier-memory-architecture && cd three-tier-memory-architecture
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

根據 三層記憶架構系統 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Three-Tier Memory Architecture"""
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
"""Main orchestrator for Three-Tier Memory Architecture"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 三層記憶架構系統 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 三層記憶架構系統 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/three-tier-memory-architecture.log 2>&1
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
