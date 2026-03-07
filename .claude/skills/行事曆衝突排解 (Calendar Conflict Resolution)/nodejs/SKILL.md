---
name: 行事曆衝突排解 (Calendar Conflict Resolution)/nodejs
description: "Use Case #050 Node.js 方案: 行事曆衝突排解。使用 Node.js 實作 Calendar Conflict Resolution 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #050: 行事曆衝突排解 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 日历智能提醒

## 简介

传统的日历提醒只是简单地在事件前通知你。这个使用案例提供基于上下文的智能提醒，考虑你的当前状态、交通时间、准备需求，甚至天气情况。

**为什么重要**：不再错过重要事件，确保每次会议都有充分准备。

**真实例子**：一位顾问使用此代理后，不再因为准备不足而匆忙参加会议，代理会提前提醒他需要准备的材料并估算交通时间。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 访问日历 |
| `maps` | [ClawdHub](https://clawhub.com/skills/maps) | 计算交通时间 |
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 查找相关材料 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送提醒 |

---

## 设置步骤

### 1. 前置条件

- 日历访问权限
- 地图 API 密钥
- 常用位置（家、办公室）

### 2. 提示词模板

```markdown
## 日历智能提醒

你是我的智能助理。监控我的日历并提供上下文感知的提醒：

### 提醒类型

**1. 准备提醒（会议前 24 小时）**
- 会议目的和议程
- 需要准备的材料
- 相关邮件或文档链接
- 参与者背景信息

**2. 出发提醒（根据交通动态计算）**
- 当前位置到会议地点的时间
- 交通状况和替代路线
- 天气对交通的影响
- 建议出发时间

**3. 即时提醒（会议前 15 分钟）**
- 会议链接或地址
- 主要讨论要点
- 需要提出的问题

### 上下文考虑
- 当前位置
- 交通状况
- 天气条件
- 前一项会议的结束时间
- 准备时间需求

### 智能规则
- 如果会议需要出行，提前计算交通时间
- 如果是重要客户，额外准备背景研究
- 如果是首次会议，准备自我介绍要点
- 如果天气恶劣，建议提前出发
```

### 3. 配置

```
Schedule: */15 * * * *
Action: 监控日历 → 计算上下文 → 发送智能提醒
```

---

## 成功指标

- [ ] 从不迟到会议
- [ ] 每次会议都有充分准备
- [ ] 不再错过重要事件
- [ ] 减少会议焦虑

---

## 变体与扩展

### 变体 1：团队会议管理
协调团队会议，确保所有人都有空。

### 变体 2：旅行行程整合
整合航班、酒店和会议到统一提醒。

---

## 故障排除

### 问题：交通时间不准确
**解决方案**：检查地图 API 配置和实时交通数据。

### 问题：提醒过于频繁
**解决方案**：调整提醒频率和优先级规则。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🗓️ Smart Meeting Scheduler

> Schedule meetings in seconds. Timezone math done for you, conflicts detected, follow-ups automated.

---

## The Problem

Scheduling meetings across timezones is a nightmare. You're juggling Calendly links, checking five people's availability, doing timezone math in your head, and manually sending follow-up reminders. Half the meeting gets wasted because nobody sent an agenda, and action items disappear into the void after the call ends.

---

## The Solution

OpenClaw handles the entire meeting lifecycle: finds times that work across timezones, checks everyone's availability, sends calendar invites with context, reminds participants before the meeting, and automatically captures and distributes follow-up action items.

---

## Setup Guide

### Step 1: Install Calendar Skills

```bash
openclaw skill install calendar       # Google Calendar integration
openclaw skill install ical           # iCal/Apple Calendar support
openclaw skill install remind-me      # Smart reminders
openclaw skill install gmail          # Email invites
```

### Step 2: Configure Timezone Preferences

Create `~/openclaw/meetings/config.json`:

```json
{
  "myTimezone": "America/New_York",
  "workingHours": {
    "start": "09:00",
    "end": "18:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  },
  "bufferMinutes": 15,
  "defaultDuration": 30,
  "preferredTimes": ["10:00", "14:00", "16:00"],
  "avoidTimes": ["12:00-13:00"]
}
```

### Step 3: Set Up Contact Timezones

Create `~/openclaw/meetings/contacts.json`:

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
mkdir calendar-conflict-resolution && cd calendar-conflict-resolution
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
calendar-conflict-resolution/
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
  // TODO: Implement data collection for Calendar Conflict Resolution
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
  logger.info('=== 行事曆衝突排解 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 行事曆衝突排解 報告\n\n${result}`);
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
pm2 start src/index.js --name calendar-conflict-resolution  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
