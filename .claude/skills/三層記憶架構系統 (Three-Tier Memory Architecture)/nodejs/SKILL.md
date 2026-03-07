---
name: 三層記憶架構系統 (Three-Tier Memory Architecture)/nodejs
description: "Use Case #114 Node.js 方案: 三層記憶架構系統。使用 Node.js 實作 Three-Tier Memory Architecture 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #114: 三層記憶架構系統 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: AI 記憶與代理架構

---

## 原始需求 (來自 Source Repos)

# 三层记忆系统

## 简介

代理需要有效的记忆管理来保持上下文。这个使用案例实现三层记忆系统：长期核心原则、每日事件日志和项目特定追踪，平衡速度和持久性。

**为什么重要**：确保重要信息持久化，避免 Token 膨胀，保持上下文连贯。

**真实例子**：一位开发者使用此系统管理代理记忆，代理能够记住项目目标、每日决策和当前状态，工作效率提高了 3 倍。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `filesystem` | 内置 | 文件读写 |
| `memory_search` | [ClawdHub](https://clawhub.com/skills/memory) | 语义搜索 |

---

## 设置步骤

### 1. 目录结构

```
workspace/
├── MEMORY.md              # 长期：原则、锚点、目标
├── PROJECTS.md            # 项目：状态、阻塞、下一步
└── memory/
    ├── 2026-02-19.md      # 每日：事件、决策、上下文
    ├── 2026-02-18.md
    └── heartbeat-state.json
```

### 2. 提示词模板

```markdown
## 三层记忆系统

### MEMORY.md - 长期记忆

```markdown
# 长期记忆

## 核心原则
- 效率优于冗长
- 主动 > 被动
- 用理由记录决策

## 关键锚点
- 用户：[姓名]
- 风格：直接，无废话
- 偏好：具体例子 > 一般陈述

## 目标
- [ ] 构建 50 个 OpenClaw 案例
- [ ] 发布 GitHub 仓库
```

### 每日记忆

```markdown
# 记忆 - YYYY-MM-DD

## 今日事件
- [时间]：[事件描述]
- [时间]：[事件描述]

## 决策
- [决策]：[理由]

## 上下文
- 当前项目：[项目名]
- 阻塞项：[描述]
- 下一步：[描述]
```

### PROJECTS.md

```markdown
# 项目追踪

## 活跃项目

### [项目名]
**状态**：进行中
**进度**：70%
**阻塞**：[阻塞项]
**下一步**：[行动项]
```

### 记忆管理

**写入规则**
- 核心原则 → MEMORY.md
- 每日事件 → memory/YYYY-MM-DD.md
- 项目状态 → PROJECTS.md

**读取规则**
- 启动时读取 MEMORY.md
- 读取最近 7 天每日记忆
- 读取活跃项目状态

**归档规则**
- 30 天前的每日记忆归档
- 已完成项目移动到归档
```

### 3. 配置

```
Trigger: 代理启动 / 每日结束
Action: 读取记忆 → 更新记忆 → 存储
```

---

## 成功指标

- [ ] 重要信息持久化
- [ ] 上下文保持连贯
- [ ] Token 使用优化
- [ ] 代理响应准确

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
mkdir three-tier-memory-architecture && cd three-tier-memory-architecture
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
three-tier-memory-architecture/
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
  // TODO: Implement data collection for Three-Tier Memory Architecture
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
  logger.info('=== 三層記憶架構系統 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 三層記憶架構系統 報告\n\n${result}`);
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
pm2 start src/index.js --name three-tier-memory-architecture  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
