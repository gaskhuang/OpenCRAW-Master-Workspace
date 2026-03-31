---
name: 採購評分 (Procurement Intake Scorer)/python
description: "Use Case #133 Python 方案: 採購評分。使用 Python 實作 Procurement Intake Scorer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #133: 採購評分 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 企業流程

---

## 原始需求 (來自 Source Repos)

# 79 - Procurement Intake Scorer

Builds a recurring procurement intake queue from incoming procurement requests and fit/risk details.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Pulls incoming procurement requests and fit/risk details from finance and procurement systems
- Ranks exceptions by aging, value, and operational impact
- Produces a procurement intake queue for controlled follow-up

## Setup

```bash
export ACCOUNT_SCOPE='procurement intake'
export MAX_ITEMS='20'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='13 15 * * 1-5'
export CRON_NAME='Procurement Intake Scorer'
```

```bash
bash examples/runnable/79-procurement-intake-scorer/scripts/check_prereqs.sh
bash examples/runnable/79-procurement-intake-scorer/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the procurement intake queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- procurement cycle time
- exception aging
- manual review time

## Security Notes

- Keep billing, procurement, and board-prep data in restricted channels only.
- Require human approval for any outbound or system-changing action tied to money or contracts.

## Failure Modes

- Partial source data can distort value or aging calculations.
- Approval and contract workflows should remain human-controlled.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/procurement-intake-scorer
cd ~/procurement-intake-scorer
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

建立 `main.py`，實作 採購評分 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_procurement_intake_scorer():
    """執行 採購評分 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 採購評分 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_procurement_intake_scorer()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/procurement-intake-scorer && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
