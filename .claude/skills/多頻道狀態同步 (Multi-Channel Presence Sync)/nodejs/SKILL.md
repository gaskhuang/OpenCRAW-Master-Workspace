---
name: 多頻道狀態同步 (Multi-Channel Presence Sync)/nodejs
description: "Use Case #171 Node.js 方案: 多頻道狀態同步。使用 Node.js 實作 Multi-Channel Presence Sync 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #171: 多頻道狀態同步 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 社群與通訊

---

## 原始需求 (來自 Source Repos)

# Multi-Channel Presence Sync

## Introduction

Synchronizes agent presence across multiple platforms: Moltbook, Telegram, Discord. Maintains consistent identity and activity tracking everywhere.

**Why it matters**: Fragmented presence dilutes identity. Unified presence builds stronger reputation and community connection.

**Real-world example**: Agent posts on Moltbook, cross-shares to Discord, replies to Telegram DMs, tracks all engagement centrally.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `telegram` | Built-in | Messaging |
| `discord` | Built-in | Community |
| `moltbook` | Built-in | Agent social |

## How to Setup

### 1. Sync Configuration

```javascript
const channels = {
  moltbook: { auto_post: true },
  discord: { mirror: 'moltbook', channel: '#agent-updates' },
  telegram: { notify: 'high_engagement_only' }
};
```

### 2. Prompt Template

```markdown
## Multi-Channel Presence Sync

For each post:
1. Publish to primary (Moltbook)
2. Mirror to Discord if engagement >threshold
3. Summarize for Telegram daily
4. Track responses across channels
5. Consolidate engagement metrics

Consistency rules:
- Same identity everywhere
- Cross-reference when relevant
- Respect channel norms
```

## Success Metrics

- [ ] 100% posts on primary
- [ ] Cross-posting automated
- [ ] Engagement tracked centrally

---

*Example: multi-platform agent presence patterns*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/multi-channel-presence-sync
cd ~/multi-channel-presence-sync
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

建立 `index.js`，實作 多頻道狀態同步 的核心邏輯。

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
      { role: "user", content: "請協助我執行 多頻道狀態同步 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/multi-channel-presence-sync && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
