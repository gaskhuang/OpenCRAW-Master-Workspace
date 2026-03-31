---
name: 潛在客戶資料豐富 (Lead Enrichment)/nodejs
description: "Use Case #060 Node.js 方案: 潛在客戶資料豐富。使用 Node.js 實作 Lead Enrichment 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #060: 潛在客戶資料豐富 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 🎯 Lead Scoring System

> Focus on leads that convert. Stop wasting time on tire-kickers.

---

## The Problem

Not all leads are equal, but treating them equally wastes time. Your inbox mixes hot prospects with students, competitors, and people who'll never buy. Without scoring, you either respond to everyone (burnout) or miss the good ones.

---

## The Solution

OpenClaw automatically scores every lead based on signals you define: company size, title, engagement, tech stack, funding status. You see a prioritized list and act accordingly.

---

## Setup Guide

### Step 1: Install Sales Skills

```bash
openclaw skill install hubspot  # or your CRM
openclaw skill install apollo
openclaw skill install gmail
openclaw skill install linkedin
```

### Step 2: Define Scoring Criteria

Create `~/openclaw/leads/scoring.json`:

```json
{
  "firmographics": {
    "employeeCount": {
      "1-10": 5,
      "11-50": 15,
      "51-200": 25,
      "201-1000": 20,
      "1000+": 10
    },
    "funding": {
      "seed": 10,
      "seriesA": 20,
      "seriesB+": 25,
      "public": 15
    }
  },
  "title": {
    "CEO/Founder": 30,
    "VP/Director": 25,
    "Manager": 15,
    "Individual": 5
  },
  "engagement": {
    "visitedPricing": 20,
    "downloadedContent": 15,
    "openedEmails": 10,
    "bookedDemo": 40
  },
  "thresholds": {
    "hot": 70,
    "warm": 40,
    "cold": 0
  }
}
```

### Step 3: Set Up Routing Rules

Create `~/openclaw/leads/routing.md`:

```markdown
# Lead Routing

## Hot Leads (70+)
- Notify immediately
- Personal outreach within 1 hour
- Research company before call

## Warm Leads (40-69)
- Add to nurture sequence
- Respond within 24 hours
- Automated follow-up

## Cold Leads (<40)
- Automated acknowledgment
- Marketing nurture only
- Review weekly for reclassification
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `hubspot` | CRM integration |
| `apollo` | Lead enrichment |
| `gmail` | Email monitoring |
| `linkedin` | Profile enrichment |

---

## Example Prompts

**Score new lead:**
```
New lead: [name] from [company]. Score them and tell me what I should know before reaching out.
```

**Daily prioritization:**
```
Show me today's leads ranked by score. Who should I focus on first?
```

**Pattern analysis:**
```
What do my converted customers have in common? Update my scoring weights.
```

**Enrich missing data:**
```
This lead is missing company info. Research them and update the record.
```

---

## Cron Schedule

```
*/15 * * * *   # Every 15 min - score new leads
0 8 * * 1-5    # 8 AM weekdays - daily priority list
0 10 * * 1     # Monday 10 AM - weekly pipeline review
```

---

## Expected Results

**Week 1:**
- All leads auto-scored
- Clear prioritization

**Month 1:**
- 50% more time on high-value leads
- Faster response to hot prospects

**Month 3:**
- Higher conversion rate
- Data-driven scoring refinement
- Sales efficiency up 30%+


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
mkdir lead-enrichment && cd lead-enrichment
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
lead-enrichment/
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
  // TODO: Implement data collection for Lead Enrichment
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
  logger.info('=== 潛在客戶資料豐富 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 潛在客戶資料豐富 報告\n\n${result}`);
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
pm2 start src/index.js --name lead-enrichment  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
