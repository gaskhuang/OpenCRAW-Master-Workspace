---
name: AI 模型費用追蹤中心 (AI Model Cost Tracker)/python
description: "Use Case #089 Python 方案: AI 模型費用追蹤中心。使用 Python 實作 AI Model Cost Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #089: AI 模型費用追蹤中心 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 監控與維運

---

## 原始需求 (來自 Source Repos)

# AI 成本追踪

## 简介

追踪 OpenClaw 和 AI 服务的使用成本，生成成本报告，帮助优化支出。

**为什么重要**：了解 AI 使用成本，优化模型选择，控制预算。

**真实例子**：一个团队使用此代理追踪 AI 成本，发现可以切换到更便宜的模型而不影响质量，每月节省 40% 成本。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `logging` | [ClawdHub](https://clawhub.com/skills/logging) | 使用记录 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 成本分析 |
| `dashboard` | [ClawdHub](https://clawhub.com/skills/dashboard) | 成本仪表板 |

---

## 使用方式

### 记录使用
追踪每次 API 调用

### 计算成本
根据模型和价格计算成本

### 生成报告
- 每日成本
- 模型使用分布
- 优化建议

---

## 来源

- 来源：Stack Junkie


---

# Token 使用优化器

## 简介

优化 LLM Token 使用效率，降低成本，提高响应质量。

**为什么重要**：控制 AI 成本，提高效率，优化模型选择。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `llm` | [ClawdHub](https://clawhub.com/skills/llm) | LLM 管理 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 使用分析 |

---

## 使用方式

分析使用模式，获取优化建议

---

## 来源

- 作者：OpenClaw 社区


---

# 💸 AI Cost Tracker

> Know exactly what you're spending on AI. No surprises, just optimization.

---

## The Problem

AI API costs add up fast and unpredictably. You're using Claude, GPT-4, Gemini across different tools and projects. The bill arrives and you have no idea what drove the spike or how to optimize.

---

## The Solution

OpenClaw tracks your AI usage across all providers, alerts on unusual spending, identifies cost optimization opportunities, and helps you choose the right model for each task.

---

## Setup Guide

### Step 1: Install Tracking Skills

```bash
openclaw skill install claude-code-usage
openclaw skill install codex-quota
openclaw skill install minimax-usage
```

### Step 2: Configure Providers

Create `~/openclaw/ai-costs/providers.json`:

```json
{
  "providers": [
    {
      "name": "Anthropic",
      "budgetMonthly": 100,
      "alertThreshold": 80
    },
    {
      "name": "OpenAI",
      "budgetMonthly": 50,
      "alertThreshold": 80
    },
    {
      "name": "Google",
      "budgetMonthly": 30,
      "alertThreshold": 80
    }
  ],
  "totalBudget": 200
}
```

### Step 3: Set Up Cost Rules

Create `~/openclaw/ai-costs/rules.md`:

```markdown
# AI Cost Optimization Rules

## Model Selection
- Simple tasks: Use cheapest model (GPT-3.5, Claude Instant)
- Complex reasoning: Use best model
- Bulk processing: Batch API when available

## Alerts
- Daily spend > $10: Warning
- Weekly spend > $40: Alert
- Approaching 80% of budget: Alert

## Review Weekly
- Highest cost tasks
- Potential model downgrades
- Unused subscriptions
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `claude-code-usage` | Claude/Anthropic usage |
| `codex-quota` | OpenAI Codex usage |
| `minimax-usage` | MiniMax usage |

---

## Example Prompts

**Daily check:**
```
What's my AI spend today across all providers? Any unusual spikes?
```

**Optimization analysis:**
```
Analyze my AI usage this week. Where am I overspending? Which tasks could use cheaper models?
```

**Budget planning:**
```
Based on my usage patterns, what should my monthly A

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
ai-model-cost-tracker/
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
mkdir -p ai-model-cost-tracker && cd ai-model-cost-tracker
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

根據 AI 模型費用追蹤中心 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for AI Model Cost Tracker"""
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
"""Main orchestrator for AI Model Cost Tracker"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== AI 模型費用追蹤中心 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 AI 模型費用追蹤中心 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/ai-model-cost-tracker.log 2>&1
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
