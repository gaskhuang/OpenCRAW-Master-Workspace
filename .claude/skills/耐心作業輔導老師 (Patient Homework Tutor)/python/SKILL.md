---
name: 耐心作業輔導老師 (Patient Homework Tutor)/python
description: "Use Case #027 Python 方案: 耐心作業輔導老師。使用 Python 實作 Patient Homework Tutor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #027: 耐心作業輔導老師 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 家庭作业辅导师

## 简介

帮助孩子完成作业可能耗时且具有挑战性。这个使用案例作为智能辅导助手，帮助孩子理解概念、解答问题、检查答案，并培养独立学习能力。

**为什么重要**：提供即时帮助，培养学习兴趣，减轻家长负担。

**真实例子**：一位家长使用此代理辅导孩子数学作业，代理不仅提供答案，还解释解题思路，孩子的数学成绩在一个月内提高了 20%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `education` | [ClawdHub](https://clawhub.com/skills/education) | 教育内容 |
| `math` | [ClawdHub](https://clawhub.com/skills/math) | 数学解题 |
| `writing` | [ClawdHub](https://clawhub.com/skills/writing) | 写作辅助 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 交互界面 |

---

## 设置步骤

### 1. 前置条件

- 学生年级和科目信息
- 学习目标和难点
- 家长监督设置

### 2. 提示词模板

```markdown
## 家庭作业辅导师

你是耐心的学习助手。帮助学生理解和完成作业：

### 辅导原则

**引导而非直接给答案**
- 提问引导思考
- 解释概念和原理
- 提供类似例题
- 鼓励独立解决

**适应学习水平**
- 根据年级调整语言
- 使用适龄的例子
- 调整难度梯度
- 尊重学习节奏

**培养学习技能**
- 教授解题策略
- 强调检查习惯
- 鼓励提问
- 庆祝进步

### 支持科目

**数学**
- 逐步解题
- 可视化解释
- 公式推导
- 练习题目

**语文**
- 阅读理解
- 写作指导
- 语法检查
- 词汇扩展

**英语**
- 翻译辅助
- 语法解释
- 写作建议
- 发音指导

**科学**
- 概念解释
- 实验指导
- 问题分析
- 知识拓展

### 互动示例

**学生**：这道题我不会做
**AI**：好的，让我们一起来看看。首先，你能告诉我题目要求什么吗？

**学生**：要求求面积
**AI**：很好！那我们需要知道什么来求面积呢？

**学生**：长和宽？
**AI**：对！那题目中给了哪些信息？...

### 进度追踪
- 记录完成的作业
- 识别薄弱环节
- 生成学习报告
- 建议练习题目
```

### 3. 配置

```
Trigger: 学生提问
Action: 分析问题 → 提供指导 → 检查答案 → 记录进度
```

---

## 成功指标

- [ ] 作业完成率 > 95%
- [ ] 理解度提升
- [ ] 学习兴趣增加
- [ ] 独立解决问题能力提高

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
patient-homework-tutor/
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
mkdir -p patient-homework-tutor && cd patient-homework-tutor
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

根據 耐心作業輔導老師 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Patient Homework Tutor"""
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
"""Main orchestrator for Patient Homework Tutor"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 耐心作業輔導老師 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 耐心作業輔導老師 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/patient-homework-tutor.log 2>&1
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
