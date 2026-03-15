---
name: 入職清單管家 (Onboarding Checklist Concierge)/nodejs
description: "Use Case #132 Node.js 方案: 入職清單管家。使用 Node.js 實作 Onboarding Checklist Concierge 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #132: 入職清單管家 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 人力資源

---

## 原始需求 (來自 Source Repos)

# 73 - Onboarding Checklist Concierge

Builds a recurring onboarding readiness digest from new-hire onboarding tasks and readiness checks.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install todoist
npx clawhub@latest install slack
```

## What It Does

- Collects new-hire onboarding tasks and readiness checks from people workflows
- Flags delays, readiness gaps, and coordination risk
- Produces an onboarding readiness digest for hiring or people leads

## Setup

```bash
export TEAM_SCOPE='new hires'
export MAX_ITEMS='20'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='31 9 * * 4'
export CRON_NAME='Onboarding Checklist Concierge'
```

```bash
bash examples/runnable/73-onboarding-checklist-concierge/scripts/check_prereqs.sh
bash examples/runnable/73-onboarding-checklist-concierge/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the onboarding readiness digest includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- onboarding tasks completed on time
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
mkdir -p ~/onboarding-checklist-concierge
cd ~/onboarding-checklist-concierge
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

建立 `index.js`，實作 入職清單管家 的核心邏輯。

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
      { role: "user", content: "請協助我執行 入職清單管家 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/onboarding-checklist-concierge && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
