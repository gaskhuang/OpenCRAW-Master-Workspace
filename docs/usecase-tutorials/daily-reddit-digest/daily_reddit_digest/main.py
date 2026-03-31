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


def save_digest_locally(digest: str, output_dir: str, date_str: str) -> str:
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

    logger.info("Digest date: %s (%s)", date_display, config.timezone)
    logger.info("Subreddits: %s", ", ".join(config.reddit.subreddits))

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
        msg = "No posts fetched from any subreddit. Nothing to summarize."
        logger.warning(msg)
        telegram.send_message(f"[Daily Reddit Digest]\n\n{msg}")
        sys.exit(0)

    total_posts = sum(len(v) for v in posts_by_sub.values())
    logger.info("Fetched %d posts from %d subreddits", total_posts, len(posts_by_sub))

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
        filepath = save_digest_locally(digest, config.output_dir, date_str)
    except Exception as e:
        logger.warning("Failed to save digest locally: %s", e)
        # Non-fatal: continue to send via Telegram

    # --- 6. Send via Telegram ---
    logger.info("--- Phase 4: Sending via Telegram ---")
    header = f"Reddit Daily Digest - {date_display}\n{'=' * 40}\n\n"
    full_message = header + digest

    success = telegram.send_message(full_message)

    if success:
        logger.info("Digest delivered successfully via Telegram!")
    else:
        logger.error("Failed to deliver digest via Telegram.")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("Daily Reddit Digest - Complete")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()
