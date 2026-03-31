---
name: 郵件自動分類器 (Email Auto Classifier)/python
description: "Use Case #046 Python 方案: 郵件自動分類器。使用 Python 實作 Email Auto Classifier 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #046: 郵件自動分類器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 邮件自动分类器

## 简介

收件箱被大量邮件淹没？这个使用案例自动分类和优先级排序你的邮件，将重要邮件突出显示，自动归档低优先级邮件，并为需要回复的邮件设置提醒。

**为什么重要**：减少邮件处理时间，确保重要邮件不被遗漏。

**真实例子**：一位项目经理每天收到 200+ 邮件，使用此代理后，只需关注被标记为"紧急"和"重要"的 20-30 封邮件，效率提高了 3 倍。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 读取和分类邮件 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 自然语言处理 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 设置提醒 |

---

## 设置步骤

### 1. 前置条件

- 邮件账号访问权限
- 分类规则偏好

### 2. 提示词模板

```markdown
## 邮件自动分类器

你是我的邮件助手。每 15 分钟检查一次新邮件并执行以下操作：

### 分类规则

**紧急**（立即通知）
- 来自直接上级的邮件
- 包含"紧急"、"ASAP"、"立即"等关键词
- 系统故障或安全警报

**重要**（1 小时内处理）
- 客户邮件
- 项目截止日期相关
- 会议邀请需要回复

**普通**（当天处理）
- 内部通知
- 一般询问
- 更新和公告

**低优先级**（批量处理）
- 新闻通讯
- 营销邮件
- 自动通知

### 自动操作
1. **归档**：新闻通讯、营销邮件自动归档
2. **标记**：项目相关邮件添加标签
3. **提醒**：需要回复的邮件设置提醒
4. **摘要**：每小时发送重要邮件摘要

### 学习规则
- 根据我的操作学习偏好
- 记住我常联系的人
- 识别重要项目关键词
- 调整分类准确性
```

### 3. 配置

```
Schedule: */15 * * * *
Action: 检查邮件 → 分类 → 执行操作 → 发送摘要
```

---

## 成功指标

- [ ] 邮件处理时间减少 50%
- [ ] 重要邮件零遗漏
- [ ] 收件箱保持整洁
- [ ] 自动分类准确率 > 90%

---

## 变体与扩展

### 变体 1：智能回复建议
为常见邮件类型生成回复建议。

### 变体 2：邮件摘要报告
每天生成邮件活动摘要报告。

---

## 故障排除

### 问题：邮件分类错误
**解决方案**：提供反馈给代理，帮助它学习你的偏好。

### 问题：重要邮件被归档
**解决方案**：调整分类规则和关键词。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📧 Email Triage Autopilot

> Transform inbox chaos into organized action. Stop drowning in emails—let OpenClaw surface what matters.

---

## The Problem

The average professional receives 120+ emails daily, spending 2-3 hours just reading and sorting them. Most are noise (newsletters, notifications, CC chains), but buried in there are urgent requests, deadlines, and opportunities that get missed. You either live in your inbox anxiously or miss important things while trying to batch-check. Neither works.

---

## The Solution

OpenClaw continuously monitors your inbox, categorizes every email by urgency and importance, drafts responses to routine queries, extracts action items into your todo system, and delivers a concise morning briefing of what actually needs your attention. You check email once or twice a day, fully informed, and respond only to what matters.

**The magic:** OpenClaw learns YOUR priorities—who's important, what topics are urgent, which newsletters you actually read vs. ignore.

---

## Setup Guide

### Step 1: Install the Gmail Skill (5 minutes)

```bash
# Install the gmail skill
openclaw skill install gmail

# Authenticate (opens browser for OAuth)
openclaw skill gmail auth
```

For other providers:
- **Outlook:** `openclaw skill install outlook`
- **IMAP:** `openclaw skill install imap` (works with any provider)

### Step 2: Create Your Priority Rules File

Create `~/openclaw/email-rules.md`:

```markdown
# Email Priority Rules

## 🔴 URGENT (notify immediately)
- From: [boss@company.com, ceo@company.com, wife@family.com]
- Subject contains: "urgent", "asap", "emergency", "deadline today"
- Clients: *@bigclient.com, *@importantcustomer.io

##

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
email-auto-classifier/
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
mkdir -p email-auto-classifier && cd email-auto-classifier
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

根據 郵件自動分類器 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Email Auto Classifier"""
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
"""Main orchestrator for Email Auto Classifier"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 郵件自動分類器 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 郵件自動分類器 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/email-auto-classifier.log 2>&1
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
