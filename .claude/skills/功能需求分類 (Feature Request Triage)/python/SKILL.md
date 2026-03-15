---
name: 功能需求分類 (Feature Request Triage)/python
description: "Use Case #124 Python 方案: 功能需求分類。使用 Python 實作 Feature Request Triage 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #124: 功能需求分類 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 產品管理

---

## 原始需求 (來自 Source Repos)

# 25 - Feature Request Triage

Converts incoming feature requests into an evidence-ranked engineering queue.

## Skill Stack

```bash
npx clawhub@latest install github
npx clawhub@latest install summarize
npx clawhub@latest install todoist
```

## What It Does

- Pulls new feature issues and related discussion context
- Deduplicates overlapping requests
- Outputs prioritized triage list with rationale and proposed next action

## Setup

```bash
export REPO='owner/repo'
export ISSUE_LABEL='feature-request'
export WINDOW_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='0 14 * * 1-5'
export CRON_NAME='Feature Request Triage'
```

```bash
bash examples/runnable/25-feature-request-triage/scripts/check_prereqs.sh
bash examples/runnable/25-feature-request-triage/scripts/install_cron.sh
```

## Smoke Test

- Trigger one run and verify duplicate requests are grouped.
- Confirm each priority item has issue link + action recommendation.

## KPI

- Median issue triage time
- Duplicate request ratio
- Time-to-first-response for feature requests

## Security Notes

- Keep repo access read-only for analysis phase.
- Avoid exposing private issues in broad channels.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/feature-request-triage
cd ~/feature-request-triage
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

建立 `main.py`，實作 功能需求分類 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_feature_request_triage():
    """執行 功能需求分類 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 功能需求分類 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_feature_request_triage()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/feature-request-triage && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
