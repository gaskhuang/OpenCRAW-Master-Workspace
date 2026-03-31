---
name: 看板自動整理 (Kanban Auto Organizer)/python
description: "Use Case #051 Python 方案: 看板自動整理。使用 Python 實作 Kanban Auto Organizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #051: 看板自動整理 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Trello/Notion 整理助手

## 简介

项目管理看板变得混乱？这个使用案例自动整理你的 Trello 或 Notion 看板，归档已完成任务，更新状态，生成进度报告，并提醒即将到期的任务。

**为什么重要**：保持项目井井有条，确保任务按时完成，提高团队效率。

**真实例子**：一个 10 人团队使用此代理管理产品开发，代理每天整理看板、更新状态、提醒截止日期，使项目按时交付率提高了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `trello` | [ClawdHub](https://clawhub.com/skills/trello) | 管理 Trello |
| `notion` | [ClawdHub](https://clawhub.com/skills/notion) | 管理 Notion |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 检查日期 |

---

## 设置步骤

### 1. 前置条件

- Trello/Notion 账号
- API 密钥
- 看板访问权限

### 2. 提示词模板

```markdown
## Trello/Notion 整理助手

你是我的项目管理助手。每天整理和更新看板：

### 每日整理任务

**1. 归档已完成**
- 识别已完成超过 7 天的卡片
- 归档到"已完成"列表
- 记录完成时间

**2. 更新状态**
- 检查进行中的任务
- 更新进度百分比
- 标记阻塞的任务

**3. 提醒即将到期**
- 识别 3 天内到期的任务
- 发送提醒通知
- 标记高优先级

**4. 整理标签**
- 统一标签格式
- 清理未使用的标签
- 更新颜色编码

### 每周报告

**进度摘要**
```
📊 项目周报 - YYYY-MM-DD

✅ 本周完成
- 任务 1
- 任务 2

🔄 进行中
- 任务 3 (70%)
- 任务 4 (30%)

⚠️ 风险
- 任务 5 (逾期 2 天)

📅 下周计划
- 任务 6 (截止周三)
- 任务 7 (截止周五)
```

**团队统计**
- 每人完成任务数
- 平均完成时间
- 阻塞问题统计

### 自动化规则

**状态自动更新**
- 所有子任务完成 → 父任务自动完成
- 逾期任务 → 自动标记红色
- 阻塞任务 → 通知负责人

**模板应用**
- 新任务自动添加检查清单
- 根据类型应用标签
- 设置默认截止日期
```

### 3. 配置

```
Schedule: 0 9 * * *
Action: 扫描看板 → 整理 → 更新 → 发送报告
```

---

## 成功指标

- [ ] 看板保持整洁
- [ ] 任务按时完成率 > 90%
- [ ] 团队效率提升
- [ ] 零遗漏重要任务

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# Trello 看板整理器

## 简介

智能整理 Trello 看板，归档旧卡片，更新状态，优化布局。

**为什么重要**：保持看板整洁，提高工作效率，优化项目管理。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `trello` | [ClawdHub](https://clawhub.com/skills/trello) | Trello API |

---

## 使用方式

连接看板，设置整理规则

---

## 来源

- 作者：OpenClaw 社区


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
kanban-auto-organizer/
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
mkdir -p kanban-auto-organizer && cd kanban-auto-organizer
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

根據 看板自動整理 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Kanban Auto Organizer"""
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
"""Main orchestrator for Kanban Auto Organizer"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 看板自動整理 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 看板自動整理 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/kanban-auto-organizer.log 2>&1
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
