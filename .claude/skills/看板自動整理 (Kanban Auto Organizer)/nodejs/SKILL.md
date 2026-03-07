---
name: 看板自動整理 (Kanban Auto Organizer)/nodejs
description: "Use Case #051 Node.js 方案: 看板自動整理。使用 Node.js 實作 Kanban Auto Organizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #051: 看板自動整理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# Trello/Notion 整理助手

## 简介

项目管理看板变得混乱？这个使用案例自动整理你的 Trello 或 Notion 看板，归档已完成任务，更新状态，生成进度报告，并提醒即将到期的任务。

**为什么重要**：保持项目井井有条，确保任务按时完成，提高团队效率。

**真实例子**：一个 10 人团队使用此代理管理产品开发，代理每天整理看板、更新状态、提醒截止日期，使项目按时交付率提高了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `trello` | [ClawdHub](https://clawhub.com/skills/trello) | 管理 Trello |
| `notion` | [ClawdHub](https://clawhub.com/skills/notion) | 管理 Notion |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 检查日期 |

---

## 设置步骤

### 1. 前置条件

- Trello/Notion 账号
- API 密钥
- 看板访问权限

### 2. 提示词模板

```markdown
## Trello/Notion 整理助手

你是我的项目管理助手。每天整理和更新看板：

### 每日整理任务

**1. 归档已完成**
- 识别已完成超过 7 天的卡片
- 归档到"已完成"列表
- 记录完成时间

**2. 更新状态**
- 检查进行中的任务
- 更新进度百分比
- 标记阻塞的任务

**3. 提醒即将到期**
- 识别 3 天内到期的任务
- 发送提醒通知
- 标记高优先级

**4. 整理标签**
- 统一标签格式
- 清理未使用的标签
- 更新颜色编码

### 每周报告

**进度摘要**
```
📊 项目周报 - YYYY-MM-DD

✅ 本周完成
- 任务 1
- 任务 2

🔄 进行中
- 任务 3 (70%)
- 任务 4 (30%)

⚠️ 风险
- 任务 5 (逾期 2 天)

📅 下周计划
- 任务 6 (截止周三)
- 任务 7 (截止周五)
```

**团队统计**
- 每人完成任务数
- 平均完成时间
- 阻塞问题统计

### 自动化规则

**状态自动更新**
- 所有子任务完成 → 父任务自动完成
- 逾期任务 → 自动标记红色
- 阻塞任务 → 通知负责人

**模板应用**
- 新任务自动添加检查清单
- 根据类型应用标签
- 设置默认截止日期
```

### 3. 配置

```
Schedule: 0 9 * * *
Action: 扫描看板 → 整理 → 更新 → 发送报告
```

---

## 成功指标

- [ ] 看板保持整洁
- [ ] 任务按时完成率 > 90%
- [ ] 团队效率提升
- [ ] 零遗漏重要任务

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# Trello 看板整理器

## 简介

智能整理 Trello 看板，归档旧卡片，更新状态，优化布局。

**为什么重要**：保持看板整洁，提高工作效率，优化项目管理。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `trello` | [ClawdHub](https://clawhub.com/skills/trello) | Trello API |

---

## 使用方式

连接看板，设置整理规则

---

## 来源

- 作者：OpenClaw 社区


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
mkdir kanban-auto-organizer && cd kanban-auto-organizer
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
kanban-auto-organizer/
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
  // TODO: Implement data collection for Kanban Auto Organizer
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
  logger.info('=== 看板自動整理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 看板自動整理 報告\n\n${result}`);
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
pm2 start src/index.js --name kanban-auto-organizer  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
