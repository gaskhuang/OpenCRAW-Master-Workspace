---
name: Reddit 產品聲量追蹤 (Reddit Product Buzz Tracking)/nodejs
description: "Use Case #008 Node.js 方案: Reddit 產品聲量追蹤。使用 Node.js 實作 Reddit Product Buzz Tracking 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #008: Reddit 產品聲量追蹤 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# Daily Reddit Digest
Run a daily digest everyday to give you the top performing posts from your favourite subreddits.

What to use it for:

• Browsing subreddits (hot/new/top posts)
• Searching posts by topic
• Pulling comment threads for context
• Building shortlists of posts to manually review/reply to later

> It's read-only. No posting, voting, or commenting.

## Skills you Need
[reddit-readonly](https://clawhub.ai/buksan1950/reddit-readonly) skill. It doesn't need auth. 

## How to Set it Up
After installing the skill, prompt your OpenClaw:
```text
I want you to give me the top performing posts from the following subreddits.
<paste the list here>
Create a separate memory for the reddit processes, about the type of posts I like to see and every day ask me if I liked the list you provided. Save my preference as rules in the memory to use for a better digest curation. (e.g. do not include memes.)
Every day at 5pm, run this process and give me the digest.
```

---

# 客户信号扫描器

## 简介

扫描客户行为信号，识别 upsell 机会、流失风险、满意度变化。

**为什么重要**：主动客户管理，提高留存率，发现增长机会。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `crm` | [ClawdHub](https://clawhub.com/skills/crm) | 客户数据 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 行为分析 |

---

## 使用方式

连接客户数据源，设置信号规则

---

## 来源

- 作者：OpenClaw 社区


---

# Competitor Radar 🎯

> Automated competitive intelligence that keeps you one step ahead

## The Problem

You're building a product but have no idea what competitors are doing until customers tell you they switched. Manually checking competitor websites, blogs, and social media is a time sink that falls off your radar within a week. By the time you notice a competitor launched a killer feature or slashed prices, you've already lost deals.

## The Solution

OpenClaw becomes your always-on competitive intelligence analyst. It monitors competitor websites for pricing changes, scans their blogs for product announcements, tracks their social media activity, and delivers a weekly digest with strategic recommendations. When something big happens (major price drop, new feature launch), you get an instant alert.

---

## Setup Guide

### Step 1: Create Your Competitor Config File

Create `competitors.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/competitor-radar
```

```json
// ~/openclaw/competitor-radar/competitors.json
{
  "competitors": [
    {
      "name": "Acme Corp",
      "website": "https://acme.com",
      "pricing_page": "https://acme.com/pricing",
      "blog": "https://acme.com/blog",
      "twitter": "acmecorp",
      "linkedin": "company/acme-corp"
    },
    {
      "name": "BigCo",
      "website": "https://bigco.io",
      "pricing_page": "https://bigco.io/pricing",
      "blog": "https://bigco.io/resources/blog",
      "twitter": "bigco_io"
    },
    {
      "name": "StartupX",
      "website": "https://startupx.com",
      "pricing_page": "https://startupx.com/plans",
      "changelog": "https://startupx.com/changelog"

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
mkdir reddit-product-buzz-tracking && cd reddit-product-buzz-tracking
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
reddit-product-buzz-tracking/
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
  // TODO: Implement data collection for Reddit Product Buzz Tracking
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
  logger.info('=== Reddit 產品聲量追蹤 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 Reddit 產品聲量追蹤 報告\n\n${result}`);
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
pm2 start src/index.js --name reddit-product-buzz-tracking  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
