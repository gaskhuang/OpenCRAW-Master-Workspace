---
name: 內部 FAQ 路由 (Internal FAQ Router)/nodejs
description: "Use Case #137 Node.js 方案: 內部 FAQ 路由。使用 Node.js 實作 Internal FAQ Router 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #137: 內部 FAQ 路由 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 企業流程

---

## 原始需求 (來自 Source Repos)

# 99 - Internal FAQ Router

Builds a recurring internal FAQ queue from internal FAQ requests that need fast routing or reuse.

## Skill Stack

```bash
npx clawhub@latest install slack
npx clawhub@latest install summarize
npx clawhub@latest install notion
```

## What It Does

- Collects internal FAQ requests that need fast routing or reuse from configured operational sources
- Flags urgent, stale, or conflicting items
- Produces an internal FAQ queue for daily review

## Setup

```bash
export TEAM_SCOPE='internal support'
export MAX_ITEMS='25'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='33 11 * * 1-5'
export CRON_NAME='Internal FAQ Router'
```

```bash
bash examples/runnable/99-internal-faq-router/scripts/check_prereqs.sh
bash examples/runnable/99-internal-faq-router/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the internal FAQ queue includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- first-answer time
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
mkdir -p ~/internal-faq-router
cd ~/internal-faq-router
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

建立 `index.js`，實作 內部 FAQ 路由 的核心邏輯。

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
      { role: "user", content: "請協助我執行 內部 FAQ 路由 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/internal-faq-router && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
