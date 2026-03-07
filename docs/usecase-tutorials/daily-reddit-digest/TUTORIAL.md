# 每日 Reddit 摘要 (Daily Reddit Digest) - 完整實作教學

> **方案**: Python + PRAW + Claude API + Telegram Bot
> **難度**: 初中級
> **預估時間**: 30-45 分鐘
> **最後更新**: 2026-03

---

## 目錄

1. [方案總覽](#1-方案總覽)
2. [所需套件](#2-所需套件-pip-install)
3. [前置作業](#3-前置作業)
4. [專案結構](#4-專案結構)
5. [完整程式碼](#5-完整程式碼)
6. [Cron 排程設定](#6-cron-排程設定)
7. [測試步驟](#7-測試步驟)
8. [常見陷阱與排錯](#8-常見陷阱與排錯)
9. [進階擴充](#9-進階擴充)

---

## 1. 方案總覽

### 這個專案做什麼？

每天自動從你關注的 Reddit 子版 (subreddits) 抓取當日熱門貼文，透過 Claude AI 產生一份結構化的繁體中文摘要報告，然後傳送到你的 Telegram 聊天室。整個流程由 cron 排程自動執行，你只需要在 Telegram 上閱讀就好。

### 架構流程

```
[Cron 定時觸發]
       |
       v
[reddit_fetcher.py]  -- PRAW --> Reddit API
       |                         (抓取各 subreddit 熱門貼文)
       v
[ai_summarizer.py]   -- anthropic SDK --> Claude API
       |                                  (AI 生成繁中摘要)
       v
[telegram_sender.py] -- HTTP API --> Telegram Bot
       |                             (傳送到你的聊天室)
       v
[output/]            -- 本地 .md 備份歸檔
```

### 技術選型理由

| 元件 | 選擇 | 原因 |
|------|------|------|
| Reddit 存取 | PRAW | Python 官方 Reddit API wrapper，穩定、文件完整、支援 read-only 模式 |
| AI 摘要 | Anthropic Claude | 擅長長文理解與多語言摘要，繁中輸出品質高 |
| 訊息推送 | Telegram Bot HTTP API | 免費、無訊息數限制、支援 Markdown、設定簡單 |
| 排程 | System cron | 最輕量的排程方案，不需要額外服務 |
| 設定管理 | python-dotenv | 用 `.env` 檔管理敏感資訊，避免硬編碼 |

---

## 2. 所需套件 (pip install)

### requirements.txt

```
praw==7.8.1
anthropic==0.43.0
python-telegram-bot==21.9
python-dotenv==1.0.1
pytz==2024.2
requests==2.32.3
```

### 各套件說明

| 套件 | 版本 | 用途 |
|------|------|------|
| `praw` | 7.8.1 | Python Reddit API Wrapper - 存取 Reddit 資料 |
| `anthropic` | 0.43.0 | Anthropic 官方 Python SDK - 呼叫 Claude API |
| `python-telegram-bot` | 21.9 | Telegram Bot 開發框架（本專案主要用其依賴的 httpx） |
| `python-dotenv` | 1.0.1 | 從 .env 檔載入環境變數 |
| `pytz` | 2024.2 | 時區處理 |
| `requests` | 2.32.3 | HTTP 請求（用於 Telegram Bot API 呼叫） |

### 安裝指令

```bash
# 建議使用 virtual environment
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## 3. 前置作業

### 3.1 Reddit API 憑證申請（step by step）

Reddit API 使用 OAuth2，你需要建立一個「script」類型的應用程式。

**步驟 1：登入 Reddit**

前往 https://www.reddit.com 登入你的帳號。如果沒有帳號，先註冊一個。

**步驟 2：建立 Reddit App**

1. 前往 https://www.reddit.com/prefs/apps/
2. 滾動到頁面底部，點擊 **"are you a developer? create an app..."**
3. 填寫表單：
   - **name**: `DailyRedditDigest`（隨意取名）
   - **App type**: 選擇 **script**（這很重要！）
   - **description**: `Daily digest bot`（選填）
   - **about url**: 留空
   - **redirect uri**: 填 `http://localhost:8080`（script 類型不會真的用到，但欄位必填）
4. 點擊 **"create app"**

**步驟 3：取得憑證**

建立完成後你會看到：

```
DailyRedditDigest
personal use script
--> 這裡顯示的就是 client_id（大約 14 個字元）

secret: 這裡顯示的就是 client_secret
```

- `client_id`：app 名稱下方那串短字串
- `client_secret`：標示為 `secret` 的字串

**步驟 4：記下你的 User Agent**

Reddit 要求每個 API 用戶提供唯一的 User-Agent。格式建議：

```
DailyRedditDigest/1.0 (by u/你的Reddit用戶名)
```

> **注意**：Reddit API 的 rate limit 是每分鐘 60 個請求。PRAW 會自動處理限速，但如果監控大量 subreddits，請注意不要超過。

---

### 3.2 Telegram Bot 建立（step by step）

**步驟 1：建立 Bot**

1. 在 Telegram 中搜尋 `@BotFather` 並開啟對話
2. 傳送 `/newbot`
3. 依照指示輸入：
   - Bot 名稱（顯示名稱）：`My Reddit Digest`
   - Bot username（必須以 `bot` 結尾）：`my_reddit_digest_bot`
4. BotFather 會回覆你一個 **Bot Token**，格式如：
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
5. 記下這個 Token

**步驟 2：取得你的 Chat ID**

1. 在 Telegram 中找到你剛建立的 bot 並 **傳送任意訊息**（例如 "hello"）
2. 在瀏覽器中開啟以下網址（將 `<TOKEN>` 替換為你的 Bot Token）：
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. 你會看到 JSON 回應，找到 `"chat":{"id":` 後面的數字，那就是你的 **Chat ID**

例如：
```json
{
  "ok": true,
  "result": [{
    "message": {
      "chat": {
        "id": 123456789,
        "type": "private"
      }
    }
  }]
}
```

這裡的 `123456789` 就是你的 Chat ID。

> **提示**：如果想傳送到群組，將 bot 加入群組後，對群組傳一則訊息，再用同樣方法查 getUpdates。群組的 chat_id 通常是負數。

**步驟 3（選用）：設定 Bot 描述**

```
/setdescription - 設定 bot 描述
/setabouttext   - 設定 bot 簡介
/setuserpic     - 設定 bot 頭像
```

---

### 3.3 Anthropic Claude API Key

1. 前往 https://console.anthropic.com/
2. 註冊 / 登入帳號
3. 前往 **Settings > API Keys**（https://console.anthropic.com/settings/keys）
4. 點擊 **Create Key**
5. 記下 API Key（格式：`sk-ant-api03-...`）

> **成本估算**：使用 `claude-sonnet-4-20250514` 模型，每次摘要約消耗 2,000-5,000 input tokens + 1,000-2,000 output tokens。以每日一次計算，每月成本約 USD $0.50-2.00。

---

## 4. 專案結構

```
daily-reddit-digest/
├── .env                          # 環境變數（不要提交到 git！）
├── .env.example                  # 環境變數範本
├── requirements.txt              # Python 套件清單
├── run_digest.py                 # 入口腳本（cron 呼叫這個）
├── test_components.py            # 元件測試腳本
├── daily_reddit_digest/          # 主程式套件
│   ├── __init__.py
│   ├── config.py                 # 設定管理
│   ├── reddit_fetcher.py         # Reddit 貼文抓取
│   ├── ai_summarizer.py          # Claude AI 摘要產生
│   ├── telegram_sender.py        # Telegram 訊息發送
│   └── main.py                   # 主流程編排
└── output/                       # 摘要歸檔（自動建立）
    └── reddit_digest_2026-03-04.md
```

每個檔案的職責清楚分離：

| 檔案 | 職責 |
|------|------|
| `config.py` | 從 `.env` 載入所有設定，提供驗證方法 |
| `reddit_fetcher.py` | 用 PRAW 連接 Reddit，抓取指定 subreddit 的熱門貼文與留言 |
| `ai_summarizer.py` | 將貼文資料組成 prompt，呼叫 Claude API 產生摘要 |
| `telegram_sender.py` | 透過 Telegram Bot API 發送訊息，處理長訊息分割 |
| `main.py` | 編排整體流程：抓取 -> 摘要 -> 儲存 -> 發送 |

---

## 5. 完整程式碼

### 5.1 `daily_reddit_digest/__init__.py`

```python
"""Daily Reddit Digest - Automated Reddit summary delivered via Telegram."""

__version__ = "1.0.0"
```

---

### 5.2 `daily_reddit_digest/config.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for Daily Reddit Digest.
Loads settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


@dataclass
class RedditConfig:
    """Reddit API credentials and fetch settings."""

    client_id: str = ""
    client_secret: str = ""
    user_agent: str = "DailyRedditDigest/1.0"
    # Subreddits to monitor (comma-separated in env)
    subreddits: List[str] = field(default_factory=list)
    # Number of top posts to fetch per subreddit
    post_limit: int = 10
    # Time filter: "day", "week", "month", "year", "all"
    time_filter: str = "day"

    def __post_init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID", "")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
        self.user_agent = os.getenv(
            "REDDIT_USER_AGENT", "DailyRedditDigest/1.0 (by u/your_username)"
        )
        subreddits_str = os.getenv(
            "REDDIT_SUBREDDITS", "python,MachineLearning,LocalLLaMA"
        )
        self.subreddits = [
            s.strip() for s in subreddits_str.split(",") if s.strip()
        ]
        self.post_limit = int(os.getenv("REDDIT_POST_LIMIT", "10"))
        self.time_filter = os.getenv("REDDIT_TIME_FILTER", "day")

    def validate(self) -> bool:
        """Check that required credentials are present."""
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set. "
                "Create an app at https://www.reddit.com/prefs/apps/"
            )
        if not self.subreddits:
            raise ValueError(
                "REDDIT_SUBREDDITS must contain at least one subreddit."
            )
        return True


@dataclass
class ClaudeConfig:
    """Anthropic Claude API settings."""

    api_key: str = ""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096

    def __post_init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
        self.max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))

    def validate(self) -> bool:
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY must be set. "
                "Get your key at https://console.anthropic.com/settings/keys"
            )
        return True


@dataclass
class TelegramConfig:
    """Telegram Bot settings."""

    bot_token: str = ""
    chat_id: str = ""

    def __post_init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    def validate(self) -> bool:
        if not self.bot_token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN must be set. "
                "Create a bot via @BotFather on Telegram."
            )
        if not self.chat_id:
            raise ValueError(
                "TELEGRAM_CHAT_ID must be set. "
                "Send a message to your bot, then visit "
                "https://api.telegram.org/bot<TOKEN>/getUpdates "
                "to find your chat_id."
            )
        return True


@dataclass
class AppConfig:
    """Top-level application configuration."""

    reddit: RedditConfig = field(default_factory=RedditConfig)
    claude: ClaudeConfig = field(default_factory=ClaudeConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    # Timezone for display in digest (IANA format)
    timezone: str = "Asia/Taipei"
    # Language for the summary output
    summary_language: str = "Traditional Chinese"
    # Log level
    log_level: str = "INFO"
    # Output directory for local digest archive
    output_dir: str = ""

    def __post_init__(self):
        self.timezone = os.getenv("DIGEST_TIMEZONE", "Asia/Taipei")
        self.summary_language = os.getenv(
            "DIGEST_LANGUAGE", "Traditional Chinese"
        )
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.output_dir = os.getenv(
            "DIGEST_OUTPUT_DIR",
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "output"
            ),
        )

    def validate_all(self) -> bool:
        """Validate all sub-configs. Raises ValueError on failure."""
        self.reddit.validate()
        self.claude.validate()
        self.telegram.validate()
        return True


def load_config() -> AppConfig:
    """Create and return the application config. Does NOT validate yet."""
    return AppConfig()
```

**設計重點**：

- 使用 `dataclass` 讓設定結構清楚，IDE 有完整的型別提示
- `validate()` 方法在正式執行前才呼叫，方便測試時只驗證部分元件
- 所有敏感資訊都從環境變數讀取，不會硬編碼在程式中

---

### 5.3 `daily_reddit_digest/reddit_fetcher.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit post fetcher using PRAW (Python Reddit API Wrapper).
Fetches top posts from configured subreddits and extracts
structured data for downstream summarization.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

import praw
from praw.models import Submission

from .config import RedditConfig

logger = logging.getLogger(__name__)


@dataclass
class RedditPost:
    """Structured representation of a single Reddit post."""

    id: str
    title: str
    subreddit: str
    author: str
    url: str
    permalink: str
    score: int
    upvote_ratio: float
    num_comments: int
    selftext: str
    created_utc: float
    is_self: bool
    link_flair_text: Optional[str] = None
    top_comments: List[str] = field(default_factory=list)

    @property
    def created_dt(self) -> datetime:
        return datetime.fromtimestamp(self.created_utc, tz=timezone.utc)

    @property
    def display_url(self) -> str:
        return f"https://reddit.com{self.permalink}"

    def to_summary_text(self) -> str:
        """Format post data as plain text for the AI summarizer."""
        lines = [
            f"Title: {self.title}",
            f"Subreddit: r/{self.subreddit}",
            f"Score: {self.score} (upvote ratio: {self.upvote_ratio:.0%})",
            f"Comments: {self.num_comments}",
            f"Author: u/{self.author}",
            f"URL: {self.display_url}",
        ]
        if self.link_flair_text:
            lines.append(f"Flair: {self.link_flair_text}")
        if self.selftext:
            # Truncate very long self-posts to stay within token limits
            text = self.selftext[:2000]
            if len(self.selftext) > 2000:
                text += "\n... [truncated]"
            lines.append(f"Content:\n{text}")
        if self.top_comments:
            lines.append("Top comments:")
            for i, comment in enumerate(self.top_comments, 1):
                lines.append(f"  {i}. {comment}")
        return "\n".join(lines)


class RedditFetcher:
    """Fetches top posts from Reddit using PRAW."""

    def __init__(self, config: RedditConfig):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
            # Read-only mode: no username/password needed
        )
        # Confirm read-only mode
        logger.info(
            "Reddit client initialized (read-only mode: %s)",
            self.reddit.read_only,
        )

    def _extract_top_comments(
        self, submission: Submission, limit: int = 3
    ) -> List[str]:
        """Extract the top-level comments sorted by score."""
        try:
            submission.comment_sort = "best"
            # Replace MoreComments objects to avoid extra API calls
            submission.comments.replace_more(limit=0)
            comments = []
            for comment in submission.comments[:limit]:
                body = comment.body.strip()
                if len(body) > 300:
                    body = body[:300] + "..."
                comments.append(body)
            return comments
        except Exception as e:
            logger.warning(
                "Failed to fetch comments for %s: %s", submission.id, e
            )
            return []

    def fetch_subreddit(self, subreddit_name: str) -> List[RedditPost]:
        """Fetch top posts from a single subreddit."""
        logger.info(
            "Fetching top %d posts from r/%s (time_filter=%s)",
            self.config.post_limit,
            subreddit_name,
            self.config.time_filter,
        )
        posts = []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            for submission in subreddit.top(
                time_filter=self.config.time_filter,
                limit=self.config.post_limit,
            ):
                top_comments = self._extract_top_comments(submission)
                post = RedditPost(
                    id=submission.id,
                    title=submission.title,
                    subreddit=subreddit_name,
                    author=(
                        str(submission.author)
                        if submission.author
                        else "[deleted]"
                    ),
                    url=submission.url,
                    permalink=submission.permalink,
                    score=submission.score,
                    upvote_ratio=submission.upvote_ratio,
                    num_comments=submission.num_comments,
                    selftext=submission.selftext or "",
                    created_utc=submission.created_utc,
                    is_self=submission.is_self,
                    link_flair_text=submission.link_flair_text,
                    top_comments=top_comments,
                )
                posts.append(post)
            logger.info(
                "Fetched %d posts from r/%s", len(posts), subreddit_name
            )
        except Exception as e:
            logger.error("Error fetching r/%s: %s", subreddit_name, e)
        return posts

    def fetch_all(self) -> dict[str, List[RedditPost]]:
        """
        Fetch top posts from all configured subreddits.
        Returns a dict mapping subreddit name -> list of RedditPost.
        """
        results: dict[str, List[RedditPost]] = {}
        for sub in self.config.subreddits:
            posts = self.fetch_subreddit(sub)
            if posts:
                results[sub] = posts
        total = sum(len(v) for v in results.values())
        logger.info(
            "Total fetched: %d posts from %d subreddits",
            total,
            len(results),
        )
        return results
```

**設計重點**：

- `RedditPost` dataclass 將 Reddit API 的原始資料結構化，方便後續處理
- `to_summary_text()` 方法將貼文轉成適合送進 AI prompt 的純文字格式
- `_extract_top_comments()` 抓取前 3 則留言以提供討論脈絡
- 使用 read-only 模式：只需要 `client_id` 和 `client_secret`，不需要帳號密碼
- 錯誤處理：單一 subreddit 失敗不會影響其他 subreddit 的抓取

---

### 5.4 `daily_reddit_digest/ai_summarizer.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI summarizer using Anthropic Claude API.
Takes structured Reddit post data and produces
a well-organized daily digest summary.
"""

import logging
from typing import List

import anthropic

from .config import ClaudeConfig, AppConfig
from .reddit_fetcher import RedditPost

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a professional content curator who creates \
daily Reddit digest reports.
Your task is to analyze Reddit posts and produce a well-structured, \
insightful summary.

Rules:
1. Write the summary in {language}.
2. Group posts by subreddit.
3. For each subreddit section, highlight the most interesting/impactful \
posts.
4. Include key discussion points from the comments when available.
5. Add a brief "Trends & Insights" section at the end.
6. Use clear formatting with headers, bullet points, and separators.
7. Keep the tone informative yet engaging.
8. Include the post score and comment count for context.
9. If a post links to an external URL (not a self-post), mention that.
10. Keep the total summary concise - aim for readability, not \
exhaustiveness."""


USER_PROMPT_TEMPLATE = """Here are today's top Reddit posts from the \
subreddits I follow.
Please create a daily digest summary.

Date: {date}
Timezone: {timezone}

---

{posts_text}

---

Please produce the daily digest now. Remember to write in {language}."""


class AISummarizer:
    """Generates AI-powered summaries of Reddit posts using Claude."""

    def __init__(
        self, claude_config: ClaudeConfig, app_config: AppConfig
    ):
        self.config = claude_config
        self.app_config = app_config
        self.client = anthropic.Anthropic(api_key=claude_config.api_key)
        logger.info(
            "Claude client initialized (model: %s)", claude_config.model
        )

    def _build_posts_text(
        self, posts_by_sub: dict[str, List[RedditPost]]
    ) -> str:
        """Convert structured post data into a text block for the prompt."""
        sections = []
        for subreddit, posts in posts_by_sub.items():
            section_lines = [
                f"=== r/{subreddit} ({len(posts)} posts) ===\n"
            ]
            for i, post in enumerate(posts, 1):
                section_lines.append(f"--- Post {i} ---")
                section_lines.append(post.to_summary_text())
                section_lines.append("")
            sections.append("\n".join(section_lines))
        return "\n\n".join(sections)

    def summarize(
        self,
        posts_by_sub: dict[str, List[RedditPost]],
        date_str: str,
    ) -> str:
        """
        Send posts to Claude and return the generated digest summary.

        Args:
            posts_by_sub: Dict mapping subreddit name -> list of RedditPost
            date_str: Human-readable date string for the digest header.

        Returns:
            The generated summary text (Markdown formatted).
        """
        posts_text = self._build_posts_text(posts_by_sub)

        # Calculate approximate token count
        approx_tokens = len(posts_text) // 4
        logger.info(
            "Sending %d characters (~%d tokens) to Claude",
            len(posts_text),
            approx_tokens,
        )

        system_prompt = SYSTEM_PROMPT.format(
            language=self.app_config.summary_language
        )
        user_prompt = USER_PROMPT_TEMPLATE.format(
            date=date_str,
            timezone=self.app_config.timezone,
            posts_text=posts_text,
            language=self.app_config.summary_language,
        )

        try:
            message = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            # Extract text from response
            summary = ""
            for block in message.content:
                if block.type == "text":
                    summary += block.text

            logger.info(
                "Summary generated: %d chars, usage: input=%d output=%d",
                len(summary),
                message.usage.input_tokens,
                message.usage.output_tokens,
            )
            return summary

        except anthropic.BadRequestError as e:
            logger.error("Claude API bad request: %s", e)
            raise
        except anthropic.AuthenticationError as e:
            logger.error(
                "Claude API auth error - check ANTHROPIC_API_KEY: %s", e
            )
            raise
        except anthropic.RateLimitError as e:
            logger.warning("Claude API rate limited: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error calling Claude API: %s", e)
            raise
```

**設計重點**：

- System prompt 指導 Claude 的輸出風格、語言和結構
- 將貼文資料轉成結構化純文字，避免浪費 tokens 在 JSON 語法上
- 區分不同的 API 錯誤類型（認證、限速、請求格式），方便排錯
- 記錄 token 使用量以便追蹤成本

---

### 5.5 `daily_reddit_digest/telegram_sender.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram message sender for Daily Reddit Digest.
Sends the formatted digest to a Telegram chat via Bot API.
Handles message splitting for Telegram's 4096-char limit.
"""

import logging
from typing import List

import requests

from .config import TelegramConfig

logger = logging.getLogger(__name__)

# Telegram message character limit
TELEGRAM_MAX_LENGTH = 4096


class TelegramSender:
    """Sends messages to Telegram using the Bot HTTP API."""

    def __init__(self, config: TelegramConfig):
        self.config = config
        self.base_url = (
            f"https://api.telegram.org/bot{config.bot_token}"
        )
        logger.info(
            "Telegram sender initialized for chat_id: %s",
            config.chat_id,
        )

    def _split_message(self, text: str) -> List[str]:
        """
        Split a long message into chunks that fit Telegram's limit.
        Tries to split at paragraph boundaries for clean formatting.
        """
        if len(text) <= TELEGRAM_MAX_LENGTH:
            return [text]

        chunks = []
        remaining = text

        while remaining:
            if len(remaining) <= TELEGRAM_MAX_LENGTH:
                chunks.append(remaining)
                break

            # Try to find a good split point
            # (double newline = paragraph break)
            split_at = remaining.rfind(
                "\n\n", 0, TELEGRAM_MAX_LENGTH
            )
            if split_at == -1:
                # Fall back to single newline
                split_at = remaining.rfind(
                    "\n", 0, TELEGRAM_MAX_LENGTH
                )
            if split_at == -1:
                # Last resort: hard split at limit
                split_at = TELEGRAM_MAX_LENGTH

            chunks.append(remaining[:split_at])
            remaining = remaining[split_at:].lstrip("\n")

        logger.info("Message split into %d chunks", len(chunks))
        return chunks

    def send_message(
        self, text: str, parse_mode: str = "Markdown"
    ) -> bool:
        """
        Send a text message to the configured Telegram chat.
        Automatically splits long messages.

        Args:
            text: The message text to send.
            parse_mode: "Markdown" or "HTML". Default is Markdown.

        Returns:
            True if all chunks sent successfully, False otherwise.
        """
        chunks = self._split_message(text)
        all_ok = True

        for i, chunk in enumerate(chunks):
            # Add part indicator for multi-part messages
            if len(chunks) > 1:
                header = f"({i + 1}/{len(chunks)})\n\n"
                chunk = header + chunk

            success = self._send_single(chunk, parse_mode)
            if not success:
                all_ok = False
                # If Markdown fails, retry with plain text
                logger.warning(
                    "Retrying chunk %d/%d without parse_mode",
                    i + 1,
                    len(chunks),
                )
                success = self._send_single(chunk, parse_mode=None)
                if not success:
                    logger.error(
                        "Failed to send chunk %d/%d even as plain text",
                        i + 1,
                        len(chunks),
                    )

        return all_ok

    def _send_single(
        self, text: str, parse_mode: str = None
    ) -> bool:
        """Send a single message chunk via Telegram Bot API."""
        payload = {
            "chat_id": self.config.chat_id,
            "text": text,
            "disable_web_page_preview": True,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            resp = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=30,
            )
            data = resp.json()
            if data.get("ok"):
                logger.info("Telegram message sent successfully")
                return True
            else:
                logger.error(
                    "Telegram API error: %s (code: %s)",
                    data.get("description", "unknown"),
                    data.get("error_code", "?"),
                )
                return False
        except requests.Timeout:
            logger.error("Telegram API request timed out")
            return False
        except requests.RequestException as e:
            logger.error("Telegram API request failed: %s", e)
            return False

    def send_error_notification(self, error_msg: str) -> bool:
        """Send an error notification to the Telegram chat."""
        text = (
            f"[Daily Reddit Digest ERROR]\n\n{error_msg}"
        )
        return self._send_single(text)

    def test_connection(self) -> bool:
        """Test the bot token by calling getMe."""
        try:
            resp = requests.get(
                f"{self.base_url}/getMe", timeout=10
            )
            data = resp.json()
            if data.get("ok"):
                bot_name = data["result"].get(
                    "username", "unknown"
                )
                logger.info(
                    "Telegram bot connection OK: @%s", bot_name
                )
                return True
            else:
                logger.error(
                    "Telegram bot token invalid: %s",
                    data.get("description"),
                )
                return False
        except Exception as e:
            logger.error(
                "Telegram connection test failed: %s", e
            )
            return False
```

**設計重點**：

- Telegram 單則訊息上限 4096 字元，`_split_message()` 智慧分割，盡量在段落邊界切開
- Markdown 格式失敗時自動降級為純文字重送
- `test_connection()` 在正式發送前先驗證 Bot Token 是否有效
- `send_error_notification()` 讓你在任何元件出錯時也能收到通知

---

### 5.6 `daily_reddit_digest/main.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Reddit Digest - Main orchestrator.
Coordinates fetching, summarizing, and delivering the daily digest.
"""

import logging
import os
import sys
from datetime import datetime

import pytz

from .config import load_config
from .reddit_fetcher import RedditFetcher
from .ai_summarizer import AISummarizer
from .telegram_sender import TelegramSender

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configure logging format and level."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def save_digest_locally(
    digest: str, output_dir: str, date_str: str
) -> str:
    """Save the digest to a local markdown file for archival."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"reddit_digest_{date_str}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(digest)
    logger.info("Digest saved to %s", filepath)
    return filepath


def run() -> None:
    """Main entry point: fetch -> summarize -> deliver."""

    # --- 1. Load configuration ---
    config = load_config()
    setup_logging(config.log_level)

    logger.info("=" * 60)
    logger.info("Daily Reddit Digest - Starting")
    logger.info("=" * 60)

    # Validate all credentials before doing any work
    try:
        config.validate_all()
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        sys.exit(1)

    # Determine current date in configured timezone
    tz = pytz.timezone(config.timezone)
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")
    date_display = now.strftime("%Y-%m-%d (%A)")

    logger.info(
        "Digest date: %s (%s)", date_display, config.timezone
    )
    logger.info(
        "Subreddits: %s", ", ".join(config.reddit.subreddits)
    )

    # --- 2. Initialize components ---
    telegram = TelegramSender(config.telegram)

    # Quick connectivity check for Telegram
    if not telegram.test_connection():
        logger.error("Telegram bot connection failed. Aborting.")
        sys.exit(1)

    # --- 3. Fetch Reddit posts ---
    logger.info("--- Phase 1: Fetching Reddit posts ---")
    try:
        fetcher = RedditFetcher(config.reddit)
        posts_by_sub = fetcher.fetch_all()
    except Exception as e:
        error_msg = f"Reddit fetch failed: {e}"
        logger.error(error_msg)
        telegram.send_error_notification(error_msg)
        sys.exit(1)

    if not posts_by_sub:
        msg = (
            "No posts fetched from any subreddit. "
            "Nothing to summarize."
        )
        logger.warning(msg)
        telegram.send_message(
            f"[Daily Reddit Digest]\n\n{msg}"
        )
        sys.exit(0)

    total_posts = sum(len(v) for v in posts_by_sub.values())
    logger.info(
        "Fetched %d posts from %d subreddits",
        total_posts,
        len(posts_by_sub),
    )

    # --- 4. Summarize with Claude ---
    logger.info("--- Phase 2: AI Summarization ---")
    try:
        summarizer = AISummarizer(config.claude, config)
        digest = summarizer.summarize(posts_by_sub, date_display)
    except Exception as e:
        error_msg = f"AI summarization failed: {e}"
        logger.error(error_msg)
        telegram.send_error_notification(error_msg)
        sys.exit(1)

    if not digest:
        error_msg = "AI returned empty summary."
        logger.error(error_msg)
        telegram.send_error_notification(error_msg)
        sys.exit(1)

    # --- 5. Save locally ---
    logger.info("--- Phase 3: Saving digest ---")
    try:
        filepath = save_digest_locally(
            digest, config.output_dir, date_str
        )
    except Exception as e:
        logger.warning("Failed to save digest locally: %s", e)
        # Non-fatal: continue to send via Telegram

    # --- 6. Send via Telegram ---
    logger.info("--- Phase 4: Sending via Telegram ---")
    header = (
        f"Reddit Daily Digest - {date_display}\n"
        f"{'=' * 40}\n\n"
    )
    full_message = header + digest

    success = telegram.send_message(full_message)

    if success:
        logger.info(
            "Digest delivered successfully via Telegram!"
        )
    else:
        logger.error("Failed to deliver digest via Telegram.")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("Daily Reddit Digest - Complete")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()
```

**設計重點**：

- 四個階段清楚分離：抓取 -> 摘要 -> 儲存 -> 發送
- 每個階段都有獨立的錯誤處理，失敗時會透過 Telegram 通知你
- 本地儲存失敗不會阻止 Telegram 發送（降級容錯）
- 使用 `sys.exit()` 回傳適當的 exit code，方便 cron 判斷成功/失敗

---

### 5.7 `run_digest.py`（入口腳本）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point script for Daily Reddit Digest.
Run this file directly or via cron.

Usage:
    python run_digest.py
"""

from daily_reddit_digest.main import run

if __name__ == "__main__":
    run()
```

---

### 5.8 `test_components.py`（元件測試）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component-level tests for Daily Reddit Digest.
Run each test independently to verify setup.

Usage:
    python test_components.py --test config
    python test_components.py --test reddit
    python test_components.py --test claude
    python test_components.py --test telegram
    python test_components.py --test all
"""

import argparse
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("test")


def test_config():
    """Test that configuration loads and validates."""
    print("\n=== Testing Configuration ===\n")
    from daily_reddit_digest.config import load_config

    config = load_config()

    print(f"  Reddit Client ID: "
          f"{'***' + config.reddit.client_id[-4:] if config.reddit.client_id else 'NOT SET'}")
    print(f"  Reddit Subreddits: {config.reddit.subreddits}")
    print(f"  Claude Model: {config.claude.model}")
    print(f"  Claude API Key: "
          f"{'***' + config.claude.api_key[-4:] if config.claude.api_key else 'NOT SET'}")
    print(f"  Telegram Bot Token: "
          f"{'***' + config.telegram.bot_token[-4:] if config.telegram.bot_token else 'NOT SET'}")
    print(f"  Telegram Chat ID: {config.telegram.chat_id}")
    print(f"  Timezone: {config.timezone}")
    print(f"  Language: {config.summary_language}")

    try:
        config.validate_all()
        print("\n  [PASS] All configuration validated.")
        return True
    except ValueError as e:
        print(f"\n  [FAIL] Validation error: {e}")
        return False


def test_reddit():
    """Test Reddit API connection and fetching."""
    print("\n=== Testing Reddit Fetcher ===\n")
    from daily_reddit_digest.config import load_config
    from daily_reddit_digest.reddit_fetcher import RedditFetcher

    config = load_config()
    config.reddit.validate()

    fetcher = RedditFetcher(config.reddit)

    test_sub = config.reddit.subreddits[0]
    print(f"  Fetching top 3 posts from r/{test_sub}...")

    original_limit = config.reddit.post_limit
    config.reddit.post_limit = 3
    posts = fetcher.fetch_subreddit(test_sub)
    config.reddit.post_limit = original_limit

    if posts:
        print(f"  Fetched {len(posts)} posts:")
        for p in posts:
            print(f"    - [{p.score}] {p.title[:60]}...")
        print("\n  [PASS] Reddit fetcher working.")
        return True
    else:
        print(f"  No posts for today. Try time_filter=week.")
        print("  [WARN] May be normal for low-traffic subs.")
        return True


def test_claude():
    """Test Claude API connection with a simple request."""
    print("\n=== Testing Claude API ===\n")
    from daily_reddit_digest.config import load_config
    import anthropic

    config = load_config()
    config.claude.validate()

    client = anthropic.Anthropic(api_key=config.claude.api_key)

    print(f"  Model: {config.claude.model}")
    print("  Sending test message...")

    try:
        message = client.messages.create(
            model=config.claude.model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Say 'Connection successful' only."
            }],
        )
        response_text = message.content[0].text
        print(f"  Response: {response_text}")
        print(f"  Tokens: input={message.usage.input_tokens}, "
              f"output={message.usage.output_tokens}")
        print("\n  [PASS] Claude API working.")
        return True
    except Exception as e:
        print(f"\n  [FAIL] Claude API error: {e}")
        return False


def test_telegram():
    """Test Telegram bot connection and message sending."""
    print("\n=== Testing Telegram Sender ===\n")
    from daily_reddit_digest.config import load_config
    from daily_reddit_digest.telegram_sender import TelegramSender

    config = load_config()
    config.telegram.validate()

    sender = TelegramSender(config.telegram)

    print("  Testing bot connection...")
    if not sender.test_connection():
        print("\n  [FAIL] Bot token is invalid.")
        return False

    print("  Sending test message...")
    success = sender.send_message(
        "[Daily Reddit Digest]\n\n"
        "Test message - Telegram delivery is working!",
        parse_mode=None,
    )

    if success:
        print("\n  [PASS] Check your Telegram!")
        return True
    else:
        print("\n  [FAIL] Failed to send test message.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test Daily Reddit Digest components"
    )
    parser.add_argument(
        "--test",
        choices=["config", "reddit", "claude", "telegram", "all"],
        default="all",
        help="Which component to test (default: all)",
    )
    args = parser.parse_args()

    tests = {
        "config": test_config,
        "reddit": test_reddit,
        "claude": test_claude,
        "telegram": test_telegram,
    }

    if args.test == "all":
        results = {}
        for name, func in tests.items():
            try:
                results[name] = func()
            except Exception as e:
                print(f"\n  [FAIL] Unexpected error: {e}")
                results[name] = False

        print("\n" + "=" * 40)
        print("Test Summary:")
        for name, passed in results.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {name}: [{status}]")
        print("=" * 40)

        if not all(results.values()):
            sys.exit(1)
    else:
        try:
            success = tests[args.test]()
            if not success:
                sys.exit(1)
        except Exception as e:
            print(f"\n  [FAIL] Unexpected error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
```

---

### 5.9 `.env.example`

```bash
# ===========================================
# Daily Reddit Digest - Environment Variables
# ===========================================
# Copy this file to .env and fill in your values:
#   cp .env.example .env

# --- Reddit API ---
# Create at: https://www.reddit.com/prefs/apps/
# Choose "script" type application
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=DailyRedditDigest/1.0 (by u/your_username)

# --- Subreddits to monitor (comma-separated) ---
REDDIT_SUBREDDITS=python,MachineLearning,LocalLLaMA,ClaudeAI,singularity
REDDIT_POST_LIMIT=10
REDDIT_TIME_FILTER=day

# --- Anthropic Claude API ---
# Get key at: https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096

# --- Telegram Bot ---
# Create bot: talk to @BotFather on Telegram
# Get chat_id: send message to bot, then visit
#   https://api.telegram.org/bot<TOKEN>/getUpdates
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# --- App Settings ---
DIGEST_TIMEZONE=Asia/Taipei
DIGEST_LANGUAGE=Traditional Chinese
DIGEST_OUTPUT_DIR=./output
LOG_LEVEL=INFO
```

---

## 6. Cron 排程設定

### 6.1 基本設定

假設你的專案放在 `/home/user/daily-reddit-digest/`，使用虛擬環境 `venv/`。

**編輯 crontab：**

```bash
crontab -e
```

**新增以下排程（每天早上 8 點執行）：**

```cron
# Daily Reddit Digest - runs at 8:00 AM (server local time)
0 8 * * * cd /home/user/daily-reddit-digest && /home/user/daily-reddit-digest/venv/bin/python run_digest.py >> /home/user/daily-reddit-digest/cron.log 2>&1
```

### 6.2 Cron 表達式說明

```
分 時 日 月 週 指令
0  8  *  *  *  ...
|  |  |  |  |
|  |  |  |  +-- 星期幾 (0-7, 0 和 7 都是星期日)
|  |  |  +---- 月份 (1-12)
|  |  +------- 幾號 (1-31)
|  +---------- 幾點 (0-23)
+------------- 幾分 (0-59)
```

### 6.3 常用排程範例

```cron
# 每天早上 8 點（最常見）
0 8 * * * cd /home/user/daily-reddit-digest && ...

# 每天早上 8 點和晚上 8 點（一天兩次）
0 8,20 * * * cd /home/user/daily-reddit-digest && ...

# 每週一到五早上 9 點（只有工作日）
0 9 * * 1-5 cd /home/user/daily-reddit-digest && ...

# 每 6 小時一次
0 */6 * * * cd /home/user/daily-reddit-digest && ...
```

### 6.4 macOS 使用 launchd（替代 cron）

macOS 推薦使用 `launchd`。建立 plist 檔：

```bash
nano ~/Library/LaunchAgents/com.user.reddit-digest.plist
```

內容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.reddit-digest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/user/daily-reddit-digest/venv/bin/python</string>
        <string>/Users/user/daily-reddit-digest/run_digest.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/user/daily-reddit-digest</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/user/daily-reddit-digest/cron.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/user/daily-reddit-digest/cron_error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

載入排程：

```bash
launchctl load ~/Library/LaunchAgents/com.user.reddit-digest.plist
```

檢查狀態：

```bash
launchctl list | grep reddit-digest
```

### 6.5 Cron 環境注意事項

Cron 執行時的環境與你的 shell 不同，常見問題：

```bash
# 確保 .env 路徑正確（使用絕對路徑）
# 在 crontab 最上方加入：
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

# 或者在指令中明確指定環境
0 8 * * * cd /home/user/daily-reddit-digest && \
  /home/user/daily-reddit-digest/venv/bin/python \
  /home/user/daily-reddit-digest/run_digest.py \
  >> /home/user/daily-reddit-digest/cron.log 2>&1
```

---

## 7. 測試步驟

### 7.1 環境設定

```bash
# 1. 進入專案目錄
cd daily-reddit-digest

# 2. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 3. 安裝套件
pip install -r requirements.txt

# 4. 建立 .env
cp .env.example .env
# 用你的編輯器填入真實的 API key 和 token
```

### 7.2 逐一測試各元件

使用 `test_components.py` 腳本逐步驗證：

```bash
# Step 1：測試設定是否正確載入
python test_components.py --test config

# 預期輸出：
# === Testing Configuration ===
#   Reddit Client ID: ***xxxx
#   Reddit Subreddits: ['python', 'MachineLearning', ...]
#   Claude Model: claude-sonnet-4-20250514
#   Claude API Key: ***xxxx
#   Telegram Bot Token: ***xxxx
#   Telegram Chat ID: 123456789
#   [PASS] All configuration validated.
```

```bash
# Step 2：測試 Reddit API 連線
python test_components.py --test reddit

# 預期輸出：
# === Testing Reddit Fetcher ===
#   Fetching top 3 posts from r/python...
#   Fetched 3 posts:
#     - [1234] Some post title...
#     - [567] Another post...
#   [PASS] Reddit fetcher working.
```

```bash
# Step 3：測試 Claude API 連線
python test_components.py --test claude

# 預期輸出：
# === Testing Claude API ===
#   Model: claude-sonnet-4-20250514
#   Sending test message...
#   Response: Connection successful
#   Tokens: input=15, output=4
#   [PASS] Claude API working.
```

```bash
# Step 4：測試 Telegram 發送
python test_components.py --test telegram

# 預期輸出：
# === Testing Telegram Sender ===
#   Testing bot connection...
#   Sending test message...
#   [PASS] Check your Telegram!
# --> 你的 Telegram 應該收到測試訊息
```

```bash
# Step 5：全部一起測試
python test_components.py --test all
```

### 7.3 執行完整流程

```bash
# 手動執行一次完整的 digest
python run_digest.py

# 觀察 log 輸出，確認四個階段都成功：
# Phase 1: Fetching Reddit posts
# Phase 2: AI Summarization
# Phase 3: Saving digest
# Phase 4: Sending via Telegram
```

### 7.4 測試 Cron 執行

```bash
# 模擬 cron 環境（最小化 PATH）
env -i HOME=$HOME \
  PATH=/usr/local/bin:/usr/bin:/bin \
  /path/to/venv/bin/python /path/to/run_digest.py
```

---

## 8. 常見陷阱與排錯

### 8.1 Reddit API 相關

| 問題 | 原因 | 解決方法 |
|------|------|----------|
| `401 Unauthorized` | client_id 或 client_secret 錯誤 | 重新確認 Reddit app 頁面上的憑證 |
| `403 Forbidden` | User-Agent 被封鎖 | 改用自訂的 User-Agent，不要用預設值 |
| `received 429 HTTP response` | 超過 rate limit (60/min) | 減少 subreddits 數量或加大 `time.sleep()` |
| 沒有抓到貼文 | `time_filter=day` 但該 subreddit 當天沒新帖 | 測試時改用 `time_filter=week` |
| `prawcore.exceptions.ResponseException` | Reddit API 暫時性錯誤 | 加入重試邏輯或稍後再試 |

**Reddit App 類型必須選 script**：如果選了 `web app` 或 `installed app`，認證流程會完全不同，PRAW 的 read-only 模式無法正常運作。

### 8.2 Claude API 相關

| 問題 | 原因 | 解決方法 |
|------|------|----------|
| `401 authentication_error` | API key 無效或過期 | 到 console.anthropic.com 確認 key |
| `400 invalid_request_error` | prompt 太長超過上限 | 減少 `REDDIT_POST_LIMIT` 或截短 selftext |
| `429 rate_limit_error` | 超過 API 請求限制 | 等待後重試，或升級方案 |
| `529 overloaded_error` | Claude API 過載 | 等幾分鐘後重試 |
| 摘要品質不佳 | prompt 不夠明確 | 調整 `SYSTEM_PROMPT` 中的指示 |

**Token 使用估算**：如果監控 5 個 subreddit 各 10 篇文章，含留言大約 15,000-30,000 input tokens。`claude-sonnet-4-20250514` 的上下文窗口為 200K tokens，通常不會超過。

### 8.3 Telegram 相關

| 問題 | 原因 | 解決方法 |
|------|------|----------|
| `401 Unauthorized` | Bot token 錯誤 | 到 @BotFather 確認 token |
| `400 Bad Request: chat not found` | chat_id 錯誤或 bot 尚未被啟動 | 先傳訊息給 bot，再用 getUpdates 取 chat_id |
| `400 Bad Request: can't parse entities` | Markdown 格式錯誤 | 程式已內建降級為純文字的機制 |
| 訊息被截斷 | 超過 4096 字元限制 | 程式已內建訊息分割機制 |
| `getUpdates` 回傳空陣列 | 沒有先傳訊息給 bot | 在 Telegram 中對 bot 傳送 "hello" |

**群組 Chat ID 的注意事項**：群組的 chat_id 是負數（例如 `-100123456789`）。如果用在群組中，bot 需要被加為群組成員，且可能需要管理員權限才能發送訊息。

### 8.4 Cron / 排程相關

| 問題 | 原因 | 解決方法 |
|------|------|----------|
| Cron 完全沒執行 | crontab 語法錯誤 | 用 `crontab -l` 確認，並檢查 `/var/log/syslog` |
| 找不到 python | cron 環境的 PATH 不同 | 使用 venv 的完整絕對路徑 |
| 找不到 .env | 工作目錄不對 | 在指令中加上 `cd /path/to/project &&` |
| 權限不足 | 腳本沒有執行權限 | `chmod +x run_digest.py` |
| macOS 上 cron 不執行 | macOS 需要「完全磁碟存取權」 | 改用 launchd 或授權 cron |

### 8.5 一般性建議

1. **先測試再排程**：一定要先手動 `python run_digest.py` 成功後，再設定 cron。

2. **保留 log**：cron 指令結尾的 `>> cron.log 2>&1` 會把 stdout 和 stderr 都寫入 log 檔，方便事後排錯。

3. **不要提交 .env**：在 `.gitignore` 中加入 `.env`，避免把 API key 推到 GitHub。

4. **監控 cron 執行**：如果 cron 靜默失敗，你不會收到通知。可以在 crontab 設定 `MAILTO=your@email.com` 來接收錯誤報告。

5. **selftext 截斷**：某些 Reddit 貼文的自述文非常長（上萬字），程式中已設定截斷到 2000 字以控制 Claude API 的 token 使用量。如果摘要品質不佳，可以嘗試調高這個上限。

---

## 9. 進階擴充

### 9.1 加入重試機制

安裝 `tenacity` 套件：

```bash
pip install tenacity
```

在 `ai_summarizer.py` 中加入重試裝飾器：

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
)
def summarize(self, posts_by_sub, date_str):
    # ... existing code ...
```

### 9.2 支援多個 Telegram 頻道

修改 `.env` 支援多個 chat_id：

```bash
TELEGRAM_CHAT_IDS=123456789,-100987654321,112233445
```

修改 `telegram_sender.py`：

```python
def send_to_all(self, text: str) -> dict:
    """Send to multiple chat IDs."""
    chat_ids = self.config.chat_id.split(",")
    results = {}
    for cid in chat_ids:
        self.config.chat_id = cid.strip()
        results[cid] = self.send_message(text)
    return results
```

### 9.3 加入關鍵字過濾

在 `.env` 新增：

```bash
# Posts containing these words will be excluded
REDDIT_EXCLUDE_KEYWORDS=meme,shitpost,nsfw
# Posts must contain at least one of these words (empty = no filter)
REDDIT_INCLUDE_KEYWORDS=
```

在 `reddit_fetcher.py` 的 `fetch_subreddit()` 中加入過濾邏輯。

### 9.4 歷史比對（去重）

將已處理的 post ID 存到本地 JSON：

```python
import json

HISTORY_FILE = "processed_posts.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return set(json.load(f))
    return set()

def save_history(ids: set):
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(ids), f)
```

### 9.5 部署到雲端

如果不想依賴本機 cron，可以部署到：

- **GitHub Actions**：免費，用 `schedule` trigger
- **Railway / Render**：免費方案有限制但足夠
- **AWS Lambda + EventBridge**：適合 serverless，成本極低

GitHub Actions 範例（`.github/workflows/digest.yml`）：

```yaml
name: Daily Reddit Digest
on:
  schedule:
    - cron: '0 0 * * *'  # UTC 00:00 = Taipei 08:00
  workflow_dispatch:       # Allow manual trigger

jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python run_digest.py
        env:
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

---

## 結語

這個專案的核心價值在於**讓 AI 幫你從資訊海嘯中篩選出有價值的內容**。PRAW 負責高效率地從 Reddit 抓取結構化資料，Claude 負責理解和彙整，Telegram 負責即時推送到你手邊。

三個外部 API、一個排程器、五個 Python 檔案，就能建立一個完全自動化的資訊消化管道。

如果需要監控更多平台（X/Twitter、Hacker News、GitHub Trending），同樣的架構可以輕鬆擴充 -- 只需要新增對應的 fetcher 模組即可。
