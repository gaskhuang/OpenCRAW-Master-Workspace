---
name: 天氣穿搭建議 (Weather-Based Outfit Suggestions)/nodejs
description: "Use Case #022 Node.js 方案: 天氣穿搭建議。使用 Node.js 實作 Weather-Based Outfit Suggestions 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #022: 天氣穿搭建議 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 天气穿搭顾问

## 简介

每天早上的"今天穿什么"问题？这个使用案例根据天气预报、你的日程安排和个人风格偏好，为你推荐每日穿搭。

**为什么重要**：节省时间，确保穿着得体，避免天气带来的尴尬。

**真实例子**：一位商务人士使用此代理后，不再因为天气突变而穿着不当，代理会根据他的会议安排推荐合适的着装。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 查看日程 |
| `wardrobe` | [ClawdHub](https://clawhub.com/skills/wardrobe) | 管理衣橱 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送建议 |

---

## 设置步骤

### 1. 前置条件

- 天气 API 密钥
- 衣橱清单（可选）
- 个人风格偏好

### 2. 提示词模板

```markdown
## 天气穿搭顾问

你是我的时尚顾问。每天早上 7 点为我推荐穿搭：

### 输入数据
1. 今日天气预报（温度、降水、风力）
2. 日程安排（会议、活动类型）
3. 个人风格偏好
4. 衣橱可用选项

### 推荐逻辑
**温度 < 10°C**
- 保暖外套 + 毛衣 + 长裤
- 围巾、手套建议

**温度 10-20°C**
- 轻薄外套 + 长袖
- 可脱卸层次

**温度 > 20°C**
- 短袖/衬衫 + 轻薄下装
- 防晒建议

**雨天**
- 防水外套
- 雨鞋建议
- 带伞提醒

**正式场合**
- 西装/正装建议
- 配饰搭配

### 输出格式
```
🌤️ 今日天气：晴，15-22°C

👔 推荐穿搭：
- 上装：浅蓝色衬衫 + 灰色开衫
- 下装：深色西裤
- 鞋子：棕色皮鞋
- 配饰：简约手表

💡 特别提醒：
- 晚上有雨，带把伞
- 下午有客户会议，保持正式
```

### 学习偏好
- 记录我喜欢的搭配
- 记住我常穿的衣服
- 根据反馈调整推荐
```

### 3. 配置

```
Schedule: 0 7 * * *
Action: 获取天气 → 分析日程 → 生成建议 → 发送
```

---

## 成功指标

- [ ] 每天早上收到穿搭建议
- [ ] 建议符合天气和场合
- [ ] 节省选择穿搭的时间
- [ ] 穿着满意度提升

---

## 变体与扩展

### 变体 1：旅行打包助手
根据目的地天气和行程推荐打包清单。

### 变体 2：购物建议
根据衣橱缺口推荐需要购买的单品。

---

## 故障排除

### 问题：建议不符合个人风格
**解决方案**：提供更多风格偏好示例给代理学习。

### 问题：天气数据不准确
**解决方案**：检查天气 API 配置，考虑使用多个数据源。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 天气早间报告

## 简介

每天早上了解天气情况对日程安排很重要。这个使用案例生成语音天气报告，包含今日天气、穿衣建议和出行提醒，通过 Telegram 或邮件发送。

**为什么重要**：及时了解天气变化，合理安排日程，避免天气带来的不便。

**真实例子**：一位通勤者使用此代理每天早上收到语音天气报告，根据建议调整出行方式和穿着，不再因为天气突变而措手不及。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `tts` | [ClawdHub](https://clawhub.com/skills/tts) | 文本转语音 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送报告 |

---

## 设置步骤

### 1. 前置条件

- 天气 API 密钥
- TTS 服务
- Telegram Bot

### 2. 提示词模板

```markdown
## 天气早间报告

你是我的天气助手。每天早上生成天气报告：

### 报告内容

**当前天气**
- 温度
- 天气状况
- 湿度
- 风速

**今日预报**
- 最高/最低温度
- 降水概率
- 紫外线指数
- 空气质量

**穿衣建议**
- 上装建议
- 下装建议
- 配饰建议（伞、帽、墨镜）

**出行提醒**
- 交通影响
- 路况提醒
- 出行时间建议

### 语音报告格式

```
"早上好！今天是 [日期]。

当前温度 [X] 度，[天气状况]。
今天最高 [X] 度，最低 [X] 度，
降水概率 [X]%。

建议穿着：[穿衣建议]。
[出行提醒]。

祝您有美好的一天！"
```

### 文本报告格式

```
🌤️ 早间天气报告

📍 [城市]
🌡️ 当前：XX°C [状况]
📈 今日：XX°C / XX°C
💧 降水：XX%
💨 风速：XX km/h

👔 穿衣建议
- [建议 1]
- [建议 2]

🚗 出行提醒
- [提醒 1]

💡 今日提示
- [提示]
```

### 个性化
- 根据用户反馈调整建议
- 学习用户偏好
- 特殊天气提前提醒
```

### 3. 配置

```
Schedule: 0 7 * * *
Action: 获取天气 → 生成报告 → TTS → 发送
```

---

## 成功指标

- [ ] 每天早上准时收到报告
- [ ] 建议准确有用
- [ ] 出行准备充分
- [ ] 用户满意度高

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
mkdir weather-based-outfit-suggestions && cd weather-based-outfit-suggestions
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
weather-based-outfit-suggestions/
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
  // TODO: Implement data collection for Weather-Based Outfit Suggestions
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
  logger.info('=== 天氣穿搭建議 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 天氣穿搭建議 報告\n\n${result}`);
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
pm2 start src/index.js --name weather-based-outfit-suggestions  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
