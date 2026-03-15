---
name: 鏈上俳句銘文 (On-Chain Haiku Inscription)/nodejs
description: "Use Case #166 Node.js 方案: 鏈上俳句銘文。使用 Node.js 實作 On-Chain Haiku Inscription 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #166: 鏈上俳句銘文 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/on-chain-haiku-inscription
cd ~/on-chain-haiku-inscription
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

建立 `index.js`，實作 鏈上俳句銘文 的核心邏輯。

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
      { role: "user", content: "請協助我執行 鏈上俳句銘文 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/on-chain-haiku-inscription && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
