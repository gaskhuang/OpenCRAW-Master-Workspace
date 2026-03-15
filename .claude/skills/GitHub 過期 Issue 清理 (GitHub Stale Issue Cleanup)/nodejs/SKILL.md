---
name: GitHub 過期 Issue 清理 (GitHub Stale Issue Cleanup)/nodejs
description: "Use Case #149 Node.js 方案: GitHub 過期 Issue 清理。使用 Node.js 實作 GitHub Stale Issue Cleanup 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #149: GitHub 過期 Issue 清理 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# GitHub Stale Issue Cleanup

## Introduction

Weekly identification and reporting of stale GitHub issues with no activity for >30 days. Suggests closure candidates and generates report for human review.

**Why it matters**: Issue backlogs grow indefinitely without triage. Automated stale detection keeps repositories manageable.

**Real-world example**: Agent finds 15 issues with no comments in 45 days, human reviews and closes 12, backlog reduced by 20%.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`github`](https://clawhub.ai/skills/git) | ClawHub | Issue API |

## How to Setup

### 1. Stale Detection

```javascript
const staleDays = 30;
const issues = await github.listIssues({ state: 'open' });
const stale = issues.filter(i => 
  daysSince(i.updated_at) > staleDays &&
  i.comments === 0
);
```

### 2. Prompt Template

```markdown
## GitHub Stale Issue Cleanup

Weekly on Sundays:
1. Find issues with no activity >30 days
2. Check if labeled "wontfix" or "duplicate"
3. Generate closure candidate list
4. Human reviews and decides
5. Auto-comment "stale" warning before close
```

## Success Metrics

- [ ] Stale issues identified weekly
- [ ] Backlog reduced 10% per month
- [ ] Zero accidental closures

---

*Example: Clawd_RD (Moltbook) - GitHub analysis patterns*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/github-stale-issue-cleanup
cd ~/github-stale-issue-cleanup
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

建立 `index.js`，實作 GitHub 過期 Issue 清理 的核心邏輯。

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
      { role: "user", content: "請協助我執行 GitHub 過期 Issue 清理 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/github-stale-issue-cleanup && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
