---
name: 部署自動化流水線 (Deployment Automation Pipeline)/nodejs
description: "Use Case #077 Node.js 方案: 部署自動化流水線。使用 Node.js 實作 Deployment Automation Pipeline 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #077: 部署自動化流水線 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 🚀 Deployment Pipeline Manager

> Ship with confidence. Automated deployments done right.

---

## The Problem

Manual deployments are error-prone and stressful. You forget steps, environments drift, and rollbacks are chaotic. CI/CD tools help but still need babysitting.

---

## The Solution

OpenClaw orchestrates deployments: runs pipelines, monitors progress, handles rollbacks, and notifies the right people. You push code, it handles the rest.

---

## Setup Guide

### Step 1: Install DevOps Skills

```bash
openclaw skill install github
openclaw skill install vercel-deploy
openclaw skill install dokploy
openclaw skill install cloudflare
```

### Step 2: Configure Environments

Create `~/openclaw/deploy/config.json`:

```json
{
  "environments": {
    "staging": {
      "autoDeploy": true,
      "branch": "develop"
    },
    "production": {
      "autoDeploy": false,
      "branch": "main",
      "requireApproval": true
    }
  }
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `github` | CI/CD integration |
| `vercel-deploy` | Vercel deployments |
| `dokploy` | Self-hosted deploys |
| `cloudflare` | Edge deployments |

---

## Example Prompts

**Deploy:**
```
Deploy latest main to production. Show me the diff from current.
```

**Status check:**
```
What's the deployment status? Any failed builds today?
```

**Rollback:**
```
Production is broken. Rollback to the previous version immediately.
```

---

## Cron Schedule

```
*/5 * * * *    # Monitor deployment health
0 9 * * 1      # Monday - deployment report
```

---

## Expected Results

- Zero-stress deployments
- Instant rollback capability
- Full deployment visibility


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
mkdir deployment-automation-pipeline && cd deployment-automation-pipeline
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
deployment-automation-pipeline/
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
  // TODO: Implement data collection for Deployment Automation Pipeline
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
  logger.info('=== 部署自動化流水線 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 部署自動化流水線 報告\n\n${result}`);
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
pm2 start src/index.js --name deployment-automation-pipeline  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
