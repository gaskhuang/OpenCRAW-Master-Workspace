---
name: 逾期採購單追蹤 (Overdue PO Follow-up Queue)/nodejs
description: "Use Case #134 Node.js 方案: 逾期採購單追蹤。使用 Node.js 實作 Overdue PO Follow-up Queue 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #134: 逾期採購單追蹤 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/overdue-po-follow-up-queue
cd ~/overdue-po-follow-up-queue
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

建立 `index.js`，實作 逾期採購單追蹤 的核心邏輯。

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
      { role: "user", content: "請協助我執行 逾期採購單追蹤 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/overdue-po-follow-up-queue && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
