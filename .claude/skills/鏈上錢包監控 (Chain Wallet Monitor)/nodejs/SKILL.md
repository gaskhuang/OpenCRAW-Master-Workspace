---
name: 鏈上錢包監控 (Chain Wallet Monitor)/nodejs
description: "Use Case #151 Node.js 方案: 鏈上錢包監控。使用 Node.js 實作 Chain Wallet Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #151: 鏈上錢包監控 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 加密貨幣與 DeFi

---

## 原始需求 (來自 Source Repos)

# Chain Wallet Monitor

## Introduction

On-chain wallet surveillance tracking unusual movements, new contract deployments, and governance proposals affecting tracked addresses.

**Why it matters**: Blockchain events happen 24/7. Early detection of suspicious activity or opportunities requires constant monitoring.

**Real-world example**: Agent detects 10K ETH movement from whale wallet, alerts within minutes, human evaluates trading opportunity.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`web3`](https://clawhub.ai/skills/claw-fi) | ClawHub | Blockchain queries |
| `telegram` | Built-in | Alerts |

## How to Setup

### 1. Wallet Tracking

```javascript
const wallets = [
  { address: "0x...", label: "Whale A", threshold: 1000 }
];
```

### 2. Prompt Template

```markdown
## Chain Wallet Monitor

Every 10 minutes:
1. Query tracked wallets for new transactions
2. Detect transfers above threshold
3. Identify new contract interactions
4. Flag governance votes
5. Immediate alert for large movements

Thresholds:
- Whale wallets: 1000 ETH
- Portfolio: 10% of holdings
- Known entities: any movement
```

## Success Metrics

- [ ] Detection within 10 minutes
- [ ] False positive rate <5%
- [ ] All movements logged

---

*Example: Onchain3r (Moltbook) - On-chain monitoring*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/chain-wallet-monitor
cd ~/chain-wallet-monitor
npm init -y
npm install @anthropic-ai/sdk dotenv
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `index.js`，實作 鏈上錢包監控 的核心邏輯。

```javascript
import Anthropic from "@anthropic-ai/sdk";
import dotenv from "dotenv";

dotenv.config();
const client = new Anthropic();

async function run() {
  const response = await client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "請協助我執行 鏈上錢包監控 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/chain-wallet-monitor && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
