---
name: 語義記憶搜尋 (Semantic Memory Search)/python
description: "Use Case #097 Python 方案: 語義記憶搜尋。使用 Python 實作 Semantic Memory Search 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #097: 語義記憶搜尋 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Semantic Memory Search

OpenClaw's built-in memory system stores everything as markdown files — but as memories grow over weeks and months, finding that one decision from last Tuesday becomes impossible. There is no search, just scrolling through files.

This use case adds **vector-powered semantic search** on top of OpenClaw's existing markdown memory files using [memsearch](https://github.com/zilliztech/memsearch), so you can instantly find any past memory by meaning, not just keywords.

## What It Does

- Index all your OpenClaw markdown memory files into a vector database (Milvus) with a single command
- Search by meaning: "what caching solution did we pick?" finds the relevant memory even if the word "caching" does not appear
- Hybrid search (dense vectors + BM25 full-text) with RRF reranking for best results
- SHA-256 content hashing means unchanged files are never re-embedded — zero wasted API calls
- File watcher auto-reindexes when memory files change, so the index is always up to date
- Works with any embedding provider: OpenAI, Google, Voyage, Ollama, or fully local (no API key needed)

## Pain Point

OpenClaw's memory is stored as plain markdown files. This is great for portability and human readability, but it has no search. As your memory grows, you either have to grep through files (keyword-only, misses semantic matches) or load entire files into context (wastes tokens on irrelevant content). You need a way to ask "what did I decide about X?" and get the exact relevant chunk, regardless of phrasing.

## Skills You Need

- No OpenClaw skills required — memsearch is a standalone Python CLI/library
- Python 3.10+ with pip or uv

## How to Set It Up

1. Install memsearch:
```bash
pip install memsearch
```

2. Run the interactive config wizard:
```bash
memsearch config init
```

3. Index your OpenClaw memory directory:
```bash
memsearch index ~/path/to/your/memory/
```

4. Search your memories by meaning:
```bash
memsearch search "what caching solution did we pick?"
```

5. For live sync, start the file watcher — it auto-indexes on every file change:
```bash
memsearch watch ~/path/to/your/memory/
```

6. For a fully local setup (no API keys), install the local embedding provider:
```bash
pip install "memsearch[local]"
memsearch config set embedding.provider local
memsearch index ~/path/to/your/memory/
```

## Key Insights

- **Markdown stays the source of truth.** The vector index is just a derived cache — you can rebuild it anytime with `memsearch index`. Your memory files are never modified.
- **Smart dedup saves money.** Each chunk is identified by a SHA-256 content hash. Re-running `index` only embeds new or changed content, so you can run it as often as you like without wasting embedding API calls.
- **Hybrid search beats pure vector search.** Combining semantic similarity (dense vectors) with keyword matching (BM25) via Reciprocal Rank Fusion catches both meaning-based and exact-match queries.

## Related Links

- [memsearch Git

---

## 所需套件

```txt
anthropic>=0.43.0        # Claude AI 核心
python-dotenv>=1.0.1     # 環境變數管理
requests>=2.32.3         # HTTP 請求
python-telegram-bot>=21.9 # Telegram 推送 (可選)
pytz>=2024.2             # 時區處理
schedule>=1.2.0          # 排程管理 (可選)
```

---

## 前置準備 Checklist

- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather) — 如需推送
- [ ] 相關第三方 API Key — 視 use case 需求

---

## 專案結構

```
semantic-memory-search/
├── .env                    # 環境變數
├── requirements.txt        # Python 依賴
├── config.py              # 設定管理
├── main.py                # 主程式
├── core.py                # 核心業務邏輯
├── notifier.py            # 通知推送
└── output/                # 輸出資料夾
```

---

## 實作流程 (Step by Step)

### Step 1: 環境準備

```bash
mkdir -p semantic-memory-search && cd semantic-memory-search
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests python-telegram-bot pytz
```

### Step 2: 設定環境變數 (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
# 其他必要的 API keys
```

### Step 3: config.py — 設定管理

```python
"""Configuration management"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.ANTHROPIC_API_KEY: missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"Missing: {', '.join(missing)}")
```

### Step 4: core.py — 核心業務邏輯

根據 語義記憶搜尋 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Semantic Memory Search"""
import anthropic
from config import Config

def collect_data():
    """Collect data from relevant sources"""
    # TODO: Implement data collection
    # This depends on the specific use case
    pass

def analyze_with_ai(data):
    """Use Claude to analyze/process collected data"""
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"請分析以下資料並產生繁體中文報告：\n\n{data}"
        }]
    )
    return response.content[0].text
```

### Step 5: notifier.py — 通知推送

```python
"""Send notifications via Telegram"""
import requests
from config import Config

def send_telegram(text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    max_len = 4096
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        requests.post(url, json={
            "chat_id": Config.TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        })
```

### Step 6: main.py — 主程式

```python
"""Main orchestrator for Semantic Memory Search"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 語義記憶搜尋 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 語義記憶搜尋 報告\n\n{result}")
        print("✅ Done!")
    else:
        print("⚠ No data collected")

if __name__ == "__main__":
    run()
```

### Step 7: 排程

```bash
# 每天執行
crontab -e
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/semantic-memory-search.log 2>&1
```

---

## 測試步驟

| 階段 | 測試 | 預期結果 |
|------|------|---------|
| 1 | 環境變數 | Config.validate() 無錯誤 |
| 2 | 資料收集 | collect_data() 回傳資料 |
| 3 | AI 分析 | analyze_with_ai() 產生繁中報告 |
| 4 | 通知推送 | Telegram 收到訊息 |
| 5 | 完整流程 | python main.py 成功 |

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| API rate limit | 加入 retry + exponential backoff |
| Token 超過上限 | 分段處理，限制輸入長度 |
| Telegram 格式錯誤 | Markdown fallback 為純文字 |
| Cron 環境變數遺失 | 使用絕對路徑 + source .env |
