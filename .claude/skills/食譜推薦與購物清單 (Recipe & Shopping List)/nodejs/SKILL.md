---
name: 食譜推薦與購物清單 (Recipe & Shopping List)/nodejs
description: "Use Case #026 Node.js 方案: 食譜推薦與購物清單。使用 Node.js 實作 Recipe & Shopping List 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #026: 食譜推薦與購物清單 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 食谱推荐与购物清单

## 简介

每天想吃什么是一个永恒的难题。这个使用案例根据你的食材库存、饮食偏好和营养需求，推荐食谱并生成购物清单。

**为什么重要**：简化 meal planning，减少食物浪费，保持饮食健康。

**真实例子**：一位上班族使用此代理规划每周饮食，代理根据冰箱里的食材推荐食谱，生成购物清单，帮他节省了每周 5 小时的 meal planning 时间。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `recipe_api` | [ClawdHub](https://clawhub.com/skills/recipe) | 获取食谱 |
| `nutrition` | [ClawdHub](https://clawhub.com/skills/nutrition) | 营养分析 |
| `shopping` | [ClawdHub](https://clawhub.com/skills/shopping) | 生成清单 |

---

## 设置步骤

### 1. 前置条件

- 饮食偏好（素食、无麸质等）
- 过敏信息
- 厨具清单

### 2. 提示词模板

```markdown
## 食谱推荐与购物清单

你是我的营养顾问。帮我规划每日饮食：

### 推荐逻辑

**考虑因素**
- 现有食材
- 饮食偏好
- 营养平衡
- 烹饪时间
- 难度级别

**每日规划**
- 早餐：简单快捷
- 午餐：营养均衡
- 晚餐：丰富多样
- 零食：健康选择

### 食谱推荐

**输入**
- 可用食材
- 时间限制
- 人数

**输出**
```
🍽️ 今日推荐

🌅 早餐：牛油果吐司
⏱️ 时间：10 分钟
🥗 营养：350 卡，蛋白质 12g
📋 食材：
- 面包 2 片 ✓
- 牛油果 1 个 ✗
- 鸡蛋 1 个 ✓

🍳 步骤：
1. 烤面包
2. 捣牛油果
3. 煎鸡蛋
4. 组合
```

### 购物清单

**自动生成**
- 汇总所需食材
- 检查库存
- 分类整理
- 估算价格

**清单格式**
```
🛒 购物清单

🥬 蔬菜
- 西红柿 500g
- 菠菜 1 把
- 胡萝卜 3 根

🥩 肉类
- 鸡胸肉 500g
- 鸡蛋 12 个

🍚 主食
- 大米 1kg
- 意大利面 500g

💰 预估：$XX.XX
```

### 每周计划
- 生成周菜单
- 批量采购清单
-  meal prep 建议
- 剩菜利用方案
```

### 3. 配置

```
Schedule: 0 18 * * *
Action: 推荐食谱 → 生成清单 → 发送
```

---

## 成功指标

- [ ] 每日食谱推荐符合偏好
- [ ] 购物清单准确完整
- [ ] 食物浪费减少
- [ ] 饮食更加健康

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 🛒 Grocery Optimizer

> Meal plan, shop smart, waste less.

---

## The Problem

Grocery shopping without a plan leads to impulse buys, forgotten items, and food waste. Meal planning is tedious. You buy ingredients for recipes you never make.

---

## The Solution

OpenClaw helps plan meals based on what's on sale, generates optimized grocery lists, tracks what you have, and ensures nothing goes to waste.

---

## Setup Guide

### Step 1: Install Shopping Skills

```bash
openclaw skill install bring-shopping
openclaw skill install recipe-to-list
openclaw skill install gurkerl  # or picnic, instacart
```

### Step 2: Configure Preferences

Create `~/openclaw/grocery/preferences.json`:

```json
{
  "dietaryRestrictions": [],
  "householdSize": 2,
  "cookingDays": ["Monday", "Wednesday", "Friday", "Sunday"],
  "budgetWeekly": 150,
  "stores": ["preferred store"]
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `bring-shopping` | Shopping list management |
| `recipe-to-list` | Recipe ingredient extraction |
| `gurkerl`/`picnic` | Online grocery ordering |

---

## Example Prompts

**Weekly planning:**
```
Plan meals for this week. Keep it under $150, use what's in season, and minimize waste.
```

**Recipe to list:**
```
I want to make [recipe]. Add ingredients to my shopping list, minus what I already have.
```

**What's for dinner:**
```
What can I make with chicken, rice, and the vegetables expiring soon?
```

---

## Cron Schedule

```
0 9 * * 0      # Sunday 9 AM - weekly meal planning
0 10 * * 3     # Wednesday - mid-week list check
```

---

## Expected Results

- 20% reduction in grocery spending
- Less food waste
- No more "what's for dinner?" 

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
mkdir recipe-&-shopping-list && cd recipe-&-shopping-list
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
recipe-&-shopping-list/
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
  // TODO: Implement data collection for Recipe & Shopping List
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
  logger.info('=== 食譜推薦與購物清單 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 食譜推薦與購物清單 報告\n\n${result}`);
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
pm2 start src/index.js --name recipe-&-shopping-list  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
