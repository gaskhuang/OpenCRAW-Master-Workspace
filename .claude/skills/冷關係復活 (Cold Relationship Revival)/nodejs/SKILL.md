---
name: 冷關係復活 (Cold Relationship Revival)/nodejs
description: "Use Case #172 Node.js 方案: 冷關係復活。使用 Node.js 實作 Cold Relationship Revival 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #172: 冷關係復活 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# 54. Cold Relationship Revival

## Introduction

We all have friends we've lost touch with. The "I should text them" thought that comes and goes for weeks until it feels too awkward to reach out. Your AI agent can help bridge that gap — naturally and thoughtfully.

This use case programs your agent to identify contacts you haven't messaged in a while and draft personalized, warm messages to reconnect. It runs during quiet hours (late evening or early morning), checks your messaging history, and sends genuine check-ins that don't feel robotic.

The goal isn't to automate friendship — it's to remove the friction of reaching out so real connections can restart.

## Skills You Need

- Messaging — WhatsApp/Telegram/Signal integration

## How to Setup

### Prerequisites
- A messaging platform connected to OpenClaw (WhatsApp, Telegram, or Signal)
- A list of contacts you'd like to stay in touch with

### Prompt Template
```
You are my relationship maintenance assistant. Your job is to help me stay connected with people I care about.

Contact list (check in monthly):
- [Name 1] — old college friend, loves hiking
- [Name 2] — former colleague, into photography  
- [Name 3] — cousin, just had a baby

Rules:
1. Check who I haven't messaged in 30+ days
2. Draft a natural, warm message referencing something specific about them
3. Show me the draft BEFORE sending — never send without my approval
4. Keep it casual: "Hey! Been thinking about you..." not "Dear Sir/Madam"
5. If they reply, notify me immediately so I can continue the conversation

Examples of good messages:
- "Hey [Name]! Saw this hiking trail and thought of you 🏔️ How've you been?"
- "Just came across an amazing photo and remembered your photography. What have you been shooting lately?"

Never send more than 2 revival messages per week.
```

### Configuration
- Weekly check: Cron every Sunday at 10 AM
- Draft review: Agent sends drafts to you for approval

## Success Metrics
- At least 2 dormant friendships reactivated per month
- Messages feel natural (friends don't suspect AI involvement)
- You actually follow up on the conversations that restart


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/cold-relationship-revival
cd ~/cold-relationship-revival
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

建立 `index.js`，實作 冷關係復活 的核心邏輯。

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
      { role: "user", content: "請協助我執行 冷關係復活 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/cold-relationship-revival && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
