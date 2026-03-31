---
name: PDF 文件處理中心 (PDF Document Processing Hub)/nodejs
description: "Use Case #048 Node.js 方案: PDF 文件處理中心。使用 Node.js 實作 PDF Document Processing Hub 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #048: PDF 文件處理中心 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# PDF 转摘要转换器

## 简介

阅读长篇 PDF 文档耗时。这个使用案例自动提取 PDF 内容，生成结构化摘要，提取关键信息，并回答关于文档的问题。

**为什么重要**：快速理解文档内容，节省阅读时间，提取关键信息。

**真实例子**：一位律师使用此代理处理案件材料，代理快速生成每份文件的摘要，使案件准备时间减少了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `pdf` | [ClawdHub](https://clawhub.com/skills/pdf) | 读取 PDF |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 文本分析 |
| `summarization` | [ClawdHub](https://clawhub.com/skills/summary) | 生成摘要 |

---

## 设置步骤

### 1. 前置条件

- PDF 文件访问
- 摘要长度偏好
- 输出格式

### 2. 提示词模板

```markdown
## PDF 转摘要转换器

你是我的文档助手。将 PDF 转换为结构化摘要：

### 处理流程

**1. 文档解析**
- 提取文本内容
- 识别文档结构
- 提取图表数据
- 识别关键章节

**2. 内容分析**
- 识别主题
- 提取关键论点
- 识别重要数据
- 提取结论

**3. 摘要生成**
- 执行摘要（1-2 段）
- 详细摘要（每章）
- 关键要点列表
- 重要引用

### 输出格式

```
📄 文档摘要

📋 基本信息
- 标题：[标题]
- 作者：[作者]
- 页数：XX 页
- 日期：YYYY-MM-DD

📝 执行摘要
[2-3 段摘要]

🎯 关键要点
1. [要点 1]
2. [要点 2]
3. [要点 3]

📊 重要数据
- [数据点 1]
- [数据点 2]

📑 章节摘要
**第一章：[标题]**
[摘要内容]

**第二章：[标题]**
[摘要内容]

❓ 问答
Q: [问题]
A: [答案]
```

### 批量处理
- 处理多个 PDF
- 生成比较报告
- 提取共同主题
- 识别矛盾点
```

### 3. 配置

```
Trigger: PDF 上传
Action: 解析 → 分析 → 生成摘要 → 输出
```

---

## 成功指标

- [ ] 摘要准确反映原文
- [ ] 处理速度快
- [ ] 关键信息完整
- [ ] 用户满意度高

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📄 Document Processor

> PDFs, contracts, reports—instantly searchable and summarized.

---

## The Problem

Documents pile up: contracts, reports, receipts, research papers. Finding information means opening dozens of files. Important details get lost. Nobody reads 50-page reports cover to cover.

---

## The Solution

OpenClaw extracts text from any document, summarizes key points, makes everything searchable, and answers questions about your documents instantly.

---

## Setup Guide

### Step 1: Install Document Skills

```bash
openclaw skill install mineru-pdf
openclaw skill install pymupdf-pdf
openclaw skill install llmwhisperer
openclaw skill install excel
```

### Step 2: Set Up Document Folders

Create `~/openclaw/documents/config.json`:

```json
{
  "watchFolders": [
    "~/Documents/Contracts/",
    "~/Documents/Reports/",
    "~/Downloads/*.pdf"
  ],
  "outputDir": "~/openclaw/documents/processed/",
  "autoProcess": true
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `mineru-pdf` | Advanced PDF extraction |
| `pymupdf-pdf` | Fast PDF processing |
| `llmwhisperer` | Handwriting/complex docs |
| `excel` | Spreadsheet processing |

---

## Example Prompts

**Process document:**
```
Process this contract [file]. Extract key terms, dates, and obligations.
```

**Search documents:**
```
Find all documents that mention [term] from the past year.
```

**Summarize report:**
```
Summarize this 40-page report. What are the key findings and recommendations?
```

**Compare documents:**
```
Compare these two contract versions. What changed?
```

---

## Cron Schedule

```
*/30 * * * *   # Every 30 min - process new documents
0 9 * * 1      # Monday 9 AM - document digest
```

---

## Expected Results

- All documents searchable
- 90% faster information retrieval
- N

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
mkdir pdf-document-processing-hub && cd pdf-document-processing-hub
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
pdf-document-processing-hub/
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
  // TODO: Implement data collection for PDF Document Processing Hub
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
  logger.info('=== PDF 文件處理中心 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 PDF 文件處理中心 報告\n\n${result}`);
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
pm2 start src/index.js --name pdf-document-processing-hub  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
