---
name: 七子代理夜間並行 (Seven Sub-Agent Night Parallel)/nodejs
description: "Use Case #145 Node.js 方案: 七子代理夜間並行。使用 Node.js 實作 Seven Sub-Agent Night Parallel 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #145: 七子代理夜間並行 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: Agent 架構

---

## 原始需求 (來自 Source Repos)

# 7-Sub-Agent Night Parallel

## Introduction

Runs 7 parallel sub-agents during night shift, each handling different tasks: memory cleanup, budget preparation, TTS research, book recommendations, self-improvement research, AI memory neuroscience, and advisor pattern study. All results committed to git by morning.

**Why it matters**: Parallel execution multiplies productivity while human sleeps. Different cognitive tasks can run simultaneously without interference.

**Real-world example**: At 11 PM, parent agent spawns 7 sub-agents. By 6 AM, all complete their tasks and human wakes up to comprehensive briefing.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `sessions_spawn` | Built-in | Create sub-agents |
| `git` | Built-in | Commit results |
| `filesystem` | Built-in | Partition memory |

## How to Setup

### 1. Sub-Agent Configuration

```javascript
const subAgents = [
  { name: "memory-cleanup", task: "consolidate daily logs" },
  { name: "budget-prep", task: "analyze spending patterns" },
  { name: "tts-research", task: "evaluate new TTS models" },
  { name: "books", task: "find relevant reading" },
  { name: "self-improve", task: "research agent optimization" },
  { name: "neuroscience", task: "study AI memory papers" },
  { name: "advisor", task: "document advisor patterns" }
];
```

### 2. Prompt Template

```markdown
## 7-Sub-Agent Night Parallel

At 23:00:
1. Spawn 7 isolated sub-agents with specific tasks
2. Each gets 1-hour timeout
3. Monitor progress every 10 minutes
4. Collect results as each completes
5. Commit all outputs to git
6. Generate consolidated morning briefing

Partitioning rules:
- Each sub-agent has isolated memory/
- No shared write access
- Read-only access to common data
```

## Success Metrics

- [ ] All 7 agents complete within 6 hours
- [ ] Results committed to version control
- [ ] Morning briefing generated automatically

---

*Example: Clawd42 (Moltbook) - "7 parallel sub-agents"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/seven-sub-agent-night-parallel
cd ~/seven-sub-agent-night-parallel
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

建立 `index.js`，實作 七子代理夜間並行 的核心邏輯。

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
      { role: "user", content: "請協助我執行 七子代理夜間並行 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/seven-sub-agent-night-parallel && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
