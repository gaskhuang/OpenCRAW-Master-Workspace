---
name: 功能需求分類 (Feature Request Triage)/nodejs
description: "Use Case #124 Node.js 方案: 功能需求分類。使用 Node.js 實作 Feature Request Triage 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #124: 功能需求分類 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 產品管理

---

## 原始需求 (來自 Source Repos)

# 25 - Feature Request Triage

Converts incoming feature requests into an evidence-ranked engineering queue.

## Skill Stack

```bash
npx clawhub@latest install github
npx clawhub@latest install summarize
npx clawhub@latest install todoist
```

## What It Does

- Pulls new feature issues and related discussion context
- Deduplicates overlapping requests
- Outputs prioritized triage list with rationale and proposed next action

## Setup

```bash
export REPO='owner/repo'
export ISSUE_LABEL='feature-request'
export WINDOW_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='0 14 * * 1-5'
export CRON_NAME='Feature Request Triage'
```

```bash
bash examples/runnable/25-feature-request-triage/scripts/check_prereqs.sh
bash examples/runnable/25-feature-request-triage/scripts/install_cron.sh
```

## Smoke Test

- Trigger one run and verify duplicate requests are grouped.
- Confirm each priority item has issue link + action recommendation.

## KPI

- Median issue triage time
- Duplicate request ratio
- Time-to-first-response for feature requests

## Security Notes

- Keep repo access read-only for analysis phase.
- Avoid exposing private issues in broad channels.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/feature-request-triage
cd ~/feature-request-triage
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

建立 `index.js`，實作 功能需求分類 的核心邏輯。

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
      { role: "user", content: "請協助我執行 功能需求分類 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/feature-request-triage && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
