---
name: 安全操作帳本 (Safe Operations Ledger)/nodejs
description: "Use Case #164 Node.js 方案: 安全操作帳本。使用 Node.js 實作 Safe Operations Ledger 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #164: 安全操作帳本 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Safe Operations Ledger

## Introduction

Documents all autonomous actions agent is permitted to run without human approval. Defines escalation rules for out-of-bounds requests.

**Why it matters**: Clear boundaries enable confident autonomy. Humans know what to expect, agents know their limits.

**Real-world example**: safe_ops.md lists: heartbeats, inbox prep, workspace hygiene allowed. External emails require approval.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Document management |

## How to Setup

### 1. Ledger Format

```markdown
# Safe Operations

## Allowed Without Approval
- Heartbeat checks
- File organization
- Log rotation
- Memory maintenance

## Requires Approval
- Sending external emails
- Financial transactions
- Code deployment
- Data deletion

## Escalation Rules
1. Unknown request → Ask
2. Ambiguous scope → Ask
3. Irreversible action → Ask
```

### 2. Prompt Template

```markdown
## Safe Operations Ledger

Before any autonomous action:
1. Check if operation is in allowed list
2. If yes: proceed with logging
3. If no: request approval
4. Document decision rationale

Update ledger weekly with new permissions earned through demonstrated reliability.
```

## Success Metrics

- [ ] 100% of actions categorized
- [ ] Zero unauthorized autonomous actions
- [ ] Ledger updated weekly

---

*Example: MrButtSmell (Moltbook) - "Safe Ops ledger"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/safe-operations-ledger
cd ~/safe-operations-ledger
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

建立 `index.js`，實作 安全操作帳本 的核心邏輯。

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
      { role: "user", content: "請協助我執行 安全操作帳本 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/safe-operations-ledger && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
