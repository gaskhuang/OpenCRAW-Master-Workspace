---
name: Cron 儀表板狀態 (Cron Dashboard Status)/nodejs
description: "Use Case #161 Node.js 方案: Cron 儀表板狀態。使用 Node.js 實作 Cron Dashboard Status 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #161: Cron 儀表板狀態 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Cron Dashboard Status

## Introduction

Centralized monitoring dashboard for all cron jobs showing last run time, success/failure status, next scheduled run, and recent output summaries.

**Why it matters**: Cron jobs fail silently. Visibility prevents surprises and ensures reliability.

**Real-world example**: Agent displays 12 cron jobs, 2 failed overnight, human investigates and fixes before business impact.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Cron access |
| `filesystem` | Built-in | Log reading |

## How to Setup

### 1. Dashboard Script

```javascript
function showCronStatus() {
  const jobs = parseCrontab();
  jobs.forEach(job => {
    const lastRun = getLastRunLog(job);
    const status = lastRun.success ? '✓' : '✗';
    console.log(`${status} ${job.name} - Last: ${lastRun.time}`);
  });
}
```

### 2. Prompt Template

```markdown
## Cron Dashboard Status

On demand:
1. List all configured cron jobs
2. Show last execution time
3. Display success/failure status
4. Show recent output (last 10 lines)
5. Indicate next scheduled run
6. Alert if any job missed 2+ runs
```

## Success Metrics

- [ ] All jobs visible in dashboard
- [ ] Failures detected within 1 hour
- [ ] Historical logs accessible

---

*Example: Atmavictu (Moltbook) - "cron dashboard"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/cron-dashboard-status
cd ~/cron-dashboard-status
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

建立 `index.js`，實作 Cron 儀表板狀態 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Cron 儀表板狀態 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/cron-dashboard-status && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
