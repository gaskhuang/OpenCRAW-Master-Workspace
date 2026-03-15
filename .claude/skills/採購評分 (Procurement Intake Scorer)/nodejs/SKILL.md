---
name: 採購評分 (Procurement Intake Scorer)/nodejs
description: "Use Case #133 Node.js 方案: 採購評分。使用 Node.js 實作 Procurement Intake Scorer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #133: 採購評分 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/procurement-intake-scorer
cd ~/procurement-intake-scorer
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

建立 `index.js`，實作 採購評分 的核心邏輯。

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
      { role: "user", content: "請協助我執行 採購評分 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/procurement-intake-scorer && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
