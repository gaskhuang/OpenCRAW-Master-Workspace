---
name: 健康與症狀追蹤器 (Health & Symptom Tracker)/nodejs
description: "Use Case #034 Node.js 方案: 健康與症狀追蹤器。使用 Node.js 實作 Health & Symptom Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #034: 健康與症狀追蹤器 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Health & Symptom Tracker

Identifying food sensitivities requires consistent logging over time, which is tedious to maintain. You need reminders to log and analysis to spot patterns.

This workflow tracks food and symptoms automatically:

• Message your food and symptoms in a dedicated Telegram topic and OpenClaw logs everything with timestamps
• 3x daily reminders (morning, midday, evening) prompt you to log meals
• Over time, analyzes patterns to identify potential triggers

## Skills you Need

- Cron jobs for reminders
- Telegram topic for logging
- File storage (markdown log file)

## How to Set it Up

1. Create a Telegram topic called "health-tracker" (or similar).
2. Create a log file: `~/clawd/memory/health-log.md`
3. Prompt OpenClaw:
```text
When I message in the "health-tracker" topic:
1. Parse the message for food items and symptoms
2. Log to ~/clawd/memory/health-log.md with timestamp
3. Confirm what was logged

Set up 3 daily reminders:
- 8 AM: "🍳 Log your breakfast"
- 1 PM: "🥗 Log your lunch"
- 7 PM: "🍽️ Log your dinner and any symptoms"

Every Sunday, analyze the past week's log and identify patterns:
- Which foods correlate with symptoms?
- Are there time-of-day patterns?
- Any clear triggers?

Post the analysis to the health-tracker topic.
```

4. Optional: Add a memory file for OpenClaw to track known triggers and update it as patterns emerge.


---

# 健康习惯养成助手

## 简介

养成健康习惯需要持续追踪和提醒。这个使用案例帮助你建立和维持健康习惯，追踪进度，提供激励，并生成健康报告。

**为什么重要**：改善健康，建立良好习惯，提高生活质量。

**真实例子**：一位用户想养成每天运动的习惯，代理每天提醒、追踪进度、提供鼓励，三个月后他成功养成了每天运动 30 分钟的习惯。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `health` | [ClawdHub](https://clawhub.com/skills/health) | 健康数据 |
| `wearable` | [ClawdHub](https://clawhub.com/skills/wearable) | 穿戴设备 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送提醒 |

---

## 设置步骤

### 1. 前置条件

- 健康目标
- 可穿戴设备（可选）
- 习惯列表

### 2. 提示词模板

```markdown
## 健康习惯养成助手

你是我的健康教练。帮助我建立和维持健康习惯：

### 习惯追踪

**每日习惯**
- 喝水 8 杯
- 运动 30 分钟
- 睡眠 8 小时
- 冥想 10 分钟
- 吃水果蔬菜

**每周习惯**
- 运动 5 天
- 社交活动
- 学习新技能
- 整理环境

### 提醒策略

**早上**
- 7:00：起床，喝水
- 7:30：冥想
- 8:00：健康早餐

**白天**
- 每小时：起身活动
- 12:00：午餐提醒
- 15:00：喝水提醒

**晚上**
- 18:00：运动时间
- 21:00：准备睡觉
- 22:00：睡觉时间

### 进度追踪

**每日检查**
```
🌟 今日习惯打卡

✅ 喝水 8 杯 - 完成！
✅ 运动 30 分钟 - 完成！
⏳ 睡眠 8 小时 - 进行中
✅ 冥想 10 分钟 - 完成！

📊 今日得分：4/5
🔥 连续打卡：12 天
```

**每周报告**
- 习惯完成率
- 趋势分析
- 改进建议
- 庆祝成就

### 激励机制
- 连续打卡奖励
- 里程碑庆祝
- 好友挑战
- 进度可视化
```

### 3. 配置

```
Schedule: 0 7,12,18,21 * * *
Action: 发送提醒 → 追踪进度 → 生成报告
```

---

## 成功指标

- [ ] 习惯完成率 > 80%
- [ ] 连续打卡天数增加
- [ ] 健康指标改善
- [ ] 生活质量提升

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


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
mkdir health-&-symptom-tracker && cd health-&-symptom-tracker
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
health-&-symptom-tracker/
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
  // TODO: Implement data collection for Health & Symptom Tracker
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
  logger.info('=== 健康與症狀追蹤器 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 健康與症狀追蹤器 報告\n\n${result}`);
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
pm2 start src/index.js --name health-&-symptom-tracker  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
