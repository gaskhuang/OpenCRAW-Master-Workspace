---
name: 合作夥伴更新生成器 (Partner Update Generator)/nodejs
description: "Use Case #123 Node.js 方案: 合作夥伴更新生成器。使用 Node.js 實作 Partner Update Generator 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #123: 合作夥伴更新生成器 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# 21 - Partner Update Generator

Generates concise partner updates from recent internal activity and milestones.

## Skill Stack

```bash
npx clawhub@latest install gog
npx clawhub@latest install summarize
```

## What It Does

- Pulls recent project/customer signals from selected inbox and docs context
- Drafts partner-friendly weekly update with risks and asks
- Separates confirmed updates from pending items

## Setup

```bash
export UPDATE_SCOPE='partnership alpha'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='0 12 * * 5'
export CRON_NAME='Partner Update Generator'
```

```bash
bash examples/runnable/21-partner-update-generator/scripts/check_prereqs.sh
bash examples/runnable/21-partner-update-generator/scripts/install_cron.sh
```

## Smoke Test

- Trigger one run and verify final draft has clear sections: wins, blockers, next week.
- Confirm uncertain items are marked as pending, not stated as done.

## KPI

- Time to produce weekly partner update
- Partner clarification requests per update
- On-time update delivery rate

## Security Notes

- Keep external-facing drafts in review mode until approved.
- Filter out confidential internal details by default.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/partner-update-generator
cd ~/partner-update-generator
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

建立 `index.js`，實作 合作夥伴更新生成器 的核心邏輯。

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
      { role: "user", content: "請協助我執行 合作夥伴更新生成器 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/partner-update-generator && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
