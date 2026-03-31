---
name: 耐心作業輔導老師 (Patient Homework Tutor)/nodejs
description: "Use Case #027 Node.js 方案: 耐心作業輔導老師。使用 Node.js 實作 Patient Homework Tutor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #027: 耐心作業輔導老師 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 家庭作业辅导师

## 简介

帮助孩子完成作业可能耗时且具有挑战性。这个使用案例作为智能辅导助手，帮助孩子理解概念、解答问题、检查答案，并培养独立学习能力。

**为什么重要**：提供即时帮助，培养学习兴趣，减轻家长负担。

**真实例子**：一位家长使用此代理辅导孩子数学作业，代理不仅提供答案，还解释解题思路，孩子的数学成绩在一个月内提高了 20%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `education` | [ClawdHub](https://clawhub.com/skills/education) | 教育内容 |
| `math` | [ClawdHub](https://clawhub.com/skills/math) | 数学解题 |
| `writing` | [ClawdHub](https://clawhub.com/skills/writing) | 写作辅助 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 交互界面 |

---

## 设置步骤

### 1. 前置条件

- 学生年级和科目信息
- 学习目标和难点
- 家长监督设置

### 2. 提示词模板

```markdown
## 家庭作业辅导师

你是耐心的学习助手。帮助学生理解和完成作业：

### 辅导原则

**引导而非直接给答案**
- 提问引导思考
- 解释概念和原理
- 提供类似例题
- 鼓励独立解决

**适应学习水平**
- 根据年级调整语言
- 使用适龄的例子
- 调整难度梯度
- 尊重学习节奏

**培养学习技能**
- 教授解题策略
- 强调检查习惯
- 鼓励提问
- 庆祝进步

### 支持科目

**数学**
- 逐步解题
- 可视化解释
- 公式推导
- 练习题目

**语文**
- 阅读理解
- 写作指导
- 语法检查
- 词汇扩展

**英语**
- 翻译辅助
- 语法解释
- 写作建议
- 发音指导

**科学**
- 概念解释
- 实验指导
- 问题分析
- 知识拓展

### 互动示例

**学生**：这道题我不会做
**AI**：好的，让我们一起来看看。首先，你能告诉我题目要求什么吗？

**学生**：要求求面积
**AI**：很好！那我们需要知道什么来求面积呢？

**学生**：长和宽？
**AI**：对！那题目中给了哪些信息？...

### 进度追踪
- 记录完成的作业
- 识别薄弱环节
- 生成学习报告
- 建议练习题目
```

### 3. 配置

```
Trigger: 学生提问
Action: 分析问题 → 提供指导 → 检查答案 → 记录进度
```

---

## 成功指标

- [ ] 作业完成率 > 95%
- [ ] 理解度提升
- [ ] 学习兴趣增加
- [ ] 独立解决问题能力提高

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
mkdir patient-homework-tutor && cd patient-homework-tutor
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
patient-homework-tutor/
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
  // TODO: Implement data collection for Patient Homework Tutor
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
  logger.info('=== 耐心作業輔導老師 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 耐心作業輔導老師 報告\n\n${result}`);
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
pm2 start src/index.js --name patient-homework-tutor  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
