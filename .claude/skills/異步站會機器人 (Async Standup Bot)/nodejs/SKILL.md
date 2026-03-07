---
name: 異步站會機器人 (Async Standup Bot)/nodejs
description: "Use Case #053 Node.js 方案: 異步站會機器人。使用 Node.js 實作 Async Standup Bot 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #053: 異步站會機器人 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 🤖 Async Team Standup Bot

> Run standups without the meeting. Blockers surfaced, progress tracked, time saved.

---

## The Problem

Daily standups eat 15-30 minutes of everyone's time, often at the worst part of the morning. Half the team zones out during updates that don't affect them. Remote teams across timezones struggle to find a time that works. Real blockers get buried in routine updates, and nobody actually reads the notes afterward.

---

## The Solution

OpenClaw runs async standups: collects updates via DM at each person's preferred time, identifies blockers automatically, creates digestible summaries, and alerts the right people when action is needed. Your team gets focused time back while staying more informed than before.

---

## Setup Guide

### Step 1: Install Communication Skills

```bash
openclaw skill install slack          # Slack integration
openclaw skill install discord        # Discord support
openclaw skill install telegram       # Telegram bots
openclaw skill install linear         # Issue tracker integration
```

### Step 2: Define Team Structure

Create `~/openclaw/standups/team.json`:

```json
{
  "team": "Engineering",
  "members": [
    {"name": "Alice", "handle": "@alice", "timezone": "America/New_York", "promptTime": "09:00"},
    {"name": "Bob", "handle": "@bob", "timezone": "Europe/London", "promptTime": "09:30"},
    {"name": "Priya", "handle": "@priya", "timezone": "Asia/Kolkata", "promptTime": "10:00"}
  ],
  "summaryChannel": "#engineering-standups",
  "alertChannel": "#engineering-alerts",
  "manager": "@sarah"
}
```

### Step 3: Configure Standup Questions

Create `~/openclaw/standups/questions.md`:

```markdown
# Standup Questions

## Daily (Mon-Fri)
1. What did you accomplish yesterday?
2. What are you working on today?
3. Any blockers or need help with anything?

## Monday Addition
4. What's your main goal for this week?

## Friday Addition
4. What went well this week?
5. What could have gone better?

## Blocker Keywords
- stuck, blocked, waiting on, need help
- can't, unable to, delayed
- dependency, waiting for, blocked by
```

### Step 4: Set Up Blocker Detection

Create `~/openclaw/standups/alerts.md`:

```markdown
# Alert Rules

## Immediate Alert (DM manager)
- Blocker mentioned + "urgent" or "critical"
- Same blocker mentioned 2+ days in a row
- Team member hasn't responded in 48 hours

## Daily Summary Include
- All blockers with owner
- Cross-team dependencies
- Risks to sprint commitments

## Weekly Patterns to Flag
- Team member consistently blocked
- Recurring blocker themes
- Velocity drops
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `slack` | Slack DMs and channels |
| `discord` | Discord integration |
| `telegram` | Telegram bot support |
| `linear` | Link blockers to issues |

---

## Example Prompts

**Start standup collection:**
```
Send standup prompts to the engineering team. Use each person's preferred time.
```

**Generate summary:**
```
Create today's

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
mkdir async-standup-bot && cd async-standup-bot
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
async-standup-bot/
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
  // TODO: Implement data collection for Async Standup Bot
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
  logger.info('=== 異步站會機器人 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 異步站會機器人 報告\n\n${result}`);
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
pm2 start src/index.js --name async-standup-bot  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
