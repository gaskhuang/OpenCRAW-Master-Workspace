---
name: 語音筆記轉任務 (Voice Notes to Tasks)/nodejs
description: "Use Case #047 Node.js 方案: 語音筆記轉任務。使用 Node.js 實作 Voice Notes to Tasks 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #047: 語音筆記轉任務 — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 语音笔记转日记

## 简介

将语音笔记转换为每日日记条目。无论是在通勤途中、会议后还是睡前，只需录制语音，代理会自动转录并整理成日记。

**为什么重要**：快速记录想法，无需打字，建立日记习惯。

**真实例子**：一位忙碌的高管使用此代理记录每日反思，代理自动转录并整理成结构化日记，帮助他保持自我反思的习惯。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `voice_recognition` | [ClawdHub](https://clawhub.com/skills/voice) | 语音识别 |
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 笔记管理 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容整理 |

---

## 使用方式

### 录制语音
发送语音消息给代理

### 自动转录
代理转录音频为文本

### 整理日记
代理将内容整理为结构化日记条目

---

## 来源

- 来源：Hostinger


---

# 🎤 Voice Note Organizer

> Capture thoughts anywhere. Find them organized later.

---

## The Problem

Voice notes are the fastest way to capture ideas, but they become a graveyard of untranscribed audio files. You know that brilliant idea is somewhere in your recordings, but finding it means listening to hours of audio.

---

## The Solution

OpenClaw automatically transcribes your voice notes, extracts key points, tags by topic, and makes everything searchable. Ideas captured on a walk become organized notes by the time you're home.

---

## Setup Guide

### Step 1: Install Transcription Skills

```bash
openclaw skill install voicenotes
openclaw skill install local-whisper
openclaw skill install voice-transcribe
```

### Step 2: Set Up Voice Note Sync

Create `~/openclaw/voice-notes/config.json`:

```json
{
  "inputSources": [
    "~/Library/Mobile Documents/com~apple~CloudDocs/VoiceNotes/",
    "~/Dropbox/VoiceMemos/"
  ],
  "outputDir": "~/openclaw/voice-notes/transcripts/",
  "autoTags": ["idea", "todo", "meeting", "journal", "reminder"],
  "language": "en"
}
```

### Step 3: Configure Processing Rules

Create `~/openclaw/voice-notes/rules.md`:

```markdown
# Voice Note Processing

## Auto-Tag Rules
- Contains "remind me" → todo
- Contains "meeting with" → meeting
- Contains "I think" / "what if" → idea
- Morning recordings → journal

## Extract
- Action items (make a list)
- People mentioned
- Dates/deadlines mentioned
- Questions to follow up on

## Archive
- Keep originals for 30 days
- Archive transcripts indefinitely
- Flag recordings with low confidence for review
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `voicenotes` | Voicenotes.com integration |
| `local-whisper` | Local transcription |
| `voice-transcribe` | Cloud transcription |

---

## Example Prompts

**Process new notes:**
```
Transcribe and organize all new voice notes from today.
```

**Search recordings:**
```
Find any voice notes where I talked about [topic] in the last month.
```

**Extract todos:**
```
Go through this week's voice notes and compile all action items I mentioned.
```

**Daily summary:**
```
Summarize what I recorded today. What were my main thoughts?
```

---

## Cron Schedule

```
*/30 * * * *   # Every 30 min - check for new recordings
0 21 * * *     # 9 PM - daily summary of recordings
0 10 * * 0     # Sunday 10 AM - weekly idea review
```

---

## Expected Results

**Week 1:**
- All voice notes s

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
mkdir voice-notes-to-tasks && cd voice-notes-to-tasks
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
voice-notes-to-tasks/
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
  // TODO: Implement data collection for Voice Notes to Tasks
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
  logger.info('=== 語音筆記轉任務 ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 語音筆記轉任務 報告\n\n${result}`);
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
pm2 start src/index.js --name voice-notes-to-tasks  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
