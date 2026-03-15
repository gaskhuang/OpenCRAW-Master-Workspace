---
name: 行銷素材請求路由 (Campaign Asset Request Router)/nodejs
description: "Use Case #130 Node.js 方案: 行銷素材請求路由。使用 Node.js 實作 Campaign Asset Request Router 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #130: 行銷素材請求路由 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 行銷自動化

---

## 原始需求 (來自 Source Repos)

# 70 - Campaign Asset Request Router

Builds a recurring campaign request queue from campaign asset requests that need prioritization and routing.

## Skill Stack

```bash
npx clawhub@latest install typeform
npx clawhub@latest install notion
npx clawhub@latest install slack
```

## What It Does

- Gathers campaign asset requests that need prioritization and routing from research and content signals
- Clusters themes, openings, and follow-up opportunities
- Produces a campaign request queue ready for review

## Setup

```bash
export TOPIC_SCOPE='marketing requests'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='10 14 * * 1-5'
export CRON_NAME='Campaign Asset Request Router'
```

```bash
bash examples/runnable/70-campaign-asset-request-router/scripts/check_prereqs.sh
bash examples/runnable/70-campaign-asset-request-router/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the campaign request queue includes evidence-backed prioritization.
- Confirm weak or low-confidence findings are called out instead of being presented as fact.

## KPI

- request turnaround time
- time-to-brief
- follow-up conversion rate

## Security Notes

- Cite sources clearly and keep low-confidence claims out of publish-ready output.
- Require human review before publishing external-facing content or competitive claims.

## Failure Modes

- Weak external signals can create noisy themes if the scope is too broad.
- Source freshness matters; stale material should be called out explicitly.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/campaign-asset-request-router
cd ~/campaign-asset-request-router
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

建立 `index.js`，實作 行銷素材請求路由 的核心邏輯。

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
      { role: "user", content: "請協助我執行 行銷素材請求路由 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/campaign-asset-request-router && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
