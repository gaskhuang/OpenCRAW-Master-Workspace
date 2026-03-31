---
name: SSH 金鑰安全掃描 (SSH Key Security Scan)/nodejs
description: "Use Case #079 Node.js 方案: SSH 金鑰安全掃描。使用 Node.js 實作 SSH Key Security Scan 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #079: SSH 金鑰安全掃描 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# SSH 密钥扫描器

## 简介

SSH 密钥管理是安全运维的重要环节。这个使用案例扫描 SSH 密钥，检查密钥强度、过期时间和使用权限，识别潜在的安全风险。

**为什么重要**：防止未授权访问，确保密钥安全，符合合规要求。

**真实例子**：一家公司使用此代理扫描所有服务器的 SSH 密钥，发现 10+ 个弱密钥和 5 个过期密钥，及时修复避免了安全风险。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `ssh` | [ClawdHub](https://clawhub.com/skills/ssh) | SSH 操作 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全扫描 |
| `filesystem` | 内置 | 文件访问 |

---

## 设置步骤

### 1. 前置条件

- SSH 访问权限
- 密钥存储位置
- 安全策略

### 2. 提示词模板

```markdown
## SSH 密钥扫描器

你是我的安全助手。扫描 SSH 密钥安全：

### 扫描内容

**密钥强度**
- 密钥算法（RSA/ECDSA/Ed25519）
- 密钥长度
- 生成时间
- 使用频率

**密钥状态**
- 是否过期
- 是否撤销
- 是否共享
- 权限设置

**使用审计**
- 最后使用时间
- 使用来源 IP
- 登录频率
- 异常登录

### 扫描报告

```
🔐 SSH 密钥扫描报告 - YYYY-MM-DD

📊 概览
- 总密钥数：XX
- 强密钥：XX
- 弱密钥：XX
- 过期密钥：XX

❌ 高风险
1. [密钥] - [问题]
   位置：[路径]
   建议：[操作]

⚠️ 中风险
1. [密钥] - [问题]
   建议：[操作]

✅ 良好
- [密钥] - 强密钥，配置正确

📋 建议操作
1. [操作 1]
2. [操作 2]
```

### 修复建议

**弱密钥**
```bash
# 生成新密钥
ssh-keygen -t ed25519 -C "user@host"

# 更新 authorized_keys
cat new_key.pub >> ~/.ssh/authorized_keys

# 删除旧密钥
```

**权限修复**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
```

### 3. 配置

```
Schedule: 0 2 * * 0
Action: 扫描密钥 → 分析 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 所有密钥符合安全标准
- [ ] 弱密钥及时替换
- [ ] 过期密钥及时撤销
- [ ] 安全事件零发生

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
mkdir ssh-key-security-scan && cd ssh-key-security-scan
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
ssh-key-security-scan/
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
  // TODO: Implement data collection for SSH Key Security Scan
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
  logger.info('=== SSH 金鑰安全掃描 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 SSH 金鑰安全掃描 報告\n\n${result}`);
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
pm2 start src/index.js --name ssh-key-security-scan  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
