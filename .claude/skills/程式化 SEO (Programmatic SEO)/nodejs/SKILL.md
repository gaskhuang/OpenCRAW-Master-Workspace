---
name: 程式化 SEO (Programmatic SEO)/nodejs
description: "Use Case #058 Node.js 方案: 程式化 SEO。使用 Node.js 實作 Programmatic SEO 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #058: 程式化 SEO — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 🔍 SEO Content Pipeline

> Rank higher with less effort. Data-driven content that Google loves.

---

## The Problem

Creating SEO content is time-consuming: keyword research, competitor analysis, outline creation, writing, optimization. Most content either ignores SEO (no traffic) or over-optimizes (robotic reading). Finding the balance takes expertise and hours.

---

## The Solution

OpenClaw handles the entire SEO content workflow: finds keyword opportunities, analyzes what's ranking, creates optimized outlines, and helps you write content that ranks AND reads well.

---

## Setup Guide

### Step 1: Install SEO Skills

```bash
openclaw skill install gsc  # Google Search Console
openclaw skill install brave-search
openclaw skill install web-fetch
```

### Step 2: Configure Your Site

Create `~/openclaw/seo/site-config.json`:

```json
{
  "domain": "yourdomain.com",
  "gscPropertyId": "sc-domain:yourdomain.com",
  "targetKeywords": ["main topic", "secondary topic"],
  "competitors": ["competitor1.com", "competitor2.com"],
  "contentGoals": {
    "monthlyPosts": 8,
    "targetWordCount": "1500-2500"
  }
}
```

### Step 3: Create Content Brief Template

Create `~/openclaw/seo/brief-template.md`:

```markdown
# Content Brief: {keyword}

## Keyword Data
- Search volume:
- Difficulty:
- Current ranking:

## Top 5 Ranking Pages
1. [URL] - Word count, key points
2. ...

## Content Gaps
- Topics competitors miss:
- Questions not answered:

## Recommended Outline
1. H2:
   - H3:
2. ...

## Optimization Checklist
- [ ] Keyword in title
- [ ] Keyword in first 100 words
- [ ] Related keywords included
- [ ] Internal links
- [ ] External authoritative links
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `gsc` | Google Search Console data |
| `brave-search` | SERP analysis |
| `web-fetch` | Competitor content analysis |

---

## Example Prompts

**Keyword research:**
```
Find 10 keyword opportunities for [topic]. Look for low competition, decent volume, and topics I can write authoritatively about.
```

**Content brief:**
```
Create a content brief for the keyword "[keyword]". Analyze top 5 ranking pages and find gaps I can fill.
```

**Outline review:**
```
Here's my outline for [topic]. Is it comprehensive enough to outrank the current top results?
```

**Post-publish optimization:**
```
My post on [topic] has been live for a month. Check GSC for impressions without clicks - what queries should I better optimize for?
```

---

## Cron Schedule

```
0 8 * * 1      # Monday 8 AM - weekly content planning
0 9 * * *      # Daily - check GSC for quick wins
0 10 * * 5     # Friday - performance review
```

---

## Expected Results

**Month 1:**
- Content calendar with keyword-targeted posts
- 50% reduction in research time per post

**Month 3:**
- New posts ranking within 4-6 weeks
- 30%+ increase in organic traffic

**Month 6:**
- Consistent content production
- Clear ROI from SEO efforts


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
mkdir programmatic-seo && cd programmatic-seo
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
programmatic-seo/
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
  // TODO: Implement data collection for Programmatic SEO
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
  logger.info('=== 程式化 SEO ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 程式化 SEO 報告\n\n${result}`);
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
pm2 start src/index.js --name programmatic-seo  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
