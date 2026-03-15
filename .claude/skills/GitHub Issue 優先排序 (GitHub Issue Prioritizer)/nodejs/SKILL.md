---
name: GitHub Issue 優先排序 (GitHub Issue Prioritizer)/nodejs
description: "Use Case #142 Node.js 方案: GitHub Issue 優先排序。使用 Node.js 實作 GitHub Issue Prioritizer 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #142: GitHub Issue 優先排序 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# GitHub Issue Prioritizer

## Introduction

Automated scanning and prioritization of GitHub issues across repositories. Identifies stale issues, sorts by urgency/impact, and prepares a morning digest for human review. Reduces cognitive load by surfacing what actually needs attention.

**Why it matters**: Open source projects accumulate issues faster than humans can triage. Automated prioritization ensures critical bugs get attention while low-priority items don't create noise.

**Real-world example**: Agent scans 3 repos nightly, identifies 12 issues with no response in >7 days, flags 2 as high-priority (security-related), and prepares prioritized list for morning standup.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`github`](https://clawhub.ai/skills/git) | ClawHub | API access to issues |
| `web_fetch` | Built-in | Scrape issue details |
| `telegram` | Built-in | Morning digest |

## How to Setup

### 1. Repository Configuration

Create `config/repos.json`:

```json
{
  "repositories": [
    {
      "owner": "myorg",
      "repo": "backend-api",
      "priority_labels": ["security", "critical", "bug"],
      "stale_days": 7
    },
    {
      "owner": "myorg", 
      "repo": "frontend-app",
      "priority_labels": ["ux", "performance"],
      "stale_days": 14
    }
  ]
}
```

### 2. Priority Scoring Algorithm

```javascript
function calculatePriority(issue) {
  let score = 0;
  
  // Age factor
  const daysOld = (Date.now() - new Date(issue.created_at)) / 86400000;
  score += Math.min(daysOld * 2, 20);
  
  // Label weights
  const weights = {
    "security": 50,
    "critical": 40,
    "bug": 20,
    "enhancement": 10,
    "documentation": 5
  };
  issue.labels.forEach(l => score += weights[l.name] || 0);
  
  // Engagement factor
  score += issue.comments * 3;
  
  // Urgency keywords in title
  const urgent = ["crash", "broken", "urgent", "down", "error"];
  if (urgent.some(w => issue.title.toLowerCase().includes(w))) {
    score += 30;
  }
  
  return score;
}
```

### 3. Stale Issue Detection

```javascript
async function findStaleIssues(repo, days) {
  const since = new Date(Date.now() - days * 86400000).toISOString();
  
  const issues = await github.listIssues({
    owner: repo.owner,
    repo: repo.repo,
    state: "open",
    since: since
  });
  
  return issues.filter(i => 
    !i.assignee && 
    new Date(i.updated_at) < new Date(since)
  );
}
```

### 4. Prompt Template

Add to your `SKILL.md`:

```markdown
## GitHub Issue Prioritizer

Every morning at 08:00:
1. Fetch all open issues from configured repos
2. Calculate priority score for each
3. Identify stale issues (no activity > threshold)
4. Categorize:
   - 🔥 Critical: security/crash/data loss
   - ⚠️ High: bugs affecting users
   - 📋 Medium: enhancements with engagement
   - 📎 Low: docs, questions
5. Prepare digest with top 10 issues
6. Send via Telegram with direct links

Weekly (Sundays):
- Generate stale issue report
- Suggest issues to close (no activity > 30 days)
- Report average response time trends
```

### 5. Morning Digest Format

```markdown
📋 GitHub Priority Digest - {{date}}

🔥 Critical (2)
- [#234] API crash on payment webhook
  Repo: backend-api | Age: 2 days | 👤 unassigned
  https://github.com/myorg/backend-api/issues/234

- [#198] Security: SQL injection vulnerability  
  Repo: backend-api | Age: 5 days | 👤 @dev-team
  https://github.com/myorg/backend-api/issues/198

⚠️ High (3)
- [#201] Memory leak in worker process
- [#189] Database connection timeout
- [#156] OAuth token refresh failing

📊 Stats
- Total open: 47 issues
- Avg age: 12 days
- Stale (>7 days): 8 issues
- Unassigned: 15 issues
```

### 6. Cron Configuration

```json
{
  "schedule": "0 8 * * *",
  "timezone": "America/New_York",
  "task": "github_issue_digest",
  "repos": ["backend-api", "frontend-app", "docs"]
}
```

## Success Metrics

- [ ] Critical issues flagged within 24h of creation
- [ ] Stale issues identified weekly
- [ ] Average response time tracked
- [ ] Human reviews digest within 2 hours

## Auto-Actions (Optional)

```javascript
// Auto-label based on keywords
if (issue.title.includes("security")) {
  await github.addLabel(issue, "security");
}

// Auto-assign based on code ownership
const owner = await getCodeOwner(issue.filePath);
await github.assignIssue(issue, owner);

// Ping stale issues
if (daysStale > 7) {
  await github.comment(issue, "Friendly ping - is this still relevant?");
}
```

---

*Example: Clawd_RD (Moltbook) - Data analysis patterns*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/github-issue-prioritizer
cd ~/github-issue-prioritizer
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

建立 `index.js`，實作 GitHub Issue 優先排序 的核心邏輯。

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
      { role: "user", content: "請協助我執行 GitHub Issue 優先排序 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/github-issue-prioritizer && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
