---
name: 每日 Reddit 摘要 (Daily Reddit Digest)/nodejs
description: "Use Case #001 Node.js 方案: 每日 Reddit 摘要。使用 Node.js + Reddit .json API (免註冊) + Claude API + Telegram Bot 建立每日自動摘要系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *), Bash(touch *), Bash(chmod *)
---

# Use Case #001: 每日 Reddit 摘要 — Node.js 方案

> 技術棧: Node.js 18+ / Reddit .json API (免註冊) / Anthropic SDK / node-telegram-bot-api
> 難度: 初級 | 時間: 20-30 分鐘

---

## 方案特色

| 優勢 | 說明 |
|------|------|
| **免註冊 Reddit API** | 使用公開 `.json` 端點，不需要 OAuth |
| **新手友善** | npm 一鍵安裝，零門檻 |
| **內建排程** | node-cron 不依賴系統 cron |

### Reddit .json API 原理

Reddit 每個頁面加上 `.json` 就能取得 JSON 資料，無需任何認證：
```
https://www.reddit.com/r/programming/top.json?t=day&limit=10
```

排序方式: `/hot.json` `/top.json?t=day` `/new.json` `/rising.json`

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

安裝指令:
```bash
mkdir daily-reddit-digest && cd daily-reddit-digest
npm init -y
npm install @anthropic-ai/sdk node-telegram-bot-api node-cron dotenv winston
```

---

## 前置準備 Checklist

- [ ] Node.js 18+ 已安裝 (`node --version`)
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather)
- [ ] Telegram Chat ID
- [ ] **不需要** Reddit API 註冊

### Telegram Bot 建立步驟

1. Telegram 搜尋 `@BotFather` → 發送 `/newbot`
2. 取名 → 設定 username (結尾需為 `bot`)
3. 記下 Bot Token
4. 傳訊息給 bot → 訪問 `https://api.telegram.org/bot<TOKEN>/getUpdates` → 記下 `chat.id`

---

## 專案結構

```
daily-reddit-digest/
├── .env                    # 環境變數 (勿 commit)
├── package.json
└── src/
    ├── index.js            # 主程式入口
    ├── config.js           # 設定管理
    ├── redditFetcher.js    # Reddit 資料抓取
    ├── aiSummarizer.js     # Claude AI 摘要
    ├── telegramSender.js   # Telegram 推送
    └── logger.js           # Winston logger
```

---

## 實作流程 (Step by Step)

### Step 1: 建立專案

```bash
mkdir -p daily-reddit-digest/src
cd daily-reddit-digest
npm init -y
npm install @anthropic-ai/sdk node-telegram-bot-api node-cron dotenv winston
```

在 `package.json` 加入 `"type": "module"` 以使用 ES Modules。

### Step 2: 設定環境變數

建立 `.env`:
```bash
# Claude
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Telegram
TELEGRAM_BOT_TOKEN=7123456789:AAxxxxx
TELEGRAM_CHAT_ID=123456789

# Settings
SUBREDDITS=programming,ClaudeAI,MachineLearning,LocalLLaMA
POSTS_PER_SUBREDDIT=10
SCHEDULE_CRON=0 17 * * *
```

### Step 3: logger.js — 日誌

```javascript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.printf(({ timestamp, level, message }) =>
      `[${timestamp}] ${level.toUpperCase()}: ${message}`
    )
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'digest.log' })
  ]
});

export default logger;
```

### Step 4: config.js — 設定管理

```javascript
import 'dotenv/config';

const config = {
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
  telegramChatId: process.env.TELEGRAM_CHAT_ID,
  subreddits: (process.env.SUBREDDITS || 'programming').split(',').map(s => s.trim()),
  postsPerSubreddit: parseInt(process.env.POSTS_PER_SUBREDDIT || '10'),
  scheduleCron: process.env.SCHEDULE_CRON || '0 17 * * *',
};

export function validate() {
  const required = ['anthropicApiKey', 'telegramBotToken', 'telegramChatId'];
  const missing = required.filter(k => !config[k]);
  if (missing.length) throw new Error(`Missing env: ${missing.join(', ')}`);
  return true;
}

export default config;
```

### Step 5: redditFetcher.js — Reddit 抓取 (免註冊)

```javascript
import logger from './logger.js';

const USER_AGENT = 'daily-reddit-digest/1.0';
const BASE_URL = 'https://www.reddit.com';

export async function fetchSubredditPosts(subreddit, limit = 10) {
  const url = `${BASE_URL}/r/${subreddit}/top.json?t=day&limit=${limit}`;

  const res = await fetch(url, {
    headers: { 'User-Agent': USER_AGENT }
  });

  if (!res.ok) {
    throw new Error(`Reddit API error: ${res.status} ${res.statusText}`);
  }

  const data = await res.json();

  return data.data.children.map(({ data: post }) => ({
    title: post.title,
    url: post.url,
    score: post.score,
    numComments: post.num_comments,
    subreddit,
    selftext: (post.selftext || '').slice(0, 2000),
    permalink: `https://reddit.com${post.permalink}`,
    author: post.author || '[deleted]',
  }));
}

export async function fetchAllPosts(subreddits, limit = 10) {
  const allPosts = [];

  for (const sub of subreddits) {
    try {
      const posts = await fetchSubredditPosts(sub, limit);
      allPosts.push(...posts);
      logger.info(`r/${sub}: ${posts.length} posts fetched`);

      // Rate limit: wait 1s between requests (public API ~10 req/min)
      await new Promise(r => setTimeout(r, 1000));
    } catch (err) {
      logger.error(`r/${sub}: ${err.message}`);
    }
  }

  return allPosts;
}
```

### Step 6: aiSummarizer.js — Claude AI 摘要

```javascript
import Anthropic from '@anthropic-ai/sdk';
import logger from './logger.js';

const SYSTEM_PROMPT = `你是 Reddit 每日摘要助手。請用繁體中文產生結構化的每日摘要報告。

格式要求：
1. 開頭用一句話總結今日重點趨勢
2. 依 subreddit 分類列出重點貼文
3. 每篇貼文用 2-3 句話摘要重點
4. 附上原文連結
5. 結尾列出今日關鍵字標籤`;

export async function summarizePosts(apiKey, posts) {
  const client = new Anthropic({ apiKey });

  const postsText = posts.map(p =>
    `### [${p.subreddit}] ${p.title}\n` +
    `Score: ${p.score} | Comments: ${p.numComments} | Author: u/${p.author}\n` +
    `URL: ${p.permalink}\n` +
    `Content: ${p.selftext.slice(0, 500) || '(no body)'}`
  ).join('\n\n---\n\n');

  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4096,
    system: SYSTEM_PROMPT,
    messages: [{
      role: 'user',
      content: `以下是今日 Reddit 熱門貼文，請產生每日摘要報告：\n\n${postsText}`
    }]
  });

  const summary = response.content[0].text;
  const tokensUsed = response.usage.input_tokens + response.usage.output_tokens;
  logger.info(`Claude summary generated (${tokensUsed} tokens)`);

  return summary;
}
```

### Step 7: telegramSender.js — Telegram 推送

```javascript
import TelegramBot from 'node-telegram-bot-api';
import logger from './logger.js';

export async function sendDigest(botToken, chatId, text) {
  const bot = new TelegramBot(botToken);
  const maxLen = 4096;

  // Split by paragraph boundaries
  const chunks = [];
  let current = '';

  for (const line of text.split('\n')) {
    if (current.length + line.length + 1 > maxLen) {
      if (current) chunks.push(current);
      current = line;
    } else {
      current = current ? `${current}\n${line}` : line;
    }
  }
  if (current) chunks.push(current);

  for (let i = 0; i < chunks.length; i++) {
    try {
      await bot.sendMessage(chatId, chunks[i], { parse_mode: 'Markdown' });
    } catch {
      // Fallback: send without Markdown if parsing fails
      await bot.sendMessage(chatId, chunks[i]);
    }
    logger.info(`Telegram chunk ${i + 1}/${chunks.length} sent`);
  }
}

export async function testConnection(botToken, chatId) {
  const bot = new TelegramBot(botToken);
  await bot.sendMessage(chatId, '✅ Reddit Digest Bot 連線測試成功！');
}
```

### Step 8: index.js — 主程式入口

```javascript
import { writeFileSync, mkdirSync } from 'fs';
import cron from 'node-cron';
import config, { validate } from './config.js';
import { fetchAllPosts } from './redditFetcher.js';
import { summarizePosts } from './aiSummarizer.js';
import { sendDigest } from './telegramSender.js';
import logger from './logger.js';

async function runDigest() {
  const now = new Date().toISOString().split('T')[0];
  logger.info(`===== Reddit Daily Digest - ${now} =====`);

  try {
    // 1. Validate config
    validate();

    // 2. Fetch Reddit posts
    logger.info(`Fetching from ${config.subreddits.length} subreddits...`);
    const posts = await fetchAllPosts(config.subreddits, config.postsPerSubreddit);
    logger.info(`Total: ${posts.length} posts fetched`);

    if (posts.length === 0) {
      logger.warn('No posts found, skipping.');
      return;
    }

    // 3. Generate AI summary
    logger.info('Generating AI summary...');
    const summary = await summarizePosts(config.anthropicApiKey, posts);

    // 4. Save locally
    mkdirSync('output', { recursive: true });
    const filename = `output/${now}.md`;
    writeFileSync(filename, summary, 'utf-8');
    logger.info(`Saved to ${filename}`);

    // 5. Send via Telegram
    logger.info('Sending to Telegram...');
    const header = `📰 *Reddit 每日摘要* - ${now}\n\n`;
    await sendDigest(config.telegramBotToken, config.telegramChatId, header + summary);

    logger.info('✅ Done!');
  } catch (err) {
    logger.error(`Pipeline failed: ${err.message}`);
    // Try to notify via Telegram
    try {
      const TelegramBot = (await import('node-telegram-bot-api')).default;
      const bot = new TelegramBot(config.telegramBotToken);
      await bot.sendMessage(config.telegramChatId, `❌ Digest failed: ${err.message}`);
    } catch { /* silent */ }
  }
}

// CLI: --run-once to execute immediately, otherwise start cron
const args = process.argv.slice(2);
if (args.includes('--run-once')) {
  runDigest();
} else {
  logger.info(`Scheduling digest at: ${config.scheduleCron}`);
  cron.schedule(config.scheduleCron, runDigest);
  logger.info('Cron job started. Waiting for next trigger...');
}
```

### Step 9: 執行與排程

```bash
# 立即執行一次 (測試)
node src/index.js --run-once

# 啟動內建排程 (每天 17:00)
node src/index.js

# 用 pm2 持久化 (推薦)
npm install -g pm2
pm2 start src/index.js --name reddit-digest
pm2 save
pm2 startup
```

---

## 測試步驟

| 階段 | 測試什麼 | 指令 | 預期結果 |
|------|---------|------|---------|
| 1 | 環境變數 | `node -e "import('./src/config.js').then(m => m.validate())"` | 無錯誤 |
| 2 | Reddit 抓取 | `node -e "import('./src/redditFetcher.js').then(m => m.fetchSubredditPosts('programming', 3).then(console.log))"` | 回傳 3 篇 |
| 3 | Telegram 連線 | `node -e "import('./src/telegramSender.js').then(m => m.testConnection(...))"` | 手機收到 |
| 4 | 完整流程 | `node src/index.js --run-once` | 收到完整報告 |

---

## 常見陷阱

| 問題 | 原因 | 解法 |
|------|------|------|
| `429 Too Many Requests` | 未設 User-Agent 或請求太快 | 已內建 User-Agent + 1s delay |
| `ERR_REQUIRE_ESM` | 未設 `"type": "module"` | 在 package.json 加入 |
| Telegram 訊息截斷 | 超過 4096 字元 | 已內建分段傳送 |
| node-cron 不觸發 | 時區問題 | 設定 `timezone` 參數 |
| pm2 重啟後環境變數遺失 | .env 路徑問題 | 用 `pm2 start --env` 或絕對路徑 |

---

## 完整參考

詳細程式碼 (含進階擴充): `docs/daily-reddit-digest-nodejs-tutorial.md`
