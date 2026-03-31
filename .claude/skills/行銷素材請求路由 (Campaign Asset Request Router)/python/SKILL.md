---
name: 行銷素材請求路由 (Campaign Asset Request Router)/python
description: "Use Case #130 Python 方案: 行銷素材請求路由。使用 Python 實作 Campaign Asset Request Router 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #130: 行銷素材請求路由 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 行銷自動化

---

## 原始需求 (來自 Source Repos)

# 70 - Campaign Asset Request Router

Builds a recurring campaign request queue from campaign asset requests that need prioritization and routing.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Gathers campaign asset requests that need prioritization and routing from research and content signals
- Clusters themes, openings, and follow-up opportunities
- Produces a campaign request queue ready for review

## Setup

```bash
export TOPIC_SCOPE='marketing requests'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='10 14 * * 1-5'
export CRON_NAME='Campaign Asset Request Router'
```

```bash
bash examples/runnable/70-campaign-asset-request-router/scripts/check_prereqs.sh
bash examples/runnable/70-campaign-asset-request-router/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the campaign request queue includes evidence-backed prioritization.
- Confirm weak or low-confidence findings are called out instead of being presented as fact.

## KPI

- request turnaround time
- time-to-brief
- follow-up conversion rate

## Security Notes

- Cite sources clearly and keep low-confidence claims out of publish-ready output.
- Require human review before publishing external-facing content or competitive claims.

## Failure Modes

- Weak external signals can create noisy themes if the scope is too broad.
- Source freshness matters; stale material should be called out explicitly.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/campaign-asset-request-router
cd ~/campaign-asset-request-router
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

建立 `main.py`，實作 行銷素材請求路由 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_campaign_asset_request_router():
    """執行 行銷素材請求路由 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 行銷素材請求路由 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_campaign_asset_request_router()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/campaign-asset-request-router && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
