---
name: 電子報轉 Podcast (Newsletter to Podcast)/nodejs
description: "Use Case #015 Node.js 方案: 電子報轉 Podcast。使用 Node.js 實作 Newsletter to Podcast 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #015: 電子報轉 Podcast — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: 中級 | 分類: 創意與內容製作

---

## 原始需求 (來自 Source Repos)

# 邮件转播客通勤助手

## 简介

你订阅了很多有趣的邮件新闻稿——行业更新、医疗新闻、技术摘要——但很少有时间阅读它们。如果你的 AI 代理能把这些邮件转换成通勤时听的播客会怎样？

这个使用案例自动将邮件新闻稿转换为音频简报。你的代理监控收件箱，检测新闻稿，编写对话式脚本，并使用文本转语音生成音频。结果通过 Telegram 或 Signal 发送给你，随时可播放。

无需技术技能。只需转发一封邮件并说"制作播客"，或设置为每天早上自动运行。

**为什么重要**：利用碎片时间（通勤、锻炼、做家务）获取信息，提高学习效率。

**真实例子**：一位医生每天早上通勤时听 AI 生成的医疗新闻播客，保持对最新研究的了解。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `tts` | [ClawdHub](https://clawhub.com/skills/tts) | 文本转语音生成 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 读取邮件 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送音频消息 |

---

## 设置步骤

### 1. 前置条件

- 代理可以访问的邮件账号（Gmail 需应用密码）
- 连接到 OpenClaw 的 Telegram 或 Signal 频道
- （可选）ElevenLabs API 密钥以获得更高质量的语音

### 2. 提示词模板

```markdown
## 邮件转播客

你是我的个人播客制作人。每天早上 7 点：

1. 检查我过去 24 小时收到的邮件新闻稿
2. 挑选最有趣的 3-5 个故事
3. 编写对话式播客脚本（3-5 分钟阅读时间）
4. 使用 TTS 转换为音频
5. 通过 Telegram 发送音频给我

风格：温暖、对话式，像朋友边喝咖啡边聊天。
保持在 5 分钟以内。跳过广告和促销内容。

### 成功标准
- [ ] 音频简报在通勤开始前送达
- [ ] 涵盖订阅中最相关的故事
- [ ] 收听时间少于 5 分钟
- [ ] 你期待每天收听
```

### 3. 配置

设置定时任务每天早上 7:00 运行：

```
Schedule: 0 7 * * *
Action: 检查邮件 → 生成脚本 → TTS → 发送音频
```

---

## 成功指标

- [ ] 音频简报在通勤开始前送达
- [ ] 涵盖订阅中最相关的故事
- [ ] 收听时间少于 5 分钟
- [ ] 你期待每天收听

---

## 变体与扩展

### 变体 1：特定主题播客
只关注特定主题（如 AI、医疗、金融）。

### 变体 2：多语言播客
将内容翻译成你的母语后生成音频。

### 变体 3：晚间摘要
在晚上生成当天的新闻摘要。

---

## 故障排除

### 问题：音频质量不佳
**解决方案**：使用 ElevenLabs API 获得更高质量的语音。

### 问题：邮件未检测到
**解决方案**：检查邮件过滤规则，确保新闻稿不被标记为垃圾邮件。

---

## 相关资源

- [ElevenLabs 文档](https://elevenlabs.io/docs)
- [TTS 技能指南](https://clawhub.com/skills/tts)
- [邮件技能指南](https://clawhub.com/skills/email)

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区
- 原帖标题："邮件转播客通勤助手"


---

# 医疗邮件转播客

## 简介

医疗专业人士需要持续学习最新研究和临床指南，但阅读大量医学文献耗时。这个使用案例将医学邮件和文献转换为播客，方便在通勤或锻炼时学习。

**为什么重要**：利用碎片时间学习，保持专业知识更新。

**真实例子**：一位医生使用此代理将每日医学新闻稿转换为播客，在通勤时收听，保持对最新医学进展的了解。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 读取邮件 |
| `tts` | [ClawdHub](https://clawhub.com/skills/tts) | 文本转语音 |
| `medical_nlp` | [ClawdHub](https://clawhub.com/skills/medical) | 医学内容处理 |

---

## 设置步骤

### 1. 前置条件

- 医学邮件订阅
- TTS 服务
- 播客发布渠道

### 2. 提示词模板

```markdown
## 医疗邮件转播客

你是我的医学学习助手。将医学内容转换为播客：

### 内容筛选

**来源**
- NEJM 摘要
- JAMA 新闻
- 专科协会邮件
- 医学新闻网站

**筛选标准**
- 临床相关性
- 证据等级
- 实践影响
- 新颖性

### 内容处理

**医学术语**
- 正确发音医学术语
- 解释缩写
- 提供上下文

**内容结构**
1. 研究背景
2. 方法概述
3. 关键发现
4. 临床意义
5. 实践建议

### 播客格式

```
🏥 医学每日播客 - YYYY-MM-DD

📋 今日内容
1. [研究标题]
2. [研究标题]
3. [研究标题]

🔬 深度解读
[详细解读内容]

💡 临床应用
[实践建议]
```

### 质量控制
- 事实核查
- 来源引用
- 免责声明
```

### 3. 配置

```
Schedule: 0 6 * * *
Action: 收集内容 → 筛选 → 生成播客 → 发布
```

---

## 成功指标

- [ ] 每日播客准时发布
- [ ] 内容准确可靠
- [ ] 收听完成率高
- [ ] 临床知识更新

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
mkdir newsletter-to-podcast && cd newsletter-to-podcast
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
newsletter-to-podcast/
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
  // TODO: Implement data collection for Newsletter to Podcast
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
  logger.info('=== 電子報轉 Podcast ===');
  validate();
  const data = await collectData();
  if (data) {
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 電子報轉 Podcast 報告\n\n${result}`);
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
pm2 start src/index.js --name newsletter-to-podcast  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
