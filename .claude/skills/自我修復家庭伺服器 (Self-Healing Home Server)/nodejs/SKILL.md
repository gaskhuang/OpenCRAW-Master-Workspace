---
name: 自我修復家庭伺服器 (Self-Healing Home Server)/nodejs
description: "Use Case #070 Node.js 方案: 自我修復家庭伺服器。使用 Node.js 實作 Self-Healing Home Server 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #070: 自我修復家庭伺服器 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 高級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# Self-Healing Home Server & Infrastructure Management

Running a home server means being on-call 24/7 for your own infrastructure. Services go down at 3 AM, certificates expire silently, disk fills up, and pods crash-loop — all while you're asleep or away.

This use case turns OpenClaw into a persistent infrastructure agent with SSH access, automated cron jobs, and the ability to detect, diagnose, and fix issues before you know there's a problem.

## Pain Point

Home lab operators and self-hosters face a constant maintenance burden:

- Health checks, log monitoring, and alerting require manual setup and attention
- When something breaks, you have to SSH in, diagnose, and fix — often from your phone
- Infrastructure-as-code (Terraform, Ansible, Kubernetes manifests) needs regular updates
- Knowledge about your setup lives in your head, not in searchable documentation
- Routine tasks (email triage, deployment checks, security audits) eat hours every week

## What It Does

- **Automated health monitoring**: Cron-based checks on services, deployments, and system resources
- **Self-healing**: Detects issues via health checks and applies fixes autonomously (restart pods, scale resources, fix configs)
- **Infrastructure management**: Writes and applies Terraform, Ansible, and Kubernetes manifests
- **Morning briefings**: Daily summary of system health, calendar, weather, and task board status
- **Email triage**: Scans inbox, labels actionable items, archives noise
- **Knowledge extraction**: Processes notes and conversation exports into a structured, searchable knowledge base
- **Blog publishing pipeline**: Draft → generate banner → publish to CMS → deploy to hosting — fully automated
- **Security auditing**: Regular scans for hardcoded secrets, privileged containers, and overly permissive access

## Skills You Need

- `ssh` access to home network machines
- `kubectl` for Kubernetes cluster management
- `terraform` and `ansible` for infrastructure-as-code
- `1password` CLI for secrets management
- `gog` CLI for email access
- Calendar API access
- Obsidian vault or notes directory (for knowledge base)
- `openclaw doctor` for self-diagnostics

## How to Set It Up

### 1. Core Agent Configuration

Name your agent and define its access scope in AGENTS.md:

```text
## Infrastructure Agent

You are Reef, an infrastructure management agent.

Access:
- SSH to all machines on the home network (192.168.1.0/24)
- kubectl for the K3s cluster
- 1Password vault (read-only for credentials, dedicated AI vault)
- Gmail via gog CLI
- Calendar (yours + partner's)
- Obsidian vault at ~/Documents/Obsidian/

Rules:
- NEVER hardcode secrets — always use 1Password CLI or environment variables
- NEVER push directly to main — always create a PR
- Run `openclaw doctor` as part of self-health checks
- Log all infrastructure changes to ~/logs/infra-changes.md
```

### 2. Automated Cron Job System

The power of this setup is the scheduled job system. Configure in HEARTBEAT.md:

``

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
mkdir self-healing-home-server && cd self-healing-home-server
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
self-healing-home-server/
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
  // TODO: Implement data collection for Self-Healing Home Server
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
  logger.info('=== 自我修復家庭伺服器 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 自我修復家庭伺服器 報告\n\n${result}`);
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
pm2 start src/index.js --name self-healing-home-server  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
