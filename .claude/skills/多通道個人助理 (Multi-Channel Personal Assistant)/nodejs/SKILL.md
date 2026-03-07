---
name: 多通道個人助理 (Multi-Channel Personal Assistant)/nodejs
description: "Use Case #035 Node.js 方案: 多通道個人助理。使用 Node.js 實作 Multi-Channel Personal Assistant 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #035: 多通道個人助理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Multi-Channel Personal Assistant

Context-switching between apps to manage tasks, schedule events, send messages, and track work is exhausting. You want one interface that routes to all your tools.

This workflow consolidates everything into a single AI assistant:

• Telegram as primary interface with topic-based routing (different topics for video ideas, CRM, earnings, config, etc.)
• Slack integration for team collaboration (task assignment, knowledge base saves, video idea triggers)
• Google Workspace: create calendar events, manage email, upload to Drive — all from chat
• Todoist for quick task capture
• Asana for project management
• Automated reminders: trash day, weekly company letter, etc.

## Skills you Need

- `gog` CLI (Google Workspace)
- Slack integration (bot + user tokens)
- Todoist API or skill
- Asana API or skill
- Telegram channel with multiple topics configured

## How to Set it Up

1. Set up Telegram topics for different contexts:
   - `config` — bot settings and debugging
   - `updates` — status and notifications
   - `video-ideas` — content pipeline
   - `personal-crm` — contact management
   - `earnings` — financial tracking
   - `knowledge-base` — RAG ingestion and queries

2. Connect all your tools via OpenClaw config:
   - Google OAuth (Gmail, Calendar, Drive)
   - Slack (app + user tokens)
   - Todoist API token
   - Asana API token

3. Prompt OpenClaw:
```text
You are my multi-channel assistant. Route requests based on context:

Telegram topics:
- "config" → system settings, debugging
- "updates" → daily summaries, reminders, calendar
- "video-ideas" → content pipeline and research
- "personal-crm" → contact queries and meeting prep
- "earnings" → financial tracking
- "knowledge-base" → save and search content

When I ask you to:
- "Add [task] to my todo" → use Todoist
- "Create a card for [topic]" → use Asana Video Pipeline project
- "Schedule [event]" → use gog calendar
- "Email [person] about [topic]" → draft email via gog gmail
- "Upload [file] to Drive" → use gog drive

Set up automated reminders:
- Monday 6 PM: "🗑️ Trash day tomorrow"
- Friday 3 PM: "✍️ Time to write the weekly company update"
```

4. Test each integration individually, then test cross-workflow interactions (e.g., saving a Slack link to knowledge base, then using it in a video research card).


---

# 多频道 Presence 同步

## 简介

同步多个平台的在线状态，统一管理社交媒体存在。

**为什么重要**：统一品牌形象，节省时间，提高一致性。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `social_media` | [ClawdHub](https://clawhub.com/skills/social) | 社交媒体 |
| `sync` | [ClawdHub](https://clawhub.com/skills/sync) | 数据同步 |

---

## 使用方式

连接各平台账号，设置同步规则

---

## 来源

- 作者：OpenClaw 社区


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
mkdir multi-channel-personal-assistant && cd multi-channel-personal-assistant
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
multi-channel-personal-assistant/
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
  // TODO: Implement data collection for Multi-Channel Personal Assistant
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
  logger.info('=== 多通道個人助理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 多通道個人助理 報告\n\n${result}`);
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
pm2 start src/index.js --name multi-channel-personal-assistant  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
