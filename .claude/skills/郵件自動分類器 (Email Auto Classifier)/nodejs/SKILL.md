---
name: 郵件自動分類器 (Email Auto Classifier)/nodejs
description: "Use Case #046 Node.js 方案: 郵件自動分類器。使用 Node.js 實作 Email Auto Classifier 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #046: 郵件自動分類器 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 邮件自动分类器

## 简介

收件箱被大量邮件淹没？这个使用案例自动分类和优先级排序你的邮件，将重要邮件突出显示，自动归档低优先级邮件，并为需要回复的邮件设置提醒。

**为什么重要**：减少邮件处理时间，确保重要邮件不被遗漏。

**真实例子**：一位项目经理每天收到 200+ 邮件，使用此代理后，只需关注被标记为"紧急"和"重要"的 20-30 封邮件，效率提高了 3 倍。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 读取和分类邮件 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 自然语言处理 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 设置提醒 |

---

## 设置步骤

### 1. 前置条件

- 邮件账号访问权限
- 分类规则偏好

### 2. 提示词模板

```markdown
## 邮件自动分类器

你是我的邮件助手。每 15 分钟检查一次新邮件并执行以下操作：

### 分类规则

**紧急**（立即通知）
- 来自直接上级的邮件
- 包含"紧急"、"ASAP"、"立即"等关键词
- 系统故障或安全警报

**重要**（1 小时内处理）
- 客户邮件
- 项目截止日期相关
- 会议邀请需要回复

**普通**（当天处理）
- 内部通知
- 一般询问
- 更新和公告

**低优先级**（批量处理）
- 新闻通讯
- 营销邮件
- 自动通知

### 自动操作
1. **归档**：新闻通讯、营销邮件自动归档
2. **标记**：项目相关邮件添加标签
3. **提醒**：需要回复的邮件设置提醒
4. **摘要**：每小时发送重要邮件摘要

### 学习规则
- 根据我的操作学习偏好
- 记住我常联系的人
- 识别重要项目关键词
- 调整分类准确性
```

### 3. 配置

```
Schedule: */15 * * * *
Action: 检查邮件 → 分类 → 执行操作 → 发送摘要
```

---

## 成功指标

- [ ] 邮件处理时间减少 50%
- [ ] 重要邮件零遗漏
- [ ] 收件箱保持整洁
- [ ] 自动分类准确率 > 90%

---

## 变体与扩展

### 变体 1：智能回复建议
为常见邮件类型生成回复建议。

### 变体 2：邮件摘要报告
每天生成邮件活动摘要报告。

---

## 故障排除

### 问题：邮件分类错误
**解决方案**：提供反馈给代理，帮助它学习你的偏好。

### 问题：重要邮件被归档
**解决方案**：调整分类规则和关键词。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📧 Email Triage Autopilot

> Transform inbox chaos into organized action. Stop drowning in emails—let OpenClaw surface what matters.

---

## The Problem

The average professional receives 120+ emails daily, spending 2-3 hours just reading and sorting them. Most are noise (newsletters, notifications, CC chains), but buried in there are urgent requests, deadlines, and opportunities that get missed. You either live in your inbox anxiously or miss important things while trying to batch-check. Neither works.

---

## The Solution

OpenClaw continuously monitors your inbox, categorizes every email by urgency and importance, drafts responses to routine queries, extracts action items into your todo system, and delivers a concise morning briefing of what actually needs your attention. You check email once or twice a day, fully informed, and respond only to what matters.

**The magic:** OpenClaw learns YOUR priorities—who's important, what topics are urgent, which newsletters you actually read vs. ignore.

---

## Setup Guide

### Step 1: Install the Gmail Skill (5 minutes)

```bash
# Install the gmail skill
openclaw skill install gmail

# Authenticate (opens browser for OAuth)
openclaw skill gmail auth
```

For other providers:
- **Outlook:** `openclaw skill install outlook`
- **IMAP:** `openclaw skill install imap` (works with any provider)

### Step 2: Create Your Priority Rules File

Create `~/openclaw/email-rules.md`:

```markdown
# Email Priority Rules

## 🔴 URGENT (notify immediately)
- From: [boss@company.com, ceo@company.com, wife@family.com]
- Subject contains: "urgent", "asap", "emergency", "deadline today"
- Clients: *@bigclient.com, *@importantcustomer.io

##

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
mkdir email-auto-classifier && cd email-auto-classifier
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
email-auto-classifier/
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
  // TODO: Implement data collection for Email Auto Classifier
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
  logger.info('=== 郵件自動分類器 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 郵件自動分類器 報告\n\n${result}`);
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
pm2 start src/index.js --name email-auto-classifier  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
