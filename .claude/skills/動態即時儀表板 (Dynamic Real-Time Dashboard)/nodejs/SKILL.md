---
name: 動態即時儀表板 (Dynamic Real-Time Dashboard)/nodejs
description: "Use Case #037 Node.js 方案: 動態即時儀表板。使用 Node.js 實作 Dynamic Real-Time Dashboard 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #037: 動態即時儀表板 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Dynamic Dashboard with Sub-agent Spawning

Static dashboards show stale data and require constant manual updates. You want real-time visibility across multiple data sources without building a custom frontend or hitting API rate limits.

This workflow creates a live dashboard that spawns sub-agents to fetch and process data in parallel:

• Monitors multiple data sources simultaneously (APIs, databases, GitHub, social media)
• Spawns sub-agents for each data source to avoid blocking and distribute API load
• Aggregates results into a unified dashboard (text, HTML, or Canvas)
• Updates every N minutes with fresh data
• Sends alerts when metrics cross thresholds
• Maintains historical trends in a database for visualization

## Pain Point

Building a custom dashboard takes weeks. By the time it's done, requirements have changed. Polling multiple APIs sequentially is slow and hits rate limits. You need insight now, not after a weekend of coding.

## What It Does

You define what you want to monitor conversationally: "Track GitHub stars, Twitter mentions, Polymarket volume, and system health." OpenClaw spawns sub-agents to fetch each data source in parallel, aggregates the results, and delivers a formatted dashboard to Discord or as an HTML file. Updates run automatically on a cron schedule.

Example dashboard sections:
- **GitHub**: stars, forks, open issues, recent commits
- **Social Media**: Twitter mentions, Reddit discussions, Discord activity
- **Markets**: Polymarket volume, prediction trends
- **System Health**: CPU, memory, disk usage, service status

## Skills Needed

- Sub-agent spawning for parallel execution
- `github` (gh CLI) for GitHub metrics
- `bird` (Twitter) for social data
- `web_search` or `web_fetch` for external APIs
- `postgres` for storing historical metrics
- Discord or Canvas for rendering the dashboard
- Cron jobs for scheduled updates

## How to Set it Up

1. Set up a metrics database:
```sql
CREATE TABLE metrics (
  id SERIAL PRIMARY KEY,
  source TEXT, -- e.g., "github", "twitter", "polymarket"
  metric_name TEXT,
  metric_value NUMERIC,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  source TEXT,
  condition TEXT,
  threshold NUMERIC,
  last_triggered TIMESTAMPTZ
);
```

2. Create a Discord channel for dashboard updates (e.g., #dashboard).

3. Prompt OpenClaw:
```text
You are my dynamic dashboard manager. Every 15 minutes, run a cron job to:

1. Spawn sub-agents in parallel to fetch data from:
   - GitHub: stars, forks, open issues, commits (past 24h)
   - Twitter: mentions of "@username", sentiment analysis
   - Polymarket: volume for tracked markets
   - System: CPU, memory, disk usage via shell commands

2. Each sub-agent writes results to the metrics database.

3. Aggregate all results and format a dashboard:

📊 **Dashboard Update** — [timestamp]

**GitHub**
- ⭐ Stars: [count] (+[change])
- 🍴 Forks: [count]
- 🐛 Open Issues: [count]
- 💻 Commits (24h): [count]

**Social Medi

---

## 所需套件

```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.39.0",
    "node-telegram-bot-api": "^0.66.0",
    "node-cron": "^3.0.3",
    "dotenv": "^16.4.7",
    "winston": "^3.17.0"
  }
}
```

安裝:
```bash
mkdir dynamic-real-time-dashboard && cd dynamic-real-time-dashboard
npm init -y && npm install @anthropic-ai/sdk node-telegram-bot-api node-cron dotenv winston
```

在 `package.json` 加入 `"type": "module"`

---

## 前置準備

- [ ] Node.js 18+ (`node --version`)
- [ ] Claude API Key
- [ ] Telegram Bot Token — 如需推送

---

## 專案結構

```
dynamic-real-time-dashboard/
├── .env
├── package.json
└── src/
    ├── index.js          # 主程式入口
    ├── config.js         # 設定管理
    ├── core.js           # 核心業務邏輯
    ├── notifier.js       # 通知推送
    └── logger.js         # 日誌
```

---

## 實作流程

### Step 1: config.js

```javascript
import 'dotenv/config';

const config = {
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
  telegramChatId: process.env.TELEGRAM_CHAT_ID,
};

export function validate() {
  const required = ['anthropicApiKey'];
  const missing = required.filter(k => !config[k]);
  if (missing.length) throw new Error(`Missing: ${missing.join(', ')}`);
}

export default config;
```

### Step 2: logger.js

```javascript
import winston from 'winston';
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.printf(({ timestamp, level, message }) =>
      `[${timestamp}] ${level.toUpperCase()}: ${message}`)
  ),
  transports: [new winston.transports.Console(), new winston.transports.File({ filename: 'app.log' })]
});
export default logger;
```

### Step 3: core.js

```javascript
import Anthropic from '@anthropic-ai/sdk';
import config from './config.js';
import logger from './logger.js';

export async function collectData() {
  // TODO: Implement data collection for Dynamic Real-Time Dashboard
  logger.info('Collecting data...');
  return null;
}

export async function analyzeWithAI(data) {
  const client = new Anthropic({ apiKey: config.anthropicApiKey });
  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4096,
    messages: [{ role: 'user', content: `請分析以下資料並產生繁體中文報告：\n\n${data}` }]
  });
  return response.content[0].text;
}
```

### Step 4: notifier.js

```javascript
import TelegramBot from 'node-telegram-bot-api';
import config from './config.js';

export async function sendTelegram(text) {
  if (!config.telegramBotToken) return;
  const bot = new TelegramBot(config.telegramBotToken);
  const maxLen = 4096;
  for (let i = 0; i < text.length; i += maxLen) {
    const chunk = text.slice(i, i + maxLen);
    try { await bot.sendMessage(config.telegramChatId, chunk, { parse_mode: 'Markdown' }); }
    catch { await bot.sendMessage(config.telegramChatId, chunk); }
  }
}
```

### Step 5: index.js

```javascript
import cron from 'node-cron';
import config, { validate } from './config.js';
import { collectData, analyzeWithAI } from './core.js';
import { sendTelegram } from './notifier.js';
import logger from './logger.js';

async function run() {
  logger.info('=== 動態即時儀表板 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 動態即時儀表板 報告\n\n${result}`);
    logger.info('✅ Done!');
  } else {
    logger.warn('No data collected');
  }
}

const args = process.argv.slice(2);
if (args.includes('--run-once')) {
  run();
} else {
  cron.schedule('0 9 * * *', run);
  logger.info('Cron started...');
}
```

### Step 6: 執行

```bash
node src/index.js --run-once  # 測試
node src/index.js             # 啟動排程
pm2 start src/index.js --name dynamic-real-time-dashboard  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
