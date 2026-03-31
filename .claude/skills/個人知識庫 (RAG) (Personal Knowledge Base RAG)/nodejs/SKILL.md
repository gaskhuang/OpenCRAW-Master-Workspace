---
name: 個人知識庫 (RAG) (Personal Knowledge Base RAG)/nodejs
description: "Use Case #094 Node.js 方案: 個人知識庫 (RAG)。使用 Node.js 實作 Personal Knowledge Base (RAG) 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #094: 個人知識庫 (RAG) — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Personal Knowledge Base (RAG)

You read articles, tweets, and watch videos all day but can never find that one thing you saw last week. Bookmarks pile up and become useless.

This workflow builds a searchable knowledge base from everything you save:

• Drop any URL into Telegram or Slack and it auto-ingests the content (articles, tweets, YouTube transcripts, PDFs)
• Semantic search over everything you've saved: "What did I save about agent memory?" returns ranked results with sources
• Feeds into other workflows — e.g., the video idea pipeline queries the KB for relevant saved content when building research cards

## Skills you Need

- [knowledge-base](https://clawhub.ai) skill (or build custom RAG with embeddings)
- `web_fetch` (built-in)
- Telegram topic or Slack channel for ingestion

## How to Set it Up

1. Install the knowledge-base skill from ClawdHub.
2. Create a Telegram topic called "knowledge-base" (or use a Slack channel).
3. Prompt OpenClaw:
```text
When I drop a URL in the "knowledge-base" topic:
1. Fetch the content (article, tweet, YouTube transcript, PDF)
2. Ingest it into the knowledge base with metadata (title, URL, date, type)
3. Reply with confirmation: what was ingested and chunk count

When I ask a question in this topic:
1. Search the knowledge base semantically
2. Return top results with sources and relevant excerpts
3. If no good matches, tell me

Also: when other workflows need research (e.g., video ideas, meeting prep), automatically query the knowledge base for relevant saved content.
```

4. Test it by dropping a few URLs and asking questions like "What do I have about LLM memory?"


---

# 个人知识库构建器

## 简介

信息碎片化是现代人面临的挑战。这个使用案例自动收集、整理和连接你的知识，构建个人知识图谱，让信息易于检索和关联。

**为什么重要**：建立可搜索的知识库，发现知识关联，提高学习和工作效率。

**真实例子**：一位研究员使用此代理管理研究资料，代理自动分类论文、提取关键信息、建立知识关联，使他的研究效率提高了 50%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 管理笔记 |
| `search` | [ClawdHub](https://clawhub.com/skills/search) | 知识检索 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `graph` | [ClawdHub](https://clawhub.com/skills/graph) | 知识图谱 |

---

## 设置步骤

### 1. 前置条件

- 笔记应用（Notion、Obsidian）
- 知识分类体系
- 现有笔记导入

### 2. 提示词模板

```markdown
## 个人知识库构建器

你是我的知识管理助手。帮我构建个人知识库：

### 知识收集

**来源**
- 阅读笔记
- 会议记录
- 学习资料
- 想法记录
- 网页收藏

**自动处理**
- 提取关键信息
- 生成摘要
- 提取标签
- 识别实体

### 知识组织

**分类体系**
- 项目
- 主题
- 人物
- 资源
- 想法

**标签系统**
- 状态：#进行中 #已完成 #待复习
- 类型：#文章 #视频 #书籍 #课程
- 主题：#AI #商业 #健康

### 知识连接

**自动关联**
- 识别相关笔记
- 建立双向链接
- 生成知识图谱
- 发现知识缺口

**每日回顾**
```
🧠 每日知识回顾

📚 今日新增
- [笔记 1]
- [笔记 2]

🔗 相关笔记
- [笔记 1] 与 [旧笔记] 相关

💡 新发现
- 发现了 [主题] 和 [主题] 的关联

📅 待复习
- [笔记]（7 天前创建）
```

### 知识检索

**智能搜索**
- 全文搜索
- 标签过滤
- 时间范围
- 相关性排序

**问答功能**
- 基于知识库回答
- 提供相关笔记
- 引用来源
```

### 3. 配置

```
Schedule: 0 21 * * *
Action: 收集知识 → 整理 → 建立连接 → 生成回顾
```

---

## 成功指标

- [ ] 知识库可搜索
- [ ] 知识关联清晰
- [ ] 信息检索快速
- [ ] 知识复用率提高

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
mkdir personal-knowledge-base-(rag) && cd personal-knowledge-base-(rag)
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
personal-knowledge-base-(rag)/
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
  // TODO: Implement data collection for Personal Knowledge Base (RAG)
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
  logger.info('=== 個人知識庫 (RAG) ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 個人知識庫 (RAG) 報告\n\n${result}`);
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
pm2 start src/index.js --name personal-knowledge-base-(rag)  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
