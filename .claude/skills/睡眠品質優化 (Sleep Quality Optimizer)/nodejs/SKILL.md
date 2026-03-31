---
name: 睡眠品質優化 (Sleep Quality Optimizer)/nodejs
description: "Use Case #108 Node.js 方案: 睡眠品質優化。使用 Node.js 實作 Sleep Quality Optimizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #108: 睡眠品質優化 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 😴 Sleep Optimizer

> Wake up refreshed. Optimize your nights to own your days.

---

## The Problem

Poor sleep destroys everything—focus, mood, health. You track with Whoop or Oura but never act on the data. Bedtime routines are inconsistent. You know you should sleep better but don't know what's actually hurting your sleep.

---

## The Solution

OpenClaw connects to your sleep trackers, identifies what's tanking your sleep score, enforces your wind-down routine, and adapts recommendations based on what actually works for *you*.

---

## Setup Guide

### Step 1: Install Sleep & Recovery Skills

```bash
openclaw skill install whoop
openclaw skill install oura-ring  # alternative tracker
openclaw skill install calendar
openclaw skill install remind-me
```

### Step 2: Configure Sleep Profile

Create `~/openclaw/sleep/profile.json`:

```json
{
  "targetBedtime": "22:30",
  "targetWakeTime": "06:30",
  "minSleepHours": 7.5,
  "idealSleepScore": 85,
  "tracker": "whoop",
  "windDownMinutes": 60,
  "factors": {
    "caffeineCutoff": "14:00",
    "alcoholEffect": true,
    "exerciseEffect": true,
    "screensCutoff": "21:30"
  }
}
```

### Step 3: Define Wind-Down Routine

Create `~/openclaw/sleep/routine.md`:

```markdown
# Wind-Down Routine (60 min before bed)

## T-60 minutes
- [ ] Put away work
- [ ] Dim lights
- [ ] Start winding down

## T-30 minutes
- [ ] No more screens
- [ ] Prepare for tomorrow
- [ ] Light reading or journaling

## T-10 minutes
- [ ] Bedroom
- [ ] Breathing exercises
- [ ] Sleep mask on

## Disruptors to Track
- Late caffeine
- Alcohol
- Heavy meals after 8 PM
- Intense exercise after 7 PM
- Stressful conversations
- Blue light exposure
```

### Step 4: Create Sleep Log

Create `~/openclaw/sleep/log.json`:

```json
{
  "entries": [],
  "weeklyAverage": null,
  "trends": {
    "improving": false,
    "disruptors": [],
    "helpers": []
  }
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `whoop` | Recovery/strain/sleep data |
| `oura-ring` | Sleep stage tracking |
| `calendar` | Schedule awareness |
| `remind-me` | Bedtime reminders |
| `timer` | Wind-down routine timing |

---

## Example Prompts

**Morning check-in:**
```
How did I sleep last night? What does Whoop say about my recovery?
```

**Analyze patterns:**
```
Look at my sleep data for the past 2 weeks. What's helping and what's hurting my sleep quality?
```

**Start wind-down:**
```
Start my wind-down routine. What's my target bedtime tonight?
```

**Track disruptor:**
```
Log that I had coffee at 4 PM today. Flag it for sleep correlation.
```

**Optimize schedule:**
```
I have an important meeting at 9 AM tomorrow. What time should I go to bed to be at peak recovery?
```

**Weekly review:**
```
Give me my sleep report for this week. Am I trending better or worse?
```

---

## Cron Schedule

```
0 21 * * *     # 9 PM - wind-down reminder
30 22 * * *    # 10:30 PM - final bedtime warning
0 7 * * *      # 7 AM - sleep quality report
0 9 * * 0

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
mkdir sleep-quality-optimizer && cd sleep-quality-optimizer
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
sleep-quality-optimizer/
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
  // TODO: Implement data collection for Sleep Quality Optimizer
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
  logger.info('=== 睡眠品質優化 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 睡眠品質優化 報告\n\n${result}`);
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
pm2 start src/index.js --name sleep-quality-optimizer  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
