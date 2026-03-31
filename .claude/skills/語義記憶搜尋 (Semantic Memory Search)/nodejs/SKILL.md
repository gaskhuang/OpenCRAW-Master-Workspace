---
name: 語義記憶搜尋 (Semantic Memory Search)/nodejs
description: "Use Case #097 Node.js 方案: 語義記憶搜尋。使用 Node.js 實作 Semantic Memory Search 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #097: 語義記憶搜尋 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Semantic Memory Search

OpenClaw's built-in memory system stores everything as markdown files — but as memories grow over weeks and months, finding that one decision from last Tuesday becomes impossible. There is no search, just scrolling through files.

This use case adds **vector-powered semantic search** on top of OpenClaw's existing markdown memory files using [memsearch](https://github.com/zilliztech/memsearch), so you can instantly find any past memory by meaning, not just keywords.

## What It Does

- Index all your OpenClaw markdown memory files into a vector database (Milvus) with a single command
- Search by meaning: "what caching solution did we pick?" finds the relevant memory even if the word "caching" does not appear
- Hybrid search (dense vectors + BM25 full-text) with RRF reranking for best results
- SHA-256 content hashing means unchanged files are never re-embedded — zero wasted API calls
- File watcher auto-reindexes when memory files change, so the index is always up to date
- Works with any embedding provider: OpenAI, Google, Voyage, Ollama, or fully local (no API key needed)

## Pain Point

OpenClaw's memory is stored as plain markdown files. This is great for portability and human readability, but it has no search. As your memory grows, you either have to grep through files (keyword-only, misses semantic matches) or load entire files into context (wastes tokens on irrelevant content). You need a way to ask "what did I decide about X?" and get the exact relevant chunk, regardless of phrasing.

## Skills You Need

- No OpenClaw skills required — memsearch is a standalone Python CLI/library
- Python 3.10+ with pip or uv

## How to Set It Up

1. Install memsearch:
```bash
pip install memsearch
```

2. Run the interactive config wizard:
```bash
memsearch config init
```

3. Index your OpenClaw memory directory:
```bash
memsearch index ~/path/to/your/memory/
```

4. Search your memories by meaning:
```bash
memsearch search "what caching solution did we pick?"
```

5. For live sync, start the file watcher — it auto-indexes on every file change:
```bash
memsearch watch ~/path/to/your/memory/
```

6. For a fully local setup (no API keys), install the local embedding provider:
```bash
pip install "memsearch[local]"
memsearch config set embedding.provider local
memsearch index ~/path/to/your/memory/
```

## Key Insights

- **Markdown stays the source of truth.** The vector index is just a derived cache — you can rebuild it anytime with `memsearch index`. Your memory files are never modified.
- **Smart dedup saves money.** Each chunk is identified by a SHA-256 content hash. Re-running `index` only embeds new or changed content, so you can run it as often as you like without wasting embedding API calls.
- **Hybrid search beats pure vector search.** Combining semantic similarity (dense vectors) with keyword matching (BM25) via Reciprocal Rank Fusion catches both meaning-based and exact-match queries.

## Related Links

- [memsearch Git

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
mkdir semantic-memory-search && cd semantic-memory-search
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
semantic-memory-search/
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
  // TODO: Implement data collection for Semantic Memory Search
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
  logger.info('=== 語義記憶搜尋 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 語義記憶搜尋 報告\n\n${result}`);
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
pm2 start src/index.js --name semantic-memory-search  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
