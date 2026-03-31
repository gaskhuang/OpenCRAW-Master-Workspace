---
name: 建造前點子驗證器 (Pre-Build Idea Validator)/python
description: "Use Case #096 Python 方案: 建造前點子驗證器。使用 Python 實作 Pre-Build Idea Validator 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #096: 建造前點子驗證器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Pre-Build Idea Validator

Before OpenClaw starts building anything new, it automatically checks whether the idea already exists across GitHub, Hacker News, npm, PyPI, and Product Hunt — and adjusts its approach based on what it finds.

## What It Does

- Scans 5 real data sources (GitHub, Hacker News, npm, PyPI, Product Hunt) before any code is written
- Returns a `reality_signal` score (0-100) indicating how crowded the space is
- Shows top competitors with star counts and descriptions
- Suggests pivot directions when the space is saturated
- Works as a pre-build gate: high signal = stop and discuss, low signal = proceed

## Pain Point

You tell your agent "build me an AI code review tool" and it happily spends 6 hours coding. Meanwhile, 143,000+ repos already exist on GitHub — the top one has 53,000 stars. The agent never checks because you never asked, and it doesn't know to look. You only discover competitors after you've invested significant time. This pattern repeats for every new project idea.

## Skills You Need

- [idea-reality-mcp](https://github.com/mnemox-ai/idea-reality-mcp) — MCP server that scans real data sources and returns a competition score

## How to Set It Up

1. Install idea-reality-mcp:

```bash
uvx idea-reality-mcp
```

2. Add the MCP server to your OpenClaw config:

```json
{
  "mcpServers": {
    "idea-reality": {
      "command": "uvx",
      "args": ["idea-reality-mcp"]
    }
  }
}
```

3. Add this to your OpenClaw agent instructions:

```text
Before starting any new project, feature, or tool, always run idea_check first.

Rules:
- If reality_signal > 70: STOP. Report the top 3 competitors with star counts.
  Ask me if I want to proceed, pivot, or abandon.
- If reality_signal 30-70: Show me the results and pivot_hints.
  Suggest a niche angle that existing projects don't cover.
- If reality_signal < 30: Proceed to build.
  Mention that the space is open.
- Always show the reality_signal score and top competitors before writing any code.
```

## Real World Example

**You:** "Build me a CLI tool for AI code review"

OpenClaw runs `idea_check("AI code review tool")` and responds:

> **reality_signal: 90/100 (very high)**
>
> Top competitors:
> 1. Gitea — 53,940 stars
> 2. reviewdog — 9,104 stars
> 3. Danger (Ruby) — 5,649 stars
>
> This space has 143,000+ related repos. The top players are mature and well-funded.
>
> **Pivot suggestions:**
> - Focus on a specific language (Rust/Go-only AI code review)
> - Target a specific framework (React/Vue component review)
> - Target a specific industry (financial/medical code compliance review)
>
> Should I proceed with a differentiated angle, or pivot to something else?

**You:** "What about an MCP server for pre-build idea validation?"

> **reality_signal: 8/100 (very low)**
>
> 0 direct competitors found on PyPI or npm. GitHub has some tangentially related repos but none solve this exact problem.
>
> The space is wide open. Proceeding to build.

## Variations

- **Deep mode fo

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
pre-build-idea-validator/
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
mkdir -p pre-build-idea-validator && cd pre-build-idea-validator
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

根據 建造前點子驗證器 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Pre-Build Idea Validator"""
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
"""Main orchestrator for Pre-Build Idea Validator"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 建造前點子驗證器 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 建造前點子驗證器 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/pre-build-idea-validator.log 2>&1
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
