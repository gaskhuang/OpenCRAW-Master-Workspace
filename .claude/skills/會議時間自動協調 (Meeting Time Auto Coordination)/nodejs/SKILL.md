---
name: 會議時間自動協調 (Meeting Time Auto Coordination)/nodejs
description: "Use Case #054 Node.js 方案: 會議時間自動協調。使用 Node.js 實作 Meeting Time Auto Coordination 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #054: 會議時間自動協調 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 🗓️ Smart Meeting Scheduler

> Schedule meetings in seconds. Timezone math done for you, conflicts detected, follow-ups automated.

---

## The Problem

Scheduling meetings across timezones is a nightmare. You're juggling Calendly links, checking five people's availability, doing timezone math in your head, and manually sending follow-up reminders. Half the meeting gets wasted because nobody sent an agenda, and action items disappear into the void after the call ends.

---

## The Solution

OpenClaw handles the entire meeting lifecycle: finds times that work across timezones, checks everyone's availability, sends calendar invites with context, reminds participants before the meeting, and automatically captures and distributes follow-up action items.

---

## Setup Guide

### Step 1: Install Calendar Skills

```bash
openclaw skill install calendar       # Google Calendar integration
openclaw skill install ical           # iCal/Apple Calendar support
openclaw skill install remind-me      # Smart reminders
openclaw skill install gmail          # Email invites
```

### Step 2: Configure Timezone Preferences

Create `~/openclaw/meetings/config.json`:

```json
{
  "myTimezone": "America/New_York",
  "workingHours": {
    "start": "09:00",
    "end": "18:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  },
  "bufferMinutes": 15,
  "defaultDuration": 30,
  "preferredTimes": ["10:00", "14:00", "16:00"],
  "avoidTimes": ["12:00-13:00"]
}
```

### Step 3: Set Up Contact Timezones

Create `~/openclaw/meetings/contacts.json`:

```json
{
  "contacts": [
    {"name": "Sarah", "email": "sarah@example.com", "timezone": "Europe/London"},
    {"name": "Raj", "email": "raj@example.com", "timezone": "Asia/Kolkata"},
    {"name": "Alex", "email": "alex@example.com", "timezone": "America/Los_Angeles"}
  ]
}
```

### Step 4: Create Meeting Templates

Create `~/openclaw/meetings/templates.md`:

```markdown
# Meeting Templates

## Quick Sync (15 min)
- No agenda required
- Reminder: 5 min before

## 1:1 (30 min)
- Include talking points
- Reminder: 1 hour before
- Follow-up: Action items within 24h

## Team Meeting (60 min)
- Agenda required 24h before
- Reminder: 1 day + 1 hour before
- Follow-up: Notes + recording link
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `calendar` | Google Calendar read/write |
| `ical` | Apple Calendar support |
| `remind-me` | Pre-meeting reminders |
| `gmail` | Send invites and follow-ups |

---

## Example Prompts

**Schedule a meeting:**
```
Schedule a 30-min call with Sarah and Raj sometime next week. 
Find a time that works for all timezones.
```

**Check availability:**
```
What does my Thursday look like? When am I free for a 1-hour meeting?
```

**Timezone conversion:**
```
If I schedule a call at 3 PM my time, what time is that for Sarah in London and Raj in Mumbai?
```

**Meeting follow-up:**
```
We just finished the product sync. Send follow-up notes to all participants 
with the

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
mkdir meeting-time-auto-coordination && cd meeting-time-auto-coordination
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
meeting-time-auto-coordination/
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
  // TODO: Implement data collection for Meeting Time Auto Coordination
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
  logger.info('=== 會議時間自動協調 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 會議時間自動協調 報告\n\n${result}`);
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
pm2 start src/index.js --name meeting-time-auto-coordination  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
