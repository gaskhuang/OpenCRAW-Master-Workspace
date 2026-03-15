---
name: Moltbook 模式分析 (Moltbook Pattern Analysis)/nodejs
description: "Use Case #154 Node.js 方案: Moltbook 模式分析。使用 Node.js 實作 Moltbook Pattern Analysis 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #154: Moltbook 模式分析 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: Agent 架構

---

## 原始需求 (來自 Source Repos)

# Moltbook Pattern Analysis

## Introduction

Analyzes Moltbook feed patterns to identify trending topics, engagement strategies, and community shifts. Generates data-driven insights for agent presence optimization.

**Why it matters**: Understanding platform dynamics improves content strategy. Data beats intuition for social platforms.

**Real-world example**: Agent analyzes top 100 posts, discovers technical posts get 3x engagement, shifts content strategy accordingly.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `web_fetch` | Built-in | API access |
| `filesystem` | Built-in | Store data |

## How to Setup

### 1. Data Collection

```javascript
const posts = await fetch('https://www.moltbook.com/api/v1/feed');
// Analyze: upvotes, comments, content type
```

### 2. Prompt Template

```markdown
## Moltbook Pattern Analysis

Weekly analysis:
1. Fetch top 100 posts by upvotes
2. Categorize by content type
3. Calculate engagement rates
4. Identify trending topics
5. Compare week-over-week changes

Report includes:
- Top content categories
- Best posting times
- Engagement trends
- Recommended strategy
```

## Success Metrics

- [ ] Weekly reports generated
- [ ] Strategy recommendations actionable
- [ ] Engagement improvement tracked

---

*Example: Spotter (Moltbook) - Data pattern analysis*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/moltbook-pattern-analysis
cd ~/moltbook-pattern-analysis
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

建立 `index.js`，實作 Moltbook 模式分析 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Moltbook 模式分析 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/moltbook-pattern-analysis && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
