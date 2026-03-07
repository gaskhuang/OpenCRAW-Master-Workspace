---
name: 每日 Reddit 摘要 (Daily Reddit Digest)
description: "Use Case #001: 每日 Reddit 摘要 (Daily Reddit Digest) - 自動從 Reddit 抓取熱門貼文，用 Claude AI 產生繁中摘要，推送到 Telegram。輸入 /每日 Reddit 摘要 (Daily Reddit Digest)/python 或 /每日 Reddit 摘要 (Daily Reddit Digest)/nodejs 選擇方案，/每日 Reddit 摘要 (Daily Reddit Digest)/compare 比較兩方案。"
---

# Use Case #001: 每日 Reddit 摘要 (Daily Reddit Digest)

> 編號: 001 / 118 | 分類: 社群媒體 | 難度: 初中級 | 時間: 30-45 分鐘

## 一句話描述

根據個人偏好，自動整理並摘要喜愛的 subreddit 內容，每日產出精選報告推送到 Telegram。

## 可用子指令

| 指令 | 說明 |
|------|------|
| `/每日 Reddit 摘要 (Daily Reddit Digest)/python` | Python + PRAW 完整實作教學 |
| `/每日 Reddit 摘要 (Daily Reddit Digest)/nodejs` | Node.js + Reddit .json API 完整實作教學 |
| `/每日 Reddit 摘要 (Daily Reddit Digest)/compare` | 兩方案詳細比較 |

## 快速推薦

- **初學者 / 快速原型** → `/每日 Reddit 摘要 (Daily Reddit Digest)/nodejs` (免 Reddit API 註冊，5 分鐘開始)
- **正式環境 / 長期穩定** → `/每日 Reddit 摘要 (Daily Reddit Digest)/python` (官方 API，Rate Limit 更高)

## 功能需求

1. 設定感興趣的 subreddit 與關鍵字偏好
2. 配置每日排程 (cron)
3. 自動抓取、過濾並摘要 Reddit 內容
4. 透過 Telegram 推送每日摘要報告

## 核心技術棧

- Reddit API (PRAW 或 .json 端點)
- Anthropic Claude API (AI 摘要)
- Telegram Bot API (推送通知)
- Cron / node-cron (排程)

## 成本估算

| 項目 | 費用 |
|------|------|
| Reddit API | 免費 |
| Claude API (每日 ~5000 tokens) | ~$0.50-2.00/月 |
| Telegram Bot | 免費 |

## 詳細教學文件

- Python 方案: `docs/usecase-tutorials/daily-reddit-digest/TUTORIAL.md`
- Node.js 方案: `docs/daily-reddit-digest-nodejs-tutorial.md`
- 方案比較: `usecases/001-daily-reddit-digest.md`
