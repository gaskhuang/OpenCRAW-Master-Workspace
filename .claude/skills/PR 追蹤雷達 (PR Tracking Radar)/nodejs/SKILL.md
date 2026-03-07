---
name: PR 追蹤雷達 (PR Tracking Radar)/nodejs
description: "Use Case #071 Node.js 方案: PR 追蹤雷達。使用 Node.js 實作 PR Tracking Radar 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #071: PR 追蹤雷達 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# GitHub 过期 Issue 清理

## 简介

自动识别和清理长期未活动的 GitHub Issue，保持仓库整洁。

**为什么重要**：减少 Issue 堆积，提高团队效率，保持项目健康。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `github` | [ClawdHub](https://clawhub.com/skills/github) | GitHub API |

---

## 使用方式

设置过期规则，代理自动标记和清理

---

## 来源

- 作者：OpenClaw 社区


---

# GitHub Issue 优先级排序器

## 简介

智能排序 GitHub Issue，根据影响、紧急程度、资源可用性确定优先级。

**为什么重要**：优化开发资源分配，确保重要问题优先解决。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `github` | [ClawdHub](https://clawhub.com/skills/github) | GitHub API |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |

---

## 使用方式

连接仓库，设置优先级规则

---

## 来源

- 作者：OpenClaw 社区


---

# 🔍 PR Review Assistant

> Never merge buggy code again. Get thorough reviews in minutes, not days.

---

## The Problem

Code reviews are bottlenecks. PRs sit for days waiting for busy teammates. When reviews do happen, they're often rushed, missing bugs that slip into production. Junior devs don't get the learning feedback they need.

---

## The Solution

OpenClaw automatically reviews every PR: checks for bugs, security issues, style violations, and suggests improvements. Human reviewers can focus on architecture and business logic while OpenClaw handles the tedious stuff.

---

## Setup Guide

### Step 1: Install Skills

```bash
openclaw skill install github
openclaw skill install github-pr
openclaw skill install conventional-commits
```

### Step 2: Configure Review Rules

Create `~/openclaw/pr-review/rules.md`:

```markdown
# PR Review Checklist

## Always Check
- [ ] No hardcoded secrets/credentials
- [ ] No console.log/print statements left in
- [ ] Error handling present
- [ ] Input validation for user data
- [ ] SQL injection prevention
- [ ] XSS prevention

## Code Quality
- [ ] Functions under 50 lines
- [ ] No deep nesting (max 3 levels)
- [ ] Meaningful variable names
- [ ] DRY - no copy-pasted blocks

## Tests
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Tests actually test something meaningful

## Documentation
- [ ] Complex logic has comments
- [ ] Public APIs have docstrings
- [ ] README updated if needed
```

### Step 3: Set Up GitHub Webhook (Optional)

For automatic reviews on new PRs, set up a webhook or use GitHub Actions.

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `github` | GitHub API access |
| `github-pr` | PR-specific operations |
| `conventional-commits` | Commit message validation |

---

## Example Prompts

**Review a PR:**
```
Review PR #123 in repo [owner/repo]. Focus on security, performance, and code quality.
```

**Batch review:**
```
Show me all open PRs in [repo] that haven't been reviewed in 2+ days. Give me a summary of each.
```

**Learn from feedback:**
```
What are the most common issues you've found in our PRs this month? Create a team guidelines doc.
```

**Pre-submit check:**
```
I'm about to submit a PR with these changes: [paste diff]. Any issues I should fix first?
```

---

## Cron Schedule

```
*/15 * * * *   # Every

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
mkdir pr-tracking-radar && cd pr-tracking-radar
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
pr-tracking-radar/
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
  // TODO: Implement data collection for PR Tracking Radar
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
  logger.info('=== PR 追蹤雷達 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 PR 追蹤雷達 報告\n\n${result}`);
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
pm2 start src/index.js --name pr-tracking-radar  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
