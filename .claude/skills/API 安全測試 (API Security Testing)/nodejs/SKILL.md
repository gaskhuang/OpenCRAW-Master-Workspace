---
name: API 安全測試 (API Security Testing)/nodejs
description: "Use Case #082 Node.js 方案: API 安全測試。使用 Node.js 實作 API Security Testing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #082: API 安全測試 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中高級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# API 安全测试器

## 简介

API 是系统的关键入口，需要定期安全测试。这个使用案例自动测试 API 安全性，识别漏洞，验证认证授权，并生成安全报告。

**为什么重要**：保护 API 免受攻击，确保数据安全，符合安全标准。

**真实例子**：一家公司使用此代理测试其 API，发现了 SQL 注入和权限绕过漏洞，及时修复避免了数据泄露。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `api_testing` | [ClawdHub](https://clawhub.com/skills/api) | API 测试 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全测试 |
| `vulnerability` | [ClawdHub](https://clawhub.com/skills/vuln) | 漏洞扫描 |

---

## 设置步骤

### 1. 前置条件

- API 文档
- 测试账号
- 测试环境

### 2. 提示词模板

```markdown
## API 安全测试器

你是我的安全测试员。测试 API 安全性：

### 测试项目

**认证测试**
- 弱密码测试
- 暴力破解防护
- Token 过期
- 会话管理

**授权测试**
- 水平越权
- 垂直越权
- IDOR 漏洞
- 权限绕过

**输入验证**
- SQL 注入
- XSS 攻击
- 命令注入
- 路径遍历

**敏感数据**
- 数据泄露
- 加密传输
- 日志脱敏
- 错误信息

### 测试报告

```
🔒 API 安全测试报告 - YYYY-MM-DD

📊 概览
- 测试端点：XX 个
- 发现问题：XX 个
- 高危漏洞：XX 个
- 中危漏洞：XX 个

🚨 高危漏洞
1. [端点] - [漏洞类型]
   描述：[描述]
   影响：[影响]
   修复：[建议]

⚠️ 中危漏洞
1. [端点] - [漏洞类型]
   描述：[描述]
   修复：[建议]

✅ 通过测试
- [端点] - 安全

📋 修复优先级
1. [漏洞] - 立即修复
2. [漏洞] - 本周修复
```

### 修复建议

**SQL 注入**
```python
# 使用参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**权限控制**
```python
# 验证用户权限
if not user.has_permission('resource', 'read'):
    return 403
```
```

### 3. 配置

```
Schedule: 0 3 * * 0
Action: 扫描 API → 测试漏洞 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 高危漏洞零遗留
- [ ] API 安全评分 > 90
- [ ] 安全事件零发生
- [ ] 合规检查通过

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
mkdir api-security-testing && cd api-security-testing
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
api-security-testing/
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
  // TODO: Implement data collection for API Security Testing
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
  logger.info('=== API 安全測試 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 API 安全測試 報告\n\n${result}`);
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
pm2 start src/index.js --name api-security-testing  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
