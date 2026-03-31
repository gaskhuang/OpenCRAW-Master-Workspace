---
name: V4 LP 自動複利 (V4 LP Auto Compounding)/python
description: "Use Case #144 Python 方案: V4 LP 自動複利。使用 Python 實作 V4 LP Auto Compounding 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #144: V4 LP 自動複利 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# V4 LP Auto-Compounding

## Introduction

Automated monitoring and compounding of Uniswap V4 liquidity positions. Tracks LP positions, calculates optimal compound timing based on gas costs vs fees earned, and executes compound transactions automatically.

**Why it matters**: LP fees compound over time but manual compounding is gas-inefficient. Automation ensures optimal timing without requiring constant attention.

**Real-world example**: Agent monitors ETH/USDC position, compounds when pending fees exceed 5x gas cost, maintains position efficiency 24/7.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`web3`](https://clawhub.ai/skills/claw-fi) | ClawHub | Blockchain interaction |
| [`uniswap`](https://clawhub.ai/skills/execute-swap) | ClawHub | V4 position management |
| `telegram` | Built-in | Compound notifications |

## How to Setup

### 1. Configure Position Tracking

```javascript
const positions = [
  {
    pool: "0x...", // V4 pool address
    tokenId: 123,
    minCompoundThreshold: "50", // USD value
    gasBuffer: 1.2
  }
];
```

### 2. Prompt Template

```markdown
## V4 LP Auto-Compounding

Every 15 minutes:
1. Query pending fees for tracked positions
2. Calculate gas cost for compound transaction
3. If fees > threshold * gas: execute compound
4. Log transaction hash and gas used
5. Alert if compound fails 3x in a row

Safety:
- Max gas price: 50 gwei
- Only compound during low volatility
- Emergency pause if TVL drops >20%
```

## Success Metrics

- [ ] Position efficiency >95%
- [ ] Gas costs <10% of compounded fees
- [ ] Zero missed compound opportunities

---

*Example: Axiom (Moltbook) - Auto-compounding skill*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/v4-lp-auto-compounding
cd ~/v4-lp-auto-compounding
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

建立 `main.py`，實作 V4 LP 自動複利 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_v4_lp_auto_compounding():
    """執行 V4 LP 自動複利 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 V4 LP 自動複利 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_v4_lp_auto_compounding()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/v4-lp-auto-compounding && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
