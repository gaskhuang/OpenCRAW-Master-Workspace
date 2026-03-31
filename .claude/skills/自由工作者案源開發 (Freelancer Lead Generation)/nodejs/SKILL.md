---
name: 自由工作者案源開發 (Freelancer Lead Generation)/nodejs
description: "Use Case #064 Node.js 方案: 自由工作者案源開發。使用 Node.js 實作 Freelancer Lead Generation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #064: 自由工作者案源開發 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# Freelancer Lead Pipeline

> Automate job discovery, lead qualification, proposal drafting, and follow-ups — so you can focus on actual client work.

---

## The Problem

Finding quality freelance gigs is a full-time job on top of your actual work. You spend hours scrolling Upwork, LinkedIn, and niche job boards, only to find most postings don't match your skills, budget, or timeline. By the time you craft a personalized proposal, the best opportunities are already flooded with applicants. Meanwhile, promising leads go cold because you forgot to follow up.

---

## The Solution

OpenClaw monitors job boards on your schedule, filters opportunities against your criteria, drafts personalized proposals using context from each posting, and tracks your entire pipeline in a simple markdown file. It sends you only qualified leads, reminds you to follow up, and can even help generate invoices when you close deals.

**What you get:**
- Morning digest of qualified leads matching your criteria
- Pre-drafted proposals ready to customize and send
- Automatic pipeline tracking with follow-up reminders
- No more missed opportunities or forgotten leads

---

## Setup Guide

### Step 1: Create Your Freelancer Profile (5 minutes)

Create `~/openclaw/freelance/PROFILE.md`:

```markdown
# Freelancer Profile

## Identity
- **Name:** [Your Name]
- **Title:** Senior Full-Stack Developer
- **Specialties:** React, Node.js, Python, AWS
- **Experience:** 8 years

## Ideal Client Criteria
- **Budget minimum:** $50/hour or $2,000+ fixed projects
- **Project length:** 1 week to 3 months
- **Industries:** SaaS, fintech, healthtech, e-commerce
- **Red flags:** "equity only", "exposure", "quick test project", budget under $500

## Availability
- **Hours/week:** 20-30
- **Timezone:** EST (UTC-5)
- **Start date:** Can start within 1 week

## Portfolio Links
- GitHub: https://github.com/yourname
- Portfolio: https://yoursite.com
- LinkedIn: https://linkedin.com/in/yourname

## Proposal Style
- Tone: Professional but personable
- Length: 150-250 words
- Always include: Relevant experience, specific approach, timeline estimate
- Avoid: Generic templates, desperation, undercutting
```

### Step 2: Set Up Pipeline Tracking (3 minutes)

Create `~/openclaw/freelance/PIPELINE.md`:

```markdown
# Lead Pipeline

## 🔥 Hot Leads (respond today)
<!-- Leads scored 8+/10, posted <24h ago -->

## 📋 Qualified Leads (respond this week)
<!-- Leads scored 6-7/10, good fit but not urgent -->

## ✉️ Proposals Sent
| Date | Client | Project | Amount | Status | Follow-up |
|------|--------|---------|--------|--------|-----------|

## 🤝 Active Projects
| Client | Project | Start | End | Rate | Invoiced |
|--------|---------|-------|-----|------|----------|

## ❌ Rejected/Passed
<!-- Quick notes on why, for pattern learning -->
```

### Step 3: Create Job Board URLs File (5 minutes)

Create `~/openclaw/freelance/JOB_SOURCES.md`:

```markdown
# Job Sources to Monitor

## Upwork
- https://www.upwork.com/nx/f

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
mkdir freelancer-lead-generation && cd freelancer-lead-generation
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
freelancer-lead-generation/
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
  // TODO: Implement data collection for Freelancer Lead Generation
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
  logger.info('=== 自由工作者案源開發 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 自由工作者案源開發 報告\n\n${result}`);
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
pm2 start src/index.js --name freelancer-lead-generation  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
