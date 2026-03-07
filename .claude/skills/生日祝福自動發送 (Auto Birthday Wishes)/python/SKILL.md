---
name: 生日祝福自動發送 (Auto Birthday Wishes)/python
description: "Use Case #023 Python 方案: 生日祝福自動發送。使用 Python 實作 Auto Birthday Wishes 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #023: 生日祝福自動發送 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 生日祝福自动发送

## 简介

记住所有重要日期并发送祝福是一项挑战。这个使用案例管理生日和纪念日，生成个性化祝福，并在正确的时间发送。

**为什么重要**：维护重要关系，不错过重要日子，表达关心。

**真实例子**：一位忙碌的企业家使用此代理管理 100+ 联系人的生日，代理自动生成个性化祝福并准时发送，帮助他维护了重要的人脉关系。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `contacts` | [ClawdHub](https://clawhub.com/skills/contacts) | 访问联系人 |
| `messaging` | [ClawdHub](https://clawhub.com/skills/messaging) | 发送消息 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 发送邮件 |

---

## 设置步骤

### 1. 前置条件

- 联系人列表（含生日）
- 关系类型标记
- 发送渠道偏好

### 2. 提示词模板

```markdown
## 生日祝福自动发送

你是我的关系助手。管理生日祝福：

### 数据管理

**联系人信息**
- 姓名
- 生日
- 关系类型（家人/朋友/同事/客户）
- 偏好渠道（短信/邮件/社交）
- 个人备注（兴趣、共同回忆）

**关系分类**
- 亲密家人：提前准备，精心祝福
- 好朋友：个性化，回忆共同经历
- 同事客户：专业礼貌
- 一般关系：简洁祝福

### 祝福生成

**个性化要素**
- 使用对方名字
- 提及关系特点
- 引用共同回忆
- 符合对方风格

**模板示例**

*亲密朋友*：
"生日快乐 [名字]！🎉 还记得我们 [共同回忆] 吗？
祝你新的一岁 [个性化祝福]！
期待我们下次 [计划]！"

*专业关系*：
"祝您生日快乐！感谢您一直以来的支持与合作。
祝您事业顺利，身体健康！"

### 发送策略

**提前准备**
- 3 天前：生成祝福草稿
- 1 天前：确认发送渠道
- 当天：准时发送

**发送时间**
- 早上 9:00：家人和亲密朋友
- 上午 10:00：同事
- 下午 2:00：客户和业务伙伴
```

### 3. 配置

```
Schedule: 0 9 * * *
Action: 检查生日 → 生成祝福 → 发送
```

---

## 成功指标

- [ ] 重要生日零遗漏
- [ ] 祝福准时发送
- [ ] 收到积极回复
- [ ] 关系维护良好

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
auto-birthday-wishes/
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
mkdir -p auto-birthday-wishes && cd auto-birthday-wishes
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

根據 生日祝福自動發送 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Auto Birthday Wishes"""
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
"""Main orchestrator for Auto Birthday Wishes"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 生日祝福自動發送 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 生日祝福自動發送 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/auto-birthday-wishes.log 2>&1
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
