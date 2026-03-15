---
name: 設備問題分類 (Device Issue Triage Queue)/nodejs
description: "Use Case #136 Node.js 方案: 設備問題分類。使用 Node.js 實作 Device Issue Triage Queue 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #136: 設備問題分類 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/device-issue-triage-queue
cd ~/device-issue-triage-queue
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

建立 `index.js`，實作 設備問題分類 的核心邏輯。

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
      { role: "user", content: "請協助我執行 設備問題分類 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/device-issue-triage-queue && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
