---
name: API 安全測試 (API Security Testing)/python
description: "Use Case #082 Python 方案: API 安全測試。使用 Python 實作 API Security Testing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #082: API 安全測試 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中高級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# API 安全测试器

## 简介

API 是系统的关键入口，需要定期安全测试。这个使用案例自动测试 API 安全性，识别漏洞，验证认证授权，并生成安全报告。

**为什么重要**：保护 API 免受攻击，确保数据安全，符合安全标准。

**真实例子**：一家公司使用此代理测试其 API，发现了 SQL 注入和权限绕过漏洞，及时修复避免了数据泄露。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `api_testing` | [ClawdHub](https://clawhub.com/skills/api) | API 测试 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全测试 |
| `vulnerability` | [ClawdHub](https://clawhub.com/skills/vuln) | 漏洞扫描 |

---

## 设置步骤

### 1. 前置条件

- API 文档
- 测试账号
- 测试环境

### 2. 提示词模板

```markdown
## API 安全测试器

你是我的安全测试员。测试 API 安全性：

### 测试项目

**认证测试**
- 弱密码测试
- 暴力破解防护
- Token 过期
- 会话管理

**授权测试**
- 水平越权
- 垂直越权
- IDOR 漏洞
- 权限绕过

**输入验证**
- SQL 注入
- XSS 攻击
- 命令注入
- 路径遍历

**敏感数据**
- 数据泄露
- 加密传输
- 日志脱敏
- 错误信息

### 测试报告

```
🔒 API 安全测试报告 - YYYY-MM-DD

📊 概览
- 测试端点：XX 个
- 发现问题：XX 个
- 高危漏洞：XX 个
- 中危漏洞：XX 个

🚨 高危漏洞
1. [端点] - [漏洞类型]
   描述：[描述]
   影响：[影响]
   修复：[建议]

⚠️ 中危漏洞
1. [端点] - [漏洞类型]
   描述：[描述]
   修复：[建议]

✅ 通过测试
- [端点] - 安全

📋 修复优先级
1. [漏洞] - 立即修复
2. [漏洞] - 本周修复
```

### 修复建议

**SQL 注入**
```python
# 使用参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**权限控制**
```python
# 验证用户权限
if not user.has_permission('resource', 'read'):
    return 403
```
```

### 3. 配置

```
Schedule: 0 3 * * 0
Action: 扫描 API → 测试漏洞 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 高危漏洞零遗留
- [ ] API 安全评分 > 90
- [ ] 安全事件零发生
- [ ] 合规检查通过

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
api-security-testing/
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
mkdir -p api-security-testing && cd api-security-testing
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

根據 API 安全測試 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for API Security Testing"""
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
"""Main orchestrator for API Security Testing"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== API 安全測試 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 API 安全測試 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/api-security-testing.log 2>&1
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
