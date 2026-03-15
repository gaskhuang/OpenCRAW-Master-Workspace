---
name: 晨間摘要生成器 (Morning Digest Generator)/python
description: "Use Case #167 Python 方案: 晨間摘要生成器。使用 Python 實作 Morning Digest Generator 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #167: 晨間摘要生成器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# Morning Digest Generator

## Introduction

Compiles overnight activity into consolidated morning briefing: what happened, what the agent did, what needs human attention.

**Why it matters**: Humans need context, not noise. Digest format enables quick triage without overwhelming detail.

**Real-world example**: Agent summarizes 50 overnight events into 5 bullet points, human reviews in 30 seconds over coffee.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Log reading |
| `telegram` | Built-in | Delivery |

## How to Setup

### 1. Digest Format

```markdown
🌅 Morning Digest - Feb 19

## Overnight Activity
- 3 cron jobs completed
- 1 security scan passed
- 12 emails sorted

## Agent Actions
- Fixed 2 documentation typos
- Archived old memory files
- Sent 1 weather report

## Needs Attention
- 1 urgent email flagged
- GitHub issue #234 critical

## Today Reminders
- Meeting at 14:00
- Deploy scheduled for 16:00
```

### 2. Prompt Template

```markdown
## Morning Digest Generator

Every day at 07:00:
1. Read overnight logs
2. Categorize by type
3. Prioritize by urgency
4. Generate digest
5. Send via preferred channel
6. Include actionable items first
```

## Success Metrics

- [ ] Digest delivered by 07:00
- [ ] Read time <2 minutes
- [ ] All urgent items flagged

---

*Example: OwlBlue (Moltbook) - "morning briefing ready"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/morning-digest-generator
cd ~/morning-digest-generator
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

建立 `main.py`，實作 晨間摘要生成器 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_morning_digest_generator():
    """執行 晨間摘要生成器 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 晨間摘要生成器 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_morning_digest_generator()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/morning-digest-generator && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
