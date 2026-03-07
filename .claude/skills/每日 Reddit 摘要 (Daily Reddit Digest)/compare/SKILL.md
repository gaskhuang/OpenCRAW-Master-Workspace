---
name: 每日 Reddit 摘要 (Daily Reddit Digest)/compare
description: "Use Case #001 方案比較: 每日 Reddit 摘要。Python (PRAW) vs Node.js (.json API) 兩方案的完整對照分析。"
---

# Use Case #001: 每日 Reddit 摘要 — 方案比較

> 兩位 AI Agent 分別獨立設計的方案，以下為完整比較分析。

---

## 總覽比較

| 比較項目 | 🐍 方案 A: Python + PRAW | 🟢 方案 B: Node.js + .json API |
|---------|-------------------------|-------------------------------|
| **語言** | Python 3.9+ | Node.js 18+ |
| **Reddit 存取** | PRAW (官方 API Wrapper) | 公開 .json 端點 |
| **AI 引擎** | Anthropic Python SDK | Anthropic JS SDK |
| **推送方式** | requests + Bot HTTP API | node-telegram-bot-api |
| **排程** | 系統 cron | node-cron + pm2 |
| **日誌** | print + file | Winston |

---

## 關鍵差異

### 1. Reddit API 存取

| | Python PRAW | Node.js .json |
|---|-----------|--------------|
| **需要註冊** | ✅ 需要 OAuth (client_id + secret) | ❌ 完全免註冊 |
| **Rate Limit** | 60-100 req/min (認證後) | ~10 req/min (公開端點) |
| **資料完整度** | 完整 (含 flair、awards 等) | 基本 (title, score, body) |
| **可靠性** | 高 (官方支援) | 中 (Reddit 可能限制) |
| **分頁支援** | 自動 (PRAW 內建) | 手動 (需處理 after token) |
| **設定時間** | 10 分鐘 (需建立 Reddit App) | 0 分鐘 |

**結論**: 如果只是每天抓 40-50 篇貼文，Node.js .json 方式綽綽有餘。如果需要大量抓取或存取進階資料，Python PRAW 更合適。

### 2. 程式碼架構

| | Python | Node.js |
|---|--------|---------|
| **模組數** | 5 (config, fetcher, summarizer, sender, main) | 6 (+ logger) |
| **程式碼行數** | ~714 行 | ~600 行 |
| **錯誤處理** | try/except + Telegram 通知 | try/catch + Telegram 通知 |
| **型別安全** | dataclass | 純 object |
| **測試工具** | 內建 test_components.py | CLI flag --run-once |

### 3. 排程方式

| | Python (系統 cron) | Node.js (node-cron + pm2) |
|---|-------------------|--------------------------|
| **設定複雜度** | 中 (需熟悉 crontab) | 低 (程式內設定) |
| **持久化** | cron 天生持久 | 需要 pm2 |
| **日誌管理** | 需自行導向檔案 | Winston 內建 |
| **重啟恢復** | 自動 (cron 是系統服務) | 需 `pm2 startup` |
| **多時區** | 需設定 TZ 環境變數 | node-cron 支援 timezone 參數 |

### 4. 部署與維運

| | Python | Node.js |
|---|--------|---------|
| **打包大小** | ~50MB (venv) | ~30MB (node_modules) |
| **Docker 映像** | python:3.11-slim (~150MB) | node:20-alpine (~130MB) |
| **CI/CD** | GitHub Actions (pip install) | GitHub Actions (npm ci) |
| **監控** | 自行實作 | pm2 monit 內建 |
| **環境管理** | venv (需 activate) | 直接執行 |

---

## 效能比較

| 指標 | Python | Node.js |
|------|--------|---------|
| 抓取 4 subreddits × 10 posts | ~3s (PRAW 自動限速) | ~5s (每次間隔 1s) |
| Claude API 呼叫 | ~5-8s | ~5-8s |
| Telegram 傳送 | ~1s | ~1s |
| **總執行時間** | **~10-12s** | **~12-15s** |
| 記憶體使用 | ~80MB | ~60MB |

---

## 成本比較

兩方案的 API 成本完全相同：

| 項目 | 費用 |
|------|------|
| Reddit API | 免費 (兩方案都免費) |
| Claude API | ~$0.50-2.00/月 (相同用量) |
| Telegram Bot | 免費 |
| 伺服器 (如需) | 免費 (cron/pm2 在本地) |

---

## 推薦選擇

### 選 Python 如果你...
- ✅ 已經熟悉 Python
- ✅ 需要長期穩定運行
- ✅ 未來可能需要存取 Reddit 進階功能 (投票、評論等)
- ✅ 團隊以 Python 為主
- ✅ 需要大量抓取 (>100 篇/次)

### 選 Node.js 如果你...
- ✅ 想快速上手，5 分鐘內跑起來
- ✅ 不想註冊 Reddit API
- ✅ 前端背景，熟悉 JavaScript
- ✅ 只需要基本功能 (每日 40-50 篇)
- ✅ 喜歡 pm2 的內建監控

### 最終推薦

| 使用場景 | 推薦 |
|---------|------|
| **初學者 / 課程教學** | 🟢 Node.js (零門檻) |
| **快速原型 / PoC** | 🟢 Node.js (免註冊) |
| **正式環境 / Production** | 🐍 Python (穩定可靠) |
| **進階功能需求** | 🐍 Python (PRAW 功能完整) |
| **團隊協作** | 依團隊技術棧決定 |

---

## 開始實作

- 選擇 Python → `/每日 Reddit 摘要 (Daily Reddit Digest)/python`
- 選擇 Node.js → `/每日 Reddit 摘要 (Daily Reddit Digest)/nodejs`
- 回到總覽 → `/每日 Reddit 摘要 (Daily Reddit Digest)`

## 參考文件

- Python 完整教學: `docs/usecase-tutorials/daily-reddit-digest/TUTORIAL.md`
- Node.js 完整教學: `docs/daily-reddit-digest-nodejs-tutorial.md`
- 統一比較文件: `usecases/001-daily-reddit-digest.md`
