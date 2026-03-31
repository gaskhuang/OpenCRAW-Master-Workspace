---
name: 自動排程社群發文 (Auto-Schedule Social Posts)/nodejs
description: "Use Case #006 Node.js 方案: 自動排程社群發文。使用 Node.js 實作 Auto-Schedule Social Posts 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #006: 自動排程社群發文 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# 自动社交发布

## 简介

保持社交媒体活跃需要持续发布内容。这个使用案例自动安排和发布社交媒体内容，基于你的内容日历和最佳发布时间，保持一致的在线存在。

**为什么重要**：节省时间，保持一致的社交媒体存在，优化发布时间。

**真实例子**：一位内容创作者使用此代理管理多个社交平台，代理根据每个平台的最佳时间自动发布，粉丝互动率提高了 60%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `twitter` | [ClawdHub](https://clawhub.com/skills/twitter) | 发布推文 |
| `linkedin` | [ClawdHub](https://clawhub.com/skills/linkedin) | 发布 LinkedIn |
| `instagram` | [ClawdHub](https://clawhub.com/skills/instagram) | 发布 Instagram |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 分析表现 |

---

## 设置步骤

### 1. 前置条件

- 社交媒体账号
- API 访问权限
- 内容日历

### 2. 提示词模板

```markdown
## 自动社交发布

你是我的社交媒体经理。自动发布和管理内容：

### 发布策略

**内容类型**
- 教育内容：分享知识和技巧
- 幕后内容：展示工作过程
- 互动内容：提问和投票
- 推广内容：产品/服务
- 娱乐内容：轻松有趣

**发布频率**
- Twitter：每天 3-5 条
- LinkedIn：每天 1-2 条
- Instagram：每天 1-2 条

**最佳时间**
- 早上 8-9 点：通勤时间
- 中午 12-1 点：午餐时间
- 下午 5-6 点：下班时间
- 晚上 8-9 点：休闲时间

### 内容准备

**内容库**
- 预写文章
- 图片素材
- 视频内容
- 引用和名言

**自动调整**
- 根据平台调整格式
- 添加相关标签
- 优化发布时间
- A/B 测试标题

### 互动管理

**自动响应**
- 感谢新关注者
- 回复常见问题
- 转发正面提及

**监控指标**
- 互动率
- 粉丝增长
- 内容表现
- 最佳发布时间

### 每周报告
```
📈 社交媒体周报 - YYYY-MM-DD

📊 关键指标
- 总互动：[数量]
- 新粉丝：[数量]
- 内容发布：[数量]
- 平均互动率：[百分比]

🔥 最佳表现
1. [内容摘要] - [互动数]
2. [内容摘要] - [互动数]

💡 下周建议
- [建议内容]
```
```

### 3. 配置

```
Schedule: 0 8,12,17,20 * * *
Action: 选择内容 → 调整格式 → 发布 → 监控
```

---

## 成功指标

- [ ] 每天按时发布
- [ ] 粉丝稳定增长
- [ ] 互动率提升
- [ ] 节省时间 > 5 小时/周

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📱 Social Media Scheduler

> Post once, publish everywhere. Stop juggling 5 apps to share the same content.

---

## The Problem

Managing social media presence across Twitter/X, LinkedIn, Bluesky, and Instagram means logging into each platform, reformatting content for each, and posting at optimal times. Most people either spend 2+ hours daily on this or let their accounts go stale. Both hurt growth.

---

## The Solution

OpenClaw takes one piece of content and automatically adapts it for each platform's format, character limits, and best practices. Schedule once, post everywhere at optimal times, and track what's working.

---

## Setup Guide

### Step 1: Install Required Skills (5 minutes)

```bash
openclaw skill install bluesky
openclaw skill install linkedin
openclaw skill install upload-post
```

### Step 2: Create Content Templates

Create `~/openclaw/social-templates/`:

```markdown
# Social Media Templates

## Thread Format (Twitter/X, Bluesky)
- Hook in first post (curiosity gap)
- Max 280 chars per post
- Number posts: 1/, 2/, etc.
- End with CTA

## LinkedIn Format
- Professional tone
- 1300 char limit
- Use line breaks for readability
- 3-5 relevant hashtags

## Instagram Caption
- Conversational tone
- Emoji-friendly
- 2200 char max
- 20-30 hashtags in first comment
```

### Step 3: Set Up Content Queue

Create `~/openclaw/content-queue.json`:

```json
{
  "queue": [],
  "posted": [],
  "schedule": {
    "twitter": ["09:00", "13:00", "17:00"],
    "linkedin": ["08:00", "12:00"],
    "bluesky": ["10:00", "15:00"]
  }
}
`

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
mkdir auto-schedule-social-posts && cd auto-schedule-social-posts
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
auto-schedule-social-posts/
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
  // TODO: Implement data collection for Auto-Schedule Social Posts
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
  logger.info('=== 自動排程社群發文 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 自動排程社群發文 報告\n\n${result}`);
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
pm2 start src/index.js --name auto-schedule-social-posts  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
