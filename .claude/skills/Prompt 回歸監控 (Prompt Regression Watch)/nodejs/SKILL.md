---
name: Prompt 回歸監控 (Prompt Regression Watch)/nodejs
description: "Use Case #126 Node.js 方案: Prompt 回歸監控。使用 Node.js 實作 Prompt Regression Watch 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #126: Prompt 回歸監控 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: AI 運維

---

## 原始需求 (來自 Source Repos)

# 42 - Prompt Regression Watch

Builds a recurring prompt regression brief from model cost and behavior anomalies after prompt or configuration changes.

## Skill Stack

```bash
npx clawhub@latest install model-usage
npx clawhub@latest install summarize
npx clawhub@latest install slack
```

## What It Does

- Scans model cost and behavior anomalies after prompt or configuration changes across configured engineering tools
- Ranks issues by risk, recurrence, and delivery impact
- Produces a prompt regression brief for operator review

## Setup

```bash
export TARGET_SCOPE='high-traffic prompts'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='54 10 * * 1-5'
export CRON_NAME='Prompt Regression Watch'
```

```bash
bash examples/runnable/42-prompt-regression-watch/scripts/check_prereqs.sh
bash examples/runnable/42-prompt-regression-watch/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the prompt regression brief includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- regressions caught before rollout
- triage latency
- repeat issue escape rate

## Security Notes

- Use read-only repository or analytics scopes for the first rollout.
- Deliver only to trusted engineering channels and require human review for follow-up writes.

## Failure Modes

- Missing repository scopes can hide critical context.
- Noisy data can over-rank low-value issues unless thresholds are tuned.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/prompt-regression-watch
cd ~/prompt-regression-watch
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

建立 `index.js`，實作 Prompt 回歸監控 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Prompt 回歸監控 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/prompt-regression-watch && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
