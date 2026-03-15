---
name: 面試匯報整理 (Candidate Debrief Compiler)/nodejs
description: "Use Case #131 Node.js 方案: 面試匯報整理。使用 Node.js 實作 Candidate Debrief Compiler 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #131: 面試匯報整理 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 人力資源

---

## 原始需求 (來自 Source Repos)

# 71 - Candidate Debrief Compiler

Builds a recurring candidate debrief brief from candidate interviews, notes, and scorecard signals.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install summarize
npx clawhub@latest install notion
```

## What It Does

- Collects candidate interviews, notes, and scorecard signals from people workflows
- Flags delays, readiness gaps, and coordination risk
- Produces a candidate debrief brief for hiring or people leads

## Setup

```bash
export TEAM_SCOPE='candidate pipeline'
export MAX_ITEMS='20'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='17 15 * * 1-5'
export CRON_NAME='Candidate Debrief Compiler'
```

```bash
bash examples/runnable/71-candidate-debrief-compiler/scripts/check_prereqs.sh
bash examples/runnable/71-candidate-debrief-compiler/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the candidate debrief brief includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- interviewer recap latency
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/candidate-debrief-compiler
cd ~/candidate-debrief-compiler
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

建立 `index.js`，實作 面試匯報整理 的核心邏輯。

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
      { role: "user", content: "請協助我執行 面試匯報整理 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/candidate-debrief-compiler && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
