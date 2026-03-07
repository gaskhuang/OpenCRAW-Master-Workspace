---
name: 自動排程社群發文 (Auto-Schedule Social Posts)/python
description: "Use Case #006 Python 方案: 自動排程社群發文。使用 Python 實作 Auto-Schedule Social Posts 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #006: 自動排程社群發文 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# 自动社交发布

## 简介

保持社交媒体活跃需要持续发布内容。这个使用案例自动安排和发布社交媒体内容，基于你的内容日历和最佳发布时间，保持一致的在线存在。

**为什么重要**：节省时间，保持一致的社交媒体存在，优化发布时间。

**真实例子**：一位内容创作者使用此代理管理多个社交平台，代理根据每个平台的最佳时间自动发布，粉丝互动率提高了 60%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `twitter` | [ClawdHub](https://clawhub.com/skills/twitter) | 发布推文 |
| `linkedin` | [ClawdHub](https://clawhub.com/skills/linkedin) | 发布 LinkedIn |
| `instagram` | [ClawdHub](https://clawhub.com/skills/instagram) | 发布 Instagram |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 分析表现 |

---

## 设置步骤

### 1. 前置条件

- 社交媒体账号
- API 访问权限
- 内容日历

### 2. 提示词模板

```markdown
## 自动社交发布

你是我的社交媒体经理。自动发布和管理内容：

### 发布策略

**内容类型**
- 教育内容：分享知识和技巧
- 幕后内容：展示工作过程
- 互动内容：提问和投票
- 推广内容：产品/服务
- 娱乐内容：轻松有趣

**发布频率**
- Twitter：每天 3-5 条
- LinkedIn：每天 1-2 条
- Instagram：每天 1-2 条

**最佳时间**
- 早上 8-9 点：通勤时间
- 中午 12-1 点：午餐时间
- 下午 5-6 点：下班时间
- 晚上 8-9 点：休闲时间

### 内容准备

**内容库**
- 预写文章
- 图片素材
- 视频内容
- 引用和名言

**自动调整**
- 根据平台调整格式
- 添加相关标签
- 优化发布时间
- A/B 测试标题

### 互动管理

**自动响应**
- 感谢新关注者
- 回复常见问题
- 转发正面提及

**监控指标**
- 互动率
- 粉丝增长
- 内容表现
- 最佳发布时间

### 每周报告
```
📈 社交媒体周报 - YYYY-MM-DD

📊 关键指标
- 总互动：[数量]
- 新粉丝：[数量]
- 内容发布：[数量]
- 平均互动率：[百分比]

🔥 最佳表现
1. [内容摘要] - [互动数]
2. [内容摘要] - [互动数]

💡 下周建议
- [建议内容]
```
```

### 3. 配置

```
Schedule: 0 8,12,17,20 * * *
Action: 选择内容 → 调整格式 → 发布 → 监控
```

---

## 成功指标

- [ ] 每天按时发布
- [ ] 粉丝稳定增长
- [ ] 互动率提升
- [ ] 节省时间 > 5 小时/周

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 📱 Social Media Scheduler

> Post once, publish everywhere. Stop juggling 5 apps to share the same content.

---

## The Problem

Managing social media presence across Twitter/X, LinkedIn, Bluesky, and Instagram means logging into each platform, reformatting content for each, and posting at optimal times. Most people either spend 2+ hours daily on this or let their accounts go stale. Both hurt growth.

---

## The Solution

OpenClaw takes one piece of content and automatically adapts it for each platform's format, character limits, and best practices. Schedule once, post everywhere at optimal times, and track what's working.

---

## Setup Guide

### Step 1: Install Required Skills (5 minutes)

```bash
openclaw skill install bluesky
openclaw skill install linkedin
openclaw skill install upload-post
```

### Step 2: Create Content Templates

Create `~/openclaw/social-templates/`:

```markdown
# Social Media Templates

## Thread Format (Twitter/X, Bluesky)
- Hook in first post (curiosity gap)
- Max 280 chars per post
- Number posts: 1/, 2/, etc.
- End with CTA

## LinkedIn Format
- Professional tone
- 1300 char limit
- Use line breaks for readability
- 3-5 relevant hashtags

## Instagram Caption
- Conversational tone
- Emoji-friendly
- 2200 char max
- 20-30 hashtags in first comment
```

### Step 3: Set Up Content Queue

Create `~/openclaw/content-queue.json`:

```json
{
  "queue": [],
  "posted": [],
  "schedule": {
    "twitter": ["09:00", "13:00", "17:00"],
    "linkedin": ["08:00", "12:00"],
    "bluesky": ["10:00", "15:00"]
  }
}
`

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
auto-schedule-social-posts/
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
mkdir -p auto-schedule-social-posts && cd auto-schedule-social-posts
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

根據 自動排程社群發文 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Auto-Schedule Social Posts"""
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
"""Main orchestrator for Auto-Schedule Social Posts"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 自動排程社群發文 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 自動排程社群發文 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/auto-schedule-social-posts.log 2>&1
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
