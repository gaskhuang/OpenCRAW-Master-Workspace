---
name: SSH 金鑰安全掃描 (SSH Key Security Scan)/python
description: "Use Case #079 Python 方案: SSH 金鑰安全掃描。使用 Python 實作 SSH Key Security Scan 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #079: SSH 金鑰安全掃描 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# SSH 密钥扫描器

## 简介

SSH 密钥管理是安全运维的重要环节。这个使用案例扫描 SSH 密钥，检查密钥强度、过期时间和使用权限，识别潜在的安全风险。

**为什么重要**：防止未授权访问，确保密钥安全，符合合规要求。

**真实例子**：一家公司使用此代理扫描所有服务器的 SSH 密钥，发现 10+ 个弱密钥和 5 个过期密钥，及时修复避免了安全风险。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `ssh` | [ClawdHub](https://clawhub.com/skills/ssh) | SSH 操作 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全扫描 |
| `filesystem` | 内置 | 文件访问 |

---

## 设置步骤

### 1. 前置条件

- SSH 访问权限
- 密钥存储位置
- 安全策略

### 2. 提示词模板

```markdown
## SSH 密钥扫描器

你是我的安全助手。扫描 SSH 密钥安全：

### 扫描内容

**密钥强度**
- 密钥算法（RSA/ECDSA/Ed25519）
- 密钥长度
- 生成时间
- 使用频率

**密钥状态**
- 是否过期
- 是否撤销
- 是否共享
- 权限设置

**使用审计**
- 最后使用时间
- 使用来源 IP
- 登录频率
- 异常登录

### 扫描报告

```
🔐 SSH 密钥扫描报告 - YYYY-MM-DD

📊 概览
- 总密钥数：XX
- 强密钥：XX
- 弱密钥：XX
- 过期密钥：XX

❌ 高风险
1. [密钥] - [问题]
   位置：[路径]
   建议：[操作]

⚠️ 中风险
1. [密钥] - [问题]
   建议：[操作]

✅ 良好
- [密钥] - 强密钥，配置正确

📋 建议操作
1. [操作 1]
2. [操作 2]
```

### 修复建议

**弱密钥**
```bash
# 生成新密钥
ssh-keygen -t ed25519 -C "user@host"

# 更新 authorized_keys
cat new_key.pub >> ~/.ssh/authorized_keys

# 删除旧密钥
```

**权限修复**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
```

### 3. 配置

```
Schedule: 0 2 * * 0
Action: 扫描密钥 → 分析 → 生成报告 → 发送通知
```

---

## 成功指标

- [ ] 所有密钥符合安全标准
- [ ] 弱密钥及时替换
- [ ] 过期密钥及时撤销
- [ ] 安全事件零发生

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
ssh-key-security-scan/
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
mkdir -p ssh-key-security-scan && cd ssh-key-security-scan
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

根據 SSH 金鑰安全掃描 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for SSH Key Security Scan"""
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
"""Main orchestrator for SSH Key Security Scan"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== SSH 金鑰安全掃描 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 SSH 金鑰安全掃描 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/ssh-key-security-scan.log 2>&1
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
