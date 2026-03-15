---
name: 審批例外佇列 (Approval Exception Queue)/nodejs
description: "Use Case #129 Node.js 方案: 審批例外佇列。使用 Node.js 實作 Approval Exception Queue 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #129: 審批例外佇列 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 企業流程

---

## 原始需求 (來自 Source Repos)

# 58 - Approval Exception Queue

Builds a recurring approval exception board from approvals that are stalled or missing context.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Collects approvals that are stalled or missing context from configured operational sources
- Flags urgent, stale, or conflicting items
- Produces an approval exception board for daily review

## Setup

```bash
export TEAM_SCOPE='cross-functional approvals'
export MAX_ITEMS='25'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='46 10 * * 1-5'
export CRON_NAME='Approval Exception Queue'
```

```bash
bash examples/runnable/58-approval-exception-queue/scripts/check_prereqs.sh
bash examples/runnable/58-approval-exception-queue/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the approval exception board includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- approval cycle time
- time-to-intervention
- false-positive rate

## Security Notes

- Keep customer or internal operations content in trusted workspaces only.
- Start in draft-only mode and avoid automatic replies until operators trust the workflow.

## Failure Modes

- Stale inbox or task sync can surface outdated items.
- Low-quality inputs can create false urgency without a human review step.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/approval-exception-queue
cd ~/approval-exception-queue
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

建立 `index.js`，實作 審批例外佇列 的核心邏輯。

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
      { role: "user", content: "請協助我執行 審批例外佇列 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/approval-exception-queue && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
