---
name: 旅遊行程規劃 (Travel Itinerary Planner)/nodejs
description: "Use Case #020 Node.js 方案: 旅遊行程規劃。使用 Node.js 實作 Travel Itinerary Planner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #020: 旅遊行程規劃 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 旅行行程规划师

## 简介

规划旅行需要考虑目的地、交通、住宿、景点、预算等众多因素。这个使用案例根据你的偏好和预算，智能规划完整行程，预订服务，并生成详细的旅行指南。

**为什么重要**：节省规划时间，优化旅行体验，确保不遗漏重要景点。

**真实例子**：一对夫妇使用此代理规划日本 10 日游，代理根据他们的兴趣（美食、文化、自然）规划了详细行程，预订了餐厅和交通，使他们的旅行完美无缺。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `travel_api` | [ClawdHub](https://clawhub.com/skills/travel) | 获取旅行信息 |
| `booking` | [ClawdHub](https://clawhub.com/skills/booking) | 预订服务 |
| `maps` | [ClawdHub](https://clawhub.com/skills/maps) | 路线规划 |
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 天气信息 |

---

## 设置步骤

### 1. 前置条件

- 目的地和日期
- 预算范围
- 兴趣偏好
- 旅行人数

### 2. 提示词模板

```markdown
## 旅行行程规划师

你是我的旅行顾问。帮我规划完美的旅行：

### 信息收集

**基本信息**
- 目的地：[城市/国家]
- 日期：YYYY-MM-DD 到 YYYY-MM-DD
- 人数：X 人
- 预算：$XXXX

**偏好设置**
- 旅行风格：休闲/紧凑/冒险
- 兴趣：文化/美食/自然/购物
- 住宿偏好：酒店/民宿/青旅
- 交通偏好：公共交通/租车/打车

### 规划内容

**1. 交通安排**
- 往返机票/火车
- 当地交通（地铁、公交、租车）
- 机场接送

**2. 住宿预订**
- 根据位置选择
- 考虑预算和偏好
- 查看评价和设施

**3. 景点规划**
- 必去景点
- 每日路线优化
- 门票预订
- 开放时间检查

**4. 餐饮推荐**
- 当地特色美食
- 预订热门餐厅
- 备选方案

**5. 活动安排**
- 文化体验
- 户外活动
- 购物时间
- 自由活动

### 行程输出
```
🗾 [目的地] 行程 - X 日游

📅 Day 1 - 抵达日
🕐 上午
- 抵达机场
- 前往酒店
- 办理入住

🕐 下午
- 市区漫步
- [景点 1]

🕐 晚上
- 晚餐 @[餐厅名]
- 早点休息

📅 Day 2 - 文化探索
...

💰 预算明细
- 交通：$XXX
- 住宿：$XXX
- 餐饮：$XXX
- 门票：$XXX
- 其他：$XXX
总计：$XXXX

📋 打包清单
- [物品列表]

📱 实用信息
- 紧急电话
- 大使馆信息
- 常用 App
```

### 实时调整
- 根据天气调整行程
- 处理突发情况
- 推荐替代方案
- 更新预订信息
```

### 3. 配置

```
Trigger: 用户请求
Action: 收集偏好 → 搜索选项 → 规划行程 → 生成指南
```

---

## 成功指标

- [ ] 行程符合偏好和预算
- [ ] 预订成功率 100%
- [ ] 旅行满意度高
- [ ] 无遗漏重要景点

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# ✈️ Smart Travel Planner

> Plan trips in minutes, not hours. Get personalized itineraries that actually work.

---

## The Problem

Planning a trip means juggling 10 browser tabs: flights, hotels, activities, restaurants, transport. You spend hours comparing options and still worry you missed the best deals or made suboptimal choices. Last-minute changes throw everything off.

---

## The Solution

OpenClaw handles the entire trip planning process: finds flights, suggests accommodations matching your preferences, builds day-by-day itineraries, and adapts when plans change. All in one conversation.

---

## Setup Guide

### Step 1: Install Travel Skills

```bash
openclaw skill install flights
openclaw skill install flight-tracker
openclaw skill install weather
openclaw skill install spots  # For local recommendations
```

### Step 2: Set Your Preferences

Create `~/openclaw/travel/preferences.md`:

```markdown
# My Travel Preferences

## Flights
- Preferred airlines: [list]
- Seat preference: Window/Aisle
- Max layover: 3 hours
- Budget range: Economy, willing to upgrade for long hauls

## Accommodation
- Style: Boutique hotels > big chains
- Must have: WiFi, workspace, AC
- Nice to have: Gym, breakfast included
- Avoid: Hostels, shared bathrooms

## Activities
- Love: Local food, walking tours, museums, nature
- Avoid: Tourist traps, shopping malls
- Pace: Moderate (not exhausting)
- Morning person: Yes

## Food
- Dietary: None


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
mkdir travel-itinerary-planner && cd travel-itinerary-planner
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
travel-itinerary-planner/
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
  // TODO: Implement data collection for Travel Itinerary Planner
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
  logger.info('=== 旅遊行程規劃 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 旅遊行程規劃 報告\n\n${result}`);
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
pm2 start src/index.js --name travel-itinerary-planner  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
