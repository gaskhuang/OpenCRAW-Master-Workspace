---
name: 冷外聯自動化 (Cold Outreach Automation)/nodejs
description: "Use Case #061 Node.js 方案: 冷外聯自動化。使用 Node.js 實作 Cold Outreach Automation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #061: 冷外聯自動化 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# ✉️ Cold Outreach Automation

> Personalized at scale. Not spray-and-pray, but thoughtful outreach multiplied.

---

## The Problem

Cold outreach works when it's personal. But personalization doesn't scale—researching each prospect takes 15 minutes. So you either send generic emails (ignored) or limit your outreach (slow growth).

---

## The Solution

OpenClaw researches prospects automatically, finds personalization hooks, generates custom messages, and manages follow-up sequences. You review and send—personal touch at scale.

---

## Setup Guide

### Step 1: Install Outreach Skills

```bash
openclaw skill install apollo
openclaw skill install linkedin
openclaw skill install gmail
openclaw skill install web-fetch
```

### Step 2: Define Ideal Customer Profile

Create `~/openclaw/outreach/icp.md`:

```markdown
# Ideal Customer Profile

## Company
- Size: 50-500 employees
- Industry: SaaS, Tech, E-commerce
- Growth stage: Series A-C
- Tech stack: Uses [relevant tools]

## Persona
- Title: VP/Director of [department]
- Responsibility: [specific area]
- Pain points: [list]

## Disqualifiers
- Less than 10 employees
- Non-English speaking
- Already using competitor
```

### Step 3: Create Message Templates

Create `~/openclaw/outreach/templates.md`:

```markdown
# Outreach Templates

## First Touch
Subject: {personalization_hook}

Hi {first_name},

{personalized_opener_based_on_research}

[Value prop in 1 sentence]

Would it make sense to chat for 15 minutes?

## Follow-up 1 (Day 3)
Subject: Re: {original_subject}

{name}, wanted to bump this up...

## Follow-up 2 (Day 7)
Subject: Quick question, {name}

Different angle/value prop...

## Break-up (Day 14)
Subject: Should I close your file?

Last attempt, remove friction...
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `apollo` | Prospect research |
| `linkedin` | Profile insights |
| `gmail` | Email sending |
| `web-fetch` | Company research |

---

## Example Prompts

**Research prospect:**
```
Research [person] at [company]. Find personalization hooks: recent news, common connections, content they've shared.
```

**Generate sequence:**
```
Create a 4-email sequence for [persona] at [company type]. Focus on [pain point].
```

**Review and send:**
```
Show me today's outreach queue with draft messages. Let me approve or edit before sending.
```

**Optimize:**
```
Which subject lines and openers got the best response rates? Update my templates.
```

---

## Cron Schedule

```
0 7 * * 1-5    # 7 AM weekdays - prepare daily outreach
0 9 * * 1-5    # 9 AM - send first touch emails
0 14 * * 1-5   # 2 PM - send follow-ups
0 10 * * 1     # Monday - weekly metrics review
```

---

## Expected Results

**Week 1:**
- 5x outreach volume with same effort
- Personalized messages for every prospect

**Month 1:**
- Higher response rates than generic outreach
- Clear data on what messaging works

**Month 3:**
- Predictable meeting pipeline
- Continuously optimized messaging
- Scalable pros

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
mkdir cold-outreach-automation && cd cold-outreach-automation
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
cold-outreach-automation/
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
  // TODO: Implement data collection for Cold Outreach Automation
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
  logger.info('=== 冷外聯自動化 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 冷外聯自動化 報告\n\n${result}`);
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
pm2 start src/index.js --name cold-outreach-automation  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
