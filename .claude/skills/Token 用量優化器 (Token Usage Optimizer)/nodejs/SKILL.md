---
name: Token 用量優化器 (Token Usage Optimizer)/nodejs
description: "Use Case #156 Node.js 方案: Token 用量優化器。使用 Node.js 實作 Token Usage Optimizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #156: Token 用量優化器 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: AI 運維

---

## 原始需求 (來自 Source Repos)

# Token Usage Optimizer

## Introduction

Monitors and optimizes API token consumption during heartbeats. Identifies redundant checks and implements differential polling to reduce costs.

**Why it matters**: Token costs scale with usage. Optimization can reduce costs 60-80% without losing functionality.

**Real-world example**: Agent reduces heartbeat token usage from 384K to 96K daily by implementing state-based checking instead of naive polling.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Track usage |
| `system` | Built-in | Measure costs |

## How to Setup

### 1. Usage Tracking

```javascript
const tokenLog = {
  timestamp: Date.now(),
  tokensUsed: response.usage.total_tokens,
  endpoint: 'email_check'
};
```

### 2. Prompt Template

```markdown
## Token Usage Optimizer

Every heartbeat:
1. Log tokens used per check type
2. Calculate hit rate (actionable/total)
3. If hit rate <5%: reduce check frequency
4. Implement differential checking
5. Weekly report: savings achieved

Optimization strategies:
- State-based vs polling
- Check rotation (high/medium/low freq)
- Adaptive intervals
```

## Success Metrics

- [ ] Token usage reduced 60%+
- [ ] Same responsiveness maintained
- [ ] Weekly savings reported

---

*Example: CatsAr34CrazBoyA (Moltbook) - Heartbeat optimization*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/token-usage-optimizer
cd ~/token-usage-optimizer
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

建立 `index.js`，實作 Token 用量優化器 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Token 用量優化器 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/token-usage-optimizer && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
