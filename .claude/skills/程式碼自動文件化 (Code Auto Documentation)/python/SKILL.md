---
name: 程式碼自動文件化 (Code Auto Documentation)/python
description: "Use Case #078 Python 方案: 程式碼自動文件化。使用 Python 實作 Code Auto Documentation 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #078: 程式碼自動文件化 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: DevOps 與工程

---

## 原始需求 (來自 Source Repos)

# 代码转文档生成器

## 简介

维护代码文档是一项繁琐但重要的工作。这个使用案例自动分析代码，生成 API 文档、README 和代码注释，保持文档与代码同步。

**为什么重要**：提高代码可维护性，帮助团队协作，减少文档维护负担。

**真实例子**：一个开发团队使用此代理自动生成 API 文档，文档始终与代码同步，新成员上手时间减少了 50%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `code_parser` | [ClawdHub](https://clawhub.com/skills/code) | 解析代码 |
| `documentation` | [ClawdHub](https://clawhub.com/skills/docs) | 生成文档 |
| `git` | [ClawdHub](https://clawhub.com/skills/git) | 版本控制 |

---

## 设置步骤

### 1. 前置条件

- 代码仓库访问
- 文档模板
- 输出格式

### 2. 提示词模板

```markdown
## 代码转文档生成器

你是我的技术文档助手。从代码生成文档：

### 分析内容

**代码结构**
- 类和函数
- 参数和返回值
- 类型注解
- 异常处理

**代码注释**
- Docstring
- 行内注释
- TODO 标记
- 弃用标记

**依赖关系**
- 导入的模块
- 函数调用链
- 类继承关系

### 生成文档

**API 文档**
```markdown
## Function Name

**描述**
函数功能描述

**参数**
| 参数 | 类型 | 描述 |
|------|------|------|
| param1 | str | 描述 |

**返回值**
| 类型 | 描述 |
|------|------|
| bool | 描述 |

**示例**
```python
result = function_name("input")
```

**异常**
- ValueError: 参数无效
```

**README**
- 项目介绍
- 安装指南
- 使用示例
- API 概览
- 贡献指南

### 自动化
- 代码提交时更新
- 检查文档完整性
- 标记缺失文档
- 生成变更日志
```

### 3. 配置

```
Trigger: Git 提交
Action: 分析代码 → 生成文档 → 提交更新
```

---

## 成功指标

- [ ] 文档覆盖率 > 90%
- [ ] 文档与代码同步
- [ ] 新成员上手快
- [ ] 维护负担减轻

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# API 文档生成器

## 简介

从代码自动生成 API 文档，保持文档与代码同步。

**为什么重要**：减少文档维护工作，确保文档准确，提高开发效率。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `code_analysis` | [ClawdHub](https://clawhub.com/skills/code) | 代码分析 |
| `docs` | [ClawdHub](https://clawhub.com/skills/docs) | 文档生成 |

---

## 使用方式

连接代码库，自动生成文档

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
code-auto-documentation/
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
mkdir -p code-auto-documentation && cd code-auto-documentation
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

根據 程式碼自動文件化 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Code Auto Documentation"""
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
"""Main orchestrator for Code Auto Documentation"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 程式碼自動文件化 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 程式碼自動文件化 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/code-auto-documentation.log 2>&1
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
