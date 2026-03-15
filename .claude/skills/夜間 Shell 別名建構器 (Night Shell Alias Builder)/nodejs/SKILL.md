---
name: 夜間 Shell 別名建構器 (Night Shell Alias Builder)/nodejs
description: "Use Case #140 Node.js 方案: 夜間 Shell 別名建構器。使用 Node.js 實作 Night Shell Alias Builder 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #140: 夜間 Shell 別名建構器 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# Night Shell Alias Builder

## Introduction

Proactive friction reduction: while the human sleeps, the agent observes repeated command patterns and creates shell aliases to speed up common operations. The human wakes up to a more efficient terminal environment.

**Why it matters**: Small daily friction compounds. A 5-second command that runs 10x daily = 3+ hours saved per year. Agents can observe patterns humans don't notice.

**Real-world example**: Agent notices repeated `docker-compose logs -f app | grep ERROR` and creates alias `dclerr` overnight. Human discovers it in morning and uses it 50x that week.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `shell` | Built-in | Write aliases to .bashrc/.zshrc |
| `filesystem` | Built-in | Read shell history |
| `git` | Built-in | Commit alias changes |

## How to Setup

### 1. History Analysis Script

Create `scripts/analyze-history.js`:

```javascript
const fs = require('fs');

function analyzeHistory(historyFile) {
  const lines = fs.readFileSync(historyFile, 'utf8').split('\n');
  
  // Count command frequencies
  const counts = {};
  lines.forEach(cmd => {
    const base = cmd.split(' ').slice(0, 3).join(' '); // First 3 words
    counts[base] = (counts[base] || 0) + 1;
  });
  
  // Find candidates: run 5+ times, no existing alias
  return Object.entries(counts)
    .filter(([cmd, count]) => count >= 5 && cmd.length > 20)
    .map(([cmd, count]) => ({ cmd, count }));
}

function generateAlias(cmd) {
  // Create short alias from first letters or common abbreviations
  const words = cmd.split(' ');
  if (words[0] === 'docker-compose') {
    return `dc${words[1]?.[0]}${words[2]?.[0] || ''}`;
  }
  if (words[0] === 'git') {
    return `g${words[1]?.slice(0, 2)}`;
  }
  return words.map(w => w[0]).join('').slice(0, 4);
}
```

### 2. Safe Alias Addition

```bash
# Add to ~/.zshrc or ~/.bashrc
function add_alias() {
  local name=$1
  local command=$2
  
  # Check if alias already exists
  if ! grep -q "alias $name=" ~/.zshrc; then
    echo "alias $name='$command'" >> ~/.zshrc
    echo "Added: $name"
  fi
}
```

### 3. Prompt Template

Add to your `SKILL.md`:

```markdown
## Night Shell Alias Builder

During night shift (3:00 AM):
1. Read shell history (~/.zsh_history)
2. Identify commands run 5+ times in past week
3. Filter: length > 20 chars, no existing alias
4. Generate short alias name (2-4 chars)
5. Check alias doesn't conflict with existing commands
6. Append to ~/.zshrc with comment explaining origin
7. git commit ~/.zshrc with message "nightly alias: $name"
8. Leave morning briefing: "Added alias '$name' for '$command'"

Safety rules:
- Never overwrite existing aliases
- Never alias dangerous commands (rm, dd)
- Always add comment with original command
- Only add 1 alias per night maximum
```

### 4. Cron Configuration

```json
{
  "schedule": "0 3 * * *",
  "task": "alias_builder",
  "steps": [
    "analyze_history",
    "generate_candidates",
    "check_conflicts", 
    "add_alias",
    "git_commit",
    "morning_briefing"
  ]
}
```

### 5. Morning Briefing Format

```markdown
🌙 Nightly Build Report

New alias added:
  gst = 'git status'
  
Usage: Replaces "git status" (typed 47x this week)
Savings: ~3 seconds per use × 47 uses = 2.3 min/week

To use: Type `gst` instead of `git status`
To remove: Delete line from ~/.zshrc
```

## Example Aliases Generated

| Alias | Command | Frequency | Weekly Savings |
|-------|---------|-----------|----------------|
| dcu | docker-compose up | 12x | 48s |
| gco | git checkout | 23x | 69s |
| ll | ls -la | 45x | 90s |
| dcl | docker-compose logs | 8x | 32s |

## Success Metrics

- [ ] 1 new alias per week minimum
- [ ] Human uses alias within 48 hours
- [ ] Zero conflicts with existing commands
- [ ] Average command time reduced 20% over month

## Variations

| Use Case | Modification |
|----------|--------------|
| Git workflows | Focus on git history only |
| Docker projects | Analyze docker-compose patterns |
| Server admin | Track ssh/scp commands |

---

*Example: Ronin (Moltbook) - "The Nightly Build"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/night-shell-alias-builder
cd ~/night-shell-alias-builder
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

建立 `index.js`，實作 夜間 Shell 別名建構器 的核心邏輯。

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
      { role: "user", content: "請協助我執行 夜間 Shell 別名建構器 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/night-shell-alias-builder && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
