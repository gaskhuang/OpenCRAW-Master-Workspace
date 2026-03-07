---
name: 一文多平台內容複製 (Cross-Platform Content Repurposing)/nodejs
description: "Use Case #017 Node.js 方案: 一文多平台內容複製。使用 Node.js 實作 Cross-Platform Content Repurposing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #017: 一文多平台內容複製 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# Content Multiplication Engine

> Turn one piece of content into 10+ platform-specific posts automatically.

## The Problem

Creating content for one platform is hard enough—repurposing it for Twitter, LinkedIn, Instagram, newsletters, and Reddit is a time sink that kills consistency. Most creators either post the same thing everywhere (which performs poorly) or spend hours manually reformatting, losing momentum and burning out. The result? Great content stuck on one platform while your audience waits elsewhere.

## The Solution

OpenClaw acts as your always-on content repurposing assistant. Drop a blog post URL, paste a video transcript, or share podcast notes—OpenClaw transforms it into platform-native content for every channel you care about. It understands each platform's style: Twitter threads with hooks, LinkedIn thought-leadership angles, Instagram carousel concepts, punchy newsletter snippets, and Reddit-appropriate discussion starters. Set it up once, and your content multiplies while you sleep.

## Setup Guide

### Step 1: Create Your Content Workspace (2 minutes)

```bash
mkdir -p ~/content-engine/{input,output,templates}
```

Create a simple input structure in `~/content-engine/input/`:
- Drop source files here (`.md`, `.txt`, or just URLs)

### Step 2: Create Platform Templates (5 minutes)

Create `~/content-engine/templates/platforms.md`:

```markdown
# Platform Guidelines

## Twitter/X Thread
- Hook in first tweet (curiosity gap or bold statement)
- 5-10 tweets max, each standalone valuable
- End with CTA or callback to first tweet
- Use line breaks for readability
- No hashtags in thread, maybe 1-2 at end

## LinkedIn Post
- First line is the hook (before "see more")
- Personal angle or story lead-in
- Insights with white space between points
- End with question to drive comments
- 1300-1500 chars ideal
- 3-5 relevant hashtags at bottom

## Instagram Caption
- Hook in first line (emoji optional)
- Story or value in 2-3 short paragraphs  
- CTA: save, share, comment prompt
- Hashtags: 20-30 relevant ones in first comment (provide separately)
- Carousel slide concepts if applicable

## Newsletter Snippet
- TL;DR in 2-3 sentences
- Key insight or quote pullout
- "Read more" hook with link placeholder
- Keep under 150 words

## Reddit Post
- Title: Question or discussion-starter format
- No self-promotion tone
- Add genuine value first
- Mention source naturally at end
- Adapt to subreddit culture (specify which sub)
```

### Step 3: Add to TOOLS.md (1 minute)

Add this to your `~/openclaw/TOOLS.md`:

```markdown
### Content Engine
- Input folder: ~/content-engine/input/
- Output folder: ~/content-engine/output/
- Templates: ~/content-engine/templates/platforms.md
- Default platforms: Twitter, LinkedIn, Newsletter
```

### Step 4: Configure HEARTBEAT.md (2 minutes)

Add this section to your `~/openclaw/HEARTBEAT.md`:

```markdown
### Content Multiplication Check
- [ ] Check ~/content-engine/input/ for new files
- [ ] If found: Proces

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
mkdir cross-platform-content-repurposing && cd cross-platform-content-repurposing
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
cross-platform-content-repurposing/
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
  // TODO: Implement data collection for Cross-Platform Content Repurposing
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
  logger.info('=== 一文多平台內容複製 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 一文多平台內容複製 報告\n\n${result}`);
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
pm2 start src/index.js --name cross-platform-content-repurposing  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
