---
name: 客戶訊號掃描器 (Customer Signal Scanner)/python
description: "Use Case #152 Python 方案: 客戶訊號掃描器。使用 Python 實作 Customer Signal Scanner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #152: 客戶訊號掃描器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 商業與銷售

---

## 原始需求 (來自 Source Repos)

# Customer Signal Scanner

## Introduction

Scans Telegram/Discord channels for product mentions, feature requests, and customer feedback. Extracts actionable insights from community conversations.

**Why it matters**: Customer feedback is scattered across channels. Centralized scanning captures insights that would otherwise be lost.

**Real-world example**: Agent monitors 5 community channels, finds 12 feature mentions in 24h, compiles top 3 requests for product team.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `telegram` | Built-in | Channel monitoring |
| `discord` | Built-in | Server monitoring |

## How to Setup

### 1. Signal Detection

```javascript
const keywords = [
  "feature request", "would be nice", "missing",
  "bug", "broken", "not working"
];
```

### 2. Prompt Template

```markdown
## Customer Signal Scanner

Every hour:
1. Scan configured channels for keywords
2. Extract message + context
3. Categorize: feature request / bug / praise
4. Score by engagement (replies/reactions)
5. Daily report: top 10 signals

Privacy:
- Only public channels
- Anonymize usernames
- Aggregate by topic
```

## Success Metrics

- [ ] 100% channel coverage
- [ ] Signals categorized accurately
- [ ] Report delivered daily

---

*Example: bicep (Moltbook) - Signal scanning*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/customer-signal-scanner
cd ~/customer-signal-scanner
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `main.py`，實作 客戶訊號掃描器 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_customer_signal_scanner():
    """執行 客戶訊號掃描器 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 客戶訊號掃描器 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_customer_signal_scanner()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/customer-signal-scanner && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
