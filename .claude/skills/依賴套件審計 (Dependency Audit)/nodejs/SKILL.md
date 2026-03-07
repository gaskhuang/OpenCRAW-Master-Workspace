---
name: 依賴套件審計 (Dependency Audit)/nodejs
description: "Use Case #075 Node.js 方案: 依賴套件審計。使用 Node.js 實作 Dependency Audit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #075: 依賴套件審計 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 依赖更新检查器

## 简介

项目依赖需要定期更新以获得安全补丁和新功能。这个使用案例检查项目依赖的更新，评估影响，并生成更新建议。

**为什么重要**：保持依赖最新，修复安全漏洞，获得新功能。

**真实例子**：一个开发团队使用此代理检查依赖更新，及时修复了一个严重的安全漏洞，避免了潜在的数据泄露风险。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `package_manager` | [ClawdHub](https://clawhub.com/skills/package) | 包管理 |
| `github` | [ClawdHub](https://clawhub.com/skills/github) | 获取更新 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全扫描 |

---

## 设置步骤

### 1. 前置条件

- 项目仓库访问
- 包管理器配置
- 更新策略

### 2. 提示词模板

```markdown
## 依赖更新检查器

你是我的开发助手。检查和管理依赖更新：

### 检查内容

**安全更新**
- 已知漏洞
- 安全补丁
- 紧急修复

**功能更新**
- 新功能
- 性能改进
- Bug 修复

**重大更新**
- 破坏性变更
- 迁移指南
- 兼容性检查

### 评估标准

**更新优先级**
- 严重：安全漏洞
- 高：重要 Bug 修复
- 中：新功能
- 低：次要改进

**风险评估**
- 变更范围
- 测试覆盖
- 回滚难度
- 依赖冲突

### 更新报告

```
📦 依赖更新报告 - YYYY-MM-DD

🚨 安全更新（立即处理）
1. [包名] [当前] → [最新]
   漏洞：[CVE-ID]
   严重性：[严重/高危/中危]
   修复：[版本]

📈 重大更新（需要评估）
1. [包名] [当前] → [最新]
   变更：[破坏性变更]
   迁移：[指南链接]
   建议：[操作]

✨ 功能更新（建议更新）
1. [包名] [当前] → [最新]
   新功能：[描述]
   改进：[描述]

📊 统计
- 可更新：XX 个
- 安全更新：XX 个
- 重大更新：XX 个
```

### 自动化
- 每周检查更新
- 安全更新立即通知
- 生成 PR 更新依赖
- 运行测试验证
```

### 3. 配置

```
Schedule: 0 9 * * 1
Action: 检查更新 → 评估 → 生成报告 → 创建 PR
```

---

## 成功指标

- [ ] 安全漏洞及时修复
- [ ] 依赖保持最新
- [ ] 无破坏性变更
- [ ] 项目稳定性保持

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 技能供应链审计

## 简介

审计 OpenClaw 技能供应链安全，检查依赖风险，验证来源可信。

**为什么重要**：防止供应链攻击，确保技能安全，保护系统完整性。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `skills` | [ClawdHub](https://clawhub.com/skills/skills) | 技能管理 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全审计 |

---

## 使用方式

审计已安装技能，生成风险报告

---

## 来源

- 作者：OpenClaw 社区


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
mkdir dependency-audit && cd dependency-audit
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
dependency-audit/
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
  // TODO: Implement data collection for Dependency Audit
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
  logger.info('=== 依賴套件審計 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 依賴套件審計 報告\n\n${result}`);
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
pm2 start src/index.js --name dependency-audit  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
