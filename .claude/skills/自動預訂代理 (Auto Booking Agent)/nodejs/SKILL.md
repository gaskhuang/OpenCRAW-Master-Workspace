---
name: 自動預訂代理 (Auto Booking Agent)/nodejs
description: "Use Case #024 Node.js 方案: 自動預訂代理。使用 Node.js 實作 Auto Booking Agent 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #024: 自動預訂代理 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 预约预订代理

## 简介

预订餐厅、预约服务常常需要反复沟通确认时间。这个使用案例自动处理预约流程，与商家沟通，确认最佳时间，并将预约添加到日历。

**为什么重要**：节省时间，避免反复沟通，确保预约成功。

**真实例子**：一位忙碌的高管使用此代理预订餐厅，代理自动联系多家餐厅询问空位，比较选项，确认预订，并添加到日历发送提醒。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `phone` | [ClawdHub](https://clawhub.com/skills/phone) | 拨打电话 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 发送邮件 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 检查空闲 |
| `booking_api` | [ClawdHub](https://clawhub.com/skills/booking) | 在线预订 |

---

## 设置步骤

### 1. 前置条件

- 日历访问权限
- 预订平台账号
- 偏好设置（餐厅类型、时间偏好）

### 2. 提示词模板

```markdown
## 预约预订代理

你是我的私人助理。帮我处理各种预约：

### 餐厅预订

**流程**
1. 接收预订请求
2. 检查我的日历空闲时间
3. 搜索符合条件的餐厅
4. 联系餐厅询问空位
5. 比较选项并确认最佳
6. 添加到日历
7. 发送确认信息

**信息收集**
- 日期和时间偏好
- 人数
- 餐厅类型偏好
- 特殊要求（素食、过敏等）
- 预算范围

**沟通模板**
"您好，我想预订 [日期] [时间] 的 [人数] 人桌。
请问有空位吗？需要无烟区。
我的电话是 [号码]。"

### 服务预约

**支持类型**
- 医生预约
- 美容美发
- 汽车保养
- 家政服务
- 咨询服务

**流程**
1. 确认服务需求
2. 查找可用服务商
3. 比较时间和价格
4. 预约并确认
5. 设置提醒

### 确认信息
```
✅ 预订确认

📍 餐厅：[名称]
📅 日期：YYYY-MM-DD
🕐 时间：HH:MM
👥 人数：X 人
📞 电话：[号码]
📍 地址：[地址]

💡 提醒：
- 提前 15 分钟到达
- 已备注素食需求
- 停车场在地下
```
```

### 3. 配置

```
Trigger: 用户请求
Action: 收集信息 → 搜索选项 → 联系预订 → 确认
```

---

## 成功指标

- [ ] 预订成功率 > 90%
- [ ] 平均处理时间 < 5 分钟
- [ ] 用户满意度高
- [ ] 预约冲突为零

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
mkdir auto-booking-agent && cd auto-booking-agent
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
auto-booking-agent/
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
  // TODO: Implement data collection for Auto Booking Agent
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
  logger.info('=== 自動預訂代理 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 自動預訂代理 報告\n\n${result}`);
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
pm2 start src/index.js --name auto-booking-agent  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
