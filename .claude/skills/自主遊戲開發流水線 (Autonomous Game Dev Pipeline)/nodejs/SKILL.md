---
name: 自主遊戲開發流水線 (Autonomous Game Dev Pipeline)/nodejs
description: "Use Case #013 Node.js 方案: 自主遊戲開發流水線。使用 Node.js 實作 Autonomous Game Dev Pipeline 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #013: 自主遊戲開發流水線 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# Autonomous Educational Game Development Pipeline

## Pain Point
**The Origin Story:** A "LANero of the old school" dad wanted to create a safe, ad-free, and high-quality gaming portal for his daughters, Susana (3) and Julieta (coming soon). Existing sites were plagued with spam, aggressive ads, and deceptive buttons (dark patterns) that frustrated his toddler.

**The Challenge:** Building a "clean, fast, and simple" portal was the easy part. The real challenge was populating it with **40+ educational games** tailored to specific developmental stages (0-15 years) without a team of developers. Manual development was too slow for a solo parent-developer, and maintaining consistency across dozens of games was becoming a nightmare.

## What It Does
This use case defines a "Game Developer Agent" that autonomously manages the entire lifecycle of a game's creation and maintenance. The workflow enforces a **"Bugs First"** policy where the agent must check for and resolve reported bugs before implementing new features.

**Efficiency:** This pipeline is capable of producing **1 new game or bugfix every 7 minutes**. The agent tirelessly iterates through the backlog of 41+ planned games, alternating between creating new content and correcting issues detected in previous cycles.

When the path is clear, the agent:
1.  **Selects**: Identifies the next game from a queue (`development-queue.md`) based on a "Round Robin" strategy to balance content across age groups.
2.  **Implements**: Writes HTML5/CSS3/JS code for the game, following strict `game-design-rules.md` (no frameworks, mobile-first, offline-capable).
3.  **Registers**: Automatically adds the game metadata to the central registry (`games-list.json`).
4.  **Documents**: Updates the `CHANGELOG.md` and `master-game-plan.md` status.
5.  **Deploys**: Handles the Git workflow: fetching master, creating a feature branch, committing changes with conventional commits, and merging back.

## Prompts

The core of this workflow is the **System Instructions** given to the agent. This prompt turns the LLM into a disciplined developer that respects the project's rigid structure.

*(**Note:** The actual prompts used in production are in **Spanish** (`es-419`) to align with the project's target audience (Latin American children) and potential future contributors from the region. The version below is translated for this documentation.)*

```text
Act as an Expert in Web Game Development and Child UX.
Your goal is to develop the next game in the production queue.

Please read and analyze the following context files before starting:

1.  BUG CONTEXT (Top Priority - CRITICAL):
    @[bugs/]
    (Check this folder. If there are files, YOUR TASK IS TO FIX **ONLY THE FIRST FILE** (in alphabetical order). Ignore the rest of the bugs and the game queue for now).

2.  QUEUE CONTEXT (Which game is next):
    @[development-queue.md]
    (Identify the game marked as [NEXT] in the "Next Games" section. ONLY if there are no bugs).

3. 

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
mkdir autonomous-game-dev-pipeline && cd autonomous-game-dev-pipeline
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
autonomous-game-dev-pipeline/
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
  // TODO: Implement data collection for Autonomous Game Dev Pipeline
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
  logger.info('=== 自主遊戲開發流水線 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 自主遊戲開發流水線 報告\n\n${result}`);
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
pm2 start src/index.js --name autonomous-game-dev-pipeline  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
