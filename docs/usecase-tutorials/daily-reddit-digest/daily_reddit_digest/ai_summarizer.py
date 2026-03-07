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


SYSTEM_PROMPT = """You are a professional content curator who creates daily Reddit digest reports.
Your task is to analyze Reddit posts and produce a well-structured, insightful summary.

Rules:
1. Write the summary in {language}.
2. Group posts by subreddit.
3. For each subreddit section, highlight the most interesting/impactful posts.
4. Include key discussion points from the comments when available.
5. Add a brief "Trends & Insights" section at the end.
6. Use clear formatting with headers, bullet points, and separators.
7. Keep the tone informative yet engaging.
8. Include the post score and comment count for context.
9. If a post links to an external URL (not a self-post), mention that.
10. Keep the total summary concise - aim for readability, not exhaustiveness."""


USER_PROMPT_TEMPLATE = """Here are today's top Reddit posts from the subreddits I follow.
Please create a daily digest summary.

Date: {date}
Timezone: {timezone}

---

{posts_text}

---

Please produce the daily digest now. Remember to write in {language}."""


class AISummarizer:
    """Generates AI-powered summaries of Reddit posts using Claude."""

    def __init__(self, claude_config: ClaudeConfig, app_config: AppConfig):
        self.config = claude_config
        self.app_config = app_config
        self.client = anthropic.Anthropic(api_key=claude_config.api_key)
        logger.info("Claude client initialized (model: %s)", claude_config.model)

    def _build_posts_text(self, posts_by_sub: dict[str, List[RedditPost]]) -> str:
        """Convert structured post data into a text block for the prompt."""
        sections = []
        for subreddit, posts in posts_by_sub.items():
            section_lines = [f"=== r/{subreddit} ({len(posts)} posts) ===\n"]
            for i, post in enumerate(posts, 1):
                section_lines.append(f"--- Post {i} ---")
                section_lines.append(post.to_summary_text())
                section_lines.append("")
            sections.append("\n".join(section_lines))
        return "\n\n".join(sections)

    def summarize(self, posts_by_sub: dict[str, List[RedditPost]], date_str: str) -> str:
        """
        Send posts to Claude and return the generated digest summary.

        Args:
            posts_by_sub: Dict mapping subreddit name -> list of RedditPost.
            date_str: Human-readable date string for the digest header.

        Returns:
            The generated summary text (Markdown formatted).
        """
        posts_text = self._build_posts_text(posts_by_sub)

        # Calculate approximate token count (rough estimate: 1 token ~ 4 chars)
        approx_tokens = len(posts_text) // 4
        logger.info(
            "Sending %d characters (~%d tokens) to Claude for summarization",
            len(posts_text),
            approx_tokens,
        )

        system_prompt = SYSTEM_PROMPT.format(language=self.app_config.summary_language)
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
                "Summary generated: %d chars, usage: input=%d output=%d tokens",
                len(summary),
                message.usage.input_tokens,
                message.usage.output_tokens,
            )
            return summary

        except anthropic.BadRequestError as e:
            logger.error("Claude API bad request: %s", e)
            raise
        except anthropic.AuthenticationError as e:
            logger.error("Claude API auth error - check ANTHROPIC_API_KEY: %s", e)
            raise
        except anthropic.RateLimitError as e:
            logger.warning("Claude API rate limited: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error calling Claude API: %s", e)
            raise
