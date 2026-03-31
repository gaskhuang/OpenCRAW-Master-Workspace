---
name: 活動賓客電話確認 (Event Guest Phone Confirmation)/nodejs
description: "Use Case #045 Node.js 方案: 活動賓客電話確認。使用 Node.js 實作 Event Guest Phone Confirmation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #045: 活動賓客電話確認 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Event Guest Confirmation

You're hosting an event — a dinner party, a wedding, a company offsite — and you need to confirm attendance from a list of guests. Manually calling 20+ people is tedious: you play phone tag, forget who said what, and lose track of dietary restrictions or plus-ones. Texting works sometimes, but people ignore messages. A real phone call gets a much higher response rate.

This use case has OpenClaw call each guest on your list using the [SuperCall](https://clawhub.ai/xonder/supercall) plugin, confirm whether they're attending, collect any notes, and compile everything into a summary for you.

## What It Does

- Iterates through a guest list (names + phone numbers) and calls each one
- The AI introduces itself as your event coordinator with a friendly persona
- Confirms the event date, time, and location with the guest
- Asks if they're attending, and collects any notes (dietary needs, plus-ones, arrival time, etc.)
- After all calls are complete, compiles a summary: who confirmed, who declined, who didn't pick up, and any notes

## Why SuperCall

This use case works with the [SuperCall](https://clawhub.ai/xonder/supercall) plugin specifically — not the built-in `voice_call` plugin. The key difference: SuperCall is a fully standalone voice agent. The AI persona on the call **only has access to the context you provide** (the persona name, the goal, and the opening line). It cannot access your gateway agent, your files, your other tools, or anything else.

This matters for guest confirmation because:

- **Safety**: The person on the other end of the call can't manipulate or access your agent through the conversation. There's no risk of prompt injection or data leakage.
- **Better conversations**: Because the AI is scoped to a single focused task (confirm attendance), it stays on-topic and handles the call more naturally than a general-purpose voice agent would.
- **Batch-friendly**: You're making many calls to different people. A sandboxed persona that resets per call is exactly what you want — no bleed-over between conversations.

## Skills You Need

- [SuperCall](https://clawhub.ai/xonder/supercall) — install via `openclaw plugins install @xonder/supercall`
- A Twilio account with a phone number (for making outbound calls)
- An OpenAI API key (for the GPT-4o Realtime voice AI)
- ngrok (for webhook tunneling — free tier works)

See the [SuperCall README](https://github.com/xonder/supercall) for full configuration instructions.

## How to Set It Up

1. Install and configure SuperCall following the [setup guide](https://github.com/xonder/supercall#configuration). Make sure hooks are enabled in your OpenClaw config.

2. Prepare your guest list. You can paste it directly in chat or keep it in a file:

```text
Guest List — Summer BBQ, Saturday June 14th, 4 PM, 23 Oak Street

- Sarah Johnson: +15551234567
- Mike Chen: +15559876543
- Rachel Torres: +15555551234
- David Kim: +15558887777
```

3. Prompt OpenClaw:

```text
I need you

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
mkdir event-guest-phone-confirmation && cd event-guest-phone-confirmation
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
event-guest-phone-confirmation/
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
  // TODO: Implement data collection for Event Guest Phone Confirmation
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
  logger.info('=== 活動賓客電話確認 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 活動賓客電話確認 報告\n\n${result}`);
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
pm2 start src/index.js --name event-guest-phone-confirmation  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
