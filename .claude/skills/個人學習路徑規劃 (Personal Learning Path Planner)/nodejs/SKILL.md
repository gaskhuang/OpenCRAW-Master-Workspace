---
name: 個人學習路徑規劃 (Personal Learning Path Planner)/nodejs
description: "Use Case #111 Node.js 方案: 個人學習路徑規劃。使用 Node.js 實作 Personal Learning Path Planner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #111: 個人學習路徑規劃 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 健康與個人成長

---

## 原始需求 (來自 Source Repos)

# 📚 Learning Path Creator

> Learn anything systematically. No more random YouTube binges.

---

## The Problem

Self-directed learning is chaotic. You want to learn [skill] but don't know where to start, what order to learn things, or when you've "finished." Most people bounce between resources without a plan.

---

## The Solution

OpenClaw creates personalized curricula: assesses your starting point, finds the best resources, creates a structured path, tracks progress, and adjusts when you struggle or excel.

---

## Setup Guide

### Step 1: Install Learning Skills

```bash
openclaw skill install context7
openclaw skill install literature-review
openclaw skill install youtube-summarizer
```

### Step 2: Define Learning Goals

Create `~/openclaw/learning/goals.json`:

```json
{
  "currentGoal": {
    "topic": "Machine Learning",
    "level": "beginner",
    "timeCommitment": "5 hours/week",
    "deadline": "3 months",
    "learningStyle": "video + hands-on projects"
  },
  "preferences": {
    "freeResourcesPreferred": true,
    "languages": ["English"],
    "formats": ["video", "interactive", "book"]
  }
}
```

### Step 3: Create Progress Tracker

Create `~/openclaw/learning/progress.md`:

```markdown
# Learning Progress

## Current: Machine Learning Fundamentals

### Completed
- [x] Module 1: Linear algebra basics
- [x] Module 2: Statistics refresher

### In Progress
- [ ] Module 3: Python for ML (60%)

### Up Next
- [ ] Module 4: Supervised learning

### Notes
- Struggling with: gradient descent intuition
- Should review: matrix multiplication
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `context7` | Library documentation |
| `literature-review` | Academic resources |
| `youtube-summarizer` | Video content |
| `brave-search` | Resource discovery |

---

## Example Prompts

**Create curriculum:**
```
I want to learn [topic] from scratch. I can commit 5 hours per week for 3 months. Create a learning path with the best free resources.
```

**Daily practice:**
```
I have 45 minutes to study. What should I work on today based on my learning plan?
```

**Stuck on concept:**
```
I don't understand [concept]. Explain it differently and find additional resources that explain it well.
```

**Progress check:**
```
Review my learning progress. Am I on track? What should I adjust?
```

---

## Cron Schedule

```
0 7 * * *      # 7 AM - daily learning reminder
0 20 * * 0     # 8 PM Sunday - weekly progress review
0 10 1 * *     # 1st of month - curriculum adjustment
```

---

## Expected Results

**Week 1:**
- Clear learning path created
- Know exactly what to study

**Month 1:**
- Steady progress visible
- Concepts building on each other
- No more resource paralysis

**Month 3:**
- Measurable skill acquisition
- Portfolio of completed projects
- Ready for next learning goal


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
mkdir personal-learning-path-planner && cd personal-learning-path-planner
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
personal-learning-path-planner/
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
  // TODO: Implement data collection for Personal Learning Path Planner
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
  logger.info('=== 個人學習路徑規劃 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 個人學習路徑規劃 報告\n\n${result}`);
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
pm2 start src/index.js --name personal-learning-path-planner  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
