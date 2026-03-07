---
name: 投資組合監控 (Portfolio Monitor)/nodejs
description: "Use Case #104 Node.js 方案: 投資組合監控。使用 Node.js 實作 Portfolio Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #104: 投資組合監控 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# 投资组合监控

## 简介

自动监控被投公司的关键指标、新闻动态、里程碑事件，生成投资组合报告。

**为什么重要**：及时了解被投公司状况，主动提供支持，优化投后管理。

**真实例子**：一家 VC 使用此代理监控 30+ 被投公司，代理自动收集指标和新闻，每周生成投资组合健康报告。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |
| `news` | [ClawdHub](https://clawhub.com/skills/news) | 新闻监控 |
| `reporting` | [ClawdHub](https://clawhub.com/skills/reporting) | 报告生成 |

---

## 使用方式

### 数据收集
- 财务指标
- 用户增长
- 新闻动态
- 社交媒体

### 异常检测
识别需要关注的变化

### 生成报告
投资组合健康度评估

---

## 来源

- 来源：Data Driven VC


---

# 📈 Stock Portfolio Tracker

> Stay informed on your investments. Without checking every hour.

---

## The Problem

Portfolio tracking apps show prices but miss context. What earnings are coming? What news affects your holdings? Most investors either check obsessively (stress) or ignore completely (risk).

---

## The Solution

OpenClaw monitors your portfolio with context: tracks prices, alerts on significant moves, summarizes relevant news, and reminds you of earnings dates. Informed without obsessed.

---

## Setup Guide

### Step 1: Install Finance Skills

```bash
openclaw skill install stock-analysis
openclaw skill install yahoo-finance
openclaw skill install portfolio-watcher
```

### Step 2: Enter Your Holdings

Create `~/openclaw/portfolio/holdings.json`:

```json
{
  "holdings": [
    {
      "symbol": "AAPL",
      "shares": 50,
      "costBasis": 145.00
    },
    {
      "symbol": "GOOGL",
      "shares": 20,
      "costBasis": 125.00
    },
    {
      "symbol": "VTI",
      "shares": 100,
      "costBasis": 220.00
    }
  ],
  "watchlist": ["MSFT", "AMZN", "NVDA"]
}
```

### Step 3: Set Alert Thresholds

Create `~/openclaw/portfolio/alerts.md`:

```markdown
# Portfolio Alerts

## Price Alerts
- Position up/down > 5% in a day
- Hit target price (set per stock)
- 52-week high/low

## News Alerts
- Earnings announcement
- Major news (M&A, leadership, product)
- Analyst rating changes

## Regular Updates
- Daily: Portfolio summary
- Weekly: Performance review
- Quarterly: Rebalancing check
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `stock-analysis` | Stock analysis and metrics |
| `yahoo-finance` | Price and fundamental data |
| `portfolio-watcher` | Portfolio tracking |

---

## Example Prompts

**Morning briefing:**
```
How's my portfolio doing? Any pre-market movers? What earnings are coming this week?
```

**Deep dive:**
```
Analyze AAPL. How's it valued vs peers? What are analysts saying? Any concerns?
```

**Rebalancing:**
```
My tech allocation is 60% of portfolio now. Suggest trades to get back to my 40% target.
```

**Tax planning:**
```
Which positions have losses I could harvest? What's my overall tax situation this year?
```

---

## Cron Schedule

```
0 6 * * 1-5    # 6 AM weekdays - pre-market briefing
0 16 * * 1-5   # 4 PM weekdays - market close summary
0 9 * * 0      # Sunday 9 AM - weekly performance review
0 0 1 */3 *    # Quarterly - rebalancing check
`

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
mkdir portfolio-monitor && cd portfolio-monitor
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
portfolio-monitor/
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
  // TODO: Implement data collection for Portfolio Monitor
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
  logger.info('=== 投資組合監控 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 投資組合監控 報告\n\n${result}`);
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
pm2 start src/index.js --name portfolio-monitor  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
