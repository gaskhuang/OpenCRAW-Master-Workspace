# 每日 Reddit 摘要 (Daily Reddit Digest) -- Node.js 完整實作教學

> **Agent B - 點子王 Node.js 方案**
> 技術棧：Node.js + Reddit .json API (免註冊) + Anthropic SDK + node-telegram-bot-api
> 撰寫日期：2026-03-04

---

## 目錄

1. [方案優勢與架構總覽](#1-方案優勢與架構總覽)
2. [前置準備 Prerequisites](#2-前置準備-prerequisites)
3. [所需套件 Required Packages](#3-所需套件-required-packages)
4. [專案結構 Project Structure](#4-專案結構-project-structure)
5. [完整程式碼 Complete Code](#5-完整程式碼-complete-code)
6. [排程設定 Scheduling Setup](#6-排程設定-scheduling-setup)
7. [測試步驟 Testing Steps](#7-測試步驟-testing-steps)
8. [常見陷阱 Common Pitfalls](#8-常見陷阱-common-pitfalls)
9. [進階擴充 Advanced Extensions](#9-進階擴充-advanced-extensions)

---

## 1. 方案優勢與架構總覽

### 為什麼選這個方案？

| 特點 | 說明 |
|------|------|
| **免註冊 Reddit API** | 使用公開 `.json` 端點，不需要 OAuth、不需要建立 Reddit App、不需要 client_id/secret |
| **新手友善** | 純 Node.js，無需 Python 環境，npm 一鍵安裝 |
| **AI 摘要** | 使用 Claude API 產生高品質繁體中文摘要 |
| **即時推送** | 透過 Telegram Bot 推送到手機，隨時查看 |
| **排程自動化** | node-cron 內建排程，或搭配系統 cron |

### 架構流程圖

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐     ┌──────────────┐
│  node-cron  │────>│  redditFetcher   │────>│ aiSummarizer │────>│telegramSender│
│  (每日觸發)  │     │  (抓取 Reddit)    │     │ (Claude 摘要) │     │ (推送 TG)    │
└─────────────┘     └──────────────────┘     └──────────────┘     └──────────────┘
                           │                        │
                    Reddit .json API          Anthropic API
                    (公開免註冊)              (需 API Key)
```

### Reddit .json API 原理

Reddit 的每個頁面，只要在 URL 後面加上 `.json`，就會回傳 JSON 格式的資料。這是 Reddit 的公開功能，不需要任何認證：

```
一般頁面：https://www.reddit.com/r/programming/hot
JSON 版本：https://www.reddit.com/r/programming/hot.json

一般頁面：https://www.reddit.com/r/ClaudeAI/top?t=day
JSON 版本：https://www.reddit.com/r/ClaudeAI/top.json?t=day&limit=10
```

可用的排序方式：
- `/hot.json` -- 熱門（預設）
- `/top.json?t=day` -- 今日最高分
- `/top.json?t=week` -- 本週最高分
- `/new.json` -- 最新
- `/rising.json` -- 上升中

---

## 2. 前置準備 Prerequisites

### 2.1 Node.js 環境

需要 Node.js 18 或以上版本（支援原生 fetch）。

```bash
# 確認 Node.js 版本
node --version
# 應顯示 v18.x.x 或更高

# 如果沒有安裝，使用 nvm 安裝
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20
```

### 2.2 建立 Telegram Bot（逐步教學）

**步驟 1：找到 BotFather**
1. 打開 Telegram App（手機或桌面版皆可）
2. 在搜尋欄搜尋 `@BotFather`
3. 點選帶有藍色勾勾驗證標誌的官方帳號

**步驟 2：建立新 Bot**
1. 發送 `/newbot` 給 BotFather
2. BotFather 會問你要幫 Bot 取什麼名字（顯示名稱），例如：`我的 Reddit 摘要機器人`
3. 接著會問 username（必須以 `bot` 結尾），例如：`my_reddit_digest_bot`
4. BotFather 回覆中會包含一段 **API Token**，格式類似：
   ```
   7123456789:AAH1Bcd2EfGhIjKlMnOpQrStUvWxYz12345
   ```
5. **請妥善保管此 Token**，稍後會用到

**步驟 3：取得你的 Chat ID**
1. 在 Telegram 搜尋 `@userinfobot` 並開始對話
2. 發送任意訊息，Bot 會回覆你的 User ID（純數字），例如 `123456789`
3. 或者搜尋 `@raw_data_bot`，發送 `/start` 也能取得

**步驟 4：啟用你的 Bot**
1. 在 Telegram 搜尋你剛建立的 Bot username
2. 點選 `Start` 或發送 `/start`
3. 這個步驟很重要！如果不先啟用，Bot 無法發送訊息給你

**（可選）群組使用**
如果想把摘要發送到群組：
1. 將 Bot 加入群組
2. 在群組中發送任意訊息
3. 訪問 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. 在回傳的 JSON 中找到 `chat.id`（群組的 ID 通常是負數，如 `-1001234567890`）

### 2.3 取得 Claude API Key

1. 前往 [Anthropic Console](https://console.anthropic.com/)
2. 註冊或登入帳號
3. 左側選單點選 **API Keys**
4. 點選 **Create Key**，輸入名稱如 `reddit-digest`
5. 複製產生的 API Key（以 `sk-ant-` 開頭）
6. **此 Key 只會顯示一次**，請立刻保存

> 注意：Claude API 是付費服務。claude-sonnet-4-20250514 模型的費用約為每百萬 input tokens $3、每百萬 output tokens $15。
> 每日一次的 Reddit 摘要大約消耗 2,000~5,000 tokens，月費約 $0.01~$0.05 美元，非常便宜。

### 2.4 驗證 Reddit .json API（快速測試）

在瀏覽器或終端機測試：

```bash
# 測試取得 r/programming 的熱門貼文
curl -s "https://www.reddit.com/r/programming/hot.json?limit=3" \
  -H "User-Agent: DailyRedditDigest/1.0" | head -c 500

# 測試取得 r/ClaudeAI 今日最高分貼文
curl -s "https://www.reddit.com/r/ClaudeAI/top.json?t=day&limit=3" \
  -H "User-Agent: DailyRedditDigest/1.0" | python3 -m json.tool | head -20
```

> 重要：Reddit .json API 要求帶有 `User-Agent` header，否則會回傳 429 (Too Many Requests)。

---

## 3. 所需套件 Required Packages

```bash
npm install @anthropic-ai/sdk@^0.39.0 node-telegram-bot-api@^0.66.0 node-cron@^3.0.3 dotenv@^16.4.7 winston@^3.17.0
```

| 套件 | 版本 | 用途 |
|------|------|------|
| `@anthropic-ai/sdk` | `^0.39.0` | Anthropic Claude API 官方 SDK |
| `node-telegram-bot-api` | `^0.66.0` | Telegram Bot API 封裝 |
| `node-cron` | `^3.0.3` | 排程任務管理 (cron 語法) |
| `dotenv` | `^16.4.7` | 環境變數管理 (.env 檔案) |
| `winston` | `^3.17.0` | 結構化日誌記錄 |

> **注意**：本方案不需要 `snoowrap`、`reddit-api` 等 Reddit 套件，因為我們直接用 Node.js 18+ 內建的 `fetch` 呼叫 Reddit 的公開 .json 端點。

---

## 4. 專案結構 Project Structure

```
daily-reddit-digest/
├── .env                    # 環境變數（API Keys 等機密資訊）
├── .env.example            # 環境變數範本（可提交到 Git）
├── .gitignore              # Git 忽略規則
├── package.json            # 專案設定與相依套件
├── src/
│   ├── index.js            # 主程式入口 & 排程器
│   ├── config.js           # 組態管理（讀取 .env 與預設值）
│   ├── redditFetcher.js    # Reddit .json API 抓取模組
│   ├── aiSummarizer.js     # Claude AI 摘要模組
│   ├── telegramSender.js   # Telegram 推送模組
│   └── logger.js           # 日誌工具
├── logs/                   # 執行日誌（自動建立）
└── README.md               # 說明文件
```

---

## 5. 完整程式碼 Complete Code

### 5.1 package.json

```json
{
  "name": "daily-reddit-digest",
  "version": "1.0.0",
  "description": "Daily Reddit Digest - Fetch top posts, AI summarize, deliver via Telegram",
  "main": "src/index.js",
  "type": "module",
  "scripts": {
    "start": "node src/index.js",
    "run-once": "node src/index.js --run-once",
    "test:reddit": "node src/redditFetcher.js",
    "test:summarize": "node src/aiSummarizer.js",
    "test:telegram": "node src/telegramSender.js",
    "test:all": "node src/index.js --run-once"
  },
  "dependencies": {
    "@anthropic-ai/sdk": "^0.39.0",
    "dotenv": "^16.4.7",
    "node-cron": "^3.0.3",
    "node-telegram-bot-api": "^0.66.0",
    "winston": "^3.17.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### 5.2 .env.example

```bash
# === Anthropic Claude API ===
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN=7123456789:AAH1Bcd2EfGhIjKlMnOpQrStUvWxYz12345
TELEGRAM_CHAT_ID=123456789

# === Reddit Settings ===
# Comma-separated list of subreddits to monitor (without r/ prefix)
SUBREDDITS=programming,ClaudeAI,LocalLLaMA,artificial,MachineLearning
# Sort method: hot, top, new, rising
REDDIT_SORT=top
# Time filter for 'top' sort: hour, day, week, month, year, all
REDDIT_TIME_FILTER=day
# Number of posts to fetch per subreddit
REDDIT_POSTS_PER_SUB=5

# === Schedule ===
# Cron expression: default is every day at 08:00 AM
CRON_SCHEDULE=0 8 * * *
# Timezone for cron
CRON_TIMEZONE=Asia/Taipei

# === AI Settings ===
# Claude model to use
CLAUDE_MODEL=claude-sonnet-4-20250514
# Maximum tokens for AI summary
CLAUDE_MAX_TOKENS=4096
# Language for summary output
SUMMARY_LANGUAGE=zh-TW
```

### 5.3 .gitignore

```
node_modules/
.env
logs/
*.log
```

### 5.4 src/logger.js -- 日誌工具

```javascript
// src/logger.js
// Structured logger using winston

import winston from "winston";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const logsDir = path.join(__dirname, "..", "logs");

// Ensure logs directory exists
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    // Console output with color
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
          const metaStr = Object.keys(meta).length
            ? ` ${JSON.stringify(meta)}`
            : "";
          return `[${timestamp}] ${level}: ${message}${metaStr}`;
        })
      ),
    }),
    // File output for persistent logs
    new winston.transports.File({
      filename: path.join(logsDir, "digest.log"),
      maxsize: 5 * 1024 * 1024, // 5MB
      maxFiles: 5,
    }),
    // Separate error log
    new winston.transports.File({
      filename: path.join(logsDir, "error.log"),
      level: "error",
      maxsize: 5 * 1024 * 1024,
      maxFiles: 3,
    }),
  ],
});

export default logger;
```

### 5.5 src/config.js -- 組態管理

```javascript
// src/config.js
// Configuration management - loads from .env with sensible defaults

import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, "..", ".env") });

/**
 * Validate that all required environment variables are set.
 * Throws an error with a helpful message if any are missing.
 */
function validateRequired(keys) {
  const missing = keys.filter((key) => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}\n` +
        `Please copy .env.example to .env and fill in the values.`
    );
  }
}

// Validate critical env vars
validateRequired([
  "ANTHROPIC_API_KEY",
  "TELEGRAM_BOT_TOKEN",
  "TELEGRAM_CHAT_ID",
]);

const config = {
  // Anthropic
  anthropic: {
    apiKey: process.env.ANTHROPIC_API_KEY,
    model: process.env.CLAUDE_MODEL || "claude-sonnet-4-20250514",
    maxTokens: parseInt(process.env.CLAUDE_MAX_TOKENS, 10) || 4096,
  },

  // Telegram
  telegram: {
    botToken: process.env.TELEGRAM_BOT_TOKEN,
    chatId: process.env.TELEGRAM_CHAT_ID,
  },

  // Reddit
  reddit: {
    subreddits: (
      process.env.SUBREDDITS ||
      "programming,ClaudeAI,LocalLLaMA,artificial"
    )
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean),
    sort: process.env.REDDIT_SORT || "top",
    timeFilter: process.env.REDDIT_TIME_FILTER || "day",
    postsPerSub: parseInt(process.env.REDDIT_POSTS_PER_SUB, 10) || 5,
    userAgent: "DailyRedditDigest/1.0 (Node.js; Educational Project)",
    baseUrl: "https://www.reddit.com",
    // Rate limit: minimum ms between requests to Reddit
    rateLimitMs: 2000,
  },

  // Schedule
  schedule: {
    cron: process.env.CRON_SCHEDULE || "0 8 * * *",
    timezone: process.env.CRON_TIMEZONE || "Asia/Taipei",
  },

  // Summary
  summary: {
    language: process.env.SUMMARY_LANGUAGE || "zh-TW",
  },
};

export default config;
```

### 5.6 src/redditFetcher.js -- Reddit 抓取模組

```javascript
// src/redditFetcher.js
// Fetch top posts from Reddit using the public .json API (no auth needed)

import config from "./config.js";
import logger from "./logger.js";

/**
 * Sleep for the specified number of milliseconds.
 * Used for rate limiting between Reddit API requests.
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Fetch posts from a single subreddit using Reddit's .json endpoint.
 *
 * @param {string} subreddit - Subreddit name without the r/ prefix
 * @returns {Promise<Array>} Array of parsed post objects
 *
 * Example URL: https://www.reddit.com/r/programming/top.json?t=day&limit=5
 */
async function fetchSubreddit(subreddit) {
  const { sort, timeFilter, postsPerSub, baseUrl, userAgent } = config.reddit;

  // Build the URL with query parameters
  const params = new URLSearchParams({
    limit: postsPerSub.toString(),
    raw_json: "1", // Prevent Reddit from encoding HTML entities
  });

  // Time filter only applies to 'top' and 'controversial' sorts
  if (sort === "top" || sort === "controversial") {
    params.set("t", timeFilter);
  }

  const url = `${baseUrl}/r/${subreddit}/${sort}.json?${params.toString()}`;

  logger.info(`Fetching r/${subreddit}`, { url, sort, timeFilter });

  const response = await fetch(url, {
    headers: {
      "User-Agent": userAgent,
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    // Handle specific HTTP errors
    if (response.status === 429) {
      throw new Error(
        `Rate limited by Reddit (429). Wait before retrying r/${subreddit}.`
      );
    }
    if (response.status === 404) {
      throw new Error(
        `Subreddit r/${subreddit} not found (404). Check the name.`
      );
    }
    if (response.status === 403) {
      throw new Error(
        `Subreddit r/${subreddit} is private or quarantined (403).`
      );
    }
    throw new Error(
      `Reddit API returned ${response.status} for r/${subreddit}`
    );
  }

  const data = await response.json();

  // Reddit wraps posts in data.data.children
  const children = data?.data?.children || [];

  // Parse each post into a clean object
  const posts = children
    .filter((child) => child.kind === "t3") // t3 = link/post
    .map((child) => {
      const d = child.data;
      return {
        subreddit: d.subreddit,
        title: d.title,
        author: d.author,
        score: d.score,
        upvoteRatio: d.upvote_ratio,
        numComments: d.num_comments,
        url: d.url,
        permalink: `https://www.reddit.com${d.permalink}`,
        selftext: d.selftext || "",
        isSelf: d.is_self,
        createdUtc: d.created_utc,
        thumbnail: d.thumbnail,
        linkFlairText: d.link_flair_text || "",
        // Truncate long self-text to avoid token waste
        selftextTruncated:
          (d.selftext || "").length > 1500
            ? d.selftext.substring(0, 1500) + "... [truncated]"
            : d.selftext || "",
      };
    });

  logger.info(`Fetched ${posts.length} posts from r/${subreddit}`);
  return posts;
}

/**
 * Fetch posts from all configured subreddits with rate limiting.
 *
 * @returns {Promise<Object>} Object keyed by subreddit name, value is array of posts
 *
 * Example return:
 * {
 *   "programming": [{ title: "...", score: 1234, ... }, ...],
 *   "ClaudeAI": [{ title: "...", score: 567, ... }, ...]
 * }
 */
async function fetchAllSubreddits() {
  const { subreddits, rateLimitMs } = config.reddit;
  const results = {};
  let totalPosts = 0;

  logger.info(`Starting fetch for ${subreddits.length} subreddits`, {
    subreddits,
  });

  for (let i = 0; i < subreddits.length; i++) {
    const sub = subreddits[i];

    try {
      results[sub] = await fetchSubreddit(sub);
      totalPosts += results[sub].length;
    } catch (error) {
      logger.error(`Failed to fetch r/${sub}: ${error.message}`);
      results[sub] = []; // Empty array so the digest continues
    }

    // Rate limit: wait between requests (except after the last one)
    if (i < subreddits.length - 1) {
      logger.debug(`Rate limiting: waiting ${rateLimitMs}ms`);
      await sleep(rateLimitMs);
    }
  }

  logger.info(`Fetch complete: ${totalPosts} total posts from ${subreddits.length} subreddits`);
  return results;
}

export { fetchSubreddit, fetchAllSubreddits };

// === Self-test: run with `node src/redditFetcher.js` ===
if (process.argv[1] && process.argv[1].endsWith("redditFetcher.js")) {
  (async () => {
    console.log("=== Reddit Fetcher Self-Test ===\n");
    try {
      const results = await fetchAllSubreddits();

      for (const [sub, posts] of Object.entries(results)) {
        console.log(`\n--- r/${sub} (${posts.length} posts) ---`);
        for (const post of posts) {
          console.log(
            `  [${post.score}] ${post.title} (${post.numComments} comments)`
          );
          console.log(`    ${post.permalink}`);
        }
      }

      console.log("\n=== Self-Test Complete ===");
    } catch (error) {
      console.error("Self-test failed:", error);
      process.exit(1);
    }
  })();
}
```

### 5.7 src/aiSummarizer.js -- Claude AI 摘要模組

```javascript
// src/aiSummarizer.js
// Summarize Reddit posts using Claude (Anthropic SDK)

import Anthropic from "@anthropic-ai/sdk";
import config from "./config.js";
import logger from "./logger.js";

// Initialize Anthropic client
const anthropic = new Anthropic({
  apiKey: config.anthropic.apiKey,
});

/**
 * Build the prompt that will be sent to Claude for summarization.
 *
 * @param {Object} postsBySubreddit - Object keyed by subreddit name
 * @returns {string} Formatted prompt string
 */
function buildPrompt(postsBySubreddit) {
  const lang = config.summary.language;
  const langLabel = lang === "zh-TW" ? "繁體中文" : "English";

  let postsContent = "";

  for (const [sub, posts] of Object.entries(postsBySubreddit)) {
    if (posts.length === 0) continue;

    postsContent += `\n## r/${sub}\n\n`;

    for (const post of posts) {
      postsContent += `### ${post.title}\n`;
      postsContent += `- Author: u/${post.author}\n`;
      postsContent += `- Score: ${post.score} | Comments: ${post.numComments} | Upvote ratio: ${post.upvoteRatio}\n`;
      postsContent += `- Flair: ${post.linkFlairText || "None"}\n`;
      postsContent += `- Link: ${post.permalink}\n`;
      if (post.selftextTruncated) {
        postsContent += `- Content:\n${post.selftextTruncated}\n`;
      }
      postsContent += "\n";
    }
  }

  const systemPrompt = `You are an expert content curator and summarizer. Your task is to create a daily digest of Reddit posts. Write in ${langLabel}. Be concise but informative. Highlight key insights, trends, and notable discussions.`;

  const userPrompt = `Please create a daily Reddit digest from the following posts. For each subreddit section:

1. Write a 1-2 sentence overview of the overall theme/trend
2. For each noteworthy post, provide:
   - A concise summary (2-3 sentences max)
   - Why it matters or what makes it interesting
   - The post link for reference
3. At the end, write a brief "Key Takeaways" section (3-5 bullet points) across all subreddits

Format the output as a clean, readable digest suitable for Telegram (use basic markdown formatting).

Important formatting rules:
- Use *bold* for emphasis (Telegram markdown)
- Use the post's permalink for links
- Keep the total digest concise (aim for readable in 2-3 minutes)
- Skip low-quality or meme posts
- Focus on substantive discussions and valuable content
- Write in ${langLabel}

Here are today's posts:
${postsContent}`;

  return { systemPrompt, userPrompt };
}

/**
 * Send posts to Claude and get a summarized digest back.
 *
 * @param {Object} postsBySubreddit - Object keyed by subreddit name
 * @returns {Promise<string>} The AI-generated digest text
 */
async function summarizePosts(postsBySubreddit) {
  // Check if there are any posts to summarize
  const totalPosts = Object.values(postsBySubreddit).reduce(
    (sum, posts) => sum + posts.length,
    0
  );

  if (totalPosts === 0) {
    logger.warn("No posts to summarize");
    return "No posts were fetched today. Please check the subreddit configuration and Reddit availability.";
  }

  const { systemPrompt, userPrompt } = buildPrompt(postsBySubreddit);

  logger.info("Sending posts to Claude for summarization", {
    totalPosts,
    model: config.anthropic.model,
    maxTokens: config.anthropic.maxTokens,
  });

  try {
    const response = await anthropic.messages.create({
      model: config.anthropic.model,
      max_tokens: config.anthropic.maxTokens,
      system: systemPrompt,
      messages: [
        {
          role: "user",
          content: userPrompt,
        },
      ],
    });

    // Extract the text content from Claude's response
    const summaryText = response.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("\n");

    logger.info("Summarization complete", {
      inputTokens: response.usage.input_tokens,
      outputTokens: response.usage.output_tokens,
      stopReason: response.stop_reason,
    });

    return summaryText;
  } catch (error) {
    if (error.status === 401) {
      throw new Error(
        "Invalid Anthropic API key. Please check ANTHROPIC_API_KEY in .env"
      );
    }
    if (error.status === 429) {
      throw new Error(
        "Anthropic API rate limit exceeded. Please wait and retry."
      );
    }
    if (error.status === 529) {
      throw new Error("Anthropic API is overloaded. Please retry later.");
    }
    throw error;
  }
}

export { summarizePosts, buildPrompt };

// === Self-test: run with `node src/aiSummarizer.js` ===
if (process.argv[1] && process.argv[1].endsWith("aiSummarizer.js")) {
  (async () => {
    console.log("=== AI Summarizer Self-Test ===\n");

    // Create mock data for testing without hitting Reddit
    const mockPosts = {
      programming: [
        {
          title: "Why Rust is taking over systems programming",
          author: "rust_lover",
          score: 2500,
          numComments: 342,
          upvoteRatio: 0.92,
          linkFlairText: "Discussion",
          permalink:
            "https://www.reddit.com/r/programming/comments/abc123/why_rust",
          selftextTruncated:
            "Rust has been the most loved language for 8 years running...",
        },
        {
          title: "New ECMAScript 2026 features are amazing",
          author: "js_dev",
          score: 1800,
          numComments: 256,
          upvoteRatio: 0.88,
          linkFlairText: "News",
          permalink:
            "https://www.reddit.com/r/programming/comments/def456/ecmascript_2026",
          selftextTruncated:
            "The TC39 committee has finalized several exciting proposals...",
        },
      ],
      ClaudeAI: [
        {
          title: "Claude Opus 4 is incredible for code generation",
          author: "ai_researcher",
          score: 890,
          numComments: 134,
          upvoteRatio: 0.95,
          linkFlairText: "Review",
          permalink:
            "https://www.reddit.com/r/ClaudeAI/comments/ghi789/claude_opus_4",
          selftextTruncated:
            "After testing Claude Opus 4 for a week on production codebases...",
        },
      ],
    };

    try {
      console.log("Sending mock data to Claude...\n");
      const summary = await summarizePosts(mockPosts);
      console.log("=== Generated Digest ===\n");
      console.log(summary);
      console.log("\n=== Self-Test Complete ===");
    } catch (error) {
      console.error("Self-test failed:", error.message);
      process.exit(1);
    }
  })();
}
```

### 5.8 src/telegramSender.js -- Telegram 推送模組

```javascript
// src/telegramSender.js
// Send digest messages via Telegram Bot

import TelegramBot from "node-telegram-bot-api";
import config from "./config.js";
import logger from "./logger.js";

// Initialize Telegram Bot (polling disabled - we only send, never receive)
const bot = new TelegramBot(config.telegram.botToken, { polling: false });

/**
 * Telegram has a 4096-character limit per message.
 * Split long messages at logical breakpoints.
 *
 * @param {string} text - The full message text
 * @param {number} maxLength - Maximum chars per chunk (default 4000, leaving buffer)
 * @returns {string[]} Array of message chunks
 */
function splitMessage(text, maxLength = 4000) {
  if (text.length <= maxLength) {
    return [text];
  }

  const chunks = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= maxLength) {
      chunks.push(remaining);
      break;
    }

    // Try to split at a double newline (paragraph break)
    let splitIndex = remaining.lastIndexOf("\n\n", maxLength);

    // Fallback: split at a single newline
    if (splitIndex === -1 || splitIndex < maxLength * 0.5) {
      splitIndex = remaining.lastIndexOf("\n", maxLength);
    }

    // Fallback: split at a space
    if (splitIndex === -1 || splitIndex < maxLength * 0.5) {
      splitIndex = remaining.lastIndexOf(" ", maxLength);
    }

    // Last resort: hard split
    if (splitIndex === -1 || splitIndex < maxLength * 0.5) {
      splitIndex = maxLength;
    }

    chunks.push(remaining.substring(0, splitIndex));
    remaining = remaining.substring(splitIndex).trimStart();
  }

  return chunks;
}

/**
 * Send a digest message to the configured Telegram chat.
 * Handles message splitting for long digests.
 *
 * @param {string} digestText - The formatted digest text
 * @returns {Promise<void>}
 */
async function sendDigest(digestText) {
  const chatId = config.telegram.chatId;

  // Add header with timestamp
  const now = new Date().toLocaleString("zh-TW", {
    timeZone: config.schedule.timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

  const fullMessage = `*Daily Reddit Digest*\n${now}\n${"─".repeat(20)}\n\n${digestText}`;

  const chunks = splitMessage(fullMessage);

  logger.info(`Sending digest to Telegram`, {
    chatId,
    totalLength: fullMessage.length,
    chunks: chunks.length,
  });

  for (let i = 0; i < chunks.length; i++) {
    try {
      // Add part indicator for multi-part messages
      let chunkText = chunks[i];
      if (chunks.length > 1) {
        chunkText = `[${i + 1}/${chunks.length}]\n${chunkText}`;
      }

      await bot.sendMessage(chatId, chunkText, {
        parse_mode: "Markdown",
        disable_web_page_preview: true, // Don't unfurl links
      });

      logger.info(`Sent message chunk ${i + 1}/${chunks.length}`);

      // Small delay between chunks to avoid rate limiting
      if (i < chunks.length - 1) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    } catch (error) {
      // If Markdown parsing fails, retry without parse_mode
      if (
        error.message &&
        error.message.includes("can't parse entities")
      ) {
        logger.warn(
          `Markdown parse failed for chunk ${i + 1}, retrying as plain text`
        );
        try {
          let plainText = chunks[i];
          if (chunks.length > 1) {
            plainText = `[${i + 1}/${chunks.length}]\n${plainText}`;
          }
          await bot.sendMessage(chatId, plainText, {
            disable_web_page_preview: true,
          });
        } catch (retryError) {
          logger.error(
            `Failed to send chunk ${i + 1} even as plain text: ${retryError.message}`
          );
          throw retryError;
        }
      } else {
        logger.error(`Failed to send chunk ${i + 1}: ${error.message}`);
        throw error;
      }
    }
  }

  logger.info("Digest sent successfully to Telegram");
}

/**
 * Send a simple status/error notification.
 *
 * @param {string} message - Short status message
 * @returns {Promise<void>}
 */
async function sendNotification(message) {
  try {
    await bot.sendMessage(config.telegram.chatId, message, {
      disable_web_page_preview: true,
    });
  } catch (error) {
    logger.error(`Failed to send notification: ${error.message}`);
  }
}

export { sendDigest, sendNotification, splitMessage };

// === Self-test: run with `node src/telegramSender.js` ===
if (process.argv[1] && process.argv[1].endsWith("telegramSender.js")) {
  (async () => {
    console.log("=== Telegram Sender Self-Test ===\n");

    try {
      const testMessage =
        "*Test Message*\n\nThis is a test from Daily Reddit Digest.\nIf you see this, the Telegram bot is working correctly!";
      await sendDigest(testMessage);
      console.log("Test message sent! Check your Telegram.\n");
      console.log("=== Self-Test Complete ===");
    } catch (error) {
      console.error("Self-test failed:", error.message);
      if (error.message.includes("chat not found")) {
        console.error(
          "\nHint: Make sure you have started a conversation with the bot first!"
        );
        console.error(
          "Search for your bot in Telegram and press /start"
        );
      }
      if (error.message.includes("Unauthorized")) {
        console.error(
          "\nHint: Check that TELEGRAM_BOT_TOKEN in .env is correct."
        );
      }
      process.exit(1);
    }
  })();
}
```

### 5.9 src/index.js -- 主程式入口與排程器

```javascript
// src/index.js
// Main entry point - orchestrates fetching, summarizing, and sending

import cron from "node-cron";
import config from "./config.js";
import { fetchAllSubreddits } from "./redditFetcher.js";
import { summarizePosts } from "./aiSummarizer.js";
import { sendDigest, sendNotification } from "./telegramSender.js";
import logger from "./logger.js";

/**
 * Run the complete digest pipeline once:
 * 1. Fetch posts from all configured subreddits
 * 2. Send to Claude for summarization
 * 3. Deliver the digest via Telegram
 *
 * @returns {Promise<void>}
 */
async function runDigest() {
  const startTime = Date.now();
  logger.info("=== Starting Daily Reddit Digest ===");

  try {
    // Step 1: Fetch posts
    logger.info("Step 1/3: Fetching Reddit posts...");
    const postsBySubreddit = await fetchAllSubreddits();

    const totalPosts = Object.values(postsBySubreddit).reduce(
      (sum, posts) => sum + posts.length,
      0
    );

    if (totalPosts === 0) {
      const msg = "No posts fetched today. Check subreddit config and Reddit availability.";
      logger.warn(msg);
      await sendNotification(`[Reddit Digest] ${msg}`);
      return;
    }

    // Step 2: Summarize with Claude
    logger.info("Step 2/3: Summarizing with Claude...");
    const digest = await summarizePosts(postsBySubreddit);

    // Step 3: Send via Telegram
    logger.info("Step 3/3: Sending via Telegram...");
    await sendDigest(digest);

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    logger.info(`=== Digest complete in ${elapsed}s ===`, {
      totalPosts,
      subreddits: Object.keys(postsBySubreddit).length,
      elapsedSeconds: elapsed,
    });
  } catch (error) {
    logger.error(`Digest pipeline failed: ${error.message}`, {
      stack: error.stack,
    });

    // Try to notify about the error via Telegram
    try {
      await sendNotification(
        `[Reddit Digest Error]\n${error.message}\nCheck logs for details.`
      );
    } catch (notifyError) {
      logger.error(
        `Could not send error notification: ${notifyError.message}`
      );
    }
  }
}

/**
 * Start the scheduler. Also runs once immediately if --run-once flag is used.
 */
function main() {
  const args = process.argv.slice(2);
  const runOnce = args.includes("--run-once");

  // Print configuration summary
  logger.info("Daily Reddit Digest - Configuration", {
    subreddits: config.reddit.subreddits,
    sort: config.reddit.sort,
    timeFilter: config.reddit.timeFilter,
    postsPerSub: config.reddit.postsPerSub,
    model: config.anthropic.model,
    schedule: config.schedule.cron,
    timezone: config.schedule.timezone,
  });

  if (runOnce) {
    // Run once and exit
    logger.info("Running in one-shot mode (--run-once)");
    runDigest().then(() => {
      logger.info("One-shot run complete. Exiting.");
      process.exit(0);
    });
    return;
  }

  // Validate cron expression
  if (!cron.validate(config.schedule.cron)) {
    logger.error(`Invalid cron expression: ${config.schedule.cron}`);
    process.exit(1);
  }

  // Schedule the recurring task
  logger.info(
    `Scheduling digest: "${config.schedule.cron}" (${config.schedule.timezone})`
  );

  cron.schedule(
    config.schedule.cron,
    () => {
      logger.info("Cron trigger fired");
      runDigest();
    },
    {
      timezone: config.schedule.timezone,
    }
  );

  logger.info("Scheduler started. Waiting for next trigger...");
  logger.info(
    `Next run will be at the time specified by cron: ${config.schedule.cron}`
  );

  // Graceful shutdown
  process.on("SIGINT", () => {
    logger.info("Received SIGINT. Shutting down gracefully...");
    process.exit(0);
  });

  process.on("SIGTERM", () => {
    logger.info("Received SIGTERM. Shutting down gracefully...");
    process.exit(0);
  });
}

// Export for testing
export { runDigest };

// Run
main();
```

---

## 6. 排程設定 Scheduling Setup

### 6.1 方式一：使用內建 node-cron（推薦）

最簡單的方式。直接啟動程式，它會根據 `.env` 中的 `CRON_SCHEDULE` 自動排程：

```bash
# 啟動排程（會持續執行）
npm start

# 或使用 node 直接執行
node src/index.js
```

搭配 `pm2` 確保程序不中斷：

```bash
# 安裝 pm2
npm install -g pm2

# 啟動並設為守護程序
pm2 start src/index.js --name reddit-digest

# 查看狀態
pm2 status

# 查看日誌
pm2 logs reddit-digest

# 設為開機自動啟動
pm2 startup
pm2 save
```

### 6.2 方式二：使用系統 cron + --run-once

如果不想讓 Node.js 程序一直跑，可以用系統 cron 觸發：

```bash
# 編輯 crontab
crontab -e

# 加入以下行（每天早上 8 點執行）
0 8 * * * cd /path/to/daily-reddit-digest && /usr/local/bin/node src/index.js --run-once >> logs/cron.log 2>&1
```

> 注意：使用系統 cron 時，要寫 `node` 的絕對路徑，因為 cron 的 PATH 環境變數與你的 shell 不同。
> 用 `which node` 確認你的 node 路徑。

### 6.3 方式三：搭配 Docker

```dockerfile
# Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "src/index.js"]
```

```bash
# 建置 & 執行
docker build -t reddit-digest .
docker run -d --name reddit-digest --env-file .env --restart unless-stopped reddit-digest
```

### Cron 表達式速查

| 表達式 | 說明 |
|--------|------|
| `0 8 * * *` | 每天早上 8:00 |
| `0 8,20 * * *` | 每天 8:00 和 20:00 |
| `0 */6 * * *` | 每 6 小時 |
| `0 8 * * 1-5` | 週一到週五的 8:00 |
| `30 7 * * *` | 每天 7:30 |

---

## 7. 測試步驟 Testing Steps

### 7.1 初始設定

```bash
# 1. 建立專案
mkdir daily-reddit-digest && cd daily-reddit-digest

# 2. 初始化
npm init -y

# 3. 安裝套件
npm install @anthropic-ai/sdk@^0.39.0 node-telegram-bot-api@^0.66.0 node-cron@^3.0.3 dotenv@^16.4.7 winston@^3.17.0

# 4. 建立目錄結構
mkdir -p src logs

# 5. 複製 .env.example 為 .env 並填入你的 API Keys
cp .env.example .env
# 編輯 .env，填入 ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
```

記得在 `package.json` 加入 `"type": "module"` 以啟用 ES Modules：

```bash
# 手動加入或用 npm pkg set
npm pkg set type="module"
```

### 7.2 逐步元件測試

**測試 1：Reddit 抓取**

```bash
node src/redditFetcher.js
```

預期輸出：
```
=== Reddit Fetcher Self-Test ===

[2026-03-04 08:00:00] info: Fetching r/programming ...
[2026-03-04 08:00:01] info: Fetched 5 posts from r/programming

--- r/programming (5 posts) ---
  [2500] Why Rust is taking over systems programming (342 comments)
    https://www.reddit.com/r/programming/comments/...
  ...

=== Self-Test Complete ===
```

如果看到 `429 Too Many Requests`，增加 `.env` 中的 `REDDIT_RATE_LIMIT_MS` 或等幾分鐘再試。

**測試 2：AI 摘要**

```bash
node src/aiSummarizer.js
```

這會使用 mock 資料測試 Claude API 連接。預期看到繁體中文的摘要輸出。

**測試 3：Telegram 發送**

```bash
node src/telegramSender.js
```

你的 Telegram 應該會收到一則測試訊息。如果沒有：
- 確認你有先對 Bot 按 `/start`
- 確認 `TELEGRAM_CHAT_ID` 正確
- 確認 `TELEGRAM_BOT_TOKEN` 正確

**測試 4：完整流程**

```bash
npm run run-once
# 或
node src/index.js --run-once
```

這會執行完整的 抓取 -> 摘要 -> 發送 流程，完成後自動退出。

### 7.3 快速驗證清單

| 測試項目 | 指令 | 預期結果 |
|----------|------|----------|
| Reddit .json API | `curl -s "https://www.reddit.com/r/programming/hot.json?limit=1" -H "User-Agent: Test/1.0"` | 回傳 JSON 資料 |
| Reddit 模組 | `node src/redditFetcher.js` | 列出各 subreddit 的貼文 |
| Claude API | `node src/aiSummarizer.js` | 輸出繁體中文摘要 |
| Telegram | `node src/telegramSender.js` | Telegram 收到測試訊息 |
| 完整流程 | `node src/index.js --run-once` | Telegram 收到完整摘要 |
| 排程啟動 | `npm start` | 顯示排程已啟動，等待觸發 |

---

## 8. 常見陷阱 Common Pitfalls

### 8.1 Reddit 相關

**問題：429 Too Many Requests**
```
Error: Rate limited by Reddit (429)
```
- 原因：請求太頻繁。Reddit 的 .json 端點對未認證請求有嚴格的 rate limit（約 10 次/分鐘）
- 解法：增加 `rateLimitMs` 到 3000-5000ms；減少監控的 subreddit 數量；減少 `postsPerSub`

**問題：403 Forbidden**
```
Error: Subreddit r/xxx is private or quarantined (403)
```
- 原因：該 subreddit 設為私密或被隔離
- 解法：從監控清單中移除該 subreddit

**問題：JSON 解析錯誤**
```
SyntaxError: Unexpected token < in JSON
```
- 原因：Reddit 回傳了 HTML 頁面而非 JSON（通常是因為缺少 User-Agent）
- 解法：確認 `User-Agent` header 已正確設定且非空字串

**問題：selftext 中的特殊字元導致 Telegram Markdown 解析失敗**
- 原因：Reddit 貼文可能包含 `*`、`_`、`` ` `` 等 Markdown 特殊字元
- 解法：程式已內建 fallback 機制，會自動以純文字重試

### 8.2 Claude API 相關

**問題：401 Unauthorized**
- 原因：API Key 無效或過期
- 解法：到 Anthropic Console 重新產生 API Key

**問題：Token 超限**
- 原因：送進去的 Reddit 貼文太長，超過模型的 context window
- 解法：減少 `postsPerSub`；`selftextTruncated` 已在程式中限制 1500 字元，可以進一步降低

**問題：摘要品質不佳**
- 解法：調整 `buildPrompt()` 中的 prompt；嘗試不同的 Claude 模型（claude-sonnet-4-20250514 性價比最高）

### 8.3 Telegram 相關

**問題：chat not found**
```
Error: ETELEGRAM: 400 Bad Request: chat not found
```
- 原因：Bot 尚未與使用者建立對話
- 解法：在 Telegram 找到你的 Bot，發送 `/start`

**問題：訊息被截斷**
- 原因：Telegram 單則訊息上限 4096 字元
- 解法：程式已內建 `splitMessage()` 自動分割

**問題：群組中 Bot 沒反應**
- 原因：Bot 可能沒有在群組中的發送權限
- 解法：在群組設定中確認 Bot 有權發送訊息；確認 `TELEGRAM_CHAT_ID` 是群組的 ID（負數）

### 8.4 Node.js 環境相關

**問題：SyntaxError: Cannot use import statement outside a module**
- 原因：`package.json` 中沒有設定 `"type": "module"`
- 解法：確認 `package.json` 包含 `"type": "module"`

**問題：fetch is not defined**
- 原因：Node.js 版本低於 18
- 解法：升級到 Node.js 18 以上，或安裝 `node-fetch` 套件

### 8.5 排程相關

**問題：程序在 SSH 斷線後停止**
- 原因：程序與 SSH session 綁定
- 解法：使用 `pm2`、`screen`、`tmux` 或 Docker

**問題：時區不對，排程在錯誤時間觸發**
- 原因：系統時區與預期不同
- 解法：在 `.env` 中明確設定 `CRON_TIMEZONE=Asia/Taipei`

---

## 9. 進階擴充 Advanced Extensions

### 9.1 新增更多 Subreddit

只需要修改 `.env`：

```bash
SUBREDDITS=programming,ClaudeAI,LocalLLaMA,artificial,MachineLearning,webdev,node,typescript
```

### 9.2 依 Subreddit 分別設定排序方式

可以擴充 config 支援 per-subreddit 設定：

```bash
# .env
SUBREDDIT_CONFIG=programming:hot:5,ClaudeAI:top:day:10,LocalLLaMA:rising:3
```

### 9.3 加入留言摘要

Reddit .json API 也支援取得留言：

```
https://www.reddit.com/r/ClaudeAI/comments/{post_id}.json
```

在 `redditFetcher.js` 新增一個函式抓取頂部留言，並在送給 Claude 時附上。

### 9.4 歷史記錄與比較

將每日結果存到本地 JSON 檔：

```javascript
// Save daily results
import fs from "fs";
const today = new Date().toISOString().split("T")[0];
fs.writeFileSync(
  `logs/digest-${today}.json`,
  JSON.stringify(postsBySubreddit, null, 2)
);
```

### 9.5 加入 Email 發送

安裝 `nodemailer`，新增 `emailSender.js` 模組，與 `telegramSender.js` 並行發送。

### 9.6 多語系支援

在 `.env` 設定 `SUMMARY_LANGUAGE=en`，prompt 會自動切換為英文摘要。

---

## 附錄：一鍵初始化腳本

將以下內容存為 `setup.sh`，一鍵建立整個專案：

```bash
#!/bin/bash
set -e

PROJECT_NAME="daily-reddit-digest"
echo "Creating ${PROJECT_NAME}..."

mkdir -p "${PROJECT_NAME}/src" "${PROJECT_NAME}/logs"
cd "${PROJECT_NAME}"

# Initialize npm
npm init -y
npm pkg set type="module"
npm pkg set scripts.start="node src/index.js"
npm pkg set scripts.run-once="node src/index.js --run-once"
npm pkg set scripts.test:reddit="node src/redditFetcher.js"
npm pkg set scripts.test:summarize="node src/aiSummarizer.js"
npm pkg set scripts.test:telegram="node src/telegramSender.js"

# Install dependencies
npm install @anthropic-ai/sdk@^0.39.0 node-telegram-bot-api@^0.66.0 node-cron@^3.0.3 dotenv@^16.4.7 winston@^3.17.0

echo ""
echo "Setup complete!"
echo "Next steps:"
echo "  1. Copy .env.example to .env and fill in your API keys"
echo "  2. Create the source files in src/"
echo "  3. Run: npm run test:reddit"
echo "  4. Run: npm run run-once"
echo "  5. Run: npm start"
```

---

## 附錄：Reddit .json API 回傳結構參考

了解 Reddit .json API 回傳的資料結構，有助於擴充功能：

```jsonc
{
  "kind": "Listing",
  "data": {
    "after": "t3_abc123",     // Pagination cursor
    "dist": 5,                // Number of items
    "children": [
      {
        "kind": "t3",         // t3 = link/post
        "data": {
          "subreddit": "programming",
          "title": "Post title here",
          "author": "username",
          "score": 1234,              // Net upvotes
          "upvote_ratio": 0.92,       // 92% upvoted
          "num_comments": 342,
          "url": "https://...",       // External link or self post URL
          "permalink": "/r/programming/comments/abc123/...",
          "selftext": "Post body for self posts...",
          "is_self": true,            // true = text post, false = link post
          "created_utc": 1709510400,  // Unix timestamp
          "thumbnail": "https://...",
          "link_flair_text": "Discussion",
          "over_18": false,           // NSFW flag
          "stickied": false,          // Pinned post
          "is_video": false,
          "domain": "self.programming"
        }
      }
      // ... more posts
    ]
  }
}
```

---

## 總結

| 項目 | 細節 |
|------|------|
| **技術棧** | Node.js 18+ / ES Modules |
| **Reddit 存取** | 公開 .json 端點（免註冊、免 OAuth） |
| **AI 摘要** | Claude claude-sonnet-4-20250514 via Anthropic SDK |
| **推送管道** | Telegram Bot API |
| **排程** | node-cron（內建）或系統 cron |
| **預估月費** | Claude API ~$0.01-$0.05 USD（每日一次） |
| **設定時間** | 約 15-30 分鐘（含 Telegram Bot 建立） |
| **程式碼量** | 約 500 行（含註解與測試） |

這個方案的最大優勢在於**零 Reddit 認證門檻** -- 不需要註冊 Reddit App、不需要 OAuth token、不需要處理 token refresh。只要 Reddit 的公開 `.json` 端點還在，就能持續使用。非常適合個人專案和快速原型開發。
