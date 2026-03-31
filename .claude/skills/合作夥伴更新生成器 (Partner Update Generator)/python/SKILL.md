---
name: 合作夥伴更新生成器 (Partner Update Generator)/python
description: "Use Case #123 Python 方案: 合作夥伴更新生成器。使用 Python 實作 Partner Update Generator 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #123: 合作夥伴更新生成器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# 21 - Partner Update Generator

Generates concise partner updates from recent internal activity and milestones.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install summarize
```

## What It Does

- Pulls recent project/customer signals from selected inbox and docs context
- Drafts partner-friendly weekly update with risks and asks
- Separates confirmed updates from pending items

## Setup

```bash
export UPDATE_SCOPE='partnership alpha'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='0 12 * * 5'
export CRON_NAME='Partner Update Generator'
```

```bash
bash examples/runnable/21-partner-update-generator/scripts/check_prereqs.sh
bash examples/runnable/21-partner-update-generator/scripts/install_cron.sh
```

## Smoke Test

- Trigger one run and verify final draft has clear sections: wins, blockers, next week.
- Confirm uncertain items are marked as pending, not stated as done.

## KPI

- Time to produce weekly partner update
- Partner clarification requests per update
- On-time update delivery rate

## Security Notes

- Keep external-facing drafts in review mode until approved.
- Filter out confidential internal details by default.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/partner-update-generator
cd ~/partner-update-generator
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

建立 `main.py`，實作 合作夥伴更新生成器 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_partner_update_generator():
    """執行 合作夥伴更新生成器 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 合作夥伴更新生成器 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_partner_update_generator()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/partner-update-generator && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
