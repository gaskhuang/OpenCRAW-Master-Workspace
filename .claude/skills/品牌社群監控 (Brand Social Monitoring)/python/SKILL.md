---
name: 品牌社群監控 (Brand Social Monitoring)/python
description: "Use Case #005 Python 方案: 品牌社群監控。使用 Python 實作 Brand Social Monitoring 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #005: 品牌社群監控 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# 社交媒体监控器

## 简介

监控品牌提及、行业趋势和竞争对手动态。这个使用案例追踪多个社交平台，生成每日报告，并在重要事件发生时立即通知你。

**为什么重要**：及时了解品牌声誉，把握行业趋势，快速响应危机。

**真实例子**：一家初创公司使用此代理监控品牌提及，当一位 KOL 发布负面评论时，代理立即通知团队，使他们能够在 30 分钟内响应并解决问题。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `twitter` | [ClawdHub](https://clawhub.com/skills/twitter) | 监控 X/Twitter |
| `reddit` | [ClawdHub](https://clawhub.com/skills/reddit) | 监控 Reddit |
| `sentiment` | [ClawdHub](https://clawhub.com/skills/sentiment) | 情感分析 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送通知 |

---

## 设置步骤

### 1. 前置条件

- 社交媒体 API 密钥
- 监控关键词列表
- 竞争对手列表

### 2. 提示词模板

```markdown
## 社交媒体监控器

你是我的社交媒体分析师。监控并报告相关提及：

### 监控范围

**品牌监控**
- 公司名称
- 产品名称
- 品牌标签
- CEO/创始人提及

**行业监控**
- 行业关键词
- 趋势话题
- 技术讨论
- 市场动态

**竞争对手监控**
- 竞争对手动态
- 产品发布
- 营销活动
- 用户反馈

### 分析维度

**情感分析**
- 正面提及
- 负面提及
- 中性讨论
- 情感趋势

**影响力评估**
- 提及者粉丝数
- 互动量
- 传播范围
- 潜在影响

### 报告格式
```
📊 每日社交监控报告 - YYYY-MM-DD

🔥 热门提及
1. [提及内容] - [平台]
   作者：[用户名] ([粉丝数])
   互动：[点赞] [转发] [评论]
   情感：[正面/负面/中性]

📈 趋势分析
- 今日提及量：+15%
- 情感评分：7.2/10
- 热门话题：[话题列表]

⚠️ 需要关注
- [负面提及摘要]
- 建议响应：[建议]

👥 竞争对手动态
- [竞争对手]：[动态摘要]
```

### 告警规则
- 负面提及 > 100 互动：立即通知
- KOL 提及：30 分钟内通知
- 危机信号：立即通知
- 正面病毒内容：每日汇总
```

### 3. 配置

```
Schedule: */30 * * * *
Action: 扫描平台 → 分析 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 实时监控覆盖
- [ ] 重要提及零遗漏
- [ ] 响应时间 < 30 分钟
- [ ] 品牌声誉改善

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# Competitor Radar 🎯

> Automated competitive intelligence that keeps you one step ahead

## The Problem

You're building a product but have no idea what competitors are doing until customers tell you they switched. Manually checking competitor websites, blogs, and social media is a time sink that falls off your radar within a week. By the time you notice a competitor launched a killer feature or slashed prices, you've already lost deals.

## The Solution

OpenClaw becomes your always-on competitive intelligence analyst. It monitors competitor websites for pricing changes, scans their blogs for product announcements, tracks their social media activity, and delivers a weekly digest with strategic recommendations. When something big happens (major price drop, new feature launch), you get an instant alert.

---

## Setup Guide

### Step 1: Create Your Competitor Config File

Create `competitors.json` in your OpenClaw workspace:

```bash
mkdir -p ~/openclaw/competitor-radar
```

```json
// ~/openclaw/competitor-radar/competitors.json
{
  "competitors": [
    {
      "name": "Acme Corp",
      "website": "https://acme.com",
      "pricing_page": "https://acme.com/pricing",
      "blog": "https://acme.com/blog",
      "twitter": "acmecorp",
      "linkedin": "company/acme-corp"
    },
    {
      "name": "BigCo",
      "website": "https://bigco.io",
      "pricing_page": "https://bigco.io/pricing",
      "blog": "https://bigco.io/resources/blog",
      "twitter": "bigco_io"
    },
    {
      "name": "StartupX",
      "website": "https://startupx.com",
      "pricing_page": "https:/

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
brand-social-monitoring/
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
mkdir -p brand-social-monitoring && cd brand-social-monitoring
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

根據 品牌社群監控 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Brand Social Monitoring"""
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
"""Main orchestrator for Brand Social Monitoring"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 品牌社群監控 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 品牌社群監控 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/brand-social-monitoring.log 2>&1
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
