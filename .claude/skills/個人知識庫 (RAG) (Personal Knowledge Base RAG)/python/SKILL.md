---
name: 個人知識庫 (RAG) (Personal Knowledge Base RAG)/python
description: "Use Case #094 Python 方案: 個人知識庫 (RAG)。使用 Python 實作 Personal Knowledge Base (RAG) 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #094: 個人知識庫 (RAG) — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 研究與學習

---

## 原始需求 (來自 Source Repos)

# Personal Knowledge Base (RAG)

You read articles, tweets, and watch videos all day but can never find that one thing you saw last week. Bookmarks pile up and become useless.

This workflow builds a searchable knowledge base from everything you save:

• Drop any URL into Telegram or Slack and it auto-ingests the content (articles, tweets, YouTube transcripts, PDFs)
• Semantic search over everything you've saved: "What did I save about agent memory?" returns ranked results with sources
• Feeds into other workflows — e.g., the video idea pipeline queries the KB for relevant saved content when building research cards

## Skills you Need

- [knowledge-base](https://clawhub.ai) skill (or build custom RAG with embeddings)
- `web_fetch` (built-in)
- Telegram topic or Slack channel for ingestion

## How to Set it Up

1. Install the knowledge-base skill from ClawdHub.
2. Create a Telegram topic called "knowledge-base" (or use a Slack channel).
3. Prompt OpenClaw:
```text
When I drop a URL in the "knowledge-base" topic:
1. Fetch the content (article, tweet, YouTube transcript, PDF)
2. Ingest it into the knowledge base with metadata (title, URL, date, type)
3. Reply with confirmation: what was ingested and chunk count

When I ask a question in this topic:
1. Search the knowledge base semantically
2. Return top results with sources and relevant excerpts
3. If no good matches, tell me

Also: when other workflows need research (e.g., video ideas, meeting prep), automatically query the knowledge base for relevant saved content.
```

4. Test it by dropping a few URLs and asking questions like "What do I have about LLM memory?"


---

# 个人知识库构建器

## 简介

信息碎片化是现代人面临的挑战。这个使用案例自动收集、整理和连接你的知识，构建个人知识图谱，让信息易于检索和关联。

**为什么重要**：建立可搜索的知识库，发现知识关联，提高学习和工作效率。

**真实例子**：一位研究员使用此代理管理研究资料，代理自动分类论文、提取关键信息、建立知识关联，使他的研究效率提高了 50%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `notes` | [ClawdHub](https://clawhub.com/skills/notes) | 管理笔记 |
| `search` | [ClawdHub](https://clawhub.com/skills/search) | 知识检索 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `graph` | [ClawdHub](https://clawhub.com/skills/graph) | 知识图谱 |

---

## 设置步骤

### 1. 前置条件

- 笔记应用（Notion、Obsidian）
- 知识分类体系
- 现有笔记导入

### 2. 提示词模板

```markdown
## 个人知识库构建器

你是我的知识管理助手。帮我构建个人知识库：

### 知识收集

**来源**
- 阅读笔记
- 会议记录
- 学习资料
- 想法记录
- 网页收藏

**自动处理**
- 提取关键信息
- 生成摘要
- 提取标签
- 识别实体

### 知识组织

**分类体系**
- 项目
- 主题
- 人物
- 资源
- 想法

**标签系统**
- 状态：#进行中 #已完成 #待复习
- 类型：#文章 #视频 #书籍 #课程
- 主题：#AI #商业 #健康

### 知识连接

**自动关联**
- 识别相关笔记
- 建立双向链接
- 生成知识图谱
- 发现知识缺口

**每日回顾**
```
🧠 每日知识回顾

📚 今日新增
- [笔记 1]
- [笔记 2]

🔗 相关笔记
- [笔记 1] 与 [旧笔记] 相关

💡 新发现
- 发现了 [主题] 和 [主题] 的关联

📅 待复习
- [笔记]（7 天前创建）
```

### 知识检索

**智能搜索**
- 全文搜索
- 标签过滤
- 时间范围
- 相关性排序

**问答功能**
- 基于知识库回答
- 提供相关笔记
- 引用来源
```

### 3. 配置

```
Schedule: 0 21 * * *
Action: 收集知识 → 整理 → 建立连接 → 生成回顾
```

---

## 成功指标

- [ ] 知识库可搜索
- [ ] 知识关联清晰
- [ ] 信息检索快速
- [ ] 知识复用率提高

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


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
personal-knowledge-base-(rag)/
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
mkdir -p personal-knowledge-base-(rag) && cd personal-knowledge-base-(rag)
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

根據 個人知識庫 (RAG) 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Personal Knowledge Base (RAG)"""
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
"""Main orchestrator for Personal Knowledge Base (RAG)"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 個人知識庫 (RAG) - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 個人知識庫 (RAG) 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/personal-knowledge-base-(rag).log 2>&1
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
