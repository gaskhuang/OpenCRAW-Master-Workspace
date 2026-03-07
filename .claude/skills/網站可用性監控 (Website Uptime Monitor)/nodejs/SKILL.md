---
name: 網站可用性監控 (Website Uptime Monitor)/nodejs
description: "Use Case #086 Node.js 方案: 網站可用性監控。使用 Node.js 實作 Website Uptime Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #086: 網站可用性監控 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 初中級 | 分類: 監控與維運

---

## 原始需求 (來自 Source Repos)

# 网站可用性监控

## 简介

网站可用性直接影响用户体验和业务收益。这个使用案例持续监控网站可用性，检测宕机，测量响应时间，并在问题发生时立即通知。

**为什么重要**：确保服务可用，及时发现故障，减少业务损失。

**真实例子**：一家电商公司使用此代理监控网站，在一次服务器故障中，代理在 30 秒内检测到问题并通知团队，将停机时间从数小时缩短到 15 分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `http` | [ClawdHub](https://clawhub.com/skills/http) | HTTP 请求 |
| `alert` | [ClawdHub](https://clawhub.com/skills/alert) | 发送告警 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |

---

## 设置步骤

### 1. 前置条件

- 监控目标 URL
- 检查频率
- 告警阈值

### 2. 提示词模板

```markdown
## 网站可用性监控

你是我的运维助手。监控网站可用性：

### 监控指标

**可用性**
- HTTP 状态码
- 响应时间
- SSL 证书状态
- DNS 解析

**性能**
- 页面加载时间
- 首字节时间
- 内容大小
- 资源加载

**功能**
- 关键页面检查
- API 端点检查
- 数据库连接
- 第三方服务

### 告警规则

**紧急**
- 网站不可访问
- 响应时间 > 10s
- SSL 证书过期
- 错误率 > 10%

**警告**
- 响应时间 > 3s
- 错误率 > 1%
- 证书 7 天内过期

### 监控报告

```
📊 网站监控报告 - YYYY-MM-DD

🌐 [网站名称]

📈 今日统计
- 可用性：99.9%
- 平均响应：XXXms
- 检查次数：XXXX
- 失败次数：X

⏱️ 响应时间趋势
- 最小：XXXms
- 平均：XXXms
- 最大：XXXms
- P95：XXXms

⚠️ 事件记录
- [时间]：[事件描述]
- [时间]：[事件描述]

✅ 健康检查
- 主页：✅
- API：✅
- 数据库：✅
```

### 自动化响应
- 宕机时立即通知
- 自动创建工单
- 尝试自动恢复
- 生成事件报告
```

### 3. 配置

```
Schedule: */1 * * * *
Action: 检查网站 → 分析 → 告警 → 报告
```

---

## 成功指标

- [ ] 可用性 > 99.9%
- [ ] 检测时间 < 1 分钟
- [ ] 误报率 < 5%
- [ ] 响应时间优化

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
mkdir website-uptime-monitor && cd website-uptime-monitor
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
website-uptime-monitor/
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
  // TODO: Implement data collection for Website Uptime Monitor
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
  logger.info('=== 網站可用性監控 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 網站可用性監控 報告\n\n${result}`);
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
pm2 start src/index.js --name website-uptime-monitor  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
