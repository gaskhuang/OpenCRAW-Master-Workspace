---
name: 目標驅動自主任務 (Goal-Driven Autonomous Tasks)/nodejs
description: "Use Case #010 Node.js 方案: 目標驅動自主任務。使用 Node.js 實作 Goal-Driven Autonomous Tasks 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #010: 目標驅動自主任務 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# 每日目标任务生成器

## 简介

将长期目标转化为每日可执行任务。代理根据你的目标自动生成每日任务列表，并帮助你追踪完成进度。

**为什么重要**：将大目标分解为小步骤，确保持续进展，避免目标遗忘。

**真实例子**：一位创业者使用此代理管理多个项目目标，代理每天早上生成 3-5 个推进目标的行动项，项目完成率提高了 60%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `task_manager` | [ClawdHub](https://clawhub.com/skills/tasks) | 任务管理 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 日程安排 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送任务 |

---

## 使用方式

### 设置目标
告诉代理你的长期目标（如"学习 Python"、"建立个人品牌"）

### 每日任务
每天早上代理生成推进目标的行动项

### 进度追踪
代理追踪任务完成情况，调整后续任务

---

## 来源

- 作者：Alex Finn
- 平台：YouTube


---

# Autonomous Project Management with Subagents

Managing complex projects with multiple parallel workstreams is exhausting. You end up context-switching constantly, tracking status across tools, and manually coordinating handoffs.

This use case implements a decentralized project management pattern where subagents work autonomously on tasks, coordinating through shared state files rather than a central orchestrator.

## Pain Point

Traditional orchestrator patterns create bottlenecks—the main agent becomes a traffic cop. For complex projects (multi-repo refactors, research sprints, content pipelines), you need agents that can work in parallel without constant supervision.

## What It Does

- **Decentralized coordination**: Agents read/write to a shared `STATE.yaml` file
- **Parallel execution**: Multiple subagents work on independent tasks simultaneously
- **No orchestrator overhead**: Main session stays thin (CEO pattern—strategy only)
- **Self-documenting**: All task state persists in version-controlled files

## Core Pattern: STATE.yaml

Each project maintains a `STATE.yaml` file that serves as the single source of truth:

```yaml
# STATE.yaml - Project coordination file
project: website-redesign
updated: 2026-02-10T14:30:00Z

tasks:
  - id: homepage-hero
    status: in_progress
    owner: pm-frontend
    started: 2026-02-10T12:00:00Z
    notes: "Working on responsive layout"
    
  - id: api-auth
    status: done
    owner: pm-backend
    completed: 2026-02-10T14:00:00Z
    output: "src/api/auth.ts"
    
  - id: content-migration
    status: blocked
    owner: pm-content
    blocked_by: api-auth
    notes: "Waiting for new endpoint schema"

next_actions:
  - "pm-content: Resume migration now that api-auth is done"
  - "pm-frontend: Review hero with design team"
```

## How It Works

1. **Main agent receives task** → spawns subagent with specific scope
2. **Subagent reads STATE.yaml** → finds its assigned tasks
3. **Subagent works autonomously** → updates STATE.yaml on progress
4. **Other agents poll STATE.yaml** → pick up unblocked work
5. **Main agent checks in periodically** → reviews state, adjusts priorities

## Skills You Need

- `sessions_spawn` / `sessions_send` for subagent management
- File system access for STATE.yaml
- Git for state versioning (optional but recommended)

## Setup: AGENTS.md Configuration

```text
## PM Delegation Pattern

M

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
mkdir goal-driven-autonomous-tasks && cd goal-driven-autonomous-tasks
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
goal-driven-autonomous-tasks/
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
  // TODO: Implement data collection for Goal-Driven Autonomous Tasks
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
  logger.info('=== 目標驅動自主任務 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 目標驅動自主任務 報告\n\n${result}`);
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
pm2 start src/index.js --name goal-driven-autonomous-tasks  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
