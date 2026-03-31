---
name: 逾期採購單追蹤 (Overdue PO Follow-up Queue)/python
description: "Use Case #134 Python 方案: 逾期採購單追蹤。使用 Python 實作 Overdue PO Follow-up Queue 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #134: 逾期採購單追蹤 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 企業流程

---

## 原始需求 (來自 Source Repos)

# 80 - Overdue PO Follow-up Queue

Builds a recurring overdue PO queue from purchase orders that are overdue or blocked.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install todoist
npx clawhub@latest install slack
```

## What It Does

- Pulls purchase orders that are overdue or blocked from finance and procurement systems
- Ranks exceptions by aging, value, and operational impact
- Produces an overdue PO queue for controlled follow-up

## Setup

```bash
export ACCOUNT_SCOPE='purchase orders'
export MAX_ITEMS='20'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='20 8 * * 1-5'
export CRON_NAME='Overdue PO Follow-up Queue'
```

```bash
bash examples/runnable/80-overdue-po-follow-up-queue/scripts/check_prereqs.sh
bash examples/runnable/80-overdue-po-follow-up-queue/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the overdue PO queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- overdue PO backlog
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
mkdir -p ~/overdue-po-follow-up-queue
cd ~/overdue-po-follow-up-queue
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

建立 `main.py`，實作 逾期採購單追蹤 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_overdue_po_follow_up_queue():
    """執行 逾期採購單追蹤 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 逾期採購單追蹤 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_overdue_po_follow_up_queue()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/overdue-po-follow-up-queue && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
