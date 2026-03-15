---
name: Pump.fun 掃描器 (Pump Fun Scanner)/nodejs
description: "Use Case #153 Node.js 方案: Pump.fun 掃描器。使用 Node.js 實作 Pump Fun Scanner 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #153: Pump.fun 掃描器 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/pump-fun-scanner
cd ~/pump-fun-scanner
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

建立 `index.js`，實作 Pump.fun 掃描器 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Pump.fun 掃描器 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/pump-fun-scanner && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
