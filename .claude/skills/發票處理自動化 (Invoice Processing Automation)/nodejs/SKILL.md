---
name: 發票處理自動化 (Invoice Processing Automation)/nodejs
description: "Use Case #106 Node.js 方案: 發票處理自動化。使用 Node.js 實作 Invoice Processing Automation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #106: 發票處理自動化 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# Invoice Chaser

> Automated invoice tracking and payment reminders for freelancers and small businesses

## The Problem

Chasing unpaid invoices is awkward, time-consuming, and easy to forget—leading to cash flow problems that kill otherwise healthy businesses. Freelancers especially struggle: you're busy doing actual work, and manually tracking who owes what, when it's due, and who needs a nudge feels like a second job. Meanwhile, that $3,000 invoice from 45 days ago quietly slips through the cracks.

## The Solution

OpenClaw becomes your accounts receivable assistant. It tracks invoices from email confirmations, manual input, or CSV imports, then automatically sends polite reminder emails at customizable intervals (7, 14, 30 days overdue). It learns which clients pay slow vs. fast, warns you about potential cash flow gaps, and keeps a running ledger you can query anytime with natural language ("Who owes me money?" / "What's my expected income this month?").

---

## Setup Guide

### Step 1: Create Your Invoice Tracker File

Create `invoices.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/data
cat > ~/openclaw/data/invoices.json << 'EOF'
{
  "invoices": [],
  "clients": {},
  "settings": {
    "reminder_days": [7, 14, 30],
    "currency": "USD",
    "your_name": "YOUR NAME",
    "your_email": "your@email.com",
    "payment_terms": "Net 30"
  }
}
EOF
```

### Step 2: Create the Invoice Template

Create `~/openclaw/templates/invoice-reminder.md`:

```markdown
Subject: Friendly Reminder: Invoice #{{invoice_id}} - {{days_overdue}} days overdue

Hi {{client_name}},

I hope you're doing well! I wanted to follow up on Invoice #{{invoice_id}} for {{amount}} {{currency}}, which was due on {{due_date}}.

**Invoice Details:**
- Invoice #: {{invoice_id}}
- Amount: {{amount}} {{currency}}
- Due Date: {{due_date}}
- Days Overdue: {{days_overdue}}
- Description: {{description}}

If payment has already been sent, please disregard this message—and thank you!

If you have any questions or need to discuss payment arrangements, I'm happy to chat.

Best regards,
{{your_name}}
```

### Step 3: Set Up Email Access

Ensure OpenClaw has email skills configured. Add to your `skills/` directory or verify existing email integration works:

```bash
# Test email access
openclaw run "Check my inbox for any emails containing 'invoice' or 'payment'"
```

### Step 4: Add Your First Invoice

Simply tell OpenClaw:

```
Add invoice: Client "Acme Corp", $2,500 for "Website Redesign", 
invoice #INV-2024-001, due date Jan 15 2025, 
contact email: billing@acmecorp.com
```

### Step 5: Configure Cron Jobs (see section below)

### Step 6: Test the System

```
Show me all outstanding invoices
```

---

## Skills Needed

| Skill | Purpose | Required? |
|-------|---------|-----------|
| **Email (Gmail/IMAP)** | Send reminder emails, scan for payment confirmations | ✅ Yes |
| **File System** | Store invoice data in JSON | ✅ Built-in |
| **Calendar** | Track due dates, sched

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
mkdir invoice-processing-automation && cd invoice-processing-automation
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
invoice-processing-automation/
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
  // TODO: Implement data collection for Invoice Processing Automation
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
  logger.info('=== 發票處理自動化 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 發票處理自動化 報告\n\n${result}`);
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
pm2 start src/index.js --name invoice-processing-automation  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
