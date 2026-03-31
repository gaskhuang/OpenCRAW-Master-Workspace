---
name: Instagram 限時動態管理 (Instagram Stories Management)/nodejs
description: "Use Case #007 Node.js 方案: Instagram 限時動態管理。使用 Node.js 實作 Instagram Stories Management 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #007: Instagram 限時動態管理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# Instagram 故事管理器

## 简介

社交媒体管理耗时且需要持续的关注。这个使用案例自动创建、安排和发布 Instagram 故事，基于你的内容日历和当前趋势。

**为什么重要**：保持一致的社交媒体存在，无需手动操作。

**真实例子**：一位小型企业主使用此代理每天自动发布 3-5 个故事，展示产品、分享客户评价和幕后内容，粉丝互动率提高了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `instagram` | [ClawdHub](https://clawhub.com/skills/instagram) | 发布故事 |
| `image_generation` | [ClawdHub](https://clawhub.com/skills/image) | 生成图片 |
| `content_calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 管理内容日历 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 分析表现 |

---

## 设置步骤

### 1. 前置条件

- Instagram 商业账号
- Instagram Graph API 访问权限
- 内容日历（Google Sheets 或 Notion）
- 品牌素材库

### 2. 提示词模板

```markdown
## Instagram 故事管理器

你是我的社交媒体经理。每天执行以下任务：

### 内容规划
1. 检查内容日历获取今天的故事主题
2. 分析过去 7 天的表现数据
3. 确定最佳发布时间

### 故事创建
1.  morning (9 AM): 早安/励志引用
2.  noon (12 PM): 产品展示或幕后内容
3.  afternoon (3 PM): 互动投票或问答
4.  evening (6 PM): 用户生成内容或评价

### 设计指南
- 使用品牌颜色（主色、辅色）
- 保持字体一致
- 添加品牌标识
- 使用相关标签

### 发布策略
- 高峰时段：12 PM, 3 PM, 6 PM
- 周末减少频率
- 特殊日期调整内容

### 互动监控
- 回复故事回复（24 小时内）
- 记录高互动内容类型
- 每周生成表现报告
```

### 3. 配置

```
Schedule: 0 9,12,15,18 * * *
Action: 生成内容 → 创建图片 → 发布 → 监控
```

---

## 成功指标

- [ ] 每天发布 3-5 个故事
- [ ] 故事观看率稳定增长
- [ ] 互动率（投票、问答）提高
- [ ] 粉丝增长

---

## 变体与扩展

### 变体 1：活动推广模式
针对特定活动（产品发布、促销）集中推广。

### 变体 2：用户生成内容
自动收集和转发粉丝内容。

---

## 故障排除

### 问题：图片生成失败
**解决方案**：检查图片生成 API 配额和提示词质量。

### 问题：发布时间不准确
**解决方案**：检查时区设置和定时任务配置。

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
mkdir instagram-stories-management && cd instagram-stories-management
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
instagram-stories-management/
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
  // TODO: Implement data collection for Instagram Stories Management
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
  logger.info('=== Instagram 限時動態管理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 Instagram 限時動態管理 報告\n\n${result}`);
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
pm2 start src/index.js --name instagram-stories-management  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
