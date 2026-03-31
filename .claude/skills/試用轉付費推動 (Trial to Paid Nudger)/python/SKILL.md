---
name: 試用轉付費推動 (Trial to Paid Nudger)/python
description: "Use Case #128 Python 方案: 試用轉付費推動。使用 Python 實作 Trial to Paid Nudger 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #128: 試用轉付費推動 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# 45 - Trial-to-Paid Nudger

Builds a recurring trial conversion follow-up queue from trial accounts nearing conversion deadlines.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Pulls trial accounts nearing conversion deadlines from configured go-to-market systems
- Highlights risk, opportunity, and missing follow-up
- Produces a trial conversion follow-up queue for revenue owners

## Setup

```bash
export ACCOUNT_SEGMENT='self-serve trials'
export MAX_ITEMS='25'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='15 13 * * 1-5'
export CRON_NAME='Trial-to-Paid Nudger'
```

```bash
bash examples/runnable/45-trial-to-paid-nudger/scripts/check_prereqs.sh
bash examples/runnable/45-trial-to-paid-nudger/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the trial conversion follow-up queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- trial conversion rate
- owner follow-up SLA
- coverage of high-value accounts

## Security Notes

- Keep account, pipeline, and commercial data in restricted channels only.
- Require human approval before any outbound customer or partner communication.

## Failure Modes

- Incomplete CRM or account data can hide risk or overstate opportunity.
- Outbound actions should remain draft-only until operators trust the ranking.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/trial-to-paid-nudger
cd ~/trial-to-paid-nudger
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

建立 `main.py`，實作 試用轉付費推動 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_trial_to_paid_nudger():
    """執行 試用轉付費推動 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 試用轉付費推動 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_trial_to_paid_nudger()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/trial-to-paid-nudger && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
