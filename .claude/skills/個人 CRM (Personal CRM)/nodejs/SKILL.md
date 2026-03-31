---
name: 個人 CRM (Personal CRM)/nodejs
description: "Use Case #033 Node.js 方案: 個人 CRM。使用 Node.js 實作 Personal CRM 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #033: 個人 CRM — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Personal CRM with Automatic Contact Discovery

Keeping track of who you've met, when, and what you discussed is impossible to do manually. Important follow-ups slip through the cracks, and you forget context before important meetings.

This workflow builds and maintains a personal CRM automatically:

• Daily cron job scans email and calendar for new contacts and interactions
• Stores contacts in a structured database with relationship context
• Natural language queries: "What do I know about [person]?", "Who needs follow-up?", "When did I last talk to [person]?"
• Daily meeting prep briefing: before each day's meetings, researches external attendees via CRM + email history and delivers a briefing

## Skills you Need

- `gog` CLI (for Gmail and Google Calendar)
- Custom CRM database (SQLite or similar) or use the [crm-query](https://clawhub.ai) skill if available
- Telegram topic for CRM queries

## How to Set it Up

1. Create a CRM database:
```sql
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  first_seen TEXT,
  last_contact TEXT,
  interaction_count INTEGER,
  notes TEXT
);
```
2. Set up a Telegram topic called "personal-crm" for queries.
3. Prompt OpenClaw:
```text
Run a daily cron job at 6 AM to:
1. Scan my Gmail and Calendar for the past 24 hours
2. Extract new contacts and update existing ones
3. Log interactions (meetings, emails) with timestamps and context

Also, every morning at 7 AM:
1. Check my calendar for today's meetings
2. For each external attendee, search my CRM and email history
3. Deliver a briefing to Telegram with: who they are, when we last spoke, what we discussed, and any follow-up items

When I ask about a contact in the personal-crm topic, search the database and give me everything you know.
```


---

# 轻量级 CRM 更新

## 简介

通话或邮件后自动提取关键字段（阶段、价值、下一步），起草 CRM 更新。适合创始人主导的销售团队。

**为什么重要**：保持 CRM 数据最新，减少手动录入，提高销售效率。

**真实例子**：一位创始人使用此代理更新 CRM，每次客户沟通后代理自动提取信息并建议 CRM 更新，CRM 数据准确率从 60% 提升到 95%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `crm` | [ClawdHub](https://clawhub.com/skills/crm) | CRM 集成 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 邮件分析 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 信息提取 |

---

## 使用方式

### 分析沟通
分析邮件或会议记录

### 提取信息
- 销售阶段
- 预计金额
- 下一步行动
- 关键决策人

### 建议更新
代理起草 CRM 更新建议，用户一键确认

---

## 来源

- 来源：Quantum Byte


---

# Client Memory Hub

> Never forget a client conversation again. Track every touchpoint, remember every preference, nail every follow-up.

## The Problem

You're juggling 30+ clients across email, calls, Slack, WhatsApp, and meetings—and your brain isn't designed to remember that Sarah mentioned her kid's soccer tournament, that Marcus prefers Tuesday calls, or that you promised to check in with Lisa after her product launch. Sticky notes get lost, CRM updates feel like homework, and you've definitely followed up asking "how did the launch go?" when you already asked last week. The mental load of relationship management is 

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
mkdir personal-crm && cd personal-crm
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
personal-crm/
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
  // TODO: Implement data collection for Personal CRM
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
  logger.info('=== 個人 CRM ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 個人 CRM 報告\n\n${result}`);
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
pm2 start src/index.js --name personal-crm  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
