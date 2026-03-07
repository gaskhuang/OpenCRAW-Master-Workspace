---
name: 訂閱費用審計 (Subscription Cost Audit)/nodejs
description: "Use Case #105 Node.js 方案: 訂閱費用審計。使用 Node.js 實作 Subscription Cost Audit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #105: 訂閱費用審計 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# 💳 Expense Tracker & Analyzer

> Know where your money goes. Without manual data entry.

---

## The Problem

Tracking expenses is tedious. You start with good intentions, manually log for a week, then stop. Bank statements show transactions but no insights. By month-end, you're wondering where the money went.

---

## The Solution

OpenClaw automatically categorizes transactions, identifies spending patterns, alerts on unusual charges, and gives you clear insights—no manual entry required.

---

## Setup Guide

### Step 1: Install Finance Skills

```bash
openclaw skill install copilot-money  # or plaid
openclaw skill install excel
```

### Step 2: Configure Categories

Create `~/openclaw/expenses/categories.json`:

```json
{
  "categories": {
    "essentials": ["rent", "utilities", "groceries", "insurance"],
    "transport": ["uber", "lyft", "gas", "transit"],
    "food": ["restaurants", "delivery", "coffee"],
    "subscriptions": ["netflix", "spotify", "gym"],
    "shopping": ["amazon", "clothing"],
    "health": ["pharmacy", "doctor"]
  },
  "budgets": {
    "food": 500,
    "subscriptions": 100,
    "shopping": 300
  }
}
```

### Step 3: Set Alert Rules

Create `~/openclaw/expenses/alerts.md`:

```markdown
# Expense Alerts

## Notify Immediately
- Transactions > $100
- New recurring charges
- International transactions
- Declined transactions

## Weekly Check
- Category over budget by >20%
- Unusual spending pattern
- Forgotten subscriptions

## Monthly Review
- Total vs budget
- Category breakdown
- Subscription audit
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `copilot-money` | Bank account integration |
| `plaid` | Financial data aggregation |
| `excel` | Export and analysis |

---

## Example Prompts

**Daily update:**
```
What did I spend today? Anything unusual?
```

**Weekly review:**
```
Give me my spending breakdown this week by category. How am I tracking against budgets?
```

**Find waste:**
```
Identify any subscriptions I haven't used in 30 days. Any duplicate services?
```

**Trend analysis:**
```
How does my food spending this month compare to the last 3 months? What's driving changes?
```

---

## Cron Schedule

```
0 8 * * *      # 8 AM - yesterday's transactions summary
0 10 * * 1     # Monday 10 AM - weekly spending report
0 9 1 * *      # 1st of month - monthly budget review
0 0 15 * *     # 15th of month - mid-month check-in
```

---

## Expected Results

**Week 1:**
- All transactions auto-categorized
- Spending visibility achieved

**Month 1:**
- Identify 10-20% wasteful spending
- Clear budget tracking

**Month 3:**
- Spending habits improved
- No surprise charges
- Financial goals on track


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
mkdir subscription-cost-audit && cd subscription-cost-audit
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
subscription-cost-audit/
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
  // TODO: Implement data collection for Subscription Cost Audit
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
  logger.info('=== 訂閱費用審計 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 訂閱費用審計 報告\n\n${result}`);
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
pm2 start src/index.js --name subscription-cost-audit  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
