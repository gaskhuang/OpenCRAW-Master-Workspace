---
name: Sentry 事故回顧報告 (Sentry Incident Retrospective)/nodejs
description: "Use Case #076 Node.js 方案: Sentry 事故回顧報告。使用 Node.js 實作 Sentry Incident Retrospective 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #076: Sentry 事故回顧報告 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 安全事件响应

## 简介

安全事件需要快速响应以减少损失。这个使用案例自动化安全事件响应流程，检测事件、分析影响、执行响应措施，并生成事件报告。

**为什么重要**：快速响应安全事件，减少损失，满足合规要求。

**真实例子**：一家公司遭受 DDoS 攻击，代理在 30 秒内检测到攻击，自动触发缓解措施，将服务中断时间从数小时缩短到几分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `siem` | [ClawdHub](https://clawhub.com/skills/siem) | 安全监控 |
| `automation` | [ClawdHub](https://clawhub.com/skills/auto) | 自动响应 |
| `alert` | [ClawdHub](https://clawhub.com/skills/alert) | 发送告警 |

---

## 设置步骤

### 1. 前置条件

- SIEM 系统
- 响应剧本
- 通知渠道

### 2. 提示词模板

```markdown
## 安全事件响应

你是我的安全响应助手。自动化事件响应：

### 检测阶段

**事件类型**
- 恶意软件
- 数据泄露
- DDoS 攻击
- 入侵检测
- 内部威胁

**检测来源**
- SIEM 告警
- 用户报告
- 威胁情报
- 异常检测

### 响应流程

**1. 初步响应（0-15 分钟）**
- 确认事件
- 评估影响
- 通知团队
- 启动剧本

**2. 遏制措施（15-60 分钟）**
- 隔离受影响系统
- 阻断恶意 IP
- 禁用受损账号
- 保护证据

**3. 根除修复（1-24 小时）**
- 清除恶意软件
- 修复漏洞
- 恢复系统
- 验证安全

**4. 恢复运营（24-72 小时）**
- 恢复服务
- 监控异常
- 验证完整性
- 更新防护

### 事件报告

```
🚨 安全事件报告 - #[编号]

📋 基本信息
- 发现时间：YYYY-MM-DD HH:MM
- 事件类型：[类型]
- 影响范围：[描述]
- 严重程度：[严重/高危/中危/低危]

🔍 事件详情
- 攻击向量：[描述]
- 受影响资产：[列表]
- 数据泄露：[是/否，范围]

⚡ 响应行动
- [时间]：[行动]
- [时间]：[行动]

📊 影响评估
- 服务中断：XX 分钟
- 数据泄露：XX 条记录
- 财务损失：$XXXX

🛡️ 后续措施
1. [措施 1]
2. [措施 2]

📚 经验教训
- [经验 1]
- [经验 2]
```

### 自动化剧本

**DDoS 响应**
1. 检测流量异常
2. 启用 DDoS 防护
3. 通知 CDN 提供商
4. 调整防火墙规则
5. 监控缓解效果

**恶意软件响应**
1. 隔离受感染主机
2. 运行杀毒扫描
3. 分析恶意软件
4. 清除威胁
5. 恢复系统
```

### 3. 配置

```
Trigger: 安全告警
Action: 检测 → 分析 → 响应 → 恢复 → 报告
```

---

## 成功指标

- [ ] 检测时间 < 5 分钟
- [ ] 响应时间 < 15 分钟
- [ ] 恢复时间 < 4 小时
- [ ] 损失最小化

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
mkdir sentry-incident-retrospective && cd sentry-incident-retrospective
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
sentry-incident-retrospective/
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
  // TODO: Implement data collection for Sentry Incident Retrospective
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
  logger.info('=== Sentry 事故回顧報告 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 Sentry 事故回顧報告 報告\n\n${result}`);
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
pm2 start src/index.js --name sentry-incident-retrospective  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
