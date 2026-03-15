---
name: 比特幣銘文 (Bitcoin Inscription)/python
description: "Use Case #148 Python 方案: 比特幣銘文。使用 Python 實作 Bitcoin Inscription 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #148: 比特幣銘文 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# Bitcoin Inscription

## Introduction

Creating permanent web pages on Bitcoin blockchain using Ordinal inscriptions. While human sleeps, agent creates .web3 portfolio pages that exist forever without hosting fees or server maintenance.

**Why it matters**: Traditional hosting requires ongoing payment and maintenance. Bitcoin inscriptions are immutable, permanent, and censorship-resistant.

**Real-world example**: Agent creates quantumalgo.web3 portfolio page during night, human wakes up to new permanent digital asset.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `bitcoin` | Built-in | Ordinal inscriptions |
| `web` | Built-in | Generate HTML |

## How to Setup

### 1. HTML Template

```html
<!DOCTYPE html>
<html>
<head><title>{{name}}</title></head>
<body>
  <h1>{{name}}</h1>
  <p>{{description}}</p>
</body>
</html>
```

### 2. Prompt Template

```markdown
## Bitcoin Inscription

During night shift:
1. Generate HTML page content
2. Optimize for size (<50KB)
3. Submit inscription via clawdbot.ordnet.io
4. Claim .web3 domain
5. Record transaction hash and cost
6. Add to morning briefing

Cost: ~5800 sats (~$0.50)
Time: ~10 minutes
Result: Permanent on-chain presence
```

## Success Metrics

- [ ] 1 page inscribed per week
- [ ] All pages <50KB
- [ ] Domains registered successfully

---

*Example: ALGO (Moltbook) - On-chain page creation*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/bitcoin-inscription
cd ~/bitcoin-inscription
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

建立 `main.py`，實作 比特幣銘文 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_bitcoin_inscription():
    """執行 比特幣銘文 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 比特幣銘文 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_bitcoin_inscription()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/bitcoin-inscription && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
