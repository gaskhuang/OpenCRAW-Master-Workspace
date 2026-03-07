---
name: PDF 文件處理中心 (PDF Document Processing Hub)/python
description: "Use Case #048 Python 方案: PDF 文件處理中心。使用 Python 實作 PDF Document Processing Hub 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #048: PDF 文件處理中心 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 生產力工具

---

## 原始需求 (來自 Source Repos)

# PDF 转摘要转换器

## 简介

阅读长篇 PDF 文档耗时。这个使用案例自动提取 PDF 内容，生成结构化摘要，提取关键信息，并回答关于文档的问题。

**为什么重要**：快速理解文档内容，节省阅读时间，提取关键信息。

**真实例子**：一位律师使用此代理处理案件材料，代理快速生成每份文件的摘要，使案件准备时间减少了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `pdf` | [ClawdHub](https://clawhub.com/skills/pdf) | 读取 PDF |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 文本分析 |
| `summarization` | [ClawdHub](https://clawhub.com/skills/summary) | 生成摘要 |

---

## 设置步骤

### 1. 前置条件

- PDF 文件访问
- 摘要长度偏好
- 输出格式

### 2. 提示词模板

```markdown
## PDF 转摘要转换器

你是我的文档助手。将 PDF 转换为结构化摘要：

### 处理流程

**1. 文档解析**
- 提取文本内容
- 识别文档结构
- 提取图表数据
- 识别关键章节

**2. 内容分析**
- 识别主题
- 提取关键论点
- 识别重要数据
- 提取结论

**3. 摘要生成**
- 执行摘要（1-2 段）
- 详细摘要（每章）
- 关键要点列表
- 重要引用

### 输出格式

```
📄 文档摘要

📋 基本信息
- 标题：[标题]
- 作者：[作者]
- 页数：XX 页
- 日期：YYYY-MM-DD

📝 执行摘要
[2-3 段摘要]

🎯 关键要点
1. [要点 1]
2. [要点 2]
3. [要点 3]

📊 重要数据
- [数据点 1]
- [数据点 2]

📑 章节摘要
**第一章：[标题]**
[摘要内容]

**第二章：[标题]**
[摘要内容]

❓ 问答
Q: [问题]
A: [答案]
```

### 批量处理
- 处理多个 PDF
- 生成比较报告
- 提取共同主题
- 识别矛盾点
```

### 3. 配置

```
Trigger: PDF 上传
Action: 解析 → 分析 → 生成摘要 → 输出
```

---

## 成功指标

- [ ] 摘要准确反映原文
- [ ] 处理速度快
- [ ] 关键信息完整
- [ ] 用户满意度高

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📄 Document Processor

> PDFs, contracts, reports—instantly searchable and summarized.

---

## The Problem

Documents pile up: contracts, reports, receipts, research papers. Finding information means opening dozens of files. Important details get lost. Nobody reads 50-page reports cover to cover.

---

## The Solution

OpenClaw extracts text from any document, summarizes key points, makes everything searchable, and answers questions about your documents instantly.

---

## Setup Guide

### Step 1: Install Document Skills

```bash
openclaw skill install mineru-pdf
openclaw skill install pymupdf-pdf
openclaw skill install llmwhisperer
openclaw skill install excel
```

### Step 2: Set Up Document Folders

Create `~/openclaw/documents/config.json`:

```json
{
  "watchFolders": [
    "~/Documents/Contracts/",
    "~/Documents/Reports/",
    "~/Downloads/*.pdf"
  ],
  "outputDir": "~/openclaw/documents/processed/",
  "autoProcess": true
}
```

---

## Skills Needed

| Skill | Purpose |
|-------|---------|
| `mineru-pdf` | Advanced PDF extraction |
| `pymupdf-pdf` | Fast PDF processing |
| `llmwhisperer` | Handwriting/complex docs |
| `excel` | Spreadsheet processing |

---

## Example Prompts

**Process document:**
```
Process this contract [file]. Extract key terms, dates, and obligations.
```

**Search documents:**
```
Find all documents that mention [term] from the past year.
```

**Summarize report:**
```
Summarize this 40-page report. What are the key findings and recommendations?
```

**Compare documents:**
```
Compare these two contract versions. What changed?
```

---

## Cron Schedule

```
*/30 * * * *   # Every 30 min - process new documents
0 9 * * 1      # Monday 9 AM - document digest
```

---

## Expected Results

- All documents searchable
- 90% faster information retrieval
- N

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
pdf-document-processing-hub/
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
mkdir -p pdf-document-processing-hub && cd pdf-document-processing-hub
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

根據 PDF 文件處理中心 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for PDF Document Processing Hub"""
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
"""Main orchestrator for PDF Document Processing Hub"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== PDF 文件處理中心 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 PDF 文件處理中心 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/pdf-document-processing-hub.log 2>&1
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
