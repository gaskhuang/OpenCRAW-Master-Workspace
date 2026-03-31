---
name: 品牌社群監控 (Brand Social Monitoring)/nodejs
description: "Use Case #005 Node.js 方案: 品牌社群監控。使用 Node.js 實作 Brand Social Monitoring 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #005: 品牌社群監控 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# 社交媒体监控器

## 简介

监控品牌提及、行业趋势和竞争对手动态。这个使用案例追踪多个社交平台，生成每日报告，并在重要事件发生时立即通知你。

**为什么重要**：及时了解品牌声誉，把握行业趋势，快速响应危机。

**真实例子**：一家初创公司使用此代理监控品牌提及，当一位 KOL 发布负面评论时，代理立即通知团队，使他们能够在 30 分钟内响应并解决问题。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `twitter` | [ClawdHub](https://clawhub.com/skills/twitter) | 监控 X/Twitter |
| `reddit` | [ClawdHub](https://clawhub.com/skills/reddit) | 监控 Reddit |
| `sentiment` | [ClawdHub](https://clawhub.com/skills/sentiment) | 情感分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送通知 |

---

## 设置步骤

### 1. 前置条件

- 社交媒体 API 密钥
- 监控关键词列表
- 竞争对手列表

### 2. 提示词模板

```markdown
## 社交媒体监控器

你是我的社交媒体分析师。监控并报告相关提及：

### 监控范围

**品牌监控**
- 公司名称
- 产品名称
- 品牌标签
- CEO/创始人提及

**行业监控**
- 行业关键词
- 趋势话题
- 技术讨论
- 市场动态

**竞争对手监控**
- 竞争对手动态
- 产品发布
- 营销活动
- 用户反馈

### 分析维度

**情感分析**
- 正面提及
- 负面提及
- 中性讨论
- 情感趋势

**影响力评估**
- 提及者粉丝数
- 互动量
- 传播范围
- 潜在影响

### 报告格式
```
📊 每日社交监控报告 - YYYY-MM-DD

🔥 热门提及
1. [提及内容] - [平台]
   作者：[用户名] ([粉丝数])
   互动：[点赞] [转发] [评论]
   情感：[正面/负面/中性]

📈 趋势分析
- 今日提及量：+15%
- 情感评分：7.2/10
- 热门话题：[话题列表]

⚠️ 需要关注
- [负面提及摘要]
- 建议响应：[建议]

👥 竞争对手动态
- [竞争对手]：[动态摘要]
```

### 告警规则
- 负面提及 > 100 互动：立即通知
- KOL 提及：30 分钟内通知
- 危机信号：立即通知
- 正面病毒内容：每日汇总
```

### 3. 配置

```
Schedule: */30 * * * *
Action: 扫描平台 → 分析 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 实时监控覆盖
- [ ] 重要提及零遗漏
- [ ] 响应时间 < 30 分钟
- [ ] 品牌声誉改善

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# Competitor Radar 🎯

> Automated competitive intelligence that keeps you one step ahead

## The Problem

You're building a product but have no idea what competitors are doing until customers tell you they switched. Manually checking competitor websites, blogs, and social media is a time sink that falls off your radar within a week. By the time you notice a competitor launched a killer feature or slashed prices, you've already lost deals.

## The Solution

OpenClaw becomes your always-on competitive intelligence analyst. It monitors competitor websites for pricing changes, scans their blogs for product announcements, tracks their social media activity, and delivers a weekly digest with strategic recommendations. When something big happens (major price drop, new feature launch), you get an instant alert.

---

## Setup Guide

### Step 1: Create Your Competitor Config File

Create `competitors.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/competitor-radar
```

```json
// ~/openclaw/competitor-radar/competitors.json
{
  "competitors": [
    {
      "name": "Acme Corp",
      "website": "https://acme.com",
      "pricing_page": "https://acme.com/pricing",
      "blog": "https://acme.com/blog",
      "twitter": "acmecorp",
      "linkedin": "company/acme-corp"
    },
    {
      "name": "BigCo",
      "website": "https://bigco.io",
      "pricing_page": "https://bigco.io/pricing",
      "blog": "https://bigco.io/resources/blog",
      "twitter": "bigco_io"
    },
    {
      "name": "StartupX",
      "website": "https://startupx.com",
      "pricing_page": "https:/

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
mkdir brand-social-monitoring && cd brand-social-monitoring
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
brand-social-monitoring/
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
  // TODO: Implement data collection for Brand Social Monitoring
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
  logger.info('=== 品牌社群監控 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 品牌社群監控 報告\n\n${result}`);
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
pm2 start src/index.js --name brand-social-monitoring  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
