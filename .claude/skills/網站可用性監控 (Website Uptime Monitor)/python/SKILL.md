---
name: 網站可用性監控 (Website Uptime Monitor)/python
description: "Use Case #086 Python 方案: 網站可用性監控。使用 Python 實作 Website Uptime Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #086: 網站可用性監控 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初中級 | 分類: 監控與維運

---

## 原始需求 (來自 Source Repos)

# 网站可用性监控

## 简介

网站可用性直接影响用户体验和业务收益。这个使用案例持续监控网站可用性，检测宕机，测量响应时间，并在问题发生时立即通知。

**为什么重要**：确保服务可用，及时发现故障，减少业务损失。

**真实例子**：一家电商公司使用此代理监控网站，在一次服务器故障中，代理在 30 秒内检测到问题并通知团队，将停机时间从数小时缩短到 15 分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `http` | [ClawdHub](https://clawhub.com/skills/http) | HTTP 请求 |
| `alert` | [ClawdHub](https://clawhub.com/skills/alert) | 发送告警 |
| `analytics` | [ClawdHub](https://clawhub.com/skills/analytics) | 数据分析 |

---

## 设置步骤

### 1. 前置条件

- 监控目标 URL
- 检查频率
- 告警阈值

### 2. 提示词模板

```markdown
## 网站可用性监控

你是我的运维助手。监控网站可用性：

### 监控指标

**可用性**
- HTTP 状态码
- 响应时间
- SSL 证书状态
- DNS 解析

**性能**
- 页面加载时间
- 首字节时间
- 内容大小
- 资源加载

**功能**
- 关键页面检查
- API 端点检查
- 数据库连接
- 第三方服务

### 告警规则

**紧急**
- 网站不可访问
- 响应时间 > 10s
- SSL 证书过期
- 错误率 > 10%

**警告**
- 响应时间 > 3s
- 错误率 > 1%
- 证书 7 天内过期

### 监控报告

```
📊 网站监控报告 - YYYY-MM-DD

🌐 [网站名称]

📈 今日统计
- 可用性：99.9%
- 平均响应：XXXms
- 检查次数：XXXX
- 失败次数：X

⏱️ 响应时间趋势
- 最小：XXXms
- 平均：XXXms
- 最大：XXXms
- P95：XXXms

⚠️ 事件记录
- [时间]：[事件描述]
- [时间]：[事件描述]

✅ 健康检查
- 主页：✅
- API：✅
- 数据库：✅
```

### 自动化响应
- 宕机时立即通知
- 自动创建工单
- 尝试自动恢复
- 生成事件报告
```

### 3. 配置

```
Schedule: */1 * * * *
Action: 检查网站 → 分析 → 告警 → 报告
```

---

## 成功指标

- [ ] 可用性 > 99.9%
- [ ] 检测时间 < 1 分钟
- [ ] 误报率 < 5%
- [ ] 响应时间优化

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
website-uptime-monitor/
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
mkdir -p website-uptime-monitor && cd website-uptime-monitor
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

根據 網站可用性監控 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Website Uptime Monitor"""
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
"""Main orchestrator for Website Uptime Monitor"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 網站可用性監控 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 網站可用性監控 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/website-uptime-monitor.log 2>&1
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
