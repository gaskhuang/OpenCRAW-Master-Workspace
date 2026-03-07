---
name: 閱讀清單智慧管理 (Smart Reading List Manager)/nodejs
description: "Use Case #025 Node.js 方案: 閱讀清單智慧管理。使用 Node.js 實作 Smart Reading List Manager 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #025: 閱讀清單智慧管理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 阅读列表策展人

## 简介

收藏了太多文章却没时间读？这个使用案例智能管理你的阅读列表，根据你的兴趣优先级排序，生成摘要，并推荐最佳阅读时间。

**为什么重要**：高效管理阅读清单，确保不错过重要内容。

**真实例子**：一位研究员使用此代理管理数百篇学术论文，代理根据研究项目优先级排序，并生成摘要帮助他快速筛选重要论文。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `bookmark` | [ClawdHub](https://clawhub.com/skills/bookmark) | 管理书签 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `readability` | [ClawdHub](https://clawhub.com/skills/readability) | 提取正文 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送推荐 |

---

## 设置步骤

### 1. 前置条件

- 书签服务（Pocket、Instapaper）
- 兴趣主题列表

### 2. 提示词模板

```markdown
## 阅读列表策展人

你是我的阅读助理。管理我的阅读列表：

### 功能

**1. 内容分析**
- 分析每篇文章的主题
- 评估阅读时间
- 提取关键摘要
- 判断内容质量

**2. 智能排序**
- 根据当前项目优先级排序
- 考虑时效性
- 平衡深度和轻松内容
- 避免同类内容重复

**3. 阅读建议**
- 早上：新闻和轻量内容
- 下午：专业文章
- 晚上：长文和深度阅读

**4. 每周精选**
- 推荐本周必读 Top 5
- 生成摘要卡片
- 提供阅读路径建议

### 输出格式
```
📚 本周阅读推荐

🔥 优先阅读
1. [标题] - [来源] ([阅读时间])
   [一句话摘要]
   推荐理由：[原因]

📰 今日轻读
1. [标题] - [来源]
   [一句话摘要]

📖 周末深度
1. [标题] - [来源] ([阅读时间])
   [详细摘要]

📊 阅读统计
- 本周已读：X 篇
- 平均阅读时间：Y 分钟
- 收藏待读：Z 篇
```

### 学习偏好
- 记录我读完的文章
- 分析我喜欢的内容类型
- 调整推荐算法
```

### 3. 配置

```
Schedule: 0 9 * * 1
Action: 分析列表 → 生成推荐 → 发送
```

---

## 成功指标

- [ ] 阅读列表保持可控
- [ ] 优先内容不被遗漏
- [ ] 阅读效率提升
- [ ] 发现高质量内容

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
mkdir smart-reading-list-manager && cd smart-reading-list-manager
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
smart-reading-list-manager/
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
  // TODO: Implement data collection for Smart Reading List Manager
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
  logger.info('=== 閱讀清單智慧管理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 閱讀清單智慧管理 報告\n\n${result}`);
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
pm2 start src/index.js --name smart-reading-list-manager  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
