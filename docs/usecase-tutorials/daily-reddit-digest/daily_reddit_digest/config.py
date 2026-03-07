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
        subreddits_str = os.getenv("REDDIT_SUBREDDITS", "python,MachineLearning,LocalLLaMA")
        self.subreddits = [s.strip() for s in subreddits_str.split(",") if s.strip()]
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
            raise ValueError("REDDIT_SUBREDDITS must contain at least one subreddit.")
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
                "https://api.telegram.org/bot<TOKEN>/getUpdates to find your chat_id."
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
        self.summary_language = os.getenv("DIGEST_LANGUAGE", "Traditional Chinese")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.output_dir = os.getenv(
            "DIGEST_OUTPUT_DIR",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "output"),
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
