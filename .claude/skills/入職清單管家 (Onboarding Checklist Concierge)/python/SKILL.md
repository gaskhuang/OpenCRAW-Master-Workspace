---
name: 入職清單管家 (Onboarding Checklist Concierge)/python
description: "Use Case #132 Python 方案: 入職清單管家。使用 Python 實作 Onboarding Checklist Concierge 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #132: 入職清單管家 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 人力資源

---

## 原始需求 (來自 Source Repos)

# 73 - Onboarding Checklist Concierge

Builds a recurring onboarding readiness digest from new-hire onboarding tasks and readiness checks.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install todoist
npx clawhub@latest install slack
```

## What It Does

- Collects new-hire onboarding tasks and readiness checks from people workflows
- Flags delays, readiness gaps, and coordination risk
- Produces an onboarding readiness digest for hiring or people leads

## Setup

```bash
export TEAM_SCOPE='new hires'
export MAX_ITEMS='20'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='31 9 * * 4'
export CRON_NAME='Onboarding Checklist Concierge'
```

```bash
bash examples/runnable/73-onboarding-checklist-concierge/scripts/check_prereqs.sh
bash examples/runnable/73-onboarding-checklist-concierge/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the onboarding readiness digest includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- onboarding tasks completed on time
- cycle time
- completion rate

## Security Notes

- Limit access to candidate and employee data to approved people-ops spaces.
- Avoid storing sensitive hiring or personnel details in broad delivery channels.

## Failure Modes

- Incomplete notes or scorecards can weaken prioritization.
- Sensitive people data should never be sent to broad channels.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/onboarding-checklist-concierge
cd ~/onboarding-checklist-concierge
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

建立 `main.py`，實作 入職清單管家 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_onboarding_checklist_concierge():
    """執行 入職清單管家 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 入職清單管家 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_onboarding_checklist_concierge()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/onboarding-checklist-concierge && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
