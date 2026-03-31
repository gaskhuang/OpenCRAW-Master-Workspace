---
name: 家庭行事曆與家務助理 (Family Calendar & Chore Assistant)/nodejs
description: "Use Case #039 Node.js 方案: 家庭行事曆與家務助理。使用 Node.js 實作 Family Calendar & Chore Assistant 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #039: 家庭行事曆與家務助理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Family Calendar Aggregation & Household Assistant

Modern families juggle five or more calendars — work, personal, shared family, kids' school, extracurriculars — across different platforms and formats. Important events slip through the cracks because no single view exists. Meanwhile, household coordination (grocery lists, pantry inventory, appointment scheduling) happens through scattered text messages that get buried.

This use case turns OpenClaw into an always-on household coordinator: aggregating calendars into a morning briefing, monitoring messages for actionable items, and managing household logistics through a shared chat interface.

## Pain Point

- **Calendar fragmentation**: Work calendars have security restrictions preventing sharing. School calendars arrive as PDFs or hand-written websites. Camp schedules live in emails. Manually checking each one every morning is unsustainable — and "copying events across calendars works well until I forget and one slips through the cracks."
- **Household coordination overhead**: "How much milk do we have?" requires physically checking the fridge, then the basement pantry, then texting back. Multiply this across a week's worth of grocery runs.
- **Missed appointments**: Appointment confirmations arrive via text message and sit there unacted upon — no calendar event, no driving time buffer, no reminder.

## What It Does

- **Morning briefing**: Aggregates all family calendars into a single daily summary delivered via your preferred channel
- **Ambient message monitoring**: Watches iMessage/text conversations and automatically creates calendar events when it detects appointments (dentist confirmations, meeting plans, etc.)
- **Driving time buffers**: Adds travel time blocks before and after detected appointments
- **Household inventory**: Maintains a running inventory of pantry/fridge items that either partner can query from anywhere
- **Grocery coordination**: Deduplicates ingredients across recipes, tracks what's running low, and generates shopping lists
- **Photo-based input**: Snap a photo of a school calendar or freezer contents and the agent processes it into structured data

## Skills You Need

- Calendar API access (Google Calendar, Apple Calendar via `ical`)
- `imessage` skill for message monitoring (macOS only)
- Telegram or Slack for the shared family chat interface
- File system access for inventory tracking
- Camera/photo processing for OCR of physical calendars

## How to Set It Up

### 1. Calendar Aggregation

Configure OpenClaw to pull from all family calendar sources:

```text
## Calendar Sources

On morning briefing (8:00 AM):

1. Fetch my Google Work Calendar (read-only OAuth)
2. Fetch shared Family Google Calendar
3. Fetch partner's calendar (shared view)
4. Check ~/Documents/school-calendars/ for any new PDFs → OCR and extract events
5. Check recent emails for calendar attachments or event invitations

Compile into a single briefing:
- Today's events (all calendars, color-coded

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
mkdir family-calendar-&-chore-assistant && cd family-calendar-&-chore-assistant
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
family-calendar-&-chore-assistant/
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
  // TODO: Implement data collection for Family Calendar & Chore Assistant
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
  logger.info('=== 家庭行事曆與家務助理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 家庭行事曆與家務助理 報告\n\n${result}`);
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
pm2 start src/index.js --name family-calendar-&-chore-assistant  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
