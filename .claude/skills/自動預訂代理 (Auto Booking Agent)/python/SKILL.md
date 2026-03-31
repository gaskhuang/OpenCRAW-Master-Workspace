---
name: 自動預訂代理 (Auto Booking Agent)/python
description: "Use Case #024 Python 方案: 自動預訂代理。使用 Python 實作 Auto Booking Agent 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #024: 自動預訂代理 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 预约预订代理

## 简介

预订餐厅、预约服务常常需要反复沟通确认时间。这个使用案例自动处理预约流程，与商家沟通，确认最佳时间，并将预约添加到日历。

**为什么重要**：节省时间，避免反复沟通，确保预约成功。

**真实例子**：一位忙碌的高管使用此代理预订餐厅，代理自动联系多家餐厅询问空位，比较选项，确认预订，并添加到日历发送提醒。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `phone` | [ClawdHub](https://clawhub.com/skills/phone) | 拨打电话 |
| `email` | [ClawdHub](https://clawhub.com/skills/email) | 发送邮件 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 检查空闲 |
| `booking_api` | [ClawdHub](https://clawhub.com/skills/booking) | 在线预订 |

---

## 设置步骤

### 1. 前置条件

- 日历访问权限
- 预订平台账号
- 偏好设置（餐厅类型、时间偏好）

### 2. 提示词模板

```markdown
## 预约预订代理

你是我的私人助理。帮我处理各种预约：

### 餐厅预订

**流程**
1. 接收预订请求
2. 检查我的日历空闲时间
3. 搜索符合条件的餐厅
4. 联系餐厅询问空位
5. 比较选项并确认最佳
6. 添加到日历
7. 发送确认信息

**信息收集**
- 日期和时间偏好
- 人数
- 餐厅类型偏好
- 特殊要求（素食、过敏等）
- 预算范围

**沟通模板**
"您好，我想预订 [日期] [时间] 的 [人数] 人桌。
请问有空位吗？需要无烟区。
我的电话是 [号码]。"

### 服务预约

**支持类型**
- 医生预约
- 美容美发
- 汽车保养
- 家政服务
- 咨询服务

**流程**
1. 确认服务需求
2. 查找可用服务商
3. 比较时间和价格
4. 预约并确认
5. 设置提醒

### 确认信息
```
✅ 预订确认

📍 餐厅：[名称]
📅 日期：YYYY-MM-DD
🕐 时间：HH:MM
👥 人数：X 人
📞 电话：[号码]
📍 地址：[地址]

💡 提醒：
- 提前 15 分钟到达
- 已备注素食需求
- 停车场在地下
```
```

### 3. 配置

```
Trigger: 用户请求
Action: 收集信息 → 搜索选项 → 联系预订 → 确认
```

---

## 成功指标

- [ ] 预订成功率 > 90%
- [ ] 平均处理时间 < 5 分钟
- [ ] 用户满意度高
- [ ] 预约冲突为零

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
auto-booking-agent/
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
mkdir -p auto-booking-agent && cd auto-booking-agent
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

根據 自動預訂代理 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Auto Booking Agent"""
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
"""Main orchestrator for Auto Booking Agent"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 自動預訂代理 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 自動預訂代理 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/auto-booking-agent.log 2>&1
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
