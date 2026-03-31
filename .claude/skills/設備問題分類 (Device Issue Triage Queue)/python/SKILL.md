---
name: 設備問題分類 (Device Issue Triage Queue)/python
description: "Use Case #136 Python 方案: 設備問題分類。使用 Python 實作 Device Issue Triage Queue 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #136: 設備問題分類 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: IT 運維

---

## 原始需求 (來自 Source Repos)

# 89 - Device Issue Triage Queue

Builds a recurring IT issue triage queue from incoming device and workplace IT issues.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install slack
npx clawhub@latest install todoist
```

## What It Does

- Scans incoming device and workplace IT issues from security and internal tooling
- Flags urgent exposure, review debt, or policy drift
- Produces an IT issue triage queue with evidence and recommended next steps

## Setup

```bash
export SYSTEM_SCOPE='employee devices'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='23 9 * * 1-5'
export CRON_NAME='Device Issue Triage Queue'
```

```bash
bash examples/runnable/89-device-issue-triage-queue/scripts/check_prereqs.sh
bash examples/runnable/89-device-issue-triage-queue/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the IT issue triage queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- first assignment time
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
mkdir -p ~/device-issue-triage-queue
cd ~/device-issue-triage-queue
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

建立 `main.py`，實作 設備問題分類 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_device_issue_triage_queue():
    """執行 設備問題分類 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 設備問題分類 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_device_issue_triage_queue()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/device-issue-triage-queue && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
