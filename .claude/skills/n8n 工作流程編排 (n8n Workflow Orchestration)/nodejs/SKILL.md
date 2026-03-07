---
name: n8n 工作流程編排 (n8n Workflow Orchestration)/nodejs
description: "Use Case #069 Node.js 方案: n8n 工作流程編排。使用 Node.js 實作 n8n Workflow Orchestration 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #069: n8n 工作流程編排 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# OpenClaw + n8n Workflow Orchestration

Letting your AI agent directly manage API keys and call external services is a recipe for security incidents. Every new integration means another credential in `.env.local`, another surface for the agent to accidentally leak or misuse.

This use case describes a pattern where OpenClaw delegates all external API interactions to n8n workflows via webhooks — the agent never touches credentials, and every integration is visually inspectable and lockable.

## Pain Point

When OpenClaw handles everything directly, you get three compounding problems:

- **No visibility**: It's hard to inspect what the agent actually built when it's buried in JavaScript skill files or shell scripts
- **Credential sprawl**: Every API key lives in the agent's environment, one bad commit away from exposure
- **Wasted tokens**: Deterministic sub-tasks (send an email, update a spreadsheet) burn LLM reasoning tokens when they could run as simple workflows

## What It Does

- **Proxy pattern**: OpenClaw writes n8n workflows with incoming webhooks, then calls those webhooks for all future API interactions
- **Credential isolation**: API keys live in n8n's credential store — the agent only knows the webhook URL
- **Visual debugging**: Every workflow is inspectable in n8n's drag-and-drop UI
- **Lockable workflows**: Once a workflow is built and tested, you lock it so the agent can't modify how it interacts with the API
- **Safeguard steps**: You can add validation, rate limiting, and approval gates in n8n before any external call executes

## How It Works

1. **Agent designs the workflow**: Tell OpenClaw what you need (e.g., "create a workflow that sends a Slack message when a new GitHub issue is labeled `urgent`")
2. **Agent builds it in n8n**: OpenClaw creates the workflow via n8n's API, including an incoming webhook trigger
3. **You add credentials**: Open n8n's UI, add your Slack token / GitHub token manually
4. **You lock the workflow**: Prevent further modifications by the agent
5. **Agent calls the webhook**: From now on, OpenClaw calls `http://n8n:5678/webhook/my-workflow` with a JSON payload — it never sees the API key

```text
┌──────────────┐     webhook call      ┌─────────────────┐     API call     ┌──────────────┐
│   OpenClaw   │ ───────────────────→  │   n8n Workflow   │ ─────────────→  │  External    │
│   (agent)    │   (no credentials)    │  (locked, with   │  (credentials   │  Service     │
│              │                       │   API keys)      │   stay here)    │  (Slack, etc)│
└──────────────┘                       └─────────────────┘                  └──────────────┘
```

## Skills You Need

- `n8n` API access (for creating/triggering workflows)
- `fetch` or `curl` for webhook calls
- Docker (if using the pre-configured stack)
- n8n credential management (manual, one-time setup per integration)

## How to Set It Up

### Option 1: Pre-configured Docker Stack

A community-maintained Docker Compose setup ([openclaw-n8

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
mkdir n8n-workflow-orchestration && cd n8n-workflow-orchestration
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
n8n-workflow-orchestration/
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
  // TODO: Implement data collection for n8n Workflow Orchestration
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
  logger.info('=== n8n 工作流程編排 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 n8n 工作流程編排 報告\n\n${result}`);
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
pm2 start src/index.js --name n8n-workflow-orchestration  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
