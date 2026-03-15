---
name: 續約風險分析 (Renewal Risk Explainer)/nodejs
description: "Use Case #127 Node.js 方案: 續約風險分析。使用 Node.js 實作 Renewal Risk Explainer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #127: 續約風險分析 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# 43 - Renewal Risk Explainer

Builds a recurring renewal risk brief from renewal accounts showing health or adoption decline.

## Skill Stack

```bash
npx clawhub@latest install api-gateway
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Pulls renewal accounts showing health or adoption decline from configured go-to-market systems
- Highlights risk, opportunity, and missing follow-up
- Produces a renewal risk brief for revenue owners

## Setup

```bash
export ACCOUNT_SEGMENT='enterprise renewals'
export MAX_ITEMS='25'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='1 11 * * 1-5'
export CRON_NAME='Renewal Risk Explainer'
```

```bash
bash examples/runnable/43-renewal-risk-explainer/scripts/check_prereqs.sh
bash examples/runnable/43-renewal-risk-explainer/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the renewal risk brief includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- early-risk coverage
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/renewal-risk-explainer
cd ~/renewal-risk-explainer
npm init -y
npm install @anthropic-ai/sdk dotenv
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `index.js`，實作 續約風險分析 的核心邏輯。

```javascript
import Anthropic from "@anthropic-ai/sdk";
import dotenv from "dotenv";

dotenv.config();
const client = new Anthropic();

async function run() {
  const response = await client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "請協助我執行 續約風險分析 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/renewal-risk-explainer && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
