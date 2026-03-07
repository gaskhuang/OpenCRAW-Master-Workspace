---
name: AI 模型費用追蹤中心 (AI Model Cost Tracker)/nodejs
description: "Use Case #089 Node.js 方案: AI 模型費用追蹤中心。使用 Node.js 實作 AI Model Cost Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #089: AI 模型費用追蹤中心 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 監控與維運

---

## 原始需求 (來自 Source Repos)

# AI 成本追踪

## 简介

追踪 OpenClaw 和 AI 服务的使用成本，生成成本报告，帮助优化支出。

**为什么重要**：了解 AI 使用成本，优化模型选择，控制预算。

**真实例子**：一个团队使用此代理追踪 AI 成本，发现可以切换到更便宜的模型而不影响质量，每月节省 40% 成本。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `logging` | [ClawdHub](https://clawhub.com/skills/logging) | 使用记录 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 成本分析 |
| `dashboard` | [ClawdHub](https://clawhub.com/skills/dashboard) | 成本仪表板 |

---

## 使用方式

### 记录使用
追踪每次 API 调用

### 计算成本
根据模型和价格计算成本

### 生成报告
- 每日成本
- 模型使用分布
- 优化建议

---

## 来源

- 来源：Stack Junkie


---

# Token 使用优化器

## 简介

优化 LLM Token 使用效率，降低成本，提高响应质量。

**为什么重要**：控制 AI 成本，提高效率，优化模型选择。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `llm` | [ClawdHub](https://clawhub.com/skills/llm) | LLM 管理 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 使用分析 |

---

## 使用方式

分析使用模式，获取优化建议

---

## 来源

- 作者：OpenClaw 社区


---

# 💸 AI Cost Tracker

> Know exactly what you're spending on AI. No surprises, just optimization.

---

## The Problem

AI API costs add up fast and unpredictably. You're using Claude, GPT-4, Gemini across different tools and projects. The bill arrives and you have no idea what drove the spike or how to optimize.

---

## The Solution

OpenClaw tracks your AI usage across all providers, alerts on unusual spending, identifies cost optimization opportunities, and helps you choose the right model for each task.

---

## Setup Guide

### Step 1: Install Tracking Skills

```bash
openclaw skill install claude-code-usage
openclaw skill install codex-quota
openclaw skill install minimax-usage
```

### Step 2: Configure Providers

Create `~/openclaw/ai-costs/providers.json`:

```json
{
  "providers": [
    {
      "name": "Anthropic",
      "budgetMonthly": 100,
      "alertThreshold": 80
    },
    {
      "name": "OpenAI",
      "budgetMonthly": 50,
      "alertThreshold": 80
    },
    {
      "name": "Google",
      "budgetMonthly": 30,
      "alertThreshold": 80
    }
  ],
  "totalBudget": 200
}
```

### Step 3: Set Up Cost Rules

Create `~/openclaw/ai-costs/rules.md`:

```markdown
# AI Cost Optimization Rules

## Model Selection
- Simple tasks: Use cheapest model (GPT-3.5, Claude Instant)
- Complex reasoning: Use best model
- Bulk processing: Batch API when available

## Alerts
- Daily spend > $10: Warning
- Weekly spend > $40: Alert
- Approaching 80% of budget: Alert

## Review Weekly
- Highest cost tasks
- Potential model downgrades
- Unused subscriptions
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `claude-code-usage` | Claude/Anthropic usage |
| `codex-quota` | OpenAI Codex usage |
| `minimax-usage` | MiniMax usage |

---

## Example Prompts

**Daily check:**
```
What's my AI spend today across all providers? Any unusual spikes?
```

**Optimization analysis:**
```
Analyze my AI usage this week. Where am I overspending? Which tasks could use cheaper models?
```

**Budget planning:**
```
Based on my usage patterns, what should my monthly A

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
mkdir ai-model-cost-tracker && cd ai-model-cost-tracker
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
ai-model-cost-tracker/
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
  // TODO: Implement data collection for AI Model Cost Tracker
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
  logger.info('=== AI 模型費用追蹤中心 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 AI 模型費用追蹤中心 報告\n\n${result}`);
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
pm2 start src/index.js --name ai-model-cost-tracker  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
