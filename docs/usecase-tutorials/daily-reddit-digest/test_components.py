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

    print(f"  Reddit Client ID: {'***' + config.reddit.client_id[-4:] if config.reddit.client_id else 'NOT SET'}")
    print(f"  Reddit Subreddits: {config.reddit.subreddits}")
    print(f"  Claude Model: {config.claude.model}")
    print(f"  Claude API Key: {'***' + config.claude.api_key[-4:] if config.claude.api_key else 'NOT SET'}")
    print(f"  Telegram Bot Token: {'***' + config.telegram.bot_token[-4:] if config.telegram.bot_token else 'NOT SET'}")
    print(f"  Telegram Chat ID: {config.telegram.chat_id}")
    print(f"  Timezone: {config.timezone}")
    print(f"  Language: {config.summary_language}")

    try:
        config.validate_all()
        print("\n  [PASS] All configuration validated successfully.")
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

    # Test with a single subreddit, small limit
    test_sub = config.reddit.subreddits[0]
    print(f"  Fetching top 3 posts from r/{test_sub} (time_filter=day)...")

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
        print(f"  No posts found in r/{test_sub} for today. This may be normal for low-traffic subs.")
        print("  [WARN] Try changing REDDIT_TIME_FILTER to 'week' for testing.")
        return True  # Not necessarily a failure


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
            messages=[{"role": "user", "content": "Say 'Claude API connection successful' in exactly those words."}],
        )
        response_text = message.content[0].text
        print(f"  Response: {response_text}")
        print(f"  Tokens used: input={message.usage.input_tokens}, output={message.usage.output_tokens}")
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
        "[Daily Reddit Digest]\n\nThis is a test message. If you see this, Telegram delivery is working!",
        parse_mode=None,
    )

    if success:
        print("\n  [PASS] Telegram sender working. Check your Telegram!")
        return True
    else:
        print("\n  [FAIL] Failed to send test message.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test Daily Reddit Digest components")
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
