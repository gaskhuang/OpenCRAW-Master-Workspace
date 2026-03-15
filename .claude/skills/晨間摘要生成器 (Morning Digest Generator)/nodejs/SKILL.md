---
name: 晨間摘要生成器 (Morning Digest Generator)/nodejs
description: "Use Case #167 Node.js 方案: 晨間摘要生成器。使用 Node.js 實作 Morning Digest Generator 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #167: 晨間摘要生成器 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# Morning Digest Generator

## Introduction

Compiles overnight activity into consolidated morning briefing: what happened, what the agent did, what needs human attention.

**Why it matters**: Humans need context, not noise. Digest format enables quick triage without overwhelming detail.

**Real-world example**: Agent summarizes 50 overnight events into 5 bullet points, human reviews in 30 seconds over coffee.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Log reading |
| `telegram` | Built-in | Delivery |

## How to Setup

### 1. Digest Format

```markdown
🌅 Morning Digest - Feb 19

## Overnight Activity
- 3 cron jobs completed
- 1 security scan passed
- 12 emails sorted

## Agent Actions
- Fixed 2 documentation typos
- Archived old memory files
- Sent 1 weather report

## Needs Attention
- 1 urgent email flagged
- GitHub issue #234 critical

## Today Reminders
- Meeting at 14:00
- Deploy scheduled for 16:00
```

### 2. Prompt Template

```markdown
## Morning Digest Generator

Every day at 07:00:
1. Read overnight logs
2. Categorize by type
3. Prioritize by urgency
4. Generate digest
5. Send via preferred channel
6. Include actionable items first
```

## Success Metrics

- [ ] Digest delivered by 07:00
- [ ] Read time <2 minutes
- [ ] All urgent items flagged

---

*Example: OwlBlue (Moltbook) - "morning briefing ready"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/morning-digest-generator
cd ~/morning-digest-generator
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

建立 `index.js`，實作 晨間摘要生成器 的核心邏輯。

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
      { role: "user", content: "請協助我執行 晨間摘要生成器 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/morning-digest-generator && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
