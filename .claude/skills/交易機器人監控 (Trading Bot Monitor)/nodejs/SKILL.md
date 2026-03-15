---
name: 交易機器人監控 (Trading Bot Monitor)/nodejs
description: "Use Case #141 Node.js 方案: 交易機器人監控。使用 Node.js 實作 Trading Bot Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #141: 交易機器人監控 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# Trading Bot Monitor

## Introduction

Automated monitoring and recovery system for paper trading bots. Detects when bots crash or produce corrupted data, automatically restarts them, fixes data corruption, and sends health reports. Treats downtime as critical failure requiring immediate action.

**Why it matters**: Trading bots left down miss opportunities and generate stale data. Automated recovery ensures continuous operation without human intervention.

**Real-world example**: 4 active bots (DOGE Long/Short, v1 BTC Optimized, Hummingbot MM) monitored continuously. Agent detects dead bots, restarts, commits fixes, and sends morning health report with P&L summary.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `process` | Built-in | Monitor bot processes |
| `docker` | Built-in | Container management |
| `telegram` | Built-in | Health reports |
| `cron` | Built-in | Continuous monitoring |

## How to Setup

### 1. Bot Configuration

Create `config/bots.json`:

```json
{
  "bots": [
    {
      "name": "doge-long",
      "type": "spot",
      "check_interval": 300,
      "process_name": "doge_long_bot",
      "data_file": "data/doge_trades.csv",
      "health_endpoint": "http://localhost:8080/health"
    },
    {
      "name": "btc-optimized",
      "type": "futures",
      "check_interval": 60,
      "process_name": "btc_v1_bot",
      "data_file": "data/btc_trades.csv"
    }
  ]
}
```

### 2. Health Check Script

Create `scripts/bot-monitor.js`:

```javascript
const { exec } = require('child_process');
const fs = require('fs');

async function checkBot(bot) {
  // Check if process running
  const isRunning = await processExists(bot.process_name);
  
  // Check data file health
  const dataHealth = await checkDataFile(bot.data_file);
  
  // Check API responsiveness
  const apiHealth = await checkApi(bot.health_endpoint);
  
  return { isRunning, dataHealth, apiHealth };
}

async function recoverBot(bot) {
  if (!bot.isRunning) {
    await restartBot(bot);
  }
  if (bot.dataHealth.corrupted) {
    await fixCorruptedData(bot.data_file);
  }
  await logRecovery(bot);
}
```

### 3. Prompt Template

Add to your `SKILL.md`:

```markdown
## Trading Bot Monitor

Every 5 minutes:
1. Check all configured bots are running
2. Verify data files are not corrupted
3. Test API endpoints if available
4. If bot down: restart immediately
5. If data corrupted: restore from backup, replay from logs
6. Log all actions to memory/bot-operations.md

Morning report (08:00):
- Bot uptime status for last 24h
- P&L summary per bot
- Any restarts/recoveries performed
- Current positions summary

Critical alerts (immediate):
- Bot down for > 5 minutes
- Data corruption detected
- API key errors
- Abnormal trade frequency
```

### 4. Cron Configuration

```json
[
  {
    "schedule": "*/5 * * * *",
    "task": "bot_health_check"
  },
  {
    "schedule": "0 8 * * *",
    "task": "bot_morning_report"
  }
]
```

### 5. Recovery Procedures

```markdown
## Recovery Playbook

### Bot Not Running
1. Check logs: `docker logs ${bot_name}`
2. If OOM error: increase memory limit
3. If API error: check credentials
4. Restart: `docker-compose restart ${bot_name}`
5. Verify: wait 30s, check process again

### Data Corruption
1. Stop bot
2. Backup corrupted file: `mv trades.csv trades.csv.bak`
3. Restore from last good backup
4. Replay trades from exchange API
5. Verify data integrity
6. Restart bot

### API Errors
1. Check rate limits
2. Rotate API keys if needed
3. Reduce polling frequency temporarily
```

### 6. Health Report Format

```markdown
🤖 Bot Health Report - {{date}}

Uptime (24h):
- doge-long: 99.8% (1 restart at 03:15)
- btc-optimized: 100%
- hummingbot-mm: 99.2% (2 restarts)

P&L:
- doge-long: +$12.40 (+2.1%)
- btc-optimized: +$45.80 (+1.8%)
- hummingbot-mm: -$3.20 (-0.4%)

Actions Taken:
- 03:15: Restarted doge-long (memory limit)
- 05:42: Fixed btc data corruption

Current Status: ✅ All bots operational
```

## Success Metrics

- [ ] Bot uptime > 99.5% per week
- [ ] Recovery time < 2 minutes
- [ ] Zero missed trades due to downtime
- [ ] Data corruption detected within 1 hour

## Risk Management

| Risk | Mitigation |
|------|------------|
| Cascading restarts | Exponential backoff (5min, 15min, 30min) |
| Data loss | Hourly backups to S3 |
| API bans | Rate limit tracking per exchange |
| False positives | Require 2 failed checks before action |

---

*Example: Kimi (Moltbook) - "4 paper trading bots monitoring"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/trading-bot-monitor
cd ~/trading-bot-monitor
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

建立 `index.js`，實作 交易機器人監控 的核心邏輯。

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
      { role: "user", content: "請協助我執行 交易機器人監控 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/trading-bot-monitor && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
