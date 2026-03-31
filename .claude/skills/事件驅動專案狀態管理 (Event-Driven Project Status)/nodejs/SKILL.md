---
name: 事件驅動專案狀態管理 (Event-Driven Project Status)/nodejs
description: "Use Case #036 Node.js 方案: 事件驅動專案狀態管理。使用 Node.js 實作 Event-Driven Project Status 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #036: 事件驅動專案狀態管理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Project State Management System: Event-Driven Alternative to Kanban

Traditional Kanban boards are static and require manual updates. You forget to move cards, lose context between sessions, and can't track the "why" behind state changes. Projects drift without clear visibility.

This workflow replaces Kanban with an event-driven system that tracks project state automatically:

• Stores project state in a database with full history
• Captures context: decisions, blockers, next steps, key insights
• Event-driven updates: "Just finished X, blocked on Y" → automatic state transition
• Natural language queries: "What's the status of [project]?", "Why did we pivot on [feature]?"
• Daily standup summaries: What happened yesterday, what's planned today, what's blocked
• Git integration: links commits to project events for traceability

## Pain Point

Kanban boards become stale. You waste time updating cards instead of doing work. Context gets lost—three months later, you can't remember why you made a key decision. There's no automatic link between code changes and project progress.

## What It Does

Instead of dragging cards, you chat with your assistant: "Finished the auth flow, starting on the dashboard." The system logs the event, updates project state, and preserves context. When you ask "Where are we on the dashboard?" it gives you the full story: what's done, what's next, what's blocking you, and why.

Git commits are automatically scanned and linked to projects. Your daily standup summary writes itself.

## Skills Needed

- `postgres` or SQLite for project state database
- `github` (gh CLI) for commit tracking
- Discord or Telegram for updates and queries
- Cron jobs for daily summaries
- Sub-agents for parallel project analysis

## How to Set it Up

1. Set up a project state database:
```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  status TEXT, -- e.g., "active", "blocked", "completed"
  current_phase TEXT,
  last_update TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  event_type TEXT, -- e.g., "progress", "blocker", "decision", "pivot"
  description TEXT,
  context TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE blockers (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  blocker_text TEXT,
  status TEXT DEFAULT 'open', -- "open", "resolved"
  created_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ
);
```

2. Create a Discord channel for project updates (e.g., #project-state).

3. Prompt OpenClaw:
```text
You are my project state manager. Instead of Kanban, I'll tell you what I'm working on conversationally.

When I say things like:
- "Finished [task]" → log a "progress" event, update project state
- "Blocked on [issue]" → create a blocker entry, update project status to "blocked"
- "Starting [new task]" → log a "progress" event, update current phase
- "Decided to [decision]" → log a "decision" 

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
mkdir event-driven-project-status && cd event-driven-project-status
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
event-driven-project-status/
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
  // TODO: Implement data collection for Event-Driven Project Status
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
  logger.info('=== 事件驅動專案狀態管理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 事件驅動專案狀態管理 報告\n\n${result}`);
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
pm2 start src/index.js --name event-driven-project-status  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
