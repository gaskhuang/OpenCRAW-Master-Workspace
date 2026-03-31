---
name: 採購與營養優化 (Grocery & Nutrition Optimizer)/nodejs
description: "Use Case #113 Node.js 方案: 採購與營養優化。使用 Node.js 實作 Grocery & Nutrition Optimizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #113: 採購與營養優化 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 🛒 Grocery Optimizer

> Meal plan, shop smart, waste less.

---

## The Problem

Grocery shopping without a plan leads to impulse buys, forgotten items, and food waste. Meal planning is tedious. You buy ingredients for recipes you never make.

---

## The Solution

OpenClaw helps plan meals based on what's on sale, generates optimized grocery lists, tracks what you have, and ensures nothing goes to waste.

---

## Setup Guide

### Step 1: Install Shopping Skills

```bash
openclaw skill install bring-shopping
openclaw skill install recipe-to-list
openclaw skill install gurkerl  # or picnic, instacart
```

### Step 2: Configure Preferences

Create `~/openclaw/grocery/preferences.json`:

```json
{
  "dietaryRestrictions": [],
  "householdSize": 2,
  "cookingDays": ["Monday", "Wednesday", "Friday", "Sunday"],
  "budgetWeekly": 150,
  "stores": ["preferred store"]
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `bring-shopping` | Shopping list management |
| `recipe-to-list` | Recipe ingredient extraction |
| `gurkerl`/`picnic` | Online grocery ordering |

---

## Example Prompts

**Weekly planning:**
```
Plan meals for this week. Keep it under $150, use what's in season, and minimize waste.
```

**Recipe to list:**
```
I want to make [recipe]. Add ingredients to my shopping list, minus what I already have.
```

**What's for dinner:**
```
What can I make with chicken, rice, and the vegetables expiring soon?
```

---

## Cron Schedule

```
0 9 * * 0      # Sunday 9 AM - weekly meal planning
0 10 * * 3     # Wednesday - mid-week list check
```

---

## Expected Results

- 20% reduction in grocery spending
- Less food waste
- No more "what's for dinner?" stress


---

# 🥗 Nutrition Tracker

> Eat smarter, not harder. Log meals, hit macros, get personalized suggestions.

---

## The Problem

Nutrition apps are tedious. Scanning barcodes, weighing portions, logging every ingredient—it's exhausting. You start motivated but quit within a week. Meanwhile, you have no idea if you're actually eating enough protein or too many carbs.

---

## The Solution

OpenClaw makes logging effortless: snap a photo or describe your meal in plain language. It estimates macros, tracks patterns, suggests meals that fit your goals, and adapts to your preferences over time.

---

## Setup Guide

### Step 1: Install Nutrition Skills

```bash
openclaw skill install nutritionix  # food database
openclaw skill install recipe-parser
openclaw skill install remind-me
openclaw skill install grocery-list  # optional
```

### Step 2: Configure Nutrition Goals

Create `~/openclaw/nutrition/profile.json`:

```json
{
  "goal": "maintain",
  "calories": 2200,
  "macros": {
    "protein": 150,
    "carbs": 220,
    "fat": 73
  },
  "preferences": {
    "diet": "none",
    "allergies": [],
    "dislikes": ["cilantro"],
    "cuisines": ["mediterranean", "asian", "mexican"]
  },
  "mealTimes": {
    "breakfast": "08:00",
    "lunch": "12:30",
    "dinner": "19:00"
  },
  

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
mkdir grocery-&-nutrition-optimizer && cd grocery-&-nutrition-optimizer
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
grocery-&-nutrition-optimizer/
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
  // TODO: Implement data collection for Grocery & Nutrition Optimizer
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
  logger.info('=== 採購與營養優化 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 採購與營養優化 報告\n\n${result}`);
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
pm2 start src/index.js --name grocery-&-nutrition-optimizer  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
