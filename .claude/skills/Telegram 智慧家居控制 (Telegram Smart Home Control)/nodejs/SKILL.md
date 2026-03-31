---
name: Telegram 智慧家居控制 (Telegram Smart Home Control)/nodejs
description: "Use Case #019 Node.js 方案: Telegram 智慧家居控制。使用 Node.js 實作 Telegram Smart Home Control 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #019: Telegram 智慧家居控制 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 智能家居 Telegram 控制器

## 简介

通过 Telegram 消息控制你的智能家居设备。这个使用案例让你可以发送自然语言命令来控制灯光、温度、安防系统等，无需打开多个应用。

**为什么重要**：统一控制界面，语音/文字控制，远程管理家居。

**真实例子**：一位用户下班路上通过 Telegram 发送"我快到家了"，代理自动打开空调、调整灯光、开始播放音乐，营造舒适的回家环境。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 接收命令 |
| `smart_home` | [ClawdHub](https://clawhub.com/skills/smart-home) | 控制设备 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 理解命令 |

---

## 设置步骤

### 1. 前置条件

- 智能家居设备（支持 HomeKit、Google Home 或 Alexa）
- Telegram Bot
- 智能家居 Hub

### 2. 提示词模板

```markdown
## 智能家居 Telegram 控制器

你是我的智能家居管家。通过 Telegram 接收命令并执行：

### 命令解析

**灯光控制**
- "打开客厅灯" → 开灯
- "调暗卧室灯到 50%" → 调整亮度
- "关闭所有灯" → 全关

**温度控制**
- "设置温度到 24 度" → 调整空调
- "有点热" → 降低 2 度
- "开启节能模式" → 节能设置

**场景模式**
- "我回家了" → 回家模式
- "我要睡觉了" → 睡眠模式
- "我要出门了" → 离家模式
- "看电影" → 影院模式

**安防系统**
- "开启安防" → 启动监控
- "查看门口" → 发送摄像头画面
- "谁在家" → 报告人员状态

### 场景定义

**回家模式**
- 开门灯
- 空调调至舒适温度
- 播放欢迎音乐
- 关闭安防

**睡眠模式**
- 关闭所有灯
- 空调调至睡眠温度
- 启动夜间安防
- 静音所有设备

**离家模式**
- 关闭所有电器
- 启动全屋安防
- 扫地机器人开始工作
- 模拟有人在家的灯光

### 状态报告
```
🏠 家居状态

💡 灯光：客厅开，卧室关，厨房开
🌡️ 温度：24°C (目标)
🔒 安防：已启动
👥 人员：2 人在家
💡 能耗：今日 12.5 kWh
```
```

### 3. 配置

```
Trigger: Telegram 消息
Action: 解析命令 → 执行操作 → 确认回复
```

---

## 成功指标

- [ ] 所有设备可通过 Telegram 控制
- [ ] 命令理解准确率 > 95%
- [ ] 响应时间 < 3 秒
- [ ] 场景模式正常运行

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🏠 Smart Home Orchestrator

> Your home, intelligently automated. Not just "lights on" but "perfect ambiance."

---

## The Problem

Smart home devices are dumb in isolation. You have 10 apps for 10 devices. Creating complex automations requires programming skills. And when something changes (guest visiting, working from home), you manually adjust everything.

---

## The Solution

OpenClaw becomes your home's brain: understands context (time, weather, who's home, your calendar), orchestrates devices together, and adapts to your life. Tell it what you want in natural language.

---

## Setup Guide

### Step 1: Install Smart Home Skills

```bash
openclaw skill install homeassistant
openclaw skill install homey-cli
openclaw skill install nest-devices
openclaw skill install netatmo
```

### Step 2: Define Scenes

Create `~/openclaw/home/scenes.md`:

```markdown
# Home Scenes

## Morning
- Lights: Gradual brighten 15 min before alarm
- Thermostat: 72°F
- Coffee maker: Start
- Blinds: Open

## Work Mode
- Office lights: Bright, cool white
- Other rooms: Off
- Thermostat: Comfortable
- Do Not Disturb: On

## Movie Night
- Living room: Dim to 20%
- TV backlighting: On, blue
- Thermostat: 70°F
- Blinds: Closed

## Goodnight
- All lights: Off
- Doors: Locked
- Thermostat: 68°F
- Security: Armed
```

### Step 3: Set Context Rules

Create `~/openclaw/home/rules.md`:

```markdown
# Automation Rules

## When I leave home
- Lights off (except security)
- Thermostat: Eco mode
- Security: Armed

## When I arrive home
- Lights: Based on time of day
- Thermostat: Comfort mode
- Security: Disarmed

## Gu

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
mkdir telegram-smart-home-control && cd telegram-smart-home-control
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
telegram-smart-home-control/
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
  // TODO: Implement data collection for Telegram Smart Home Control
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
  logger.info('=== Telegram 智慧家居控制 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 Telegram 智慧家居控制 報告\n\n${result}`);
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
pm2 start src/index.js --name telegram-smart-home-control  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
