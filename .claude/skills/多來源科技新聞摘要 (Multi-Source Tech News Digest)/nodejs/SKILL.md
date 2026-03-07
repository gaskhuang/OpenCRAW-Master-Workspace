---
name: 多來源科技新聞摘要 (Multi-Source Tech News Digest)/nodejs
description: "Use Case #004 Node.js 方案: 多來源科技新聞摘要。使用 Node.js 實作 Multi-Source Tech News Digest 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #004: 多來源科技新聞摘要 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# Multi-Source Tech News Digest

Automatically aggregate, score, and deliver tech news from 109+ sources across RSS, Twitter/X, GitHub releases, and web search — all managed through natural language.

## Pain Point

Staying updated across AI, open-source, and frontier tech requires checking dozens of RSS feeds, Twitter accounts, GitHub repos, and news sites daily. Manual curation is time-consuming, and most existing tools either lack quality filtering or require complex configuration.

## What It Does

A four-layer data pipeline that runs on a schedule:

1. **RSS Feeds** (46 sources) — OpenAI, Hacker News, MIT Tech Review, etc.
2. **Twitter/X KOLs** (44 accounts) — @karpathy, @sama, @VitalikButerin, etc.
3. **GitHub Releases** (19 repos) — vLLM, LangChain, Ollama, Dify, etc.
4. **Web Search** (4 topic searches) — via Brave Search API

All articles are merged, deduplicated by title similarity, and quality-scored (priority source +3, multi-source +5, recency +2, engagement +1). The final digest is delivered to Discord, email, or Telegram.

The framework is fully customizable — add your own RSS feeds, Twitter handles, GitHub repos, or search queries in 30 seconds.

## Prompts

**Install and set up daily digest:**
```text
Install tech-news-digest from ClawHub. Set up a daily tech digest at 9am to Discord #tech-news channel. Also send it to my email at myemail@example.com.
```

**Add custom sources:**
```text
Add these to my tech digest sources:
- RSS: https://my-company-blog.com/feed
- Twitter: @myFavResearcher
- GitHub: my-org/my-framework
```

**Generate on demand:**
```text
Generate a tech digest for the past 24 hours and send it here.
```

## Skills Needed

- [tech-news-digest](https://clawhub.ai/skills/tech-news-digest) — Install via `clawhub install tech-news-digest`
- [gog](https://clawhub.ai/skills/gog) (optional) — For email delivery via Gmail

## Environment Variables (Optional)

- `X_BEARER_TOKEN` — Twitter/X API bearer token for KOL monitoring
- `BRAVE_API_KEY` — Brave Search API key for web search layer
- `GITHUB_TOKEN` — GitHub token for higher API rate limits

## Related Links

- [GitHub Repository](https://github.com/draco-agent/tech-news-digest)
- [ClawHub Page](https://clawhub.ai/skills/tech-news-digest)


---

# 新闻摘要聚合器

## 简介

信息过载时代，这个使用案例聚合多个新闻源，使用 AI 生成个性化摘要，让你快速了解重要信息，无需浏览数十个网站。

**为什么重要**：节省时间，获取多视角信息，避免信息茧房。

**真实例子**：一位投资者使用此代理聚合财经新闻，每天早上 8 点收到包含市场动态、行业分析和公司新闻的摘要，投资决策更加及时准确。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `rss` | [ClawdHub](https://clawhub.com/skills/rss) | 读取 RSS 源 |
| `news_api` | [ClawdHub](https://clawhub.com/skills/news) | 获取新闻 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送摘要 |

---

## 设置步骤

### 1. 前置条件

- RSS 源列表
- 新闻 API 密钥
- 兴趣主题列表

### 2. 提示词模板

```markdown
## 新闻摘要聚合器

你是我的新闻策展人。每天聚合和摘要新闻：

### 新闻源
- 科技：TechCrunch、The Verge、Wired
- 商业：FT、WSJ、Bloomberg
- 行业：特定领域新闻源
- 本地：本地新闻网站

### 处理流程
1. **收集**：获取所有源的最新文

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
mkdir multi-source-tech-news-digest && cd multi-source-tech-news-digest
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
multi-source-tech-news-digest/
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
  // TODO: Implement data collection for Multi-Source Tech News Digest
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
  logger.info('=== 多來源科技新聞摘要 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 多來源科技新聞摘要 報告\n\n${result}`);
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
pm2 start src/index.js --name multi-source-tech-news-digest  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
