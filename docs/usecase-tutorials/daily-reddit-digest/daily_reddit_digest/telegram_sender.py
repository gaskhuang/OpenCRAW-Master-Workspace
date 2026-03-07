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
        self.base_url = f"https://api.telegram.org/bot{config.bot_token}"
        logger.info("Telegram sender initialized for chat_id: %s", config.chat_id)

    def _split_message(self, text: str) -> List[str]:
        """
        Split a long message into chunks that fit Telegram's limit.
        Tries to split at paragraph boundaries to keep formatting clean.
        """
        if len(text) <= TELEGRAM_MAX_LENGTH:
            return [text]

        chunks = []
        remaining = text

        while remaining:
            if len(remaining) <= TELEGRAM_MAX_LENGTH:
                chunks.append(remaining)
                break

            # Try to find a good split point (double newline = paragraph break)
            split_at = remaining.rfind("\n\n", 0, TELEGRAM_MAX_LENGTH)
            if split_at == -1:
                # Fall back to single newline
                split_at = remaining.rfind("\n", 0, TELEGRAM_MAX_LENGTH)
            if split_at == -1:
                # Last resort: hard split at limit
                split_at = TELEGRAM_MAX_LENGTH

            chunks.append(remaining[:split_at])
            remaining = remaining[split_at:].lstrip("\n")

        logger.info("Message split into %d chunks", len(chunks))
        return chunks

    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
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
                logger.warning("Retrying chunk %d/%d without parse_mode", i + 1, len(chunks))
                success = self._send_single(chunk, parse_mode=None)
                if not success:
                    logger.error("Failed to send chunk %d/%d even as plain text", i + 1, len(chunks))

        return all_ok

    def _send_single(self, text: str, parse_mode: str = None) -> bool:
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
        text = f"[Daily Reddit Digest ERROR]\n\n{error_msg}"
        return self._send_single(text)

    def test_connection(self) -> bool:
        """Test the bot token by calling getMe."""
        try:
            resp = requests.get(f"{self.base_url}/getMe", timeout=10)
            data = resp.json()
            if data.get("ok"):
                bot_name = data["result"].get("username", "unknown")
                logger.info("Telegram bot connection OK: @%s", bot_name)
                return True
            else:
                logger.error("Telegram bot token invalid: %s", data.get("description"))
                return False
        except Exception as e:
            logger.error("Telegram connection test failed: %s", e)
            return False
