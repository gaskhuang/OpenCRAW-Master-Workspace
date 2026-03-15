---
name: 試用轉付費推動 (Trial to Paid Nudger)/nodejs
description: "Use Case #128 Node.js 方案: 試用轉付費推動。使用 Node.js 實作 Trial to Paid Nudger 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #128: 試用轉付費推動 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# 45 - Trial-to-Paid Nudger

Builds a recurring trial conversion follow-up queue from trial accounts nearing conversion deadlines.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Pulls trial accounts nearing conversion deadlines from configured go-to-market systems
- Highlights risk, opportunity, and missing follow-up
- Produces a trial conversion follow-up queue for revenue owners

## Setup

```bash
export ACCOUNT_SEGMENT='self-serve trials'
export MAX_ITEMS='25'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='15 13 * * 1-5'
export CRON_NAME='Trial-to-Paid Nudger'
```

```bash
bash examples/runnable/45-trial-to-paid-nudger/scripts/check_prereqs.sh
bash examples/runnable/45-trial-to-paid-nudger/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the trial conversion follow-up queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- trial conversion rate
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
mkdir -p ~/trial-to-paid-nudger
cd ~/trial-to-paid-nudger
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

建立 `index.js`，實作 試用轉付費推動 的核心邏輯。

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
      { role: "user", content: "請協助我執行 試用轉付費推動 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/trial-to-paid-nudger && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
