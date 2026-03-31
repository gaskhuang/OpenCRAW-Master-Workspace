---
name: 廣告創意 AB 測試 (Ad Creative AB Testing)/nodejs
description: "Use Case #068 Node.js 方案: 廣告創意 A/B 測試。使用 Node.js 實作 Ad Creative A/B Testing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #068: 廣告創意 A/B 測試 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 🎨 Design Feedback Assistant

> Get instant UI/UX reviews without waiting for stakeholders. Ship better designs, faster.

---

## The Problem

Designers often work in isolation—you finish a design, share it, and wait days for feedback. When feedback comes, it's scattered across Slack, email, and Figma comments. Accessibility issues get caught in QA (too late). Design systems grow inconsistent because documentation is tedious.

---

## The Solution

OpenClaw provides instant, structured design feedback: reviews UI screenshots for usability issues, audits accessibility compliance, compares against your design system, and helps document components. Get a fresh perspective anytime, not just during review meetings.

---

## Setup Guide

### Step 1: Install Design Skills

```bash
openclaw skill install browser     # Screenshot and visual analysis
openclaw skill install web-fetch   # Reference design patterns
openclaw skill install image       # Image analysis capabilities
```

### Step 2: Create Design Workspace

```bash
mkdir -p ~/openclaw/design/{reviews,components,accessibility}
```

Create `~/openclaw/design/design-system.md`:

```markdown
# Design System Reference

## Colors
- Primary: #2563EB (Blue 600)
- Secondary: #7C3AED (Violet 600)
- Success: #059669 (Green 600)
- Warning: #D97706 (Amber 600)
- Error: #DC2626 (Red 600)

## Typography
- Headings: Inter, semi-bold
- Body: Inter, regular, 16px base
- Line height: 1.5 for body text

## Spacing
- Base unit: 4px
- Common: 8, 16, 24, 32, 48px

## Components
- Buttons: rounded-lg, min-height 44px
- Cards: rounded-xl, shadow-sm
- Inputs: border-gray-300, focus:ring-2
```

### Step 3: Set Up Review Checklist

Create `~/openclaw/design/review-checklist.md`:

```markdown
# UI/UX Review Checklist

## Usability
- [ ] Clear visual hierarchy
- [ ] Obvious primary action
- [ ] Consistent alignment
- [ ] Adequate white space
- [ ] Readable text contrast

## Accessibility
- [ ] Color contrast ≥ 4.5:1 (text)
- [ ] Touch targets ≥ 44x44px
- [ ] Focus states visible
- [ ] Alt text for images
- [ ] Screen reader friendly

## Consistency
- [ ] Matches design system colors
- [ ] Correct typography scale
- [ ] Standard component patterns
- [ ] Consistent iconography
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `browser` | Capture screenshots, inspect live sites |
| `image` | Analyze design screenshots |
| `web-fetch` | Pull design pattern references |
| `figma-api` | Connect to Figma files (optional) |

---

## Example Prompts

**UI review:**
```
Review this screenshot of my dashboard design. Check for visual hierarchy, alignment issues, and usability problems. Be specific about what to fix.
[attach screenshot]
```

**Accessibility audit:**
```
Audit this design for WCAG 2.1 AA compliance. Check color contrast, touch targets, and focus states. List all issues with severity ratings.
[attach screenshot]
```

**Design system check:**
```
Compare this component against my design system in ~/open

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
mkdir ad-creative-a/b-testing && cd ad-creative-a/b-testing
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
ad-creative-a/b-testing/
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
  // TODO: Implement data collection for Ad Creative A/B Testing
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
  logger.info('=== 廣告創意 A/B 測試 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 廣告創意 A/B 測試 報告\n\n${result}`);
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
pm2 start src/index.js --name ad-creative-a/b-testing  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
