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
        logger.info("Reddit client initialized (read-only mode: %s)", self.reddit.read_only)

    def _extract_top_comments(self, submission: Submission, limit: int = 3) -> List[str]:
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
            logger.warning("Failed to fetch comments for %s: %s", submission.id, e)
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
                time_filter=self.config.time_filter, limit=self.config.post_limit
            ):
                top_comments = self._extract_top_comments(submission)
                post = RedditPost(
                    id=submission.id,
                    title=submission.title,
                    subreddit=subreddit_name,
                    author=str(submission.author) if submission.author else "[deleted]",
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
            logger.info("Fetched %d posts from r/%s", len(posts), subreddit_name)
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
            "Total fetched: %d posts from %d subreddits", total, len(results)
        )
        return results
