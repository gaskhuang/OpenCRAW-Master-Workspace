---
name: 影子 AI 監控 (Shadow AI Watchlist)/nodejs
description: "Use Case #135 Node.js 方案: 影子 AI 監控。使用 Node.js 實作 Shadow AI Watchlist 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #135: 影子 AI 監控 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# 88 - Shadow-AI Watchlist

Builds a recurring shadow-AI watch queue from shadow-AI usage or unapproved tooling chatter.

## Skill Stack

```bash
npx clawhub@latest install slack
npx clawhub@latest install summarize
npx clawhub@latest install todoist
```

## What It Does

- Scans shadow-AI usage or unapproved tooling chatter from security and internal tooling
- Flags urgent exposure, review debt, or policy drift
- Produces a shadow-AI watch queue with evidence and recommended next steps

## Setup

```bash
export SYSTEM_SCOPE='internal tooling'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='16 8 * * 4'
export CRON_NAME='Shadow-AI Watchlist'
```

```bash
bash examples/runnable/88-shadow-ai-watchlist/scripts/check_prereqs.sh
bash examples/runnable/88-shadow-ai-watchlist/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the shadow-AI watch queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- shadow tool incidents surfaced
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
mkdir -p ~/shadow-ai-watchlist
cd ~/shadow-ai-watchlist
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

建立 `index.js`，實作 影子 AI 監控 的核心邏輯。

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
      { role: "user", content: "請協助我執行 影子 AI 監控 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/shadow-ai-watchlist && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
