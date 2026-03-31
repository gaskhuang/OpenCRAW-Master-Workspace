---
name: 語音筆記轉任務 (Voice Notes to Tasks)/python
description: "Use Case #047 Python 方案: 語音筆記轉任務。使用 Python 實作 Voice Notes to Tasks 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #047: 語音筆記轉任務 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# 语音笔记转日记

## 简介

将语音笔记转换为每日日记条目。无论是在通勤途中、会议后还是睡前，只需录制语音，代理会自动转录并整理成日记。

**为什么重要**：快速记录想法，无需打字，建立日记习惯。

**真实例子**：一位忙碌的高管使用此代理记录每日反思，代理自动转录并整理成结构化日记，帮助他保持自我反思的习惯。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `voice_recognition` | [ClawdHub](https://clawhub.com/skills/voice) | 语音识别 |
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 笔记管理 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容整理 |

---

## 使用方式

### 录制语音
发送语音消息给代理

### 自动转录
代理转录音频为文本

### 整理日记
代理将内容整理为结构化日记条目

---

## 来源

- 来源：Hostinger


---

# 🎤 Voice Note Organizer

> Capture thoughts anywhere. Find them organized later.

---

## The Problem

Voice notes are the fastest way to capture ideas, but they become a graveyard of untranscribed audio files. You know that brilliant idea is somewhere in your recordings, but finding it means listening to hours of audio.

---

## The Solution

OpenClaw automatically transcribes your voice notes, extracts key points, tags by topic, and makes everything searchable. Ideas captured on a walk become organized notes by the time you're home.

---

## Setup Guide

### Step 1: Install Transcription Skills

```bash
openclaw skill install voicenotes
openclaw skill install local-whisper
openclaw skill install voice-transcribe
```

### Step 2: Set Up Voice Note Sync

Create `~/openclaw/voice-notes/config.json`:

```json
{
  "inputSources": [
    "~/Library/Mobile Documents/com~apple~CloudDocs/VoiceNotes/",
    "~/Dropbox/VoiceMemos/"
  ],
  "outputDir": "~/openclaw/voice-notes/transcripts/",
  "autoTags": ["idea", "todo", "meeting", "journal", "reminder"],
  "language": "en"
}
```

### Step 3: Configure Processing Rules

Create `~/openclaw/voice-notes/rules.md`:

```markdown
# Voice Note Processing

## Auto-Tag Rules
- Contains "remind me" → todo
- Contains "meeting with" → meeting
- Contains "I think" / "what if" → idea
- Morning recordings → journal

## Extract
- Action items (make a list)
- People mentioned
- Dates/deadlines mentioned
- Questions to follow up on

## Archive
- Keep originals for 30 days
- Archive transcripts indefinitely
- Flag recordings with low confidence for review
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `voicenotes` | Voicenotes.com integration |
| `local-whisper` | Local transcription |
| `voice-transcribe` | Cloud transcription |

---

## Example Prompts

**Process new notes:**
```
Transcribe and organize all new voice notes from today.
```

**Search recordings:**
```
Find any voice notes where I talked about [topic] in the last month.
```

**Extract todos:**
```
Go through this week's voice notes and compile all action items I mentioned.
```

**Daily summary:**
```
Summarize what I recorded today. What were my main thoughts?
```

---

## Cron Schedule

```
*/30 * * * *   # Every 30 min - check for new recordings
0 21 * * *     # 9 PM - daily summary of recordings
0 10 * * 0     # Sunday 10 AM - weekly idea review
```

---

## Expected Results

**Week 1:**
- All voice notes s

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
voice-notes-to-tasks/
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
mkdir -p voice-notes-to-tasks && cd voice-notes-to-tasks
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

根據 語音筆記轉任務 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Voice Notes to Tasks"""
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
"""Main orchestrator for Voice Notes to Tasks"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 語音筆記轉任務 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 語音筆記轉任務 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/voice-notes-to-tasks.log 2>&1
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
