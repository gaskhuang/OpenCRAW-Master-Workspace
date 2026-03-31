---
name: PR 追蹤雷達 (PR Tracking Radar)/python
description: "Use Case #071 Python 方案: PR 追蹤雷達。使用 Python 實作 PR Tracking Radar 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #071: PR 追蹤雷達 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# GitHub 过期 Issue 清理

## 简介

自动识别和清理长期未活动的 GitHub Issue，保持仓库整洁。

**为什么重要**：减少 Issue 堆积，提高团队效率，保持项目健康。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `github` | [ClawdHub](https://clawhub.com/skills/github) | GitHub API |

---

## 使用方式

设置过期规则，代理自动标记和清理

---

## 来源

- 作者：OpenClaw 社区


---

# GitHub Issue 优先级排序器

## 简介

智能排序 GitHub Issue，根据影响、紧急程度、资源可用性确定优先级。

**为什么重要**：优化开发资源分配，确保重要问题优先解决。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `github` | [ClawdHub](https://clawhub.com/skills/github) | GitHub API |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |

---

## 使用方式

连接仓库，设置优先级规则

---

## 来源

- 作者：OpenClaw 社区


---

# 🔍 PR Review Assistant

> Never merge buggy code again. Get thorough reviews in minutes, not days.

---

## The Problem

Code reviews are bottlenecks. PRs sit for days waiting for busy teammates. When reviews do happen, they're often rushed, missing bugs that slip into production. Junior devs don't get the learning feedback they need.

---

## The Solution

OpenClaw automatically reviews every PR: checks for bugs, security issues, style violations, and suggests improvements. Human reviewers can focus on architecture and business logic while OpenClaw handles the tedious stuff.

---

## Setup Guide

### Step 1: Install Skills

```bash
openclaw skill install github
openclaw skill install github-pr
openclaw skill install conventional-commits
```

### Step 2: Configure Review Rules

Create `~/openclaw/pr-review/rules.md`:

```markdown
# PR Review Checklist

## Always Check
- [ ] No hardcoded secrets/credentials
- [ ] No console.log/print statements left in
- [ ] Error handling present
- [ ] Input validation for user data
- [ ] SQL injection prevention
- [ ] XSS prevention

## Code Quality
- [ ] Functions under 50 lines
- [ ] No deep nesting (max 3 levels)
- [ ] Meaningful variable names
- [ ] DRY - no copy-pasted blocks

## Tests
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Tests actually test something meaningful

## Documentation
- [ ] Complex logic has comments
- [ ] Public APIs have docstrings
- [ ] README updated if needed
```

### Step 3: Set Up GitHub Webhook (Optional)

For automatic reviews on new PRs, set up a webhook or use GitHub Actions.

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `github` | GitHub API access |
| `github-pr` | PR-specific operations |
| `conventional-commits` | Commit message validation |

---

## Example Prompts

**Review a PR:**
```
Review PR #123 in repo [owner/repo]. Focus on security, performance, and code quality.
```

**Batch review:**
```
Show me all open PRs in [repo] that haven't been reviewed in 2+ days. Give me a summary of each.
```

**Learn from feedback:**
```
What are the most common issues you've found in our PRs this month? Create a team guidelines doc.
```

**Pre-submit check:**
```
I'm about to submit a PR with these changes: [paste diff]. Any issues I should fix first?
```

---

## Cron Schedule

```
*/15 * * * *   # Every

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
pr-tracking-radar/
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
mkdir -p pr-tracking-radar && cd pr-tracking-radar
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

根據 PR 追蹤雷達 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for PR Tracking Radar"""
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
"""Main orchestrator for PR Tracking Radar"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== PR 追蹤雷達 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 PR 追蹤雷達 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/pr-tracking-radar.log 2>&1
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
