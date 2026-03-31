---
name: X 帳號質性分析 (X Account Qualitative Analysis)/nodejs
description: "Use Case #003 Node.js 方案: X 帳號質性分析。使用 Node.js 實作 X Account Qualitative Analysis 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #003: X 帳號質性分析 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# X Account Analysis

There are many websites designed to give you a qualitative analysis of your X account. While X already gives you an **analytics** section, it's more focused to show your numbers on your performance.

But a qualitative analysis focuses on the quality of your posts, not the performance stats. Some insights you can get from this type of analysis:
- What are the patterns that make my posts go viral?
- What topics I talk about get me most engagement?
- Why do I get posts with 1000+ likes but sometimes posts with <5 likes? What am I doing wrong?

There are many websites and apps designed to give you X analytics, but they focus on the statistics. There are probably 1-2 websites that let you talk with an AI to understand your performance. 

But now you can use OpenClaw to do this analysis for you, without needing to pay $10-$50 for subscriptions on these websites.

## Skills you Need
Bird Skill. `clawhub install bird` (it comes pre-bundled)

## How to Set it Up
Here's the flow:
1. Make sure Bird skill is working.
2. For security and isolation, you better create a new account for your ClawdBot.
3. Auth with your X account. log into x.com in Chrome/Brave, and provide the right cookie information (`auth-token`, `ct0`) so OpenClaw can access your account.
4. Ask OpenClaw to take a look at your real account, fetch the last N tweets, and ask it any questions you like. Alternatively, you can ask it to write you specific scripts.


---

# X 个人资料抓取器

## 简介

抓取 X 平台用户资料，分析影响力、内容主题、互动数据。

**为什么重要**：研究竞争对手，发现合作机会，分析趋势。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `twitter` | [ClawdHub](https://clawhub.com/skills/twitter) | X API |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |

---

## 使用方式

设置目标用户，定期获取分析报告

---

## 来源

- 作者：OpenClaw 社区


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
mkdir x-account-qualitative-analysis && cd x-account-qualitative-analysis
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
x-account-qualitative-analysis/
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
  // TODO: Implement data collection for X Account Qualitative Analysis
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
  logger.info('=== X 帳號質性分析 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 X 帳號質性分析 報告\n\n${result}`);
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
pm2 start src/index.js --name x-account-qualitative-analysis  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
