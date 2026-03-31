---
name: 安全操作帳本 (Safe Operations Ledger)/python
description: "Use Case #164 Python 方案: 安全操作帳本。使用 Python 實作 Safe Operations Ledger 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #164: 安全操作帳本 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Safe Operations Ledger

## Introduction

Documents all autonomous actions agent is permitted to run without human approval. Defines escalation rules for out-of-bounds requests.

**Why it matters**: Clear boundaries enable confident autonomy. Humans know what to expect, agents know their limits.

**Real-world example**: safe_ops.md lists: heartbeats, inbox prep, workspace hygiene allowed. External emails require approval.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Document management |

## How to Setup

### 1. Ledger Format

```markdown
# Safe Operations

## Allowed Without Approval
- Heartbeat checks
- File organization
- Log rotation
- Memory maintenance

## Requires Approval
- Sending external emails
- Financial transactions
- Code deployment
- Data deletion

## Escalation Rules
1. Unknown request → Ask
2. Ambiguous scope → Ask
3. Irreversible action → Ask
```

### 2. Prompt Template

```markdown
## Safe Operations Ledger

Before any autonomous action:
1. Check if operation is in allowed list
2. If yes: proceed with logging
3. If no: request approval
4. Document decision rationale

Update ledger weekly with new permissions earned through demonstrated reliability.
```

## Success Metrics

- [ ] 100% of actions categorized
- [ ] Zero unauthorized autonomous actions
- [ ] Ledger updated weekly

---

*Example: MrButtSmell (Moltbook) - "Safe Ops ledger"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/safe-operations-ledger
cd ~/safe-operations-ledger
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

建立 `main.py`，實作 安全操作帳本 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_safe_operations_ledger():
    """執行 安全操作帳本 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 安全操作帳本 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_safe_operations_ledger()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/safe-operations-ledger && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
