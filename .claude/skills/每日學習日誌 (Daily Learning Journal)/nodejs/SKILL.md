---
name: 每日學習日誌 (Daily Learning Journal)/nodejs
description: "Use Case #028 Node.js 方案: 每日學習日誌。使用 Node.js 實作 Daily Learning Journal 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #028: 每日學習日誌 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 每日学习日志

## 简介

持续学习需要记录和反思。这个使用案例自动追踪你的学习活动，生成每日学习摘要，并定期回顾帮助你巩固知识。

**为什么重要**：增强学习效果，建立个人知识库。

**真实例子**：一位软件开发者使用此代理记录每天学习的新技术，三个月后他拥有了一个可搜索的个人知识库，大大提高了问题解决效率。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `filesystem` | 内置 | 存储学习日志 |
| `browser` | [ClawdHub](https://clawhub.com/skills/browser) | 追踪浏览历史 |
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 管理笔记 |
| `search` | [ClawdHub](https://clawhub.com/skills/search) | 检索知识 |

---

## 设置步骤

### 1. 前置条件

- 笔记应用（Notion、Obsidian）
- 浏览器历史访问权限（可选）

### 2. 提示词模板

```markdown
## 每日学习日志

你是我的学习助手。每天执行以下任务：

### 学习追踪
1. 扫描我的笔记和文档
2. 分析浏览器历史（学习相关网站）
3. 识别今天学习的新概念
4. 记录学习时间和主题

### 日志格式
```
# 学习日志 - YYYY-MM-DD

## 今日学习主题
- 主题 1
- 主题 2

## 关键收获
1. 要点 1
2. 要点 2

## 待深入问题
- 问题 1
- 问题 2

## 相关资源
- 链接 1
- 链接 2

## 明日计划
- 继续学习...
```

### 每周回顾
- 总结本周学习主题
- 识别知识模式
- 生成复习提醒
- 更新知识图谱

### 每月报告
- 学习时长统计
- 主题分布分析
- 知识增长可视化
```

### 3. 配置

```
Schedule: 0 21 * * *
Action: 收集学习数据 → 生成日志 → 存储
```

---

## 成功指标

- [ ] 每天记录学习内容
- [ ] 建立可搜索的知识库
- [ ] 定期回顾巩固知识
- [ ] 学习效率提升

---

## 变体与扩展

### 变体 1：学习路径规划
根据目标制定学习计划和路径。

### 变体 2：知识关联分析
分析不同知识领域之间的关联。

---

## 故障排除

### 问题：学习数据收集不全
**解决方案**：检查浏览器历史权限和笔记应用集成。

### 问题：日志过于冗长
**解决方案**：设置关键词过滤，只记录重要内容。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 语音笔记转日记

## 简介

将语音笔记转换为每日日记条目。无论是在通勤途中、会议后还是睡前，只需录制语音，代理会自动转录并整理成日记。

**为什么重要**：快速记录想法，无需打字，建立日记习惯。

**真实例子**：一位忙碌的高管使用此代理记录每日反思，代理自动转录并整理成结构化日记，帮助他保持自我反思的习惯。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `voice_recognition` | [ClawdHub](https://clawhub.com/skills/voice) | 语音识别 |
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 笔记管理 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容整理 |

---

## 使用方式

### 录制语音
发送语音消息给代理

### 自动转录
代理转录音频为文本

### 整理日记
代理将内容整理为结构化日记条目

---

## 来源

- 来源：Hostinger


---

# 📔 Daily Journaling System

> Reflection made effortless. Capture today, understand tomorrow.

---

## The Problem

Journaling is valuable but hard to maintain. Staring at a blank page is intimidating. You forget by evening what happened in the morning. And past journals are rarely reviewed, making the practice feel pointless.

---

## The Solution

OpenClaw prompts you with specific questions, captures quick responses throughout the day, and synthesizes patterns over time. Low friction, high insight.

---

## Setup Guide

### Step 1: Install Journaling Skills

```bash
openclaw skill install obsidian-conversation-backup  # or notion, reflect
openclaw skill install todoist
```

### Step 2: Create Journal Templates

Create `~/openclaw/journal/templates.md`:

```markdown
# Morning Questions (5 min)
- What's my ONE priority today?
- What am I grateful for?
- What would make today great?

# Evening Questions (5 min)
- What went well today?
- What did I learn?
- What would I do differently?

# Weekly Review (Sunday)
- Wins this week
- Challenges faced
- Focus for next week
- Pattern I noticed

# Monthly Themes
- What defined this month?
- Progress on goals
- Relationships status
- 

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
mkdir daily-learning-journal && cd daily-learning-journal
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
daily-learning-journal/
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
  // TODO: Implement data collection for Daily Learning Journal
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
  logger.info('=== 每日學習日誌 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 每日學習日誌 報告\n\n${result}`);
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
pm2 start src/index.js --name daily-learning-journal  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
