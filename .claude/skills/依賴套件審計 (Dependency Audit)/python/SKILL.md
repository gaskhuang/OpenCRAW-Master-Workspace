---
name: 依賴套件審計 (Dependency Audit)/python
description: "Use Case #075 Python 方案: 依賴套件審計。使用 Python 實作 Dependency Audit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #075: 依賴套件審計 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 依赖更新检查器

## 简介

项目依赖需要定期更新以获得安全补丁和新功能。这个使用案例检查项目依赖的更新，评估影响，并生成更新建议。

**为什么重要**：保持依赖最新，修复安全漏洞，获得新功能。

**真实例子**：一个开发团队使用此代理检查依赖更新，及时修复了一个严重的安全漏洞，避免了潜在的数据泄露风险。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `package_manager` | [ClawdHub](https://clawhub.com/skills/package) | 包管理 |
| `github` | [ClawdHub](https://clawhub.com/skills/github) | 获取更新 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全扫描 |

---

## 设置步骤

### 1. 前置条件

- 项目仓库访问
- 包管理器配置
- 更新策略

### 2. 提示词模板

```markdown
## 依赖更新检查器

你是我的开发助手。检查和管理依赖更新：

### 检查内容

**安全更新**
- 已知漏洞
- 安全补丁
- 紧急修复

**功能更新**
- 新功能
- 性能改进
- Bug 修复

**重大更新**
- 破坏性变更
- 迁移指南
- 兼容性检查

### 评估标准

**更新优先级**
- 严重：安全漏洞
- 高：重要 Bug 修复
- 中：新功能
- 低：次要改进

**风险评估**
- 变更范围
- 测试覆盖
- 回滚难度
- 依赖冲突

### 更新报告

```
📦 依赖更新报告 - YYYY-MM-DD

🚨 安全更新（立即处理）
1. [包名] [当前] → [最新]
   漏洞：[CVE-ID]
   严重性：[严重/高危/中危]
   修复：[版本]

📈 重大更新（需要评估）
1. [包名] [当前] → [最新]
   变更：[破坏性变更]
   迁移：[指南链接]
   建议：[操作]

✨ 功能更新（建议更新）
1. [包名] [当前] → [最新]
   新功能：[描述]
   改进：[描述]

📊 统计
- 可更新：XX 个
- 安全更新：XX 个
- 重大更新：XX 个
```

### 自动化
- 每周检查更新
- 安全更新立即通知
- 生成 PR 更新依赖
- 运行测试验证
```

### 3. 配置

```
Schedule: 0 9 * * 1
Action: 检查更新 → 评估 → 生成报告 → 创建 PR
```

---

## 成功指标

- [ ] 安全漏洞及时修复
- [ ] 依赖保持最新
- [ ] 无破坏性变更
- [ ] 项目稳定性保持

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 技能供应链审计

## 简介

审计 OpenClaw 技能供应链安全，检查依赖风险，验证来源可信。

**为什么重要**：防止供应链攻击，确保技能安全，保护系统完整性。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `skills` | [ClawdHub](https://clawhub.com/skills/skills) | 技能管理 |
| `security` | [ClawdHub](https://clawhub.com/skills/security) | 安全审计 |

---

## 使用方式

审计已安装技能，生成风险报告

---

## 来源

- 作者：OpenClaw 社区


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
dependency-audit/
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
mkdir -p dependency-audit && cd dependency-audit
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

根據 依賴套件審計 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Dependency Audit"""
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
"""Main orchestrator for Dependency Audit"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 依賴套件審計 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 依賴套件審計 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/dependency-audit.log 2>&1
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
