---
name: YouTube 內容產線 (YouTube Content Pipeline)/nodejs
description: "Use Case #011 Node.js 方案: YouTube 內容產線。使用 Node.js 實作 YouTube Content Pipeline 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #011: YouTube 內容產線 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# YouTube Content Pipeline

As a daily YouTube creator, finding fresh, timely video ideas across the web and X/Twitter is time-consuming. Tracking what you've already covered prevents duplicates and helps you stay ahead of trends.

This workflow automates the entire content scouting and research pipeline:

• Hourly cron job scans breaking AI news (web + X/Twitter) and pitches video ideas to Telegram
• Maintains a 90-day video catalog with view counts and topic analysis to avoid re-covering topics
• Stores all pitches in a SQLite database with vector embeddings for semantic dedup (so you never get pitched the same idea twice)
• When you share a link in Slack, OpenClaw researches the topic, searches X for related posts, queries your knowledge base, and creates an Asana card with a full outline

## Skills you Need

- `web_search` (built-in)
- [x-research-v2](https://clawhub.ai) or custom X/Twitter search skill
- [knowledge-base](https://clawhub.ai) skill for RAG
- Asana integration (or Todoist)
- `gog` CLI for YouTube Analytics
- Telegram topic for receiving pitches

## How to Set it Up

1. Set up a Telegram topic for video ideas and configure it in OpenClaw.
2. Install the knowledge-base skill and x-research skill.
3. Create a SQLite database for pitch tracking:
```sql
CREATE TABLE pitches (
  id INTEGER PRIMARY KEY,
  timestamp TEXT,
  topic TEXT,
  embedding BLOB,
  sources TEXT
);
```
4. Prompt OpenClaw:
```text
Run an hourly cron job to:
1. Search web and X/Twitter for breaking AI news
2. Check against my 90-day YouTube catalog (fetch from YouTube Analytics via gog)
3. Check semantic similarity against all past pitches in the database
4. If novel, pitch the idea to my Telegram "video ideas" topic with sources

Also: when I share a link in Slack #ai_trends, automatically:
1. Research the topic
2. Search X for related posts
3. Query my knowledge base
4. Create an Asana card in Video Pipeline with a full outline
```


---

# YouTube 分析数据拉取

## 简介

每日自动拉取 YouTube 分析数据，生成报告，追踪视频表现和频道增长。

**为什么重要**：了解内容表现，优化创作策略，追踪增长趋势。

**真实例子**：一位 YouTuber 使用此代理每日获取分析数据，代理生成趋势报告，帮助他识别最受欢迎的内容类型。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `youtube_api` | [ClawdHub](https://clawhub.com/skills/youtube) | 获取数据 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送报告 |

---

## 使用方式

### 每日拉取
定时拉取 YouTube 分析数据

### 生成报告
- 观看次数
- 订阅增长
- 收入统计
- 热门视频

### 趋势分析
分析数据趋势，提供优化建议

---

## 来源

- 来源：Stack Junkie


---

# 🎬 Video Content Pipeline

> From idea to upload-ready. Script, optimize, dominate the algorithm.

---

## The Problem

YouTube success requires more than good videos—it demands optimized titles, thumbnails that pop, SEO-rich descriptions, strategic tags, and engaging scripts. Creators spend hours on metadata that could go into content. Most never nail the algorithm because they're guessing, not analyzing.

---

## The Solution

OpenClaw handles the YouTube grind: 

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
mkdir youtube-content-pipeline && cd youtube-content-pipeline
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
youtube-content-pipeline/
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
  // TODO: Implement data collection for YouTube Content Pipeline
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
  logger.info('=== YouTube 內容產線 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 YouTube 內容產線 報告\n\n${result}`);
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
pm2 start src/index.js --name youtube-content-pipeline  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
