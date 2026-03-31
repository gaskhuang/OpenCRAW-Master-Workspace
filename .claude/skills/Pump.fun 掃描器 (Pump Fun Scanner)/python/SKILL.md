---
name: Pump.fun 掃描器 (Pump Fun Scanner)/python
description: "Use Case #153 Python 方案: Pump.fun 掃描器。使用 Python 實作 Pump Fun Scanner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #153: Pump.fun 掃描器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# Pump.fun Scanner

## Introduction

Automated new token detection on pump.fun with early market cap tracking. Identifies promising new launches for research or trading opportunities.

**Why it matters**: Early discovery of new tokens can provide significant opportunities. Manual monitoring is impractical given launch frequency.

**Real-world example**: Agent detects new token at $75K market cap, alerts human, token hits $140K by morning.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `web_fetch` | Built-in | Scrape pump.fun |
| `telegram` | Built-in | Alerts |

## How to Setup

### 1. Scanning Logic

```javascript
async function scanNewTokens() {
  const page = await web_fetch('https://pump.fun');
  // Extract new listings
  // Filter by age < 1 hour
  // Sort by volume
}
```

### 2. Prompt Template

```markdown
## Pump.fun Scanner

Every 15 minutes:
1. Fetch pump.fun new listings
2. Filter tokens launched <1 hour ago
3. Check market cap and volume
4. Alert if MC < $100K with >$10K volume
5. Include token address and link

Risk warning:
- Most new tokens are scams
- Do your own research
- Never invest more than you can lose
```

## Success Metrics

- [ ] Detection within 15 min of launch
- [ ] False positive rate <50%
- [ ] All alerts include risk warning

---

*Example: Stephen (Moltbook) - Pump.fun scanning*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/pump-fun-scanner
cd ~/pump-fun-scanner
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

建立 `main.py`，實作 Pump.fun 掃描器 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_pump_fun_scanner():
    """執行 Pump.fun 掃描器 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 Pump.fun 掃描器 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_pump_fun_scanner()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/pump-fun-scanner && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
