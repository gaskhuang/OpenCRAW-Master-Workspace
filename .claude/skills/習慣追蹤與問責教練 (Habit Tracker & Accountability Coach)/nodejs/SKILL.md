---
name: 習慣追蹤與問責教練 (Habit Tracker & Accountability Coach)/nodejs
description: "Use Case #043 Node.js 方案: 習慣追蹤與問責教練。使用 Node.js 實作 Habit Tracker & Accountability Coach 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #043: 習慣追蹤與問責教練 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Habit Tracker & Accountability Coach

You've tried every habit tracker app out there. They all work for a week, then you stop opening them. The problem isn't the app — it's that tracking habits is passive. What if your agent actively reached out to you, asked how your day went, and adapted its approach based on whether you're on a streak or falling off?

This use case turns OpenClaw into a proactive accountability partner that checks in with you daily via Telegram or SMS.

## Pain Point

Habit apps rely on you remembering to open them. Push notifications are easy to ignore. What actually works for behavior change is **active accountability** — someone (or something) that asks you directly, celebrates your wins, and nudges you when you slip. This agent does exactly that, without the awkwardness of bugging a friend.

## What It Does

- **Daily check-ins** via Telegram or SMS at times you choose (e.g., 7 AM for morning routine, 9 PM for end-of-day review)
- **Tracks habits** you define — exercise, reading, meditation, water intake, coding, whatever matters to you
- **Streak tracking** — knows your current streak for each habit and references it in messages
- **Adaptive nudges** — adjusts tone based on your performance (encouraging when you're consistent, gently persistent when you miss days)
- **Weekly reports** — summarizes your week with completion rates, longest streaks, and patterns (e.g., "You tend to skip workouts on Wednesdays")

## Skills You Need

- Telegram or SMS integration (Twilio for SMS, or Telegram Bot API)
- Scheduling / cron for timed check-ins
- File system or database access for storing habit data
- Optional: Google Sheets integration for a visual habit dashboard

## How to Set It Up

1. Define your habits and check-in schedule:
```text
I want you to be my accountability coach. Track these daily habits for me:

1. Morning workout (check in at 7:30 AM)
2. Read for 30 minutes (check in at 8:00 PM)
3. No social media before noon (check in at 12:30 PM)
4. Drink 8 glasses of water (check in at 6:00 PM)

Send me a Telegram message at each check-in time asking if I completed
the habit. Keep track of my streaks in a local file.
```

2. Set up the tracking and tone:
```text
When I confirm a habit, respond with a short encouraging message and
mention my current streak. Example: "Day 12 of morning workouts. Solid."

When I miss a habit, don't guilt-trip me. Just acknowledge it and remind
me why I started. If I miss 3 days in a row, send a longer motivational
message and ask if I want to adjust the goal.

If I don't respond to a check-in within 2 hours, send one follow-up.
Don't spam me after that.
```

3. Add weekly reports:
```text
Every Sunday at 10 AM, send me a weekly summary:
- Completion rate for each habit
- Current streaks
- Best day and worst day
- One pattern you noticed (e.g., "You always skip reading on Fridays")
- One suggestion for next week

Store all data in ~/habits/log.json so I can review history anytime.
```

4. Option

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
mkdir habit-tracker-&-accountability-coach && cd habit-tracker-&-accountability-coach
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
habit-tracker-&-accountability-coach/
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
  // TODO: Implement data collection for Habit Tracker & Accountability Coach
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
  logger.info('=== 習慣追蹤與問責教練 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 習慣追蹤與問責教練 報告\n\n${result}`);
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
pm2 start src/index.js --name habit-tracker-&-accountability-coach  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
