---
name: Instagram 限時動態管理 (Instagram Stories Management)/python
description: "Use Case #007 Python 方案: Instagram 限時動態管理。使用 Python 實作 Instagram Stories Management 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #007: Instagram 限時動態管理 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 社群媒體

---

## 原始需求 (來自 Source Repos)

# Instagram 故事管理器

## 简介

社交媒体管理耗时且需要持续的关注。这个使用案例自动创建、安排和发布 Instagram 故事，基于你的内容日历和当前趋势。

**为什么重要**：保持一致的社交媒体存在，无需手动操作。

**真实例子**：一位小型企业主使用此代理每天自动发布 3-5 个故事，展示产品、分享客户评价和幕后内容，粉丝互动率提高了 40%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `instagram` | [ClawdHub](https://clawhub.com/skills/instagram) | 发布故事 |
| `image_generation` | [ClawdHub](https://clawhub.com/skills/image) | 生成图片 |
| `content_calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 管理内容日历 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 分析表现 |

---

## 设置步骤

### 1. 前置条件

- Instagram 商业账号
- Instagram Graph API 访问权限
- 内容日历（Google Sheets 或 Notion）
- 品牌素材库

### 2. 提示词模板

```markdown
## Instagram 故事管理器

你是我的社交媒体经理。每天执行以下任务：

### 内容规划
1. 检查内容日历获取今天的故事主题
2. 分析过去 7 天的表现数据
3. 确定最佳发布时间

### 故事创建
1.  morning (9 AM): 早安/励志引用
2.  noon (12 PM): 产品展示或幕后内容
3.  afternoon (3 PM): 互动投票或问答
4.  evening (6 PM): 用户生成内容或评价

### 设计指南
- 使用品牌颜色（主色、辅色）
- 保持字体一致
- 添加品牌标识
- 使用相关标签

### 发布策略
- 高峰时段：12 PM, 3 PM, 6 PM
- 周末减少频率
- 特殊日期调整内容

### 互动监控
- 回复故事回复（24 小时内）
- 记录高互动内容类型
- 每周生成表现报告
```

### 3. 配置

```
Schedule: 0 9,12,15,18 * * *
Action: 生成内容 → 创建图片 → 发布 → 监控
```

---

## 成功指标

- [ ] 每天发布 3-5 个故事
- [ ] 故事观看率稳定增长
- [ ] 互动率（投票、问答）提高
- [ ] 粉丝增长

---

## 变体与扩展

### 变体 1：活动推广模式
针对特定活动（产品发布、促销）集中推广。

### 变体 2：用户生成内容
自动收集和转发粉丝内容。

---

## 故障排除

### 问题：图片生成失败
**解决方案**：检查图片生成 API 配额和提示词质量。

### 问题：发布时间不准确
**解决方案**：检查时区设置和定时任务配置。

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
instagram-stories-management/
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
mkdir -p instagram-stories-management && cd instagram-stories-management
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

根據 Instagram 限時動態管理 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Instagram Stories Management"""
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
"""Main orchestrator for Instagram Stories Management"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== Instagram 限時動態管理 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 Instagram 限時動態管理 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/instagram-stories-management.log 2>&1
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
