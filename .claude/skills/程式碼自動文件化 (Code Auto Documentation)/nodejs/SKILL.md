---
name: 程式碼自動文件化 (Code Auto Documentation)/nodejs
description: "Use Case #078 Node.js 方案: 程式碼自動文件化。使用 Node.js 實作 Code Auto Documentation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #078: 程式碼自動文件化 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 代码转文档生成器

## 简介

维护代码文档是一项繁琐但重要的工作。这个使用案例自动分析代码，生成 API 文档、README 和代码注释，保持文档与代码同步。

**为什么重要**：提高代码可维护性，帮助团队协作，减少文档维护负担。

**真实例子**：一个开发团队使用此代理自动生成 API 文档，文档始终与代码同步，新成员上手时间减少了 50%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `code_parser` | [ClawdHub](https://clawhub.com/skills/code) | 解析代码 |
| `documentation` | [ClawdHub](https://clawhub.com/skills/docs) | 生成文档 |
| `git` | [ClawdHub](https://clawhub.com/skills/git) | 版本控制 |

---

## 设置步骤

### 1. 前置条件

- 代码仓库访问
- 文档模板
- 输出格式

### 2. 提示词模板

```markdown
## 代码转文档生成器

你是我的技术文档助手。从代码生成文档：

### 分析内容

**代码结构**
- 类和函数
- 参数和返回值
- 类型注解
- 异常处理

**代码注释**
- Docstring
- 行内注释
- TODO 标记
- 弃用标记

**依赖关系**
- 导入的模块
- 函数调用链
- 类继承关系

### 生成文档

**API 文档**
```markdown
## Function Name

**描述**
函数功能描述

**参数**
| 参数 | 类型 | 描述 |
|------|------|------|
| param1 | str | 描述 |

**返回值**
| 类型 | 描述 |
|------|------|
| bool | 描述 |

**示例**
```python
result = function_name("input")
```

**异常**
- ValueError: 参数无效
```

**README**
- 项目介绍
- 安装指南
- 使用示例
- API 概览
- 贡献指南

### 自动化
- 代码提交时更新
- 检查文档完整性
- 标记缺失文档
- 生成变更日志
```

### 3. 配置

```
Trigger: Git 提交
Action: 分析代码 → 生成文档 → 提交更新
```

---

## 成功指标

- [ ] 文档覆盖率 > 90%
- [ ] 文档与代码同步
- [ ] 新成员上手快
- [ ] 维护负担减轻

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# API 文档生成器

## 简介

从代码自动生成 API 文档，保持文档与代码同步。

**为什么重要**：减少文档维护工作，确保文档准确，提高开发效率。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `code_analysis` | [ClawdHub](https://clawhub.com/skills/code) | 代码分析 |
| `docs` | [ClawdHub](https://clawhub.com/skills/docs) | 文档生成 |

---

## 使用方式

连接代码库，自动生成文档

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
mkdir code-auto-documentation && cd code-auto-documentation
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
code-auto-documentation/
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
  // TODO: Implement data collection for Code Auto Documentation
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
  logger.info('=== 程式碼自動文件化 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 程式碼自動文件化 報告\n\n${result}`);
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
pm2 start src/index.js --name code-auto-documentation  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
