---
name: 收件匣清理器 (Inbox Cleaner)/nodejs
description: "Use Case #032 Node.js 方案: 收件匣清理器。使用 Node.js 實作 Inbox Cleaner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #032: 收件匣清理器 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Inbox De-clutter

Newsletters can take up the inbox like nothing else. Often times they pile-up without being opened at all. 

## Skills you Need
[Gmail OAuth Setup](https://clawhub.ai/kai-jar/gmail-oauth).

## How to Set it Up
1. [optional] Create a new gmail specifically for OpenClaw.
2. [optional] Unsubscribe from all newsletters from your main email and subscribe to them using the OpenClaw email.
3. Install the skill and make sure it works. 
4. Instruct OpenClaw:
```txt
I want you to run a cron job everyday at 8 p.m. to read all the newsletter emails of the past 24 hours and give me a digest of the most important bits along with links to read more. Then ask for my feedback on whether you picked good bits, and update your memory based on my preferences for better digests in the future jobs.
```

---

# 收件箱分类与跟进

## 简介

自动分类邮件、起草回复、总结线程、建议下一步行动。适合创始人、销售、客户服务和客服人员。

**为什么重要**：减少邮件处理时间，确保重要邮件不被遗漏，提高响应效率。

**真实例子**：一位销售总监使用此代理管理每日 200+ 邮件，代理自动分类、起草回复，邮件处理时间从 3 小时减少到 30 分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 邮件处理 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `task_manager` | [ClawdHub](https://clawhub.com/skills/tasks) | 创建任务 |

---

## 使用方式

### 自动分类
- 客户邮件
- 内部通知
- 营销邮件
- 紧急事项

### 起草回复
代理根据邮件内容起草回复建议

### 跟进提醒
自动创建跟进任务

---

## 来源

- 来源：Quantum Byte


---

# 📧 Email Triage Autopilot

> Transform inbox chaos into organized action. Stop drowning in emails—let OpenClaw surface what matters.

---

## The Problem

The average professional receives 120+ emails daily, spending 2-3 hours just reading and sorting them. Most are noise (newsletters, notifications, CC chains), but buried in there are urgent requests, deadlines, and opportunities that get missed. You either live in your inbox anxiously or miss important things while trying to batch-check. Neither works.

---

## The Solution

OpenClaw continuously monitors your inbox, categorizes every email by urgency and importance, drafts responses to routine queries, extracts action items into your todo system, and delivers a concise morning briefing of what actually needs your attention. You check email once or twice a day, fully informed, and respond only to what matters.

**The magic:** OpenClaw learns YOUR priorities—who's important, what topics are urgent, which newsletters you actually read vs. ignore.

---

## Setup Guide

### Step 1: Install the Gmail Skill (5 minutes)

```bash
# Install the gmail skill
openclaw skill install gmail

# Authenticate (opens browser for OAuth)
openclaw skill gmail auth
```

For other providers:
- **Outlook:** `openclaw skill install outlook`
- **IMAP:** `openclaw skill install imap` (works with any provider)

### Step 2: Create Your Priority Rules File

Create `~/openclaw/email-rules.md`:

```markdown
# Email Priority Rules

## 🔴 URGENT (notify immediately)
- From: [boss@company.com, ceo@company.com, wife@family.com]
- Subject contains: "urgent", "asap", "emergency", 

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
mkdir inbox-cleaner && cd inbox-cleaner
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
inbox-cleaner/
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
  // TODO: Implement data collection for Inbox Cleaner
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
  logger.info('=== 收件匣清理器 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 收件匣清理器 報告\n\n${result}`);
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
pm2 start src/index.js --name inbox-cleaner  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
