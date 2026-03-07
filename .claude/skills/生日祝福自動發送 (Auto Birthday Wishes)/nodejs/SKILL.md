---
name: 生日祝福自動發送 (Auto Birthday Wishes)/nodejs
description: "Use Case #023 Node.js 方案: 生日祝福自動發送。使用 Node.js 實作 Auto Birthday Wishes 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #023: 生日祝福自動發送 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 生日祝福自动发送

## 简介

记住所有重要日期并发送祝福是一项挑战。这个使用案例管理生日和纪念日，生成个性化祝福，并在正确的时间发送。

**为什么重要**：维护重要关系，不错过重要日子，表达关心。

**真实例子**：一位忙碌的企业家使用此代理管理 100+ 联系人的生日，代理自动生成个性化祝福并准时发送，帮助他维护了重要的人脉关系。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `contacts` | [ClawdHub](https://clawhub.com/skills/contacts) | 访问联系人 |
| `messaging` | [ClawdHub](https://clawhub.com/skills/messaging) | 发送消息 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 发送邮件 |

---

## 设置步骤

### 1. 前置条件

- 联系人列表（含生日）
- 关系类型标记
- 发送渠道偏好

### 2. 提示词模板

```markdown
## 生日祝福自动发送

你是我的关系助手。管理生日祝福：

### 数据管理

**联系人信息**
- 姓名
- 生日
- 关系类型（家人/朋友/同事/客户）
- 偏好渠道（短信/邮件/社交）
- 个人备注（兴趣、共同回忆）

**关系分类**
- 亲密家人：提前准备，精心祝福
- 好朋友：个性化，回忆共同经历
- 同事客户：专业礼貌
- 一般关系：简洁祝福

### 祝福生成

**个性化要素**
- 使用对方名字
- 提及关系特点
- 引用共同回忆
- 符合对方风格

**模板示例**

*亲密朋友*：
"生日快乐 [名字]！🎉 还记得我们 [共同回忆] 吗？
祝你新的一岁 [个性化祝福]！
期待我们下次 [计划]！"

*专业关系*：
"祝您生日快乐！感谢您一直以来的支持与合作。
祝您事业顺利，身体健康！"

### 发送策略

**提前准备**
- 3 天前：生成祝福草稿
- 1 天前：确认发送渠道
- 当天：准时发送

**发送时间**
- 早上 9:00：家人和亲密朋友
- 上午 10:00：同事
- 下午 2:00：客户和业务伙伴
```

### 3. 配置

```
Schedule: 0 9 * * *
Action: 检查生日 → 生成祝福 → 发送
```

---

## 成功指标

- [ ] 重要生日零遗漏
- [ ] 祝福准时发送
- [ ] 收到积极回复
- [ ] 关系维护良好

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
mkdir auto-birthday-wishes && cd auto-birthday-wishes
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
auto-birthday-wishes/
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
  // TODO: Implement data collection for Auto Birthday Wishes
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
  logger.info('=== 生日祝福自動發送 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 生日祝福自動發送 報告\n\n${result}`);
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
pm2 start src/index.js --name auto-birthday-wishes  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
