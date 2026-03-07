#!/usr/bin/env python3
"""
Regenerate all 117 SKILL.md files (002-118) with truly differentiated
Python and Node.js implementations using Claude API.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 scripts/regenerate_skills_v2.py

Features:
- Uses Claude API to generate quality, differentiated content
- Each Python vs Node.js uses genuinely different libraries & approaches
- Complete working code (no TODO placeholders)
- Resume capability: skips already-completed cases
- Rate limit handling with exponential backoff
- Progress saved to scripts/progress_v2.json

Cost estimate: ~$20-30 for all 117 cases (Claude Sonnet)
Time estimate: ~2-3 hours (rate limit pacing)
"""

import os
import sys
import json
import time
import traceback
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
BASE = "/Users/user/118usecase/.claude/worktrees/romantic-raman"
SKILLS_DIR = f"{BASE}/.claude/skills"
REPOS = {
    "main": f"{BASE}/_repos/awesome-openclaw-usecases/usecases",
    "hub": f"{BASE}/_repos/openclaw_usecase_hub/usecases",
    "var": f"{BASE}/_repos/awesome-clawdbot-usecases/usecases",
}
PROGRESS_FILE = f"{BASE}/scripts/progress_v2.json"
MODEL = "claude-sonnet-4-20250514"
MAX_RETRIES = 5
DELAY_BETWEEN_CALLS = 3  # seconds between API calls
DELAY_BETWEEN_CASES = 5  # seconds between cases

# ============================================================
# 118 USE CASES — with DIFFERENTIATED library specs
# ============================================================
# Format: (num, cn, en, cat, diff, folder_name,
#          python_libs, nodejs_libs, python_approach, nodejs_approach,
#          source_files)
#
# python_libs / nodejs_libs: key libraries that make each version unique
# python_approach / nodejs_approach: 1-line summary of the architectural diff
# ============================================================

USECASES = [
    # === 社群媒體 (1-9) ===
    (1, "每日 Reddit 摘要", "Daily Reddit Digest", "社群媒體", "初中級",
     "每日 Reddit 摘要 (Daily Reddit Digest)",
     "praw, anthropic, python-telegram-bot",
     "@anthropic-ai/sdk, node-telegram-bot-api (uses Reddit .json API, no registration)",
     "使用 PRAW 官方 Reddit API wrapper，需註冊 Reddit App",
     "使用 Reddit 公開 .json 端點，免註冊，搭配 node-cron 內建排程",
     {}),  # #001 already done manually

    (2, "每日 YouTube 摘要", "Daily YouTube Digest", "社群媒體", "初中級",
     "每日 YouTube 摘要 (Daily YouTube Digest)",
     "google-api-python-client, youtube-transcript-api, anthropic, python-telegram-bot",
     "@anthropic-ai/sdk, googleapis, youtubei.js (innertube API, no API key needed)",
     "使用 YouTube Data API v3 (需 API Key) + youtube-transcript-api 取字幕",
     "使用 youtubei.js (InnerTube 非官方 API, 免 key) 取頻道影片 + 字幕",
     {"main": ["daily-youtube-digest.md"], "hub": ["40-youtube-analytics-pull.md"], "var": ["video-content-pipeline.md"]}),

    (3, "X 帳號質性分析", "X Account Qualitative Analysis", "社群媒體", "中級",
     "X 帳號質性分析 (X Account Qualitative Analysis)",
     "tweepy, pandas, anthropic, matplotlib",
     "@anthropic-ai/sdk, twitter-api-v2, chart.js (via chartjs-node-canvas)",
     "使用 Tweepy v2 + Pandas 做資料分析，Matplotlib 產圖表",
     "使用 twitter-api-v2 + chartjs-node-canvas 生成分析圖表",
     {"main": ["x-account-analysis.md"], "hub": ["68-x-profile-scraper.md"]}),

    (4, "多來源科技新聞摘要", "Multi-Source Tech News Digest", "社群媒體", "中級",
     "多來源科技新聞摘要 (Multi-Source Tech News Digest)",
     "feedparser, tweepy, PyGithub, anthropic, jinja2",
     "@anthropic-ai/sdk, rss-parser, octokit, handlebars (HTML template)",
     "使用 feedparser 解析 RSS + tweepy 抓 Twitter + PyGithub 追 release，Jinja2 產 HTML 報告",
     "使用 rss-parser + octokit + Brave Search API，Handlebars 產 HTML email",
     {"main": ["multi-source-tech-news-digest.md"], "hub": ["09-news-digest-aggregator.md", "52-rss-news-aggregator.md"], "var": ["news-digest.md"]}),

    (5, "品牌社群監控", "Brand Social Monitoring", "社群媒體", "中級",
     "品牌社群監控 (Brand Social Monitoring)",
     "praw, tweepy, anthropic, sqlite3, schedule",
     "@anthropic-ai/sdk, snoowrap, twitter-api-v2, better-sqlite3, node-cron",
     "使用 PRAW + Tweepy 監控品牌提及，SQLite 儲存歷史，schedule 排程",
     "使用 snoowrap (Reddit) + twitter-api-v2，better-sqlite3 持久化",
     {"hub": ["14-social-media-monitor.md"], "var": ["competitor-radar.md"]}),

    (6, "自動排程社群發文", "Auto-Schedule Social Posts", "社群媒體", "中級",
     "自動排程社群發文 (Auto-Schedule Social Posts)",
     "tweepy, instabot, anthropic, apscheduler, pillow",
     "@anthropic-ai/sdk, twitter-api-v2, sharp (image processing), bull (job queue)",
     "使用 APScheduler 排程 + Tweepy 發推 + Pillow 產圖，本地 SQLite 管理佇列",
     "使用 Bull (Redis-based job queue) + twitter-api-v2 + Sharp 圖片處理",
     {"hub": ["15-auto-social-posting.md"], "var": ["social-media-scheduler.md"]}),

    (7, "Instagram 限時動態管理", "Instagram Stories Management", "社群媒體", "中級",
     "Instagram 限時動態管理 (Instagram Stories Management)",
     "instagrapi, pillow, anthropic, schedule",
     "@anthropic-ai/sdk, instagram-private-api, sharp, node-cron",
     "使用 instagrapi (unofficial Instagram API) + Pillow 產圖 + schedule",
     "使用 instagram-private-api + Sharp 圖片處理 + node-cron",
     {"hub": ["03-instagram-story-manager.md"]}),

    (8, "Reddit 產品聲量追蹤", "Reddit Product Buzz Tracking", "社群媒體", "中級",
     "Reddit 產品聲量追蹤 (Reddit Product Buzz Tracking)",
     "praw, anthropic, pandas, plotly, sqlite3",
     "@anthropic-ai/sdk, axios (Reddit .json), d3-node, better-sqlite3",
     "使用 PRAW 搜尋關鍵字 + Pandas 分析趨勢 + Plotly 產互動圖表",
     "使用 Reddit .json 搜尋 API + d3-node 生成 SVG 圖表",
     {"main": ["daily-reddit-digest.md"], "hub": ["54-customer-signal-scanner.md"], "var": ["competitor-radar.md"]}),

    (9, "X 互動管理助手", "X Engagement Manager", "社群媒體", "中級",
     "X 互動管理助手 (X Engagement Manager)",
     "tweepy, anthropic, sqlite3, schedule",
     "@anthropic-ai/sdk, twitter-api-v2, keyv (key-value store), node-cron",
     "使用 Tweepy Stream API 即時監控互動 + Claude 自動生成回覆建議",
     "使用 twitter-api-v2 polling + Keyv 快取已處理推文 + Claude 回覆",
     {"main": ["x-account-analysis.md"], "hub": ["68-x-profile-scraper.md", "59-multi-channel-presence-sync.md"]}),

    # === 創意與內容製作 (10-18) ===
    (10, "目標驅動自主任務", "Goal-Driven Autonomous Tasks", "創意與內容製作", "中級",
     "目標驅動自主任務 (Goal-Driven Autonomous Tasks)",
     "anthropic, pydantic, rich, sqlite3",
     "@anthropic-ai/sdk, zod (schema validation), ink (terminal UI), better-sqlite3",
     "使用 Pydantic 結構化目標分解 + Rich 終端 UI + SQLite 追蹤進度",
     "使用 Zod schema 驗證 + Ink (React for CLI) 互動介面",
     {"hub": ["30-daily-goal-task-generator.md"], "main": ["autonomous-project-management.md"]}),

    (11, "YouTube 內容產線", "YouTube Content Pipeline", "創意與內容製作", "中高級",
     "YouTube 內容產線 (YouTube Content Pipeline)",
     "google-api-python-client, youtube-transcript-api, moviepy, anthropic, gtts",
     "@anthropic-ai/sdk, googleapis, fluent-ffmpeg, elevenlabs (TTS)",
     "使用 MoviePy 影片編輯 + gTTS 語音合成 + YouTube Data API 上傳",
     "使用 fluent-ffmpeg + ElevenLabs TTS API + YouTube Upload API",
     {"main": ["youtube-content-pipeline.md"], "hub": ["40-youtube-analytics-pull.md"], "var": ["video-content-pipeline.md"]}),

    (12, "多代理內容工廠", "Multi-Agent Content Factory", "創意與內容製作", "高級",
     "多代理內容工廠 (Multi-Agent Content Factory)",
     "anthropic, celery, redis, jinja2, pydantic",
     "@anthropic-ai/sdk, bullmq, redis, handlebars, zod",
     "使用 Celery + Redis 多 worker 並行產生內容，Pydantic 品質把關",
     "使用 BullMQ (Redis job queue) + Worker threads 並行處理",
     {"main": ["content-factory.md"], "var": ["content-multiplication.md"]}),

    (13, "自主遊戲開發流水線", "Autonomous Game Dev Pipeline", "創意與內容製作", "高級",
     "自主遊戲開發流水線 (Autonomous Game Dev Pipeline)",
     "anthropic, pygame, pillow, pydantic",
     "@anthropic-ai/sdk, phaser (via CDN), sharp, puppeteer (screenshot testing)",
     "使用 Pygame 作為遊戲引擎 + Claude 生成遊戲邏輯 + Pillow 資源",
     "使用 Phaser.js 瀏覽器遊戲框架 + Puppeteer 自動化測試",
     {"main": ["autonomous-game-dev-pipeline.md"]}),

    (14, "Podcast 製作流水線", "Podcast Production Pipeline", "創意與內容製作", "中級",
     "Podcast 製作流水線 (Podcast Production Pipeline)",
     "anthropic, pydub, gtts, feedgen (RSS), whisper",
     "@anthropic-ai/sdk, fluent-ffmpeg, podcast-rss-generator, @google-cloud/text-to-speech",
     "使用 pydub 音訊剪輯 + gTTS/Whisper + feedgen 產 RSS feed",
     "使用 fluent-ffmpeg 音訊處理 + Google Cloud TTS + podcast RSS generator",
     {"main": ["podcast-production-pipeline.md"], "hub": ["01-email-to-podcast-commute.md"], "var": ["podcast-production.md"]}),

    (15, "電子報轉 Podcast", "Newsletter to Podcast", "創意與內容製作", "中級",
     "電子報轉 Podcast (Newsletter to Podcast)",
     "anthropic, imaplib, pydub, gtts, beautifulsoup4",
     "@anthropic-ai/sdk, imap-simple, fluent-ffmpeg, say.js (native TTS), cheerio",
     "使用 imaplib + BeautifulSoup 解析郵件 HTML → Claude 摘要 → gTTS 語音",
     "使用 imap-simple + Cheerio 解析 → Claude 摘要 → say.js 系統原生 TTS",
     {"hub": ["01-email-to-podcast-commute.md", "26-medical-email-to-podcast.md"]}),

    (16, "AI 寫作助手", "AI Writing Assistant", "創意與內容製作", "初中級",
     "AI 寫作助手 (AI Writing Assistant)",
     "anthropic, click, rich, python-docx",
     "@anthropic-ai/sdk, commander, chalk, markdown-it, pdf-lib",
     "使用 Click CLI + Rich 終端介面 + python-docx 匯出 Word",
     "使用 Commander.js CLI + Chalk 彩色輸出 + pdf-lib 匯出 PDF",
     {"var": ["writing-assistant.md"]}),

    (17, "一文多平台內容複製", "Cross-Platform Content Repurposing", "創意與內容製作", "中級",
     "一文多平台內容複製 (Cross-Platform Content Repurposing)",
     "anthropic, tweepy, requests, pillow, jinja2",
     "@anthropic-ai/sdk, twitter-api-v2, sharp, handlebars, puppeteer (screenshot)",
     "使用 Claude 改寫為不同平台格式 + Pillow 產配圖 + Jinja2 模板",
     "使用 Claude 改寫 + Puppeteer 截圖產 OG Image + Sharp 圖片",
     {"var": ["content-multiplication.md", "seo-content-pipeline.md"], "hub": ["59-multi-channel-presence-sync.md"]}),

    (18, "學術研究助手", "Academic Research Assistant", "創意與內容製作", "中級",
     "學術研究助手 (Academic Research Assistant)",
     "anthropic, arxiv, semanticscholar, bibtexparser, pandas",
     "@anthropic-ai/sdk, axios (arXiv/Semantic Scholar API), citation-js, csv-parse",
     "使用 arxiv + semanticscholar Python 套件 + bibtexparser 管理引用",
     "使用 Axios 直接呼叫 arXiv/Semantic Scholar REST API + citation-js",
     {"var": ["academic-research.md"]}),

    # === 日常生活自動化 (19-28) ===
    (19, "Telegram 智慧家居控制", "Telegram Smart Home Control", "日常生活自動化", "中級",
     "Telegram 智慧家居控制 (Telegram Smart Home Control)",
     "python-telegram-bot, anthropic, requests, paho-mqtt",
     "@anthropic-ai/sdk, telegraf (Telegram bot framework), mqtt.js, homebridge-lib",
     "使用 python-telegram-bot + paho-mqtt 連接 Home Assistant/MQTT 設備",
     "使用 Telegraf bot 框架 + mqtt.js + homebridge API 整合",
     {"hub": ["12-smart-home-telegram.md"], "var": ["home-automation.md"]}),

    (20, "旅遊行程規劃", "Travel Itinerary Planner", "日常生活自動化", "初中級",
     "旅遊行程規劃 (Travel Itinerary Planner)",
     "anthropic, googlemaps, requests, icalendar, fpdf2",
     "@anthropic-ai/sdk, @googlemaps/google-maps-services-js, ical-generator, pdfkit",
     "使用 googlemaps Python 套件 + icalendar 匯出行事曆 + FPDF 產 PDF",
     "使用 Google Maps JS SDK + ical-generator + PDFKit 產 PDF",
     {"hub": ["20-travel-itinerary-planner.md"], "var": ["travel-planner.md"]}),

    (21, "跨平台比價購物", "Cross-Platform Price Comparison", "日常生活自動化", "中級",
     "跨平台比價購物 (Cross-Platform Price Comparison)",
     "anthropic, beautifulsoup4, requests, selenium, sqlite3, pandas",
     "@anthropic-ai/sdk, puppeteer, cheerio, better-sqlite3",
     "使用 BeautifulSoup + Selenium 爬蟲抓價格 + Pandas 分析趨勢",
     "使用 Puppeteer 無頭瀏覽器抓價格 + Cheerio 解析 HTML",
     {"hub": ["17-price-comparison-shopper.md"], "var": ["price-drop-alerter.md"]}),

    (22, "天氣穿搭建議", "Weather-Based Outfit Suggestions", "日常生活自動化", "初級",
     "天氣穿搭建議 (Weather-Based Outfit Suggestions)",
     "anthropic, requests (OpenWeatherMap), python-telegram-bot, schedule",
     "@anthropic-ai/sdk, axios (OpenWeatherMap), node-telegram-bot-api, node-cron",
     "使用 OpenWeatherMap API + Claude 穿搭建議 + schedule 定時推送",
     "使用 OpenWeatherMap + Claude + node-cron 排程",
     {"hub": ["08-weather-outfit-advisor.md", "28-weather-morning-report.md"]}),

    (23, "生日祝福自動發送", "Auto Birthday Wishes", "日常生活自動化", "初級",
     "生日祝福自動發送 (Auto Birthday Wishes)",
     "anthropic, google-api-python-client (Contacts/Sheets), python-telegram-bot, schedule",
     "@anthropic-ai/sdk, googleapis (Contacts/Sheets), nodemailer, node-cron",
     "使用 Google People API 讀聯絡人生日 + Claude 產個人化祝福 + Telegram 通知",
     "使用 Google Sheets API 存生日清單 + Claude 產祝福 + Nodemailer 寄 email",
     {"hub": ["23-birthday-wish-sender.md"]}),

    (24, "自動預訂代理", "Auto Booking Agent", "日常生活自動化", "中高級",
     "自動預訂代理 (Auto Booking Agent)",
     "anthropic, selenium, beautifulsoup4, twilio",
     "@anthropic-ai/sdk, puppeteer, cheerio, twilio",
     "使用 Selenium WebDriver 自動化瀏覽器操作 + Twilio 簡訊通知",
     "使用 Puppeteer 無頭瀏覽器 + Twilio SMS 通知",
     {"hub": ["13-booking-appointment-agent.md"]}),

    (25, "閱讀清單智慧管理", "Smart Reading List Manager", "日常生活自動化", "初中級",
     "閱讀清單智慧管理 (Smart Reading List Manager)",
     "anthropic, beautifulsoup4, requests, readability-lxml, sqlite3",
     "@anthropic-ai/sdk, @mozilla/readability, jsdom, better-sqlite3, rss-parser",
     "使用 readability-lxml 抽取文章內容 + Claude 摘要分類 + SQLite 管理",
     "使用 Mozilla Readability.js (同 Firefox Reader View) + jsdom 解析 DOM",
     {"hub": ["11-reading-list-curator.md"]}),

    (26, "食譜推薦與購物清單", "Recipe & Shopping List", "日常生活自動化", "初中級",
     "食譜推薦與購物清單 (Recipe & Shopping List)",
     "anthropic, spoonacular (API), python-telegram-bot, jinja2",
     "@anthropic-ai/sdk, axios (Spoonacular/Edamam API), ejs, express",
     "使用 Spoonacular API + Claude 客製化推薦 + Jinja2 產購物清單 HTML",
     "使用 Edamam Recipe API + Express 簡易 Web UI + EJS template",
     {"hub": ["24-recipe-recommendation.md"], "var": ["grocery-optimizer.md"]}),

    (27, "耐心作業輔導老師", "Patient Homework Tutor", "日常生活自動化", "中級",
     "耐心作業輔導老師 (Patient Homework Tutor)",
     "anthropic, sympy, matplotlib, python-telegram-bot",
     "@anthropic-ai/sdk, mathjs, mermaid (diagram), discord.js",
     "使用 SymPy 數學計算驗證 + Matplotlib 畫圖 + Telegram 互動",
     "使用 math.js 數學引擎 + Mermaid 流程圖 + Discord.js bot 互動",
     {"hub": ["19-homework-tutor.md"]}),

    (28, "每日學習日誌", "Daily Learning Journal", "日常生活自動化", "初級",
     "每日學習日誌 (Daily Learning Journal)",
     "anthropic, python-telegram-bot, markdown, sqlite3",
     "@anthropic-ai/sdk, telegraf, lowdb (JSON database), markdown-it",
     "使用 python-telegram-bot 收集日誌 + SQLite 持久化 + Claude 週報",
     "使用 Telegraf bot 框架 + lowdb (JSON file DB, 零設定) + Claude 週報",
     {"hub": ["07-daily-learning-journal.md", "37-voice-notes-to-journal.md"], "var": ["daily-journaling.md"]}),

    # === 生產力工具 (29-54) ===
    (29, "自主專案管理", "Autonomous Project Management", "生產力工具", "中高級",
     "自主專案管理 (Autonomous Project Management)",
     "anthropic, PyGithub, notion-client, pydantic, networkx",
     "@anthropic-ai/sdk, octokit, @notionhq/client, zod, graphology",
     "使用 PyGithub + notion-client + NetworkX 建立任務依賴圖",
     "使用 Octokit + Notion API + Graphology 圖分析庫",
     {"main": ["autonomous-project-management.md"]}),

    (30, "多通道 AI 客服", "Multi-Channel AI Customer Service", "生產力工具", "高級",
     "多通道 AI 客服 (Multi-Channel AI Customer Service)",
     "anthropic, python-telegram-bot, flask, twilio, sqlite3",
     "@anthropic-ai/sdk, express, socket.io, telegraf, twilio, prisma",
     "使用 Flask Web 框架 + Telegram + Twilio + SQLite 統一客服",
     "使用 Express + Socket.IO (即時聊天) + Prisma ORM + 多通道整合",
     {"main": ["multi-channel-customer-service.md"], "hub": ["54-customer-signal-scanner.md"]}),

    (31, "電話語音個人助理", "Phone Voice Personal Assistant", "生產力工具", "高級",
     "電話語音個人助理 (Phone Voice Personal Assistant)",
     "anthropic, twilio, openai-whisper, pyttsx3",
     "@anthropic-ai/sdk, twilio, @google-cloud/speech, @google-cloud/text-to-speech",
     "使用 Twilio + OpenAI Whisper (本地 STT) + pyttsx3 (本地 TTS)",
     "使用 Twilio + Google Cloud Speech-to-Text/Text-to-Speech (雲端)",
     {"main": ["phone-based-personal-assistant.md"]}),

    (32, "收件匣清理器", "Inbox Cleaner", "生產力工具", "中級",
     "收件匣清理器 (Inbox Cleaner)",
     "anthropic, google-api-python-client, google-auth-oauthlib, beautifulsoup4",
     "@anthropic-ai/sdk, googleapis, imap-simple, cheerio, mailparser",
     "使用 Gmail API (OAuth2) + BeautifulSoup 解析 HTML 郵件內容",
     "使用 IMAP 協議 (imap-simple) + mailparser + Cheerio，適用任何郵件服務",
     {"main": ["inbox-declutter.md"], "hub": ["32-inbox-triage-followup.md"], "var": ["email-triage.md"]}),

    (33, "個人 CRM", "Personal CRM", "生產力工具", "中級",
     "個人 CRM (Personal CRM)",
     "anthropic, sqlite3, flask, jinja2, google-api-python-client",
     "@anthropic-ai/sdk, better-sqlite3, express, ejs, googleapis",
     "使用 Flask Web App + SQLite + Jinja2 模板，本地 CRM 介面",
     "使用 Express + better-sqlite3 + EJS，RESTful API 設計",
     {"main": ["personal-crm.md"], "hub": ["35-lightweight-crm-updates.md"], "var": ["client-memory.md"]}),

    (34, "健康與症狀追蹤器", "Health & Symptom Tracker", "生產力工具", "中級",
     "健康與症狀追蹤器 (Health & Symptom Tracker)",
     "anthropic, sqlite3, matplotlib, python-telegram-bot, pandas",
     "@anthropic-ai/sdk, better-sqlite3, chart.js (via chartjs-node-canvas), telegraf",
     "使用 Pandas + Matplotlib 資料分析與視覺化 + Telegram bot 記錄",
     "使用 Chart.js 生成圖表圖片 + Telegraf bot 記錄症狀",
     {"main": ["health-symptom-tracker.md"], "hub": ["22-health-habit-builder.md"]}),

    (35, "多通道個人助理", "Multi-Channel Personal Assistant", "生產力工具", "高級",
     "多通道個人助理 (Multi-Channel Personal Assistant)",
     "anthropic, python-telegram-bot, flask, slack-sdk, discord.py",
     "@anthropic-ai/sdk, telegraf, express, @slack/bolt, discord.js",
     "使用 Flask 作為中央 webhook 接收器 + 多 SDK 整合",
     "使用 Express middleware 架構 + @slack/bolt + discord.js",
     {"main": ["multi-channel-assistant.md"], "hub": ["59-multi-channel-presence-sync.md"]}),

    (36, "事件驅動專案狀態管理", "Event-Driven Project Status", "生產力工具", "中高級",
     "事件驅動專案狀態管理 (Event-Driven Project Status)",
     "anthropic, celery, redis, flask, pydantic",
     "@anthropic-ai/sdk, bullmq, redis, express, eventemitter3",
     "使用 Celery (task queue) + Redis + Flask webhook，事件驅動架構",
     "使用 BullMQ + Redis + Express + EventEmitter3 事件驅動",
     {"main": ["project-state-management.md"], "hub": ["56-cron-dashboard-status.md"]}),

    (37, "動態即時儀表板", "Dynamic Real-Time Dashboard", "生產力工具", "中級",
     "動態即時儀表板 (Dynamic Real-Time Dashboard)",
     "anthropic, flask, flask-socketio, plotly, sqlite3",
     "@anthropic-ai/sdk, express, socket.io, chart.js, better-sqlite3",
     "使用 Flask-SocketIO + Plotly.js 前端 + SQLite 即時儀表板",
     "使用 Express + Socket.IO + Chart.js 前端，即時推送更新",
     {"main": ["dynamic-dashboard.md"], "hub": ["31-mission-control-dashboard.md"]}),

    (38, "Todoist 透明任務管理", "Todoist Transparent Task Management", "生產力工具", "中級",
     "Todoist 透明任務管理 (Todoist Transparent Task Management)",
     "anthropic, todoist-api-python, schedule, python-telegram-bot",
     "@anthropic-ai/sdk, @doist/todoist-api-typescript, node-cron, node-telegram-bot-api",
     "使用 todoist-api-python 官方 SDK + schedule 排程 + Claude 智慧分配",
     "使用 @doist/todoist-api-typescript 官方 TS SDK + node-cron",
     {"main": ["todoist-task-manager.md"]}),

    (39, "家庭行事曆與家務助理", "Family Calendar & Chore Assistant", "生產力工具", "中級",
     "家庭行事曆與家務助理 (Family Calendar & Chore Assistant)",
     "anthropic, google-api-python-client, google-auth-oauthlib, python-telegram-bot",
     "@anthropic-ai/sdk, googleapis, ical-generator, telegraf",
     "使用 Google Calendar API (OAuth2) + Telegram 群組 bot 分配家務",
     "使用 Google Calendar API + ical-generator + Telegraf 家庭群組",
     {"main": ["family-calendar-household-assistant.md"], "hub": ["05-calendar-smart-reminder.md"]}),

    (40, "多代理專業團隊", "Multi-Agent Professional Team", "生產力工具", "高級",
     "多代理專業團隊 (Multi-Agent Professional Team)",
     "anthropic, pydantic, asyncio, networkx, rich",
     "@anthropic-ai/sdk, zod, p-queue, graphology, ink",
     "使用 asyncio 並行多 agent + NetworkX 任務依賴圖 + Rich 視覺化",
     "使用 p-queue 併發控制 + Graphology 依賴圖 + Ink CLI UI",
     {"main": ["multi-agent-team.md"]}),

    (41, "客製化晨間簡報", "Custom Morning Briefing", "生產力工具", "初中級",
     "客製化晨間簡報 (Custom Morning Briefing)",
     "anthropic, feedparser, requests, python-telegram-bot, schedule",
     "@anthropic-ai/sdk, rss-parser, axios, node-telegram-bot-api, node-cron",
     "使用 feedparser (RSS) + requests (天氣/新聞 API) + schedule 每早推送",
     "使用 rss-parser + axios + node-cron，產 HTML email (nodemailer)",
     {"main": ["custom-morning-brief.md"], "hub": ["02-morning-briefing-generator.md"]}),

    (42, "自動會議紀錄與行動項目", "Auto Meeting Notes & Action Items", "生產力工具", "中級",
     "自動會議紀錄與行動項目 (Auto Meeting Notes & Action Items)",
     "anthropic, openai-whisper, pydub, notion-client, python-docx",
     "@anthropic-ai/sdk, @google-cloud/speech, fluent-ffmpeg, @notionhq/client",
     "使用 Whisper (本地 STT) + pydub 音訊處理 + Notion API 寫入 + Word 匯出",
     "使用 Google Cloud STT (雲端) + fluent-ffmpeg + Notion API 寫入",
     {"main": ["meeting-notes-action-items.md"], "hub": ["18-meeting-notes-generator.md"], "var": ["meeting-roi.md"]}),

    (43, "習慣追蹤與問責教練", "Habit Tracker & Accountability Coach", "生產力工具", "中級",
     "習慣追蹤與問責教練 (Habit Tracker & Accountability Coach)",
     "anthropic, sqlite3, matplotlib, python-telegram-bot, schedule",
     "@anthropic-ai/sdk, lowdb, chartjs-node-canvas, telegraf, node-cron",
     "使用 SQLite + Matplotlib 產進度圖 + Telegram bot 每日打卡",
     "使用 lowdb (JSON DB) + Chart.js 產進度圖 + Telegraf 打卡",
     {"main": ["habit-tracker-accountability-coach.md"], "var": ["habit-tracker.md"]}),

    (44, "第二大腦", "Second Brain", "生產力工具", "中高級",
     "第二大腦 (Second Brain)",
     "anthropic, chromadb, sentence-transformers, flask",
     "@anthropic-ai/sdk, @xenova/transformers (local embeddings), lancedb, express",
     "使用 ChromaDB + sentence-transformers (本地向量嵌入) + Flask Web UI",
     "使用 LanceDB + @xenova/transformers (瀏覽器/Node ONNX) + Express",
     {"main": ["second-brain.md"], "hub": ["29-second-brain.md"]}),

    (45, "活動賓客電話確認", "Event Guest Phone Confirmation", "生產力工具", "高級",
     "活動賓客電話確認 (Event Guest Phone Confirmation)",
     "anthropic, twilio, pandas, google-api-python-client",
     "@anthropic-ai/sdk, twilio, csv-parse, googleapis",
     "使用 Twilio 語音 API + Pandas 管理賓客清單 + Google Sheets 同步",
     "使用 Twilio + csv-parse 讀取 CSV + Google Sheets API 同步",
     {"main": ["event-guest-confirmation.md"]}),

    (46, "郵件自動分類器", "Email Auto Classifier", "生產力工具", "中級",
     "郵件自動分類器 (Email Auto Classifier)",
     "anthropic, google-api-python-client, google-auth-oauthlib",
     "@anthropic-ai/sdk, googleapis, imap-simple, mailparser",
     "使用 Gmail API + Claude 分類 + 自動加 Label + 轉寄重要郵件",
     "使用 IMAP (通用協議) + mailparser 解析 + Claude 分類",
     {"hub": ["06-email-auto-classifier.md"], "var": ["email-triage.md", "email-templates.md"]}),

    (47, "語音筆記轉任務", "Voice Notes to Tasks", "生產力工具", "中級",
     "語音筆記轉任務 (Voice Notes to Tasks)",
     "anthropic, openai-whisper, pydub, todoist-api-python",
     "@anthropic-ai/sdk, @google-cloud/speech, fluent-ffmpeg, @doist/todoist-api-typescript",
     "使用 Whisper 本地語音辨識 + pydub 音訊切割 + Todoist API",
     "使用 Google Cloud Speech-to-Text + fluent-ffmpeg + Todoist API",
     {"hub": ["37-voice-notes-to-journal.md"], "var": ["voice-note-organizer.md"]}),

    (48, "PDF 文件處理中心", "PDF Document Processing Hub", "生產力工具", "中級",
     "PDF 文件處理中心 (PDF Document Processing Hub)",
     "anthropic, pdfplumber, PyPDF2, python-docx, tabula-py",
     "@anthropic-ai/sdk, pdf-parse, pdf-lib, xlsx, mammoth",
     "使用 pdfplumber (表格抽取) + PyPDF2 (合併/分割) + python-docx (Word 轉換)",
     "使用 pdf-parse (文字) + pdf-lib (建立/修改 PDF) + xlsx (Excel 匯出)",
     {"hub": ["33-pdf-to-summary-converter.md"], "var": ["document-processor.md"]}),

    (49, "會議前情報準備", "Pre-Meeting Intel Prep", "生產力工具", "中級",
     "會議前情報準備 (Pre-Meeting Intel Prep)",
     "anthropic, google-api-python-client, requests, beautifulsoup4, jinja2",
     "@anthropic-ai/sdk, googleapis, axios, cheerio, handlebars",
     "使用 Google Calendar API 取會議 + BeautifulSoup 爬公司資訊 + Jinja2 報告",
     "使用 Google Calendar API + Axios/Cheerio 爬公司 + Handlebars 模板",
     {"hub": ["48-meeting-prep-delivery.md"]}),

    (50, "行事曆衝突排解", "Calendar Conflict Resolution", "生產力工具", "中級",
     "行事曆衝突排解 (Calendar Conflict Resolution)",
     "anthropic, google-api-python-client, google-auth-oauthlib, python-dateutil",
     "@anthropic-ai/sdk, googleapis, luxon, ical-generator",
     "使用 Google Calendar API + python-dateutil 時間計算 + Claude 智慧排程",
     "使用 Google Calendar API + Luxon (日期時間庫) + Claude 協調",
     {"hub": ["05-calendar-smart-reminder.md"], "var": ["meeting-scheduler.md"]}),

    (51, "看板自動整理", "Kanban Auto Organizer", "生產力工具", "中級",
     "看板自動整理 (Kanban Auto Organizer)",
     "anthropic, py-trello, notion-client, schedule",
     "@anthropic-ai/sdk, trello.js, @notionhq/client, node-cron",
     "使用 py-trello (Trello API) + notion-client + Claude 自動分類移動卡片",
     "使用 trello.js + Notion API + node-cron 定期整理",
     {"hub": ["16-trello-notion-organizer.md", "76-trello-board-organizer.md"]}),

    (52, "包裹追蹤自動化", "Package Tracking Automation", "生產力工具", "初中級",
     "包裹追蹤自動化 (Package Tracking Automation)",
     "anthropic, requests, beautifulsoup4, python-telegram-bot, sqlite3",
     "@anthropic-ai/sdk, axios, cheerio, node-telegram-bot-api, lowdb",
     "使用 requests + BeautifulSoup 爬物流頁面 + SQLite 追蹤狀態變化",
     "使用 Axios + Cheerio + lowdb (JSON DB) 追蹤包裹狀態",
     {"hub": ["38-package-tracking.md"]}),

    (53, "異步站會機器人", "Async Standup Bot", "生產力工具", "中級",
     "異步站會機器人 (Async Standup Bot)",
     "anthropic, slack-sdk, apscheduler, sqlite3",
     "@anthropic-ai/sdk, @slack/bolt, node-cron, prisma",
     "使用 slack-sdk + APScheduler + SQLite，Python Slack Bot",
     "使用 @slack/bolt (Slack 官方框架) + Prisma ORM + node-cron",
     {"var": ["team-standup-bot.md"]}),

    (54, "會議時間自動協調", "Meeting Time Auto Coordination", "生產力工具", "中級",
     "會議時間自動協調 (Meeting Time Auto Coordination)",
     "anthropic, google-api-python-client, python-dateutil, pytz",
     "@anthropic-ai/sdk, googleapis, date-fns, date-fns-tz",
     "使用 Google Calendar FreeBusy API + python-dateutil + pytz 時區處理",
     "使用 Google Calendar FreeBusy API + date-fns / date-fns-tz",
     {"var": ["meeting-scheduler.md"], "hub": ["05-calendar-smart-reminder.md"]}),

    # === 商業、行銷與銷售 (55-68) ===
    (55, "競爭對手情報週報", "Competitor Intelligence Weekly", "商業、行銷與銷售", "中級",
     "競爭對手情報週報 (Competitor Intelligence Weekly)",
     "anthropic, beautifulsoup4, requests, pandas, jinja2",
     "@anthropic-ai/sdk, puppeteer, cheerio, handlebars, nodemailer",
     "使用 requests + BeautifulSoup 爬競品網站 + Pandas 趨勢分析 + Jinja2 週報",
     "使用 Puppeteer (處理 JS 渲染頁面) + Cheerio + Nodemailer 寄週報",
     {"var": ["competitor-radar.md"], "hub": ["54-customer-signal-scanner.md"]}),

    (56, "競品定價即時追蹤", "Competitor Pricing Tracker", "商業、行銷與銷售", "中級",
     "競品定價即時追蹤 (Competitor Pricing Tracker)",
     "anthropic, selenium, beautifulsoup4, pandas, sqlite3, plotly",
     "@anthropic-ai/sdk, puppeteer, cheerio, better-sqlite3, chart.js",
     "使用 Selenium 爬動態頁面 + Pandas 價格分析 + Plotly 視覺化圖表",
     "使用 Puppeteer 無頭瀏覽器 + Chart.js 價格趨勢圖",
     {"hub": ["17-price-comparison-shopper.md"], "var": ["price-drop-alerter.md"]}),

    (57, "競品情緒分析", "Competitor Sentiment Analysis", "商業、行銷與銷售", "中高級",
     "競品情緒分析 (Competitor Sentiment Analysis)",
     "anthropic, praw, tweepy, pandas, plotly, wordcloud",
     "@anthropic-ai/sdk, snoowrap, twitter-api-v2, d3-cloud (word cloud), chart.js",
     "使用 PRAW + Tweepy 收集評論 + Claude 情緒分析 + wordcloud 文字雲",
     "使用 snoowrap + twitter-api-v2 + d3-cloud 文字雲 + Chart.js",
     {"var": ["competitor-radar.md"]}),

    (58, "程式化 SEO", "Programmatic SEO", "商業、行銷與銷售", "中級",
     "程式化 SEO (Programmatic SEO)",
     "anthropic, jinja2, beautifulsoup4, requests, sitemap-generator",
     "@anthropic-ai/sdk, handlebars, puppeteer, sitemap, express",
     "使用 Jinja2 模板批量產頁面 + Claude 產 SEO 內容 + sitemap 生成",
     "使用 Handlebars + Express 動態路由 + sitemap 套件 + Puppeteer pre-render",
     {"var": ["seo-content-pipeline.md"]}),

    (59, "HARO 外鏈建設", "HARO Link Building", "商業、行銷與銷售", "中級",
     "HARO 外鏈建設 (HARO Link Building)",
     "anthropic, imaplib, beautifulsoup4, google-api-python-client",
     "@anthropic-ai/sdk, imap-simple, mailparser, nodemailer",
     "使用 imaplib 監控 HARO 郵件 + Claude 篩選匹配 + 自動起草回覆",
     "使用 imap-simple + mailparser + Claude 篩選 + Nodemailer 回覆",
     {}),

    (60, "潛在客戶資料豐富", "Lead Enrichment", "商業、行銷與銷售", "中級",
     "潛在客戶資料豐富 (Lead Enrichment)",
     "anthropic, requests, beautifulsoup4, pandas, openpyxl",
     "@anthropic-ai/sdk, axios, cheerio, xlsx, csv-parse",
     "使用 requests 爬 LinkedIn/公司頁 + Pandas + openpyxl 匯出 Excel",
     "使用 Axios + Cheerio + xlsx 套件匯出 Excel",
     {"var": ["lead-scoring.md"]}),

    (61, "冷外聯自動化", "Cold Outreach Automation", "商業、行銷與銷售", "中級",
     "冷外聯自動化 (Cold Outreach Automation)",
     "anthropic, google-api-python-client, pandas, jinja2, schedule",
     "@anthropic-ai/sdk, nodemailer, csv-parse, handlebars, node-cron",
     "使用 Gmail API 發送 + Pandas 管理聯絡人 + Jinja2 郵件模板 + 排程跟進",
     "使用 Nodemailer (SMTP) + csv-parse + Handlebars 模板 + node-cron",
     {"var": ["cold-outreach.md"]}),

    (62, "廣告效益每日報告", "Ad Performance Daily Report", "商業、行銷與銷售", "中級",
     "廣告效益每日報告 (Ad Performance Daily Report)",
     "anthropic, google-ads-api, facebook-business, pandas, plotly",
     "@anthropic-ai/sdk, google-ads-api, facebook-nodejs-business-sdk, chart.js",
     "使用 google-ads-api + facebook-business SDK + Pandas 分析 + Plotly 圖表",
     "使用 Google Ads API + Facebook Marketing API + Chart.js 報表",
     {}),

    (63, "每週策略備忘錄", "Weekly Strategy Memo", "商業、行銷與銷售", "中級",
     "每週策略備忘錄 (Weekly Strategy Memo)",
     "anthropic, notion-client, google-api-python-client, python-docx",
     "@anthropic-ai/sdk, @notionhq/client, googleapis, docx (officegen)",
     "使用 Notion API 彙整週資料 + Claude 產策略分析 + python-docx 匯出 Word",
     "使用 Notion API + Claude 策略分析 + officegen 匯出 Word/PDF",
     {}),

    (64, "自由工作者案源開發", "Freelancer Lead Generation", "商業、行銷與銷售", "中級",
     "自由工作者案源開發 (Freelancer Lead Generation)",
     "anthropic, beautifulsoup4, requests, sqlite3, schedule",
     "@anthropic-ai/sdk, puppeteer, cheerio, better-sqlite3, node-cron",
     "使用 requests + BeautifulSoup 爬 Upwork/Freelancer + Claude 匹配評分",
     "使用 Puppeteer (處理動態載入) + Cheerio + Claude 匹配",
     {"var": ["freelancer-lead-pipeline.md"]}),

    (65, "網紅發掘與外聯", "Influencer Discovery & Outreach", "商業、行銷與銷售", "中級",
     "網紅發掘與外聯 (Influencer Discovery & Outreach)",
     "anthropic, instagrapi, tweepy, pandas, jinja2",
     "@anthropic-ai/sdk, instagram-private-api, twitter-api-v2, handlebars, nodemailer",
     "使用 instagrapi + tweepy 搜尋網紅 + Pandas 分析 + Jinja2 外聯信模板",
     "使用 Instagram API + Twitter API + Handlebars 模板 + Nodemailer 發信",
     {}),

    (66, "銷售電話準備助手", "Sales Call Prep Assistant", "商業、行銷與銷售", "中級",
     "銷售電話準備助手 (Sales Call Prep Assistant)",
     "anthropic, requests, beautifulsoup4, google-api-python-client, fpdf2",
     "@anthropic-ai/sdk, axios, cheerio, googleapis, pdfkit",
     "使用 requests + BeautifulSoup 爬公司/LinkedIn + Claude 產備忘錄 + FPDF 產 PDF",
     "使用 Axios + Cheerio + Claude 分析 + PDFKit 產 PDF 備忘錄",
     {}),

    (67, "評論追蹤管理", "Review Tracking Manager", "商業、行銷與銷售", "中級",
     "評論追蹤管理 (Review Tracking Manager)",
     "anthropic, google-api-python-client (Google My Business), requests, sqlite3",
     "@anthropic-ai/sdk, googleapis, axios, better-sqlite3, node-cron",
     "使用 Google Business Profile API + requests 爬 Trustpilot + SQLite 追蹤",
     "使用 Google Business API + Axios 爬評論 + better-sqlite3",
     {}),

    (68, "廣告創意 AB 測試", "Ad Creative A/B Testing", "商業、行銷與銷售", "中級",
     "廣告創意 AB 測試 (Ad Creative AB Testing)",
     "anthropic, pillow, pandas, scipy, matplotlib",
     "@anthropic-ai/sdk, sharp, simple-statistics, chartjs-node-canvas",
     "使用 Claude 產廣告變體 + Pillow 產圖 + scipy 統計顯著性檢定 + Matplotlib",
     "使用 Claude 產變體 + Sharp 圖片處理 + simple-statistics 統計 + Chart.js",
     {"var": ["design-feedback.md"]}),

    # === DevOps 與工程 (69-78) ===
    (69, "n8n 工作流程編排", "n8n Workflow Orchestration", "DevOps 與工程", "中級",
     "n8n 工作流程編排 (n8n Workflow Orchestration)",
     "anthropic, requests, pydantic",
     "@anthropic-ai/sdk, axios, zod",
     "使用 requests 操作 n8n REST API + Pydantic 驗證工作流程 JSON",
     "使用 Axios + n8n REST API + Zod schema 驗證",
     {"main": ["n8n-workflow-orchestration.md"]}),

    (70, "自我修復家庭伺服器", "Self-Healing Home Server", "DevOps 與工程", "高級",
     "自我修復家庭伺服器 (Self-Healing Home Server)",
     "anthropic, paramiko, psutil, docker-py, schedule",
     "@anthropic-ai/sdk, ssh2, systeminformation, dockerode, node-cron",
     "使用 paramiko (SSH) + psutil (系統監控) + docker-py (Docker 管理)",
     "使用 ssh2 (SSH) + systeminformation + dockerode (Docker) + node-cron",
     {"main": ["self-healing-home-server.md"], "var": ["server-health-monitor.md"]}),

    (71, "PR 追蹤雷達", "PR Tracking Radar", "DevOps 與工程", "中級",
     "PR 追蹤雷達 (PR Tracking Radar)",
     "anthropic, PyGithub, pandas, jinja2, schedule",
     "@anthropic-ai/sdk, octokit, handlebars, node-cron",
     "使用 PyGithub + Pandas 分析 PR 趨勢 + Jinja2 產報告",
     "使用 Octokit (GitHub 官方 SDK) + Handlebars 模板 + node-cron",
     {"hub": ["49-github-stale-issue-cleanup.md", "67-github-issue-prioritizer.md"], "var": ["pr-review-assistant.md"]}),

    (72, "CI 不穩定測試修復", "CI Flaky Test Fix", "DevOps 與工程", "中高級",
     "CI 不穩定測試修復 (CI Flaky Test Fix)",
     "anthropic, PyGithub, requests, pandas, subprocess",
     "@anthropic-ai/sdk, octokit, axios, child_process, glob",
     "使用 PyGithub 取 CI log + Pandas 分析失敗模式 + Claude 建議修復",
     "使用 Octokit + Axios 取 CI logs + child_process 執行測試",
     {"hub": ["80-test-case-generator.md", "78-bug-pattern-analyzer.md"]}),

    (73, "文件漂移哨兵", "Doc Drift Sentinel", "DevOps 與工程", "中級",
     "文件漂移哨兵 (Doc Drift Sentinel)",
     "anthropic, PyGithub, gitpython, difflib",
     "@anthropic-ai/sdk, octokit, simple-git, diff",
     "使用 GitPython + difflib 比對文件變更 + Claude 判斷是否需更新",
     "使用 simple-git + diff 套件 + Claude 分析漂移",
     {"hub": ["50-night-documentation-fixer.md", "46-markdown-health-check.md"]}),

    (74, "變更日誌自動化", "Changelog Automation", "DevOps 與工程", "中級",
     "變更日誌自動化 (Changelog Automation)",
     "anthropic, gitpython, pydantic, jinja2",
     "@anthropic-ai/sdk, simple-git, conventional-changelog, handlebars",
     "使用 GitPython 解析 commit + Pydantic 結構化 + Jinja2 產 CHANGELOG",
     "使用 simple-git + conventional-changelog (業界標準) + Handlebars",
     {"var": ["changelog-generator.md"]}),

    (75, "依賴套件審計", "Dependency Audit", "DevOps 與工程", "中級",
     "依賴套件審計 (Dependency Audit)",
     "anthropic, pip-audit, safety, requests, subprocess",
     "@anthropic-ai/sdk, npm-check-updates, audit-ci, axios",
     "使用 pip-audit + safety 掃描 Python 漏洞 + Claude 產修復建議",
     "使用 npm audit + npm-check-updates + audit-ci + Claude 修復建議",
     {"hub": ["82-dependency-update-checker.md", "89-skill-supply-chain-audit.md"]}),

    (76, "Sentry 事故回顧報告", "Sentry Incident Retrospective", "DevOps 與工程", "中級",
     "Sentry 事故回顧報告 (Sentry Incident Retrospective)",
     "anthropic, requests (Sentry API), pandas, jinja2",
     "@anthropic-ai/sdk, @sentry/node, axios, handlebars",
     "使用 Sentry REST API + Pandas 分析錯誤趨勢 + Claude 產回顧報告",
     "使用 @sentry/node SDK + Axios (Sentry API) + Claude 回顧",
     {"hub": ["100-security-incident-response.md"]}),

    (77, "部署自動化流水線", "Deployment Automation Pipeline", "DevOps 與工程", "中高級",
     "部署自動化流水線 (Deployment Automation Pipeline)",
     "anthropic, paramiko, docker-py, fabric, subprocess",
     "@anthropic-ai/sdk, ssh2, dockerode, execa, github-actions-toolkit",
     "使用 Fabric (SSH deployment) + docker-py + subprocess 執行腳本",
     "使用 ssh2 + dockerode + execa (better child_process) + GitHub Actions",
     {"var": ["deployment-pipeline.md"]}),

    (78, "程式碼自動文件化", "Code Auto Documentation", "DevOps 與工程", "中級",
     "程式碼自動文件化 (Code Auto Documentation)",
     "anthropic, ast (Python AST), jinja2, gitpython",
     "@anthropic-ai/sdk, typescript (compiler API), jsdoc, handlebars",
     "使用 Python ast 模組解析 AST + Claude 產 docstring + Jinja2 產文件",
     "使用 TypeScript Compiler API 解析 + JSDoc 格式 + Handlebars 模板",
     {"hub": ["36-code-to-documentation.md", "79-api-documentation-generator.md"]}),

    # === 安全與合規 (79-84) ===
    (79, "SSH 金鑰安全掃描", "SSH Key Security Scan", "安全與合規", "中級",
     "SSH 金鑰安全掃描 (SSH Key Security Scan)",
     "anthropic, paramiko, cryptography, pathlib",
     "@anthropic-ai/sdk, ssh2, node-forge, glob",
     "使用 paramiko + cryptography 解析 SSH 金鑰強度 + Claude 安全建議",
     "使用 ssh2 + node-forge 密碼學庫 + glob 掃描檔案",
     {"hub": ["86-ssh-key-scanner.md"]}),

    (80, "AWS 憑證安全掃描", "AWS Credential Security Scan", "安全與合規", "中級",
     "AWS 憑證安全掃描 (AWS Credential Security Scan)",
     "anthropic, boto3, trufflehog (subprocess), pathlib",
     "@anthropic-ai/sdk, @aws-sdk/client-iam, trufflehog (child_process), glob",
     "使用 boto3 (AWS SDK) + trufflehog 掃描 + Claude 風險評估",
     "使用 AWS SDK v3 + trufflehog CLI + Claude 風險評估",
     {"hub": ["87-aws-credential-scanner.md"]}),

    (81, "Git 歷史敏感資訊清理", "Git History Sensitive Data Cleanup", "安全與合規", "中級",
     "Git 歷史敏感資訊清理 (Git History Sensitive Data Cleanup)",
     "anthropic, gitpython, trufflehog (subprocess), re",
     "@anthropic-ai/sdk, simple-git, trufflehog3 (child_process), glob",
     "使用 GitPython + trufflehog 掃描 + git filter-branch/BFG 清理",
     "使用 simple-git + trufflehog CLI + git filter-repo 清理",
     {"hub": ["91-git-history-cleaner.md", "99-sensitive-data-detector.md"]}),

    (82, "API 安全測試", "API Security Testing", "安全與合規", "中高級",
     "API 安全測試 (API Security Testing)",
     "anthropic, requests, pydantic, aiohttp",
     "@anthropic-ai/sdk, axios, zod, got",
     "使用 requests + aiohttp (async) 多種攻擊向量測試 + Pydantic 報告結構",
     "使用 Axios + Got (HTTP client) + Zod 報告驗證",
     {"hub": ["90-api-security-tester.md"]}),

    (83, "漏洞自動掃描", "Vulnerability Auto Scan", "安全與合規", "中級",
     "漏洞自動掃描 (Vulnerability Auto Scan)",
     "anthropic, subprocess (nmap/trivy), requests, jinja2",
     "@anthropic-ai/sdk, child_process (nmap/trivy), axios, handlebars",
     "使用 subprocess 呼叫 nmap/trivy + Claude 分析 + Jinja2 報告",
     "使用 child_process 呼叫掃描工具 + Claude 分析 + Handlebars 報告",
     {"hub": ["96-vulnerability-scanner-automation.md"]}),

    (84, "法規合規性自動檢查", "Regulatory Compliance Auto Check", "安全與合規", "中高級",
     "法規合規性自動檢查 (Regulatory Compliance Auto Check)",
     "anthropic, pydantic, pandas, jinja2, PyPDF2",
     "@anthropic-ai/sdk, zod, csv-parse, handlebars, pdf-parse",
     "使用 Pydantic 定義合規規則 + Pandas 分析 + Claude GDPR/SOC2 檢查",
     "使用 Zod schema 定義規則 + csv-parse + Claude 合規分析",
     {"hub": ["97-compliance-checker.md", "98-access-permission-audit.md"]}),

    # === 監控與維運 (85-92) ===
    (85, "SLA 守護者", "SLA Guardian", "監控與維運", "中級",
     "SLA 守護者 (SLA Guardian)",
     "anthropic, requests, prometheus-client, sqlite3, schedule",
     "@anthropic-ai/sdk, axios, prom-client, better-sqlite3, node-cron",
     "使用 requests 健康檢查 + prometheus-client 指標 + SQLite 歷史",
     "使用 Axios + prom-client (Prometheus) + better-sqlite3",
     {"hub": ["57-heartbeat-state-monitor.md"]}),

    (86, "網站可用性監控", "Website Uptime Monitor", "監控與維運", "初中級",
     "網站可用性監控 (Website Uptime Monitor)",
     "anthropic, requests, sqlite3, schedule, smtplib",
     "@anthropic-ai/sdk, axios, better-sqlite3, node-cron, nodemailer",
     "使用 requests + smtplib (內建 SMTP) + SQLite + schedule",
     "使用 Axios + Nodemailer + better-sqlite3 + node-cron",
     {"hub": ["60-website-uptime-monitor.md"]}),

    (87, "SSL 憑證到期監控", "SSL Certificate Expiry Monitor", "監控與維運", "初中級",
     "SSL 憑證到期監控 (SSL Certificate Expiry Monitor)",
     "anthropic, ssl, socket, cryptography, schedule",
     "@anthropic-ai/sdk, tls (built-in), node-cron, nodemailer",
     "使用 ssl + socket (內建) + cryptography 解析憑證詳情",
     "使用 Node.js tls 內建模組 + node-cron 排程",
     {"hub": ["61-ssl-certificate-monitor.md"]}),

    (88, "資料庫自動備份", "Database Auto Backup", "監控與維運", "中級",
     "資料庫自動備份 (Database Auto Backup)",
     "anthropic, subprocess, boto3, paramiko, schedule",
     "@anthropic-ai/sdk, child_process, @aws-sdk/client-s3, ssh2, node-cron",
     "使用 subprocess (mysqldump/pg_dump) + boto3 上傳 S3 + paramiko SSH",
     "使用 child_process + AWS S3 SDK + ssh2 遠端備份",
     {"hub": ["62-database-backup-automation.md"]}),

    (89, "AI 模型費用追蹤中心", "AI Model Cost Tracker", "監控與維運", "中級",
     "AI 模型費用追蹤中心 (AI Model Cost Tracker)",
     "anthropic, requests, pandas, plotly, sqlite3",
     "@anthropic-ai/sdk, axios, chart.js, better-sqlite3, express",
     "使用 requests (各家 API usage endpoint) + Pandas 分析 + Plotly 圖表",
     "使用 Axios 取 API 用量 + Chart.js 視覺化 + Express Web 儀表板",
     {"hub": ["47-cost-tracking.md", "71-token-usage-optimizer.md"], "var": ["ai-cost-tracker.md"]}),

    (90, "每週事故摘要", "Weekly Incident Summary", "監控與維運", "中級",
     "每週事故摘要 (Weekly Incident Summary)",
     "anthropic, requests (PagerDuty/Sentry API), pandas, jinja2",
     "@anthropic-ai/sdk, axios, handlebars, nodemailer",
     "使用 requests 取 PagerDuty/Sentry 事故 + Pandas 分析 + Jinja2 週報",
     "使用 Axios + PagerDuty/Sentry API + Handlebars + Nodemailer 寄報告",
     {"hub": ["100-security-incident-response.md", "51-log-anomaly-detection.md"]}),

    (91, "API 速率限制監控", "API Rate Limit Monitor", "監控與維運", "中級",
     "API 速率限制監控 (API Rate Limit Monitor)",
     "anthropic, requests, sqlite3, matplotlib, schedule",
     "@anthropic-ai/sdk, axios, better-sqlite3, chartjs-node-canvas, node-cron",
     "使用 requests 檢查 rate limit headers + Matplotlib 圖表 + SQLite 歷史",
     "使用 Axios interceptor 攔截 headers + Chart.js + better-sqlite3",
     {"hub": ["64-api-rate-limit-monitor.md"]}),

    (92, "智慧警報彙整去重", "Smart Alert Aggregation & Dedup", "監控與維運", "中級",
     "智慧警報彙整去重 (Smart Alert Aggregation & Dedup)",
     "anthropic, redis, fuzzywuzzy, schedule, python-telegram-bot",
     "@anthropic-ai/sdk, ioredis, fuse.js (fuzzy search), node-cron, telegraf",
     "使用 Redis 暫存 + fuzzywuzzy 模糊匹配去重 + Claude 彙整",
     "使用 ioredis + Fuse.js 模糊搜尋去重 + Claude 彙整摘要",
     {"hub": ["65-smart-alert-aggregator.md"]}),

    # === 研究與學習 (93-101) ===
    (93, "AI 財報追蹤器", "AI Financial Report Tracker", "研究與學習", "中級",
     "AI 財報追蹤器 (AI Financial Report Tracker)",
     "anthropic, yfinance, pandas, plotly, requests",
     "@anthropic-ai/sdk, yahoo-finance2, chart.js, axios",
     "使用 yfinance + Pandas 財務分析 + Plotly 互動圖表",
     "使用 yahoo-finance2 + Chart.js 圖表 + Axios",
     {"main": ["earnings-tracker.md"]}),

    (94, "個人知識庫 (RAG)", "Personal Knowledge Base (RAG)", "研究與學習", "中高級",
     "個人知識庫 (RAG) (Personal Knowledge Base RAG)",
     "anthropic, chromadb, sentence-transformers, flask, PyPDF2",
     "@anthropic-ai/sdk, lancedb, @xenova/transformers, express, pdf-parse",
     "使用 ChromaDB + sentence-transformers 本地向量 + Flask Web UI",
     "使用 LanceDB (零設定向量 DB) + Transformers.js ONNX + Express",
     {"main": ["knowledge-base-rag.md"], "hub": ["25-personal-knowledge-base.md"]}),

    (95, "市場調研與 MVP 工廠", "Market Research & MVP Factory", "研究與學習", "高級",
     "市場調研與 MVP 工廠 (Market Research & MVP Factory)",
     "anthropic, requests, beautifulsoup4, pandas, flask, pydantic",
     "@anthropic-ai/sdk, puppeteer, cheerio, express, next.js (scaffold)",
     "使用 requests 爬市場數據 + Pandas 分析 + Flask 產 MVP + Pydantic 驗證",
     "使用 Puppeteer 爬數據 + Express API + Next.js scaffold 快速 MVP",
     {"main": ["market-research-product-factory.md"], "var": ["market-research.md"]}),

    (96, "建造前點子驗證器", "Pre-Build Idea Validator", "研究與學習", "中級",
     "建造前點子驗證器 (Pre-Build Idea Validator)",
     "anthropic, requests, beautifulsoup4, pydantic, jinja2",
     "@anthropic-ai/sdk, axios, cheerio, zod, handlebars",
     "使用 requests 爬競品 + Claude 多維度驗證 + Pydantic 結構化報告",
     "使用 Axios + Cheerio + Claude 驗證 + Zod 報告結構",
     {"main": ["pre-build-idea-validator.md"]}),

    (97, "語義記憶搜尋", "Semantic Memory Search", "研究與學習", "中高級",
     "語義記憶搜尋 (Semantic Memory Search)",
     "anthropic, chromadb, sentence-transformers, click",
     "@anthropic-ai/sdk, lancedb, @xenova/transformers, commander",
     "使用 ChromaDB + sentence-transformers (本地嵌入) + Click CLI",
     "使用 LanceDB + Transformers.js (ONNX 本地) + Commander CLI",
     {"main": ["semantic-memory-search.md"]}),

    (98, "YouTube 研究分析桌", "YouTube Research Desk", "研究與學習", "中級",
     "YouTube 研究分析桌 (YouTube Research Desk)",
     "anthropic, google-api-python-client, youtube-transcript-api, pandas, plotly",
     "@anthropic-ai/sdk, googleapis, youtubei.js, chart.js, express",
     "使用 YouTube Data API + youtube-transcript-api + Pandas 分析 + Plotly",
     "使用 youtubei.js (InnerTube, 免 key) + Chart.js + Express 看板",
     {"main": ["youtube-content-pipeline.md"], "hub": ["40-youtube-analytics-pull.md"]}),

    (99, "每週研究情報摘要", "Weekly Research Intel Summary", "研究與學習", "中級",
     "每週研究情報摘要 (Weekly Research Intel Summary)",
     "anthropic, feedparser, requests, arxiv, jinja2",
     "@anthropic-ai/sdk, rss-parser, axios, handlebars, nodemailer",
     "使用 feedparser + arxiv 套件 + Claude 摘要 + Jinja2 週報",
     "使用 rss-parser + Axios (arXiv API) + Handlebars + Nodemailer",
     {"hub": ["52-rss-news-aggregator.md"]}),

    (100, "內容靈感挖掘機", "Content Inspiration Miner", "研究與學習", "中級",
     "內容靈感挖掘機 (Content Inspiration Miner)",
     "anthropic, praw, tweepy, feedparser, wordcloud",
     "@anthropic-ai/sdk, snoowrap, twitter-api-v2, rss-parser, d3-cloud",
     "使用 PRAW + Tweepy + feedparser 多源挖掘 + wordcloud 視覺化",
     "使用 snoowrap + twitter-api-v2 + rss-parser + d3-cloud 文字雲",
     {}),

    (101, "產品需求文件起草", "Product Requirements Doc Draft", "研究與學習", "中級",
     "產品需求文件起草 (Product Requirements Doc Draft)",
     "anthropic, python-docx, pydantic, jinja2",
     "@anthropic-ai/sdk, officegen, zod, handlebars, pdf-lib",
     "使用 Claude + Pydantic 結構化需求 + python-docx 匯出 Word + Jinja2 模板",
     "使用 Claude + Zod schema + officegen (Word) + pdf-lib (PDF) 匯出",
     {"main": ["overnight-mini-app-builder.md"]}),

    # === 金融與交易 (102-107) ===
    (102, "Polymarket 自動交易", "Polymarket Auto Trading", "金融與交易", "高級",
     "Polymarket 自動交易 (Polymarket Auto Trading)",
     "anthropic, web3, requests, pandas, ccxt",
     "@anthropic-ai/sdk, ethers.js, axios, ccxt",
     "使用 web3.py + ccxt + Pandas 分析 + Claude 交易策略",
     "使用 ethers.js (Web3) + ccxt + Claude 策略分析",
     {"main": ["polymarket-autopilot.md"], "hub": ["48-polymarket-scanner.md"]}),

    (103, "投資案流程管理", "Investment Deal Pipeline", "金融與交易", "中級",
     "投資案流程管理 (Investment Deal Pipeline)",
     "anthropic, notion-client, pandas, openpyxl, jinja2",
     "@anthropic-ai/sdk, @notionhq/client, xlsx, handlebars, express",
     "使用 notion-client + Pandas + openpyxl 匯出 + Jinja2 報告",
     "使用 Notion API + xlsx 套件 + Express 看板 + Handlebars",
     {"hub": ["49-investor-deal-flow.md"]}),

    (104, "投資組合監控", "Portfolio Monitor", "金融與交易", "中級",
     "投資組合監控 (Portfolio Monitor)",
     "anthropic, yfinance, pandas, plotly, schedule",
     "@anthropic-ai/sdk, yahoo-finance2, chart.js, node-cron, nodemailer",
     "使用 yfinance + Pandas 計算報酬/風險 + Plotly 互動圖表 + schedule",
     "使用 yahoo-finance2 + Chart.js + node-cron + Nodemailer 日報",
     {"hub": ["50-portfolio-monitoring.md"], "var": ["stock-portfolio-tracker.md"]}),

    (105, "訂閱費用審計", "Subscription Cost Audit", "金融與交易", "初中級",
     "訂閱費用審計 (Subscription Cost Audit)",
     "anthropic, google-api-python-client, pandas, matplotlib",
     "@anthropic-ai/sdk, googleapis, chart.js, csv-parse",
     "使用 Gmail API 掃描訂閱郵件 + Pandas 分析 + Matplotlib 圖表",
     "使用 Gmail API + csv-parse 匯入 + Chart.js 視覺化",
     {"var": ["expense-tracker.md"]}),

    (106, "發票處理自動化", "Invoice Processing Automation", "金融與交易", "中級",
     "發票處理自動化 (Invoice Processing Automation)",
     "anthropic, pdfplumber, pytesseract, pandas, openpyxl",
     "@anthropic-ai/sdk, pdf-parse, tesseract.js, xlsx",
     "使用 pdfplumber + pytesseract (OCR) + Pandas + openpyxl 匯出 Excel",
     "使用 pdf-parse + tesseract.js (瀏覽器/Node OCR) + xlsx 匯出",
     {"var": ["invoice-chaser.md"]}),

    (107, "個人財務追蹤", "Personal Finance Tracker", "金融與交易", "初中級",
     "個人財務追蹤 (Personal Finance Tracker)",
     "anthropic, sqlite3, pandas, matplotlib, python-telegram-bot",
     "@anthropic-ai/sdk, better-sqlite3, chart.js, telegraf, express",
     "使用 SQLite + Pandas 分析支出 + Matplotlib 圖表 + Telegram bot 記帳",
     "使用 better-sqlite3 + Chart.js + Express Web UI + Telegraf bot",
     {"hub": ["21-personal-finance-tracker.md"], "var": ["expense-tracker.md"]}),

    # === 健康與個人成長 (108-113) ===
    (108, "睡眠品質優化", "Sleep Quality Optimizer", "健康與個人成長", "中級",
     "睡眠品質優化 (Sleep Quality Optimizer)",
     "anthropic, fitparse, pandas, matplotlib, sqlite3",
     "@anthropic-ai/sdk, csv-parse, chart.js, better-sqlite3, express",
     "使用 fitparse 解析 Fitbit/Garmin 數據 + Pandas 分析 + Matplotlib",
     "使用 csv-parse (匯出 CSV) + Chart.js 視覺化 + Express 看板",
     {"var": ["sleep-optimizer.md"]}),

    (109, "心理健康定期打卡", "Mental Health Check-In", "健康與個人成長", "初中級",
     "心理健康定期打卡 (Mental Health Check-In)",
     "anthropic, python-telegram-bot, sqlite3, matplotlib, schedule",
     "@anthropic-ai/sdk, telegraf, lowdb, chartjs-node-canvas, node-cron",
     "使用 Telegram bot 互動打卡 + SQLite + Matplotlib 情緒趨勢圖",
     "使用 Telegraf + lowdb (JSON DB) + Chart.js 情緒圖 + node-cron",
     {"var": ["mental-health-checkin.md"]}),

    (110, "健身打卡問責系統", "Fitness Accountability System", "健康與個人成長", "中級",
     "健身打卡問責系統 (Fitness Accountability System)",
     "anthropic, python-telegram-bot, sqlite3, matplotlib, schedule",
     "@anthropic-ai/sdk, discord.js, better-sqlite3, chart.js, node-cron",
     "使用 Telegram bot 打卡 + SQLite + Matplotlib + schedule 提醒",
     "使用 Discord.js bot (群組問責) + better-sqlite3 + Chart.js",
     {"var": ["workout-accountability.md"]}),

    (111, "個人學習路徑規劃", "Personal Learning Path Planner", "健康與個人成長", "中級",
     "個人學習路徑規劃 (Personal Learning Path Planner)",
     "anthropic, networkx, matplotlib, sqlite3, click",
     "@anthropic-ai/sdk, graphology, mermaid-js, better-sqlite3, commander",
     "使用 NetworkX 建立技能樹圖 + Matplotlib 視覺化 + Click CLI",
     "使用 Graphology 技能圖 + Mermaid.js 流程圖 + Commander CLI",
     {"var": ["learning-path-creator.md"]}),

    (112, "健身數據彙整分析", "Fitness Data Aggregation", "健康與個人成長", "中級",
     "健身數據彙整分析 (Fitness Data Aggregation)",
     "anthropic, fitparse, pandas, plotly, requests",
     "@anthropic-ai/sdk, strava-v3, chart.js, axios, express",
     "使用 fitparse (Garmin FIT) + Pandas 分析 + Plotly 互動圖",
     "使用 strava-v3 (Strava API) + Chart.js + Express 看板",
     {"var": ["workout-accountability.md"]}),

    (113, "採購與營養優化", "Grocery & Nutrition Optimizer", "健康與個人成長", "中級",
     "採購與營養優化 (Grocery & Nutrition Optimizer)",
     "anthropic, requests (Edamam/USDA API), pandas, matplotlib",
     "@anthropic-ai/sdk, axios (Nutritionix API), chart.js, express",
     "使用 Edamam/USDA API + Pandas 營養分析 + Matplotlib 圖表",
     "使用 Nutritionix API + Chart.js + Express 計畫頁面",
     {"var": ["grocery-optimizer.md", "nutrition-tracker.md"]}),

    # === AI 記憶與代理架構 (114-118) ===
    (114, "三層記憶架構系統", "Three-Tier Memory Architecture", "AI 記憶與代理架構", "高級",
     "三層記憶架構系統 (Three-Tier Memory Architecture)",
     "anthropic, chromadb, redis, sqlite3, pydantic",
     "@anthropic-ai/sdk, lancedb, ioredis, better-sqlite3, zod",
     "使用 Redis (短期) + SQLite (中期) + ChromaDB (長期向量) 三層記憶",
     "使用 ioredis (短期) + better-sqlite3 (中期) + LanceDB (長期向量)",
     {"hub": ["66-three-tier-memory-system.md"]}),

    (115, "知識圖譜重建", "Knowledge Graph Reconstruction", "AI 記憶與代理架構", "高級",
     "知識圖譜重建 (Knowledge Graph Reconstruction)",
     "anthropic, networkx, chromadb, sentence-transformers, pyvis",
     "@anthropic-ai/sdk, graphology, lancedb, @xenova/transformers, vis-network",
     "使用 NetworkX + ChromaDB + pyvis (互動圖譜視覺化)",
     "使用 Graphology + LanceDB + vis-network (瀏覽器互動圖譜)",
     {"hub": ["73-knowledge-graph-rebuilder.md"]}),

    (116, "每週記憶封存", "Weekly Memory Archive", "AI 記憶與代理架構", "中級",
     "每週記憶封存 (Weekly Memory Archive)",
     "anthropic, chromadb, sqlite3, schedule, jinja2",
     "@anthropic-ai/sdk, lancedb, better-sqlite3, node-cron, handlebars",
     "使用 ChromaDB + SQLite + schedule 週排程 + Jinja2 封存報告",
     "使用 LanceDB + better-sqlite3 + node-cron + Handlebars 報告",
     {"hub": ["74-weekly-memory-archive.md"]}),

    (117, "每日自我提升 Cron", "Daily Self-Improvement Cron", "AI 記憶與代理架構", "中級",
     "每日自我提升 Cron (Daily Self-Improvement Cron)",
     "anthropic, chromadb, sqlite3, schedule, rich",
     "@anthropic-ai/sdk, lancedb, lowdb, node-cron, chalk",
     "使用 ChromaDB 記憶 + SQLite 追蹤 + Rich 終端報告 + schedule",
     "使用 LanceDB + lowdb + Chalk 彩色輸出 + node-cron",
     {"hub": ["39-daily-self-improvement-cron.md"]}),

    (118, "夜間自動化回報追蹤", "Nightly Automation Report Tracker", "AI 記憶與代理架構", "中級",
     "夜間自動化回報追蹤 (Nightly Automation Report Tracker)",
     "anthropic, sqlite3, pandas, jinja2, schedule, smtplib",
     "@anthropic-ai/sdk, better-sqlite3, chart.js, handlebars, node-cron, nodemailer",
     "使用 SQLite + Pandas 分析自動化執行結果 + Jinja2 + smtplib 寄報告",
     "使用 better-sqlite3 + Chart.js 圖表 + Handlebars + Nodemailer",
     {"hub": ["58-night-work-roi-tracker.md", "44-7-sub-agent-night-parallel.md"]}),
]


# ============================================================
# SOURCE FILE READER
# ============================================================
def read_source_files(source_files):
    """Read all source files for a use case and combine them."""
    combined = ""
    for repo_key, filenames in source_files.items():
        repo_path = REPOS.get(repo_key, "")
        for fname in filenames:
            fpath = os.path.join(repo_path, fname)
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                combined += f"\n\n--- SOURCE: {repo_key}/{fname} ---\n\n{content}"
    return combined[:8000]  # Limit to avoid token overflow


# ============================================================
# CLAUDE API CALLER
# ============================================================
def call_claude(system_prompt, user_prompt, max_tokens=6000):
    """Call Claude API with retry and rate limit handling."""
    import anthropic
    client = anthropic.Anthropic()

    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "overloaded" in err.lower() or "529" in err:
                wait = (2 ** attempt) * 10
                print(f"    Rate limited, waiting {wait}s... (attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                print(f"    API error: {err}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(5)
                else:
                    raise
    raise Exception("Max retries exceeded")


# ============================================================
# PROMPTS
# ============================================================

SYSTEM_PYTHON = """你是一位 Python 自動化教學專家。你的任務是為一個 Claude Code Skill 寫一份完整的 Python 實作教學。

要求：
1. 所有說明文字用繁體中文
2. 程式碼註解用英文
3. 必須使用指定的 Python 套件，寫出完整可跑的程式碼（不能有 TODO 或 placeholder）
4. 每個檔案的程式碼都要完整，學生可以直接複製貼上執行
5. 包含：所需套件（含版本號）、前置準備 checklist、專案結構、Step by Step 實作、測試步驟、常見陷阱
6. 輸出格式必須是 SKILL.md 格式，開頭有 YAML frontmatter

重要：程式碼必須是真正能跑的，不能只是框架或骨架。"""

SYSTEM_NODEJS = """你是一位 Node.js 自動化教學專家。你的任務是為一個 Claude Code Skill 寫一份完整的 Node.js 實作教學。

要求：
1. 所有說明文字用繁體中文
2. 程式碼註解用英文
3. 必須使用指定的 Node.js 套件，寫出完整可跑的程式碼（不能有 TODO 或 placeholder）
4. 使用 ES Modules (import/export)，package.json 設定 "type": "module"
5. 每個檔案的程式碼都要完整，學生可以直接複製貼上執行
6. 包含：所需套件（含版本號）、前置準備 checklist、專案結構、Step by Step 實作、測試步驟、常見陷阱
7. 輸出格式必須是 SKILL.md 格式，開頭有 YAML frontmatter
8. 排程使用 node-cron，持久化推薦 pm2

重要：程式碼必須是真正能跑的，不能只是框架或骨架。跟 Python 版本要使用不同的技術方案和套件。"""

SYSTEM_COMPARE = """你是一位技術方案比較專家。請為 Python 和 Node.js 兩個實作方案寫一份詳細比較文件。

要求：
1. 繁體中文撰寫
2. 包含：方案總覽表、技術差異詳解、適用場景、效能比較、學習曲線、部署方式比較、成本比較
3. 給出明確推薦（不同場景推薦不同方案）
4. 輸出格式必須是 SKILL.md 格式，開頭有 YAML frontmatter"""


def make_python_prompt(num, cn, en, cat, diff, folder, py_libs, py_approach, source_text):
    return f"""請為以下 Use Case 寫完整的 Python 實作教學 SKILL.md：

## Use Case 資訊
- 編號: #{num:03d}
- 中文名: {cn}
- 英文名: {en}
- 分類: {cat}
- 難度: {diff}
- 資料夾名: {folder}

## Python 技術方案
- 使用套件: {py_libs}
- 技術路線: {py_approach}

## YAML Frontmatter 格式（必須完全照這個格式）
```yaml
---
name: {folder}/python
description: "Use Case #{num:03d} Python 方案: {cn}。{py_approach}"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---
```

## 原始參考資料
{source_text[:4000] if source_text else f"本案例需要建立一個 {cn} ({en}) 的自動化系統。"}

請寫出完整的 SKILL.md，包含完整可執行的程式碼。每個 Python 檔案都要有完整實作，不能有 TODO。"""


def make_nodejs_prompt(num, cn, en, cat, diff, folder, js_libs, js_approach, source_text):
    return f"""請為以下 Use Case 寫完整的 Node.js 實作教學 SKILL.md：

## Use Case 資訊
- 編號: #{num:03d}
- 中文名: {cn}
- 英文名: {en}
- 分類: {cat}
- 難度: {diff}
- 資料夾名: {folder}

## Node.js 技術方案
- 使用套件: {js_libs}
- 技術路線: {js_approach}

## YAML Frontmatter 格式（必須完全照這個格式）
```yaml
---
name: {folder}/nodejs
description: "Use Case #{num:03d} Node.js 方案: {cn}。{js_approach}"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---
```

## 原始參考資料
{source_text[:4000] if source_text else f"本案例需要建立一個 {cn} ({en}) 的自動化系統。"}

請寫出完整的 SKILL.md，包含完整可執行的程式碼。使用 ES Modules。每個 JS 檔案都要有完整實作，不能有 TODO。
注意：跟 Python 版本要使用不同的核心套件和架構方式。"""


def make_compare_prompt(num, cn, en, cat, diff, folder, py_libs, js_libs, py_approach, js_approach):
    return f"""請為以下 Use Case 的 Python 和 Node.js 兩個方案寫比較文件：

## Use Case 資訊
- 編號: #{num:03d}
- 名稱: {cn} ({en})
- 分類: {cat}
- 難度: {diff}

## Python 方案
- 套件: {py_libs}
- 技術路線: {py_approach}

## Node.js 方案
- 套件: {js_libs}
- 技術路線: {js_approach}

## YAML Frontmatter 格式
```yaml
---
name: {folder}/compare
description: "Use Case #{num:03d} 方案比較: {cn}。Python ({py_libs.split(',')[0].strip()}) vs Node.js ({js_libs.split(',')[0].strip()}) 完整比較。"
---
```

請產生完整的比較 SKILL.md，包含對照表、技術差異、推薦場景等。"""


def make_main_prompt(num, cn, en, cat, diff, folder, py_approach, js_approach, source_text):
    return f"""請為以下 Use Case 寫主頁 SKILL.md（概述頁，不含程式碼）：

## Use Case 資訊
- 編號: #{num:03d}
- 中文名: {cn}
- 英文名: {en}
- 分類: {cat}
- 難度: {diff}
- 資料夾名: {folder}

## 子指令
- `/{folder}/python` — Python 方案: {py_approach}
- `/{folder}/nodejs` — Node.js 方案: {js_approach}
- `/{folder}/compare` — 兩方案比較

## YAML Frontmatter 格式
```yaml
---
name: {folder}
description: "Use Case #{num:03d}: {cn} ({en}) - 輸入 /{folder}/python 或 /{folder}/nodejs 選擇方案，/{folder}/compare 比較兩方案。"
---
```

## 原始參考資料
{source_text[:2000] if source_text else ""}

請產生概述 SKILL.md，包含：一句話描述、功能需求、核心技術棧、成本估算、子指令導航表。不需要程式碼。"""


# ============================================================
# PROGRESS TRACKING
# ============================================================
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


# ============================================================
# MAIN
# ============================================================
def main():
    progress = load_progress()
    total = len(USECASES)
    skipped = 0
    generated = 0
    errors = []

    print("=" * 70)
    print(f"Regenerate Skills v2 — {datetime.now():%Y-%m-%d %H:%M}")
    print(f"Total cases: {total}")
    print(f"Already done: {len([k for k, v in progress.items() if v.get('done')])}")
    print("=" * 70)

    for idx, case in enumerate(USECASES):
        num, cn, en, cat, diff, folder, py_libs, js_libs, py_approach, js_approach, source_files = case
        case_key = f"{num:03d}"

        # Skip #001 (manually crafted)
        if num == 1:
            print(f"\n[{idx+1}/{total}] #{num:03d} {cn} — SKIP (manually crafted)")
            skipped += 1
            continue

        # Skip if already completed
        if progress.get(case_key, {}).get("done"):
            print(f"\n[{idx+1}/{total}] #{num:03d} {cn} — SKIP (already done)")
            skipped += 1
            continue

        print(f"\n[{idx+1}/{total}] #{num:03d} {cn} ({en})")
        print(f"  Python: {py_libs}")
        print(f"  Node.js: {js_libs}")

        # Read source material
        source_text = read_source_files(source_files)

        # Ensure directories exist
        skill_dir = os.path.join(SKILLS_DIR, folder)
        for sub in ["", "python", "nodejs", "compare"]:
            os.makedirs(os.path.join(skill_dir, sub), exist_ok=True)

        case_progress = progress.get(case_key, {})

        try:
            # Generate main SKILL.md
            if not case_progress.get("main"):
                print("  → Generating main SKILL.md...")
                content = call_claude(
                    "你是 Claude Code Skill 文件撰寫專家。用繁體中文撰寫。",
                    make_main_prompt(num, cn, en, cat, diff, folder, py_approach, js_approach, source_text),
                    max_tokens=3000
                )
                with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(content)
                case_progress["main"] = True
                save_progress({**progress, case_key: case_progress})
                print("    ✓ main done")
                time.sleep(DELAY_BETWEEN_CALLS)

            # Generate Python SKILL.md
            if not case_progress.get("python"):
                print("  → Generating Python SKILL.md...")
                content = call_claude(
                    SYSTEM_PYTHON,
                    make_python_prompt(num, cn, en, cat, diff, folder, py_libs, py_approach, source_text),
                    max_tokens=8000
                )
                with open(os.path.join(skill_dir, "python", "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(content)
                case_progress["python"] = True
                save_progress({**progress, case_key: case_progress})
                print("    ✓ python done")
                time.sleep(DELAY_BETWEEN_CALLS)

            # Generate Node.js SKILL.md
            if not case_progress.get("nodejs"):
                print("  → Generating Node.js SKILL.md...")
                content = call_claude(
                    SYSTEM_NODEJS,
                    make_nodejs_prompt(num, cn, en, cat, diff, folder, js_libs, js_approach, source_text),
                    max_tokens=8000
                )
                with open(os.path.join(skill_dir, "nodejs", "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(content)
                case_progress["nodejs"] = True
                save_progress({**progress, case_key: case_progress})
                print("    ✓ nodejs done")
                time.sleep(DELAY_BETWEEN_CALLS)

            # Generate Compare SKILL.md
            if not case_progress.get("compare"):
                print("  → Generating Compare SKILL.md...")
                content = call_claude(
                    SYSTEM_COMPARE,
                    make_compare_prompt(num, cn, en, cat, diff, folder, py_libs, js_libs, py_approach, js_approach),
                    max_tokens=4000
                )
                with open(os.path.join(skill_dir, "compare", "SKILL.md"), "w", encoding="utf-8") as f:
                    f.write(content)
                case_progress["compare"] = True
                save_progress({**progress, case_key: case_progress})
                print("    ✓ compare done")

            # Mark as done
            case_progress["done"] = True
            case_progress["timestamp"] = datetime.now().isoformat()
            progress[case_key] = case_progress
            save_progress(progress)
            generated += 1
            print(f"  ✅ #{num:03d} complete!")

            time.sleep(DELAY_BETWEEN_CASES)

        except Exception as e:
            error_msg = f"#{num:03d} {cn}: {str(e)}"
            errors.append(error_msg)
            print(f"  ❌ Error: {e}")
            traceback.print_exc()
            progress[case_key] = case_progress
            save_progress(progress)
            time.sleep(10)  # Wait longer on error

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Generated: {generated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"    ❌ {e}")
    print(f"\n  Progress saved to: {PROGRESS_FILE}")
    print(f"  Re-run this script to retry failed cases (resume supported)")


if __name__ == "__main__":
    main()
