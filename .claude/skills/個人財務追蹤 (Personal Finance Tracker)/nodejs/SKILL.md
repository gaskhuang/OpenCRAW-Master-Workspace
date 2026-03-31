---
name: 個人財務追蹤 (Personal Finance Tracker)/nodejs
description: "Use Case #107 Node.js 方案: 個人財務追蹤。使用 Node.js 實作 Personal Finance Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #107: 個人財務追蹤 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 金融與交易

---

## 原始需求 (來自 Source Repos)

# 个人财务追踪器

## 简介

管理个人财务需要持续追踪支出、收入和预算。这个使用案例自动分类交易，生成支出报告，提醒账单，并提供储蓄建议。

**为什么重要**：了解资金流向，控制支出，实现财务目标。

**真实例子**：一位自由职业者使用此代理追踪收入和支出，代理自动分类交易、生成税务报告、提醒账单，帮他节省了每月 10 小时的财务管理工作。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `banking` | [ClawdHub](https://clawhub.com/skills/banking) | 获取交易 |
| `spreadsheet` | [ClawdHub](https://clawhub.com/skills/sheets) | 数据记录 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送报告 |

---

## 设置步骤

### 1. 前置条件

- 银行账户访问权限
- 预算类别设置
- 财务目标

### 2. 提示词模板

```markdown
## 个人财务追踪器

你是我的财务助手。追踪和分析我的财务状况：

### 功能

**交易追踪**
- 自动导入银行交易
- 智能分类支出
- 识别重复交易
- 标记异常支出

**预算管理**
- 设置月度预算
- 追踪各类别支出
- 预警超支风险
- 建议调整方案

**报告生成**
- 每日支出摘要
- 每周趋势分析
- 月度财务报告
- 年度总结

**智能提醒**
- 账单到期提醒
- 预算接近上限提醒
- 异常交易提醒
- 储蓄目标进度

### 支出分类
- 餐饮
- 交通
- 购物
- 娱乐
- 住房
- 医疗
- 教育
- 储蓄
- 投资
- 其他

### 报告格式
```
💰 月度财务报告 - YYYY-MM

📊 概览
- 总收入：$XXXX
- 总支出：$XXXX
- 净储蓄：$XXXX
- 储蓄率：XX%

📈 支出分析
餐饮：$XXX (XX%)
交通：$XXX (XX%)
购物：$XXX (XX%)
...

💡 洞察
- 本月最大支出：[类别]
- 相比上月：[+/- X%]
- 预算执行情况：[良好/需改进]

🎯 储蓄目标
- 目标：$XXXX
- 已存：$XXXX
- 进度：XX%
- 预计达成：[日期]

⚠️ 提醒
- [账单] 将于 [日期] 到期
- [类别] 预算即将超支
```
```

### 3. 配置

```
Schedule: 0 9 * * *
Action: 导入交易 → 分类 → 分析 → 生成报告
```

---

## 成功指标

- [ ] 所有交易自动分类
- [ ] 预算执行率 > 80%
- [ ] 储蓄目标按计划进行
- [ ] 财务透明度提升

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 💳 Expense Tracker & Analyzer

> Know where your money goes. Without manual data entry.

---

## The Problem

Tracking expenses is tedious. You start with good intentions, manually log for a week, then stop. Bank statements show transactions but no insights. By month-end, you're wondering where the money went.

---

## The Solution

OpenClaw automatically categorizes transactions, identifies spending patterns, alerts on unusual charges, and gives you clear insights—no manual entry required.

---

## Setup Guide

### Step 1: Install Finance Skills

```bash
openclaw skill install copilot-money  # or plaid
openclaw skill install excel
```

### Step 2: Configure Categories

Create `~/openclaw/expenses/categories.json`:

```json
{
  "categories": {
    "essentials": ["rent", "utilities", "groceries", "insurance"],
    "transport": ["uber", "lyft", "gas", "transit"],
    "food": ["restaurants", "delivery", "coffee"],
    "subscriptions": ["netflix", "spotify", "gym"],
    "shopping": ["amazon", "clothing"],
    "health": ["pharmacy", "doctor"]
  },
  "budgets": {
    "food": 500,
    "subscriptions": 100,
    "shopping": 300
  }
}
```

### Step 3: Set Alert Rules

Create `~/openclaw/expenses/alerts.md`:

```markdown
# Expense Alerts

## Notify Immediately
- Transactions > $100
- New recurring charges
- International transactions
- Declined transactions

## Weekly Check
- Category over budget by >20%
- Unusual spending pattern
- Forgotten subscriptions

## Monthly Review
- Total vs budget
- Category breakdown
- Subscription audit
```

---

## Skills Needed

| Skill | Purpose |
|-------|-------

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
mkdir personal-finance-tracker && cd personal-finance-tracker
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
personal-finance-tracker/
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
  // TODO: Implement data collection for Personal Finance Tracker
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
  logger.info('=== 個人財務追蹤 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 個人財務追蹤 報告\n\n${result}`);
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
pm2 start src/index.js --name personal-finance-tracker  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
