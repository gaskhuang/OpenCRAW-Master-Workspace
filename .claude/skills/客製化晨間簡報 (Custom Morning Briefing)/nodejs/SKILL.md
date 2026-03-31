---
name: 客製化晨間簡報 (Custom Morning Briefing)/nodejs
description: "Use Case #041 Node.js 方案: 客製化晨間簡報。使用 Node.js 實作 Custom Morning Briefing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #041: 客製化晨間簡報 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Custom Morning Brief

You wake up and spend the first 30 minutes of your day catching up — scrolling news, checking your calendar, reviewing your to-do list, trying to figure out what matters today. What if all of that was already done and waiting for you as a text message?

This workflow has OpenClaw send you a fully customized morning briefing every day at a scheduled time, covering news, tasks, ideas, and proactive recommendations.

## What It Does

- Sends a structured morning report to Telegram, Discord, or iMessage at the same time every day (e.g., 8:00 AM)
- Researches overnight news relevant to your interests by browsing the web
- Reviews your to-do list and surfaces tasks for the day
- Generates creative output (full scripts, email drafts, business proposals — not just ideas) while you sleep
- Recommends tasks the AI can complete autonomously to help you that day

## Pain Point

You're spending your most productive morning hours just getting oriented. Meanwhile, your AI agent sits idle all night. The morning brief turns idle overnight hours into productive prep time — you wake up to work already done.

## Skills You Need

- Telegram, Discord, or iMessage integration
- Todoist / Apple Reminders / Asana integration (whichever you use for tasks)
- [x-research-v2](https://clawhub.ai) for social media trend research (optional)

## How to Set It Up

1. Connect OpenClaw to your messaging platform and task manager.

2. Prompt OpenClaw:
```text
I want to set up a regular morning brief. Every morning at 8:00 AM,
send me a report through Telegram.

I want this report to include:
1. News stories relevant to my interests (AI, startups, tech)
2. Ideas for content I can create today
3. Tasks I need to complete today (pull from my to-do list)
4. Recommendations for tasks you can complete for me today

For the content ideas, write full draft scripts/outlines — not just titles.
```

3. OpenClaw will schedule this automatically. Verify it's working by checking your messages the next morning.

4. Customize over time — just text your bot:
```text
Add weather forecast to my morning brief.
Stop including general news, focus only on AI.
Include a motivational quote each morning.
```

5. If you can't think of what to include, you don't have to — just say:
```text
I want this report to include things relevant to me.
Think of what would be most helpful to put in this report.
```

## Key Insights

- The AI-recommended tasks section is the most powerful part — it has the agent proactively think of ways to help you, rather than waiting for instructions.
- You can customize the brief just by texting. Say "Add stock prices to my morning brief" and it updates.
- Full drafts (not just ideas) are the key to saving time. Wake up to scripts, not suggestions.
- It doesn't matter what industry you're in — a morning brief with tasks, news, and proactive suggestions is universally useful.

## Based On

Inspired by [Alex Finn's video on life-changing OpenClaw use cases](https:

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
mkdir custom-morning-briefing && cd custom-morning-briefing
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
custom-morning-briefing/
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
  // TODO: Implement data collection for Custom Morning Briefing
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
  logger.info('=== 客製化晨間簡報 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 客製化晨間簡報 報告\n\n${result}`);
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
pm2 start src/index.js --name custom-morning-briefing  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
