---
name: AI 寫作助手 (AI Writing Assistant)/nodejs
description: "Use Case #016 Node.js 方案: AI 寫作助手。使用 Node.js 實作 AI Writing Assistant 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #016: AI 寫作助手 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# ✍️ Writing Assistant

> From blank page to published post. Your personal editor that never sleeps.

---

## The Problem

Writing quality blog content is exhausting: research, drafting, editing, SEO optimization, formatting, publishing. Most writers either spend 8+ hours per post or publish half-baked content. The editing loop alone kills momentum—you're too close to your own words to see what's wrong.

---

## The Solution

OpenClaw becomes your writing partner: helps research topics, generates first drafts, edits for clarity and style, optimizes for SEO, and handles the publishing workflow. You provide the ideas and voice; OpenClaw handles the heavy lifting.

---

## Setup Guide

### Step 1: Install Writing Skills

```bash
openclaw skill install gsc           # Google Search Console
openclaw skill install brave-search  # Research & SERP analysis
openclaw skill install web-fetch     # Reference gathering
openclaw skill install ghost         # Blog publishing (if using Ghost)
```

### Step 2: Create Writing Workspace

```bash
mkdir -p ~/openclaw/writing/{drafts,published,research}
```

Create `~/openclaw/writing/style-guide.md`:

```markdown
# My Writing Style Guide

## Voice
- Conversational but authoritative
- Use contractions (it's, you'll, don't)
- Second person ("you") to speak directly to reader

## Structure
- Short paragraphs (3-4 sentences max)
- Use subheadings every 200-300 words
- Include actionable takeaways

## Avoid
- Passive voice
- Jargon without explanation
- Walls of text

## SEO Requirements
- Target keyword in title
- Keyword in first 100 words
- Include 3-5 internal links
```

### Step 3: Set Up Blog Config

Create `~/openclaw/writing/blog-config.json`:

```json
{
  "platform": "ghost",
  "siteUrl": "https://yourblog.com",
  "author": "Your Name",
  "defaultCategory": "Tech",
  "wordCountTarget": "1500-2500",
  "publishDays": ["Tuesday", "Thursday"],
  "seoKeywords": ["main topic", "related topic"]
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `gsc` | Track keyword rankings and opportunities |
| `brave-search` | Research topics and analyze competition |
| `web-fetch` | Pull reference content and citations |
| `ghost` / `wordpress` | Direct blog publishing |
| `grammarly-api` | Grammar and style checking (optional) |

---

## Example Prompts

**Topic research:**
```
I want to write about [topic]. Research the top 10 ranking articles, identify gaps in their coverage, and suggest 5 unique angles I could take.
```

**Draft generation:**
```
Create a first draft for a blog post about [topic]. Target keyword: [keyword]. Follow my style guide in ~/openclaw/writing/style-guide.md. Aim for 1800 words.
```

**Editing pass:**
```
Edit this draft for clarity and flow. Remove fluff, strengthen weak sentences, and ensure it matches my voice. Be ruthless—cut anything that doesn't add value.
```

**SEO optimization:**
```
Optimize this post for SEO. Check keyword density, suggest meta description, add internal lin

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
mkdir ai-writing-assistant && cd ai-writing-assistant
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
ai-writing-assistant/
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
  // TODO: Implement data collection for AI Writing Assistant
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
  logger.info('=== AI 寫作助手 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 AI 寫作助手 報告\n\n${result}`);
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
pm2 start src/index.js --name ai-writing-assistant  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
