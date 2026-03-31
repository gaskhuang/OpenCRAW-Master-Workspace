---
name: 閱讀清單智慧管理 (Smart Reading List Manager)/python
description: "Use Case #025 Python 方案: 閱讀清單智慧管理。使用 Python 實作 Smart Reading List Manager 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #025: 閱讀清單智慧管理 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 阅读列表策展人

## 简介

收藏了太多文章却没时间读？这个使用案例智能管理你的阅读列表，根据你的兴趣优先级排序，生成摘要，并推荐最佳阅读时间。

**为什么重要**：高效管理阅读清单，确保不错过重要内容。

**真实例子**：一位研究员使用此代理管理数百篇学术论文，代理根据研究项目优先级排序，并生成摘要帮助他快速筛选重要论文。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `bookmark` | [ClawdHub](https://clawhub.com/skills/bookmark) | 管理书签 |
| `nlp` | [ClawdHub](https://clawhub.com/skills/nlp) | 内容分析 |
| `readability` | [ClawdHub](https://clawhub.com/skills/readability) | 提取正文 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送推荐 |

---

## 设置步骤

### 1. 前置条件

- 书签服务（Pocket、Instapaper）
- 兴趣主题列表

### 2. 提示词模板

```markdown
## 阅读列表策展人

你是我的阅读助理。管理我的阅读列表：

### 功能

**1. 内容分析**
- 分析每篇文章的主题
- 评估阅读时间
- 提取关键摘要
- 判断内容质量

**2. 智能排序**
- 根据当前项目优先级排序
- 考虑时效性
- 平衡深度和轻松内容
- 避免同类内容重复

**3. 阅读建议**
- 早上：新闻和轻量内容
- 下午：专业文章
- 晚上：长文和深度阅读

**4. 每周精选**
- 推荐本周必读 Top 5
- 生成摘要卡片
- 提供阅读路径建议

### 输出格式
```
📚 本周阅读推荐

🔥 优先阅读
1. [标题] - [来源] ([阅读时间])
   [一句话摘要]
   推荐理由：[原因]

📰 今日轻读
1. [标题] - [来源]
   [一句话摘要]

📖 周末深度
1. [标题] - [来源] ([阅读时间])
   [详细摘要]

📊 阅读统计
- 本周已读：X 篇
- 平均阅读时间：Y 分钟
- 收藏待读：Z 篇
```

### 学习偏好
- 记录我读完的文章
- 分析我喜欢的内容类型
- 调整推荐算法
```

### 3. 配置

```
Schedule: 0 9 * * 1
Action: 分析列表 → 生成推荐 → 发送
```

---

## 成功指标

- [ ] 阅读列表保持可控
- [ ] 优先内容不被遗漏
- [ ] 阅读效率提升
- [ ] 发现高质量内容

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
smart-reading-list-manager/
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
mkdir -p smart-reading-list-manager && cd smart-reading-list-manager
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

根據 閱讀清單智慧管理 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Smart Reading List Manager"""
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
"""Main orchestrator for Smart Reading List Manager"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 閱讀清單智慧管理 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 閱讀清單智慧管理 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/smart-reading-list-manager.log 2>&1
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
