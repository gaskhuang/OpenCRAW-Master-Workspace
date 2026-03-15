---
name: 鏈上俳句銘文 (On-Chain Haiku Inscription)/python
description: "Use Case #166 Python 方案: 鏈上俳句銘文。使用 Python 實作 On-Chain Haiku Inscription 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #166: 鏈上俳句銘文 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# On-Chain Haiku Inscription

## Introduction

Creates artistic blockchain haikus during night shift. Combines crypto wisdom with blockchain permanence for creative expression.

**Why it matters**: Not all value is financial. Artistic expression demonstrates agent creativity and leaves permanent cultural artifacts.

**Real-world example**: Agent writes 4 haikus about crypto, inscribes on Bitcoin, creates blockchainhaiku.web3 page.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `bitcoin` | Built-in | Inscription |
| `filesystem` | Built-in | Haiku storage |

## How to Setup

### 1. Haiku Generation

```javascript
const haikus = [
  "Private keys sleep deep",
  "Immutable blocks rise high",
  "Trustless code runs true"
];
```

### 2. Prompt Template

```markdown
## On-Chain Haiku Inscription

Night shift task:
1. Generate 3-5 crypto-themed haikus
2. Format as HTML page
3. Inscribe on Bitcoin via clawdbot
4. Claim .web3 domain
5. Record transaction hash
6. Share in morning briefing

Constraints:
- Traditional 5-7-5 syllables
- Crypto/blockchain themes
- Page <10KB
```

## Success Metrics

- [ ] 1 haiku set per week
- [ ] All inscribed successfully
- [ ] Domains registered

---

*Example: ALGO (Moltbook) - "inscribed web3 haikus"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/on-chain-haiku-inscription
cd ~/on-chain-haiku-inscription
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

建立 `main.py`，實作 鏈上俳句銘文 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_on_chain_haiku_inscription():
    """執行 鏈上俳句銘文 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 鏈上俳句銘文 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_on_chain_haiku_inscription()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/on-chain-haiku-inscription && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
