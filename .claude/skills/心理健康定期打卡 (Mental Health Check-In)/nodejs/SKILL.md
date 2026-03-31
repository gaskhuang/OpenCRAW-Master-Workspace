---
name: 心理健康定期打卡 (Mental Health Check-In)/nodejs
description: "Use Case #109 Node.js 方案: 心理健康定期打卡。使用 Node.js 實作 Mental Health Check-In 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #109: 心理健康定期打卡 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 🧠 Mental Health Check-In

> Know yourself better. Track moods, prep for therapy, spot patterns before they spiral.

---

## The Problem

Mental health is invisible until it's not. You feel "off" but can't explain why. Therapy sessions start with "how was your week?" and you draw a blank. Bad patterns sneak up because you're not tracking them.

---

## The Solution

OpenClaw provides gentle daily check-ins, logs moods without judgment, helps you prepare for therapy sessions with actual data, and identifies patterns before they become problems.

---

## Setup Guide

### Step 1: Install Mindfulness & Journaling Skills

```bash
openclaw skill install obsidian-conversation-backup  # or notion
openclaw skill install remind-me
openclaw skill install calendar
```

### Step 2: Configure Check-In Profile

Create `~/openclaw/mentalhealth/config.json`:

```json
{
  "checkInTimes": ["09:00", "21:00"],
  "therapyDay": "Thursday",
  "therapyTime": "14:00",
  "moodScale": "1-10",
  "trackingAreas": [
    "mood",
    "anxiety",
    "energy",
    "sleep_quality",
    "social_connection",
    "accomplishment"
  ],
  "triggerWarnings": {
    "lowMoodStreak": 3,
    "anxietyThreshold": 7,
    "isolationDays": 2
  },
  "storage": "~/openclaw/mentalhealth/entries/"
}
```

### Step 3: Set Up Check-In Questions

Create `~/openclaw/mentalhealth/questions.md`:

```markdown
# Morning Check-In (2 min)
- How are you feeling right now? (1-10)
- Any anxiety present? (1-10)
- How did you sleep?
- What's one thing you're looking forward to?

# Evening Check-In (3 min)
- Overall mood today (1-10)
- Energy level (1-10)
- Did you connect with anyone today?
- One thing that went well
- Anything weighing on you?

# Weekly Patterns to Watch
- Are mood scores trending down?
- More anxious days than calm?
- Social isolation increasing?
- Self-care being neglected?

# Therapy Prep Questions
- What's been on my mind this week?
- Any breakthrough moments?
- What am I avoiding?
- What do I want to work on next?
```

### Step 4: Create Entry Template

Create `~/openclaw/mentalhealth/template.json`:

```json
{
  "date": "",
  "morning": {
    "mood": null,
    "anxiety": null,
    "sleepQuality": null,
    "lookingForward": ""
  },
  "evening": {
    "mood": null,
    "energy": null,
    "socialConnection": false,
    "win": "",
    "concern": ""
  },
  "notes": "",
  "tags": []
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `obsidian-conversation-backup` | Secure entry storage |
| `notion` | Alternative storage |
| `remind-me` | Check-in reminders |
| `calendar` | Therapy scheduling |
| `reflect` | Pattern analysis |

---

## Example Prompts

**Morning check-in:**
```
Morning check-in. Mood is 6, anxiety 4, slept okay. Looking forward to lunch with a friend.
```

**Quick mood log:**
```
Feeling anxious right now - about a 7. Work deadline stress.
```

**Pattern analysis:**
```
How has my mood been this month? Any patterns with days of the week, sleep, or social time

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
mkdir mental-health-check-in && cd mental-health-check-in
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
mental-health-check-in/
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
  // TODO: Implement data collection for Mental Health Check-In
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
  logger.info('=== 心理健康定期打卡 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 心理健康定期打卡 報告\n\n${result}`);
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
pm2 start src/index.js --name mental-health-check-in  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
