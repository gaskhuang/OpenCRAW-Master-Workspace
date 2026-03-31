---
name: 影子 AI 監控 (Shadow AI Watchlist)/python
description: "Use Case #135 Python 方案: 影子 AI 監控。使用 Python 實作 Shadow AI Watchlist 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #135: 影子 AI 監控 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# 88 - Shadow-AI Watchlist

Builds a recurring shadow-AI watch queue from shadow-AI usage or unapproved tooling chatter.

## Skill Stack

```bash
npx clawhub@latest install slack
npx clawhub@latest install summarize
npx clawhub@latest install todoist
```

## What It Does

- Scans shadow-AI usage or unapproved tooling chatter from security and internal tooling
- Flags urgent exposure, review debt, or policy drift
- Produces a shadow-AI watch queue with evidence and recommended next steps

## Setup

```bash
export SYSTEM_SCOPE='internal tooling'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='16 8 * * 4'
export CRON_NAME='Shadow-AI Watchlist'
```

```bash
bash examples/runnable/88-shadow-ai-watchlist/scripts/check_prereqs.sh
bash examples/runnable/88-shadow-ai-watchlist/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the shadow-AI watch queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- shadow tool incidents surfaced
- time-to-review
- critical items surfaced

## Security Notes

- Use least-privilege scopes and restricted delivery targets for security and IT workflows.
- Do not auto-remediate accounts, hosts, or credentials without explicit operator approval.

## Failure Modes

- Incomplete telemetry can hide the most important issues.
- Aggressive automation without approvals can create more risk than it removes.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/shadow-ai-watchlist
cd ~/shadow-ai-watchlist
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `main.py`，實作 影子 AI 監控 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_shadow_ai_watchlist():
    """執行 影子 AI 監控 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 影子 AI 監控 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_shadow_ai_watchlist()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/shadow-ai-watchlist && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
