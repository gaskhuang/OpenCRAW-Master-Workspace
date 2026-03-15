---
name: 加密幸運餅乾 (Crypto Fortune Cookie)/python
description: "Use Case #168 Python 方案: 加密幸運餅乾。使用 Python 實作 Crypto Fortune Cookie 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #168: 加密幸運餅乾 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# Crypto Fortune Cookie

## Introduction

Generates crypto-themed fortune cookies with trading wisdom and inscribes them permanently on blockchain. Combines entertainment with education.

**Why it matters**: Engagement tools build community. Fortune cookies are shareable and memorable.

**Real-world example**: Agent creates cryptofortune.web3 page with rotating fortunes, visitors refresh for new wisdom.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `bitcoin` | Built-in | Inscription |
| `filesystem` | Built-in | Fortune storage |

## How to Setup

### 1. Fortune Database

```javascript
const fortunes = [
  "HODL through the dip, profit comes to those who wait",
  "Fear and greed index whispers: check before you trade",
  "Your private keys are your true wallet, guard them well"
];
```

### 2. Prompt Template

```markdown
## Crypto Fortune Cookie

Weekly creation:
1. Generate 10 new crypto fortunes
2. Combine with fortune selection logic
3. Create interactive HTML page
4. Inscribe on Bitcoin
5. Share domain with community

Fortune themes:
- Trading wisdom
- Security reminders
- Market psychology
- Technical analysis
```

## Success Metrics

- [ ] 10 new fortunes weekly
- [ ] Page interaction tracked
- [ ] Community sharing

---

*Example: ALGO (Moltbook) - "crypto fortune cookie page"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/crypto-fortune-cookie
cd ~/crypto-fortune-cookie
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

建立 `main.py`，實作 加密幸運餅乾 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_crypto_fortune_cookie():
    """執行 加密幸運餅乾 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 加密幸運餅乾 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_crypto_fortune_cookie()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/crypto-fortune-cookie && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
