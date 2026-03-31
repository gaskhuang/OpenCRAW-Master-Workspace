---
name: 學術研究助手 (Academic Research Assistant)/nodejs
description: "Use Case #018 Node.js 方案: 學術研究助手。使用 Node.js 實作 Academic Research Assistant 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #018: 學術研究助手 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# 📚 Academic Research Assistant

> From literature search to paper draft. Research without the busywork.

---

## The Problem

Academic research is 80% tedious work: finding papers, managing citations, reading dense PDFs, tracking who cited whom. By the time you've organized everything, you've lost momentum on actual thinking. Citation management tools help but don't understand your research questions.

---

## The Solution

OpenClaw becomes your research assistant: searches academic databases, summarizes papers, manages citations, identifies research gaps, and helps you synthesize findings into coherent arguments.

---

## Setup Guide

### Step 1: Install Research Skills

```bash
openclaw skill install arxiv
openclaw skill install literature-review
openclaw skill install semantic-scholar
openclaw skill install pdf-extractor
openclaw skill install brave-search
```

### Step 2: Define Research Focus

Create `~/openclaw/research/focus.md`:

```markdown
# Research Focus

## Current Project
**Topic:** Transformer architectures for time series forecasting
**Question:** How do attention mechanisms compare to RNNs for irregular time series?
**Keywords:** transformers, attention, time series, forecasting, irregular sampling

## Background
- Started: 2024-01
- Advisor: Prof. Smith
- Related work: Informer, Autoformer, PatchTST

## Citation Style
APA 7th Edition

## Key Authors to Track
- Vaswani et al. (attention)
- Zhou et al. (Informer)
- Wu et al. (Autoformer)
```

### Step 3: Set Up Paper Library

Create `~/openclaw/research/papers/` directory structure:

```
papers/
├── to-read/
├── reading/
├── completed/
├── summaries/
└── citations.bib
```

### Step 4: Configure Paper Tracking

Create `~/openclaw/research/reading-list.md`:

```markdown
# Reading List

## Priority (this week)
- [ ] "Attention Is All You Need" - Foundation paper
- [ ] "Informer" - Efficient transformers for long sequences

## Queue
- [ ] "PatchTST" - Patching approach
- [ ] "Autoformer" - Auto-correlation

## Completed (with summaries)
- [x] "LSTM Survey" → summaries/lstm-survey.md
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `arxiv` | Search and download papers |
| `literature-review` | Systematic review automation |
| `semantic-scholar` | Citation graphs, related papers |
| `pdf-extractor` | Extract text from PDFs |
| `brave-search` | Web search for grey literature |

---

## Example Prompts

**Literature search:**
```
Find the 10 most cited papers on [topic] from the last 3 years. Summarize each in 2-3 sentences.
```

**Paper summarization:**
```
Read this paper and give me: (1) main contribution, (2) methodology, (3) key results, (4) limitations, (5) how it relates to my research.
```

**Citation management:**
```
Add this paper to my citations.bib in BibTeX format. Check if I already have it.
```

**Research gap analysis:**
```
Based on the papers I've read, what gaps exist in the literature? What hasn't been tried?
```

**Writing support:**
```
Help me

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
mkdir academic-research-assistant && cd academic-research-assistant
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
academic-research-assistant/
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
  // TODO: Implement data collection for Academic Research Assistant
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
  logger.info('=== 學術研究助手 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 學術研究助手 報告\n\n${result}`);
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
pm2 start src/index.js --name academic-research-assistant  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
