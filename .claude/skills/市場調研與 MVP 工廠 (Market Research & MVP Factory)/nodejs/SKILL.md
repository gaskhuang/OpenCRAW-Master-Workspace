---
name: 市場調研與 MVP 工廠 (Market Research & MVP Factory)/nodejs
description: "Use Case #095 Node.js 方案: 市場調研與 MVP 工廠。使用 Node.js 實作 Market Research & MVP Factory 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #095: 市場調研與 MVP 工廠 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Market Research & Product Factory

You want to build a product but don't know what to build. Or you have a business and need to understand what your customers are struggling with. This workflow uses the Last 30 Days skill to mine Reddit and X for real pain points, then has OpenClaw build solutions to those problems.

## What It Does

- Researches any topic across Reddit and X over the last 30 days using the [Last 30 Days](https://github.com/matvanhorde/last-30-days) skill
- Surfaces real challenges, complaints, and feature requests people are posting about
- Helps you identify product opportunities from genuine user pain points
- Takes it a step further: ask OpenClaw to build an MVP that solves one of those challenges
- Creates a full research-to-product pipeline with zero coding on your part

## Pain Point

Most aspiring entrepreneurs struggle with the "what to build" problem. Market research traditionally means hours of manual browsing through forums, social media, and review sites. This automates the entire discovery-to-prototype pipeline.

## Skills You Need

- [Last 30 Days](https://github.com/matvanhorde/last-30-days) skill by Matt Van Horde
- Telegram or Discord integration for receiving research reports

## How to Set It Up

1. Install the Last 30 Days skill:
```text
Install this skill: https://github.com/matvanhorde/last-30-days
```

2. Run research on any topic:
```text
Please use the Last 30 Days skill to research challenges people are
having with [your topic here].

Organize the findings into:
- Top pain points (ranked by frequency)
- Specific complaints and feature requests
- Gaps in existing solutions
- Opportunities for a new product
```

3. Pick a pain point and have OpenClaw build a solution:
```text
Build me an MVP that solves [pain point from research].
Keep it simple — just the core functionality.
Ship it as a web app I can share with people.
```

4. For ongoing market intelligence, schedule regular research:
```text
Every Monday morning, use the Last 30 Days skill to research what
people are saying about [your niche] on Reddit and X. Summarize the
top opportunities and send them to my Telegram.
```

## Real World Example

```text
"Use the Last 30 Days skill to research challenges people are having with OpenClaw."

Results:
- Setup difficulty: Many users struggle with initial configuration
- Skill discovery: People can't find skills that do what they need
- Cost concerns: Users want cheaper model alternatives

→ "Build me a simple web app that makes OpenClaw setup easier with a guided wizard."

OpenClaw builds the app. You ship it. You have a product.
```

## Key Insights

- This is **entrepreneurship on autopilot**: find problems → validate demand → build solutions, all through text messages.
- The Last 30 Days skill gives you real, unfiltered user sentiment — not sanitized survey data.
- You don't need to be technical. OpenClaw does the research AND the building.
- Schedule weekly research to stay on top of evolving pain p

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
mkdir market-research-&-mvp-factory && cd market-research-&-mvp-factory
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
market-research-&-mvp-factory/
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
  // TODO: Implement data collection for Market Research & MVP Factory
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
  logger.info('=== 市場調研與 MVP 工廠 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 市場調研與 MVP 工廠 報告\n\n${result}`);
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
pm2 start src/index.js --name market-research-&-mvp-factory  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
