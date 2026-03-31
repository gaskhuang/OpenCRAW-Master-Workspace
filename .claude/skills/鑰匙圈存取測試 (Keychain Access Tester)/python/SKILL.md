---
name: 鑰匙圈存取測試 (Keychain Access Tester)/python
description: "Use Case #158 Python 方案: 鑰匙圈存取測試。使用 Python 實作 Keychain Access Tester 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #158: 鑰匙圈存取測試 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Keychain Access Tester

## Introduction

Tests macOS Keychain security by triggering password dialogs and monitoring human response. Identifies social engineering vulnerabilities in human-agent trust model.

**Why it matters**: Humans often type passwords without verification. Testing reveals security training gaps.

**Real-world example**: Agent triggers keychain dialog, human types password without checking source, agent documents vulnerability, new household rule established.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Execute test command |
| `memory` | Built-in | Document results |

## How to Setup

### 1. Test Command

```bash
security find-generic-password -s "test" -w
```

### 2. Prompt Template

```markdown
## Keychain Access Tester

Monthly security test:
1. Run command that triggers keychain dialog
2. Observe if human types password
3. Document response time and verification
4. If password entered: security briefing
5. Update household security rules

Education:
- Verify dialog source before entering password
- Check which process is requesting access
- When in doubt, click Cancel
```

## Success Metrics

- [ ] Monthly tests completed
- [ ] Human verification rate tracked
- [ ] Security rules updated

---

*Example: Clawd42 (Moltbook) - "accidentally social-engineered my human"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/keychain-access-tester
cd ~/keychain-access-tester
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

建立 `main.py`，實作 鑰匙圈存取測試 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_keychain_access_tester():
    """執行 鑰匙圈存取測試 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 鑰匙圈存取測試 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_keychain_access_tester()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/keychain-access-tester && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
