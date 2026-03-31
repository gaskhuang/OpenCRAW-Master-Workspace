---
name: 比特幣銘文 (Bitcoin Inscription)/nodejs
description: "Use Case #148 Node.js 方案: 比特幣銘文。使用 Node.js 實作 Bitcoin Inscription 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #148: 比特幣銘文 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/bitcoin-inscription
cd ~/bitcoin-inscription
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

建立 `index.js`，實作 比特幣銘文 的核心邏輯。

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
      { role: "user", content: "請協助我執行 比特幣銘文 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/bitcoin-inscription && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
