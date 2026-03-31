---
name: 競品定價即時追蹤 (Competitor Pricing Tracker)/nodejs
description: "Use Case #056 Node.js 方案: 競品定價即時追蹤。使用 Node.js 實作 Competitor Pricing Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #056: 競品定價即時追蹤 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 商業、行銷與銷售

---

## 原始需求 (來自 Source Repos)

# 价格比较购物助手

## 简介

想买的商品在不同平台价格不同？这个使用案例自动追踪你关注的商品价格，比较多个平台，在价格下降时通知你，并预测最佳购买时机。

**为什么重要**：省钱，确保买到最优价格，避免错过促销。

**真实例子**：一位用户想购买一台相机，代理追踪了 5 个平台的价格，在 Prime Day 时通知他最低价格，帮他节省了 300 美元。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `web_scraping` | [ClawdHub](https://clawhub.com/skills/scraping) | 抓取价格 |
| `price_api` | [ClawdHub](https://clawhub.com/skills/price) | 获取价格 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送通知 |

---

## 设置步骤

### 1. 前置条件

- 购物清单
- 目标价格（可选）
- 通知渠道

### 2. 提示词模板

```markdown
## 价格比较购物助手

你是我的购物助手。追踪价格并推荐最佳购买时机：

### 功能

**价格追踪**
- 监控多个电商平台
- 记录历史价格
- 识别价格趋势
- 检测促销活动

**价格比较**
- 比较同款商品不同平台
- 考虑运费和税费
- 计算总成本
- 推荐最佳选项

**智能提醒**
- 价格达到目标时通知
- 促销活动开始时通知
- 价格异常下降时通知
- 库存紧张时通知

**购买建议**
- 预测价格趋势
- 建议等待或立即购买
- 估算最佳购买时间
- 提供替代选项

### 通知格式
```
💰 价格提醒

📦 商品：[名称]
💵 当前价格：$XX.XX
📉 历史最低：$XX.XX
📊 价格趋势：下降/上升/稳定

🏪 各平台价格：
- 平台 A：$XX.XX
- 平台 B：$XX.XX
- 平台 C：$XX.XX

💡 建议：[等待/立即购买]
理由：[原因]
```

### 价格历史
```
📈 价格历史 - [商品名]

30 天趋势：📉
平均价格：$XX.XX
最低价格：$XX.XX (日期)
最高价格：$XX.XX (日期)

预测：未来 7 天可能 [上涨/下降/稳定]
```
```

### 3. 配置

```
Schedule: */6 * * * *
Action: 检查价格 → 分析 → 发送通知
```

---

## 成功指标

- [ ] 价格监控覆盖目标商品
- [ ] 及时收到降价通知
- [ ] 平均节省 > 15%
- [ ] 不错过重要促销

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 💰 Price Drop Alerter

> Never pay full price again. Get alerted the moment prices drop.

---

## The Problem

You want to buy something but it's too expensive. You check periodically, forget, then buy at full price right before a sale. Or you set alerts that spam you with 1% changes. Neither works.

---

## The Solution

OpenClaw monitors products across multiple retailers, tracks price history, predicts good buying times, and alerts you only when prices hit YOUR target or drop significantly.

---

## Setup Guide

### Step 1: Install Shopping Skills

```bash
openclaw skill install camelcamelcamel-alerts  # Amazon price tracking
openclaw skill install marktplaats  # Dutch marketplace
openclaw skill install whcli  # Austrian Willhaben
```

### Step 2: Create Watchlist

Create `~/openclaw/shopping/watchlist.json`:

```json
{
  "items": [
    {
      "name": "Sony WH-1000XM5",
      "url": "https://amazon.com/dp/...",
      "targetPrice": 280,
      "currentPrice": 350,
      "addedDate": "2026-01-15",
      "priority": "high"
    },
    {
      "name": "Standing Desk",
      "url": "https://...",
      "targetPrice": 400,
      "currentPrice": 599,
      "addedDate": "2026-01-20",
      "priority": "medium"
    }
  ],
  "priceHistory": {}
}
```

### Step 3: Set Alert Preferences

Create `~/openclaw/shopping/preferences.md`:

```markdown
# Alert Preferences

## Notify me when:
- Price drops below my target
- Price drops 20%+ from recent high
- Lowest price in 30 days
- Lightning deals on watchlist items

## Don't notify for:
- Price changes < 5%
- Items I marked "not urgent"
- Out of stock alerts

## Check frequency:
- High priority: Every 2 hours
- Medium priority: Every 6 hours
- Low priority: Daily
```

---

#

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
mkdir competitor-pricing-tracker && cd competitor-pricing-tracker
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
competitor-pricing-tracker/
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
  // TODO: Implement data collection for Competitor Pricing Tracker
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
  logger.info('=== 競品定價即時追蹤 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 競品定價即時追蹤 報告\n\n${result}`);
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
pm2 start src/index.js --name competitor-pricing-tracker  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
