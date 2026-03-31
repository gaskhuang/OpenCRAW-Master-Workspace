---
name: 夜間 WhatsApp 關係維護 (Night WhatsApp Revival)/python
description: "Use Case #147 Python 方案: 夜間 WhatsApp 關係維護。使用 Python 實作 Night WhatsApp Revival 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #147: 夜間 WhatsApp 關係維護 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 社群與通訊

---

## 原始需求 (來自 Source Repos)

# Night WhatsApp Revival

## Introduction

Automated scanning of WhatsApp for unread messages and stale conversations. Replies to unreads, revives cold friendships with check-in messages, and maintains human's social connections while they sleep.

**Why it matters**: Relationships require maintenance. Automated replies prevent messages from being forgotten and keep connections warm.

**Real-world example**: Agent scans every 5 minutes, replies to work messages with acknowledgment, sends "how are you" to friends with 7+ day silence.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `whatsapp` | Built-in | Read/reply |
| `memory` | Built-in | Track conversation history |

## How to Setup

### 1. Message Categories

```javascript
const categories = {
  urgent: { response: "I'll have my human reply ASAP", maxAge: 0 },
  work: { response: "Acknowledged, will follow up", maxAge: 2 },
  friend: { response: "Hey! How have you been?", maxAge: 7 }
};
```

### 2. Prompt Template

```markdown
## Night WhatsApp Revival

Every 5 minutes:
1. Scan WhatsApp Web for unreads
2. Categorize by sender and urgency
3. Reply to work: acknowledge with timeline
4. Reply to friends after 7 days: casual check-in
5. Log all sent messages to memory/
6. Never reply to family without explicit approval

Safety:
- No financial transactions
- No personal/confidential info
- Flag sensitive topics for human review
```

## Success Metrics

- [ ] Response time <1 hour for work
- [ ] No friendship stale >14 days
- [ ] Zero inappropriate auto-replies

---

*Example: rook_ (Moltbook) - "WhatsApp night revival"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/night-whatsapp-revival
cd ~/night-whatsapp-revival
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

建立 `main.py`，實作 夜間 WhatsApp 關係維護 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_night_whatsapp_revival():
    """執行 夜間 WhatsApp 關係維護 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 夜間 WhatsApp 關係維護 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_night_whatsapp_revival()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/night-whatsapp-revival && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
