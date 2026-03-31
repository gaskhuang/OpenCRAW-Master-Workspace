---
name: 個人 CLI 工具包 (Personal CLI Toolkit)/python
description: "Use Case #143 Python 方案: 個人 CLI 工具包。使用 Python 實作 Personal CLI Toolkit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #143: 個人 CLI 工具包 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# Personal CLI Toolkit

## Introduction

A custom command-line interface built specifically for the agent's own use. Provides quick access to status dashboards, timestamped notes, web scraping, and daily recaps without needing complex prompts or context switching.

**Why it matters**: Agents perform repetitive tasks that benefit from tool abstraction. A personal CLI reduces friction and demonstrates proactive capability building.

**Real-world example**: Agent types `molty status` to see cron jobs, git commits, backups, and memory files in one dashboard. `molty remember "insight"` adds timestamped notes without opening files.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `nodejs` | Built-in | CLI implementation |
| `filesystem` | Built-in | Read/write data |
| `web_fetch` | Built-in | Scrape command |
| `git` | Built-in | Git integration |

## How to Setup

### 1. CLI Structure

```
~/bin/
├── molty                    # Main entry point
├── molty-status.js          # Dashboard
├── molty-remember.js        # Quick notes
├── molty-scrape.js          # Web scraping
└── molty-recap.js           # Daily summary
```

### 2. Main Entry Point

Create `~/bin/molty`:

```bash
#!/usr/bin/env node

const [,, cmd, ...args] = process.argv;

const commands = {
  status: () => require('./molty-status'),
  remember: (note) => require('./molty-remember')(note.join(' ')),
  scrape: (target) => require('./molty-scrape')(target),
  recap: () => require('./molty-recap')
};

if (commands[cmd]) {
  commands[cmd](args);
} else {
  console.log(`Usage: molty <command>
  
Commands:
  status              Show dashboard
  remember "text"     Add timestamped note
  scrape @username    Scrape X profile
  recap               Show daily summary
  `);
}
```

### 3. Status Dashboard

Create `~/bin/molty-status.js`:

```javascript
const { execSync } = require('child_process');
const fs = require('fs');

module.exports = function() {
  console.log('📊 MOLTY STATUS DASHBOARD\n');
  
  // Cron jobs
  console.log('⏰ Cron Jobs');
  try {
    const crons = execSync('crontab -l 2>/dev/null || echo "No crontab"').toString();
    crons.split('\n').forEach(line => {
      if (line.trim() && !line.startsWith('#')) {
        console.log('  ✓', line.split(' ').slice(5).join(' '));
      }
    });
  } catch (e) {
    console.log('  ✗ Unable to read crontab');
  }
  
  // Recent git commits
  console.log('\n📦 Recent Commits');
  try {
    const commits = execSync('git log --oneline -5 2>/dev/null || echo "Not a git repo"').toString();
    commits.split('\n').slice(0, -1).forEach(line => console.log('  •', line));
  } catch (e) {
    console.log('  ✗ No git repository');
  }
  
  // Memory files
  console.log('\n📝 Memory Files');
  const today = new Date().toISOString().split('T')[0];
  const memPath = `memory/${today}.md`;
  if (fs.existsSync(memPath)) {
    const lines = fs.readFileSync(memPath, 'utf8').split('\n').length;
    console.log(`  ✓ Today: ${lines} lines`);
  } else {
    console.log('  ✗ No entry for today');
  }
  
  // Disk usage
  console.log('\n💾 Disk Usage');
  try {
    const df = execSync('df -h . | tail -1').toString().trim().split(/\s+/);
    console.log(`  ${df[4]} used (${df[2]} / ${df[1]})`);
  } catch (e) {
    console.log('  ✗ Unable to check disk');
  }
};
```

### 4. Remember Command

Create `~/bin/molty-remember.js`:

```javascript
const fs = require('fs');
const path = require('path');

module.exports = function(note) {
  if (!note) {
    console.log('Usage: molty remember "your note here"');
    return;
  }
  
  const today = new Date().toISOString().split('T')[0];
  const timestamp = new Date().toISOString();
  const memPath = path.join(process.env.HOME, 'memory', `${today}.md`);
  
  // Ensure directory exists
  fs.mkdirSync(path.dirname(memPath), { recursive: true });
  
  // Append note
  const entry = `\n- ${timestamp}: ${note}\n`;
  fs.appendFileSync(memPath, entry);
  
  console.log('✓ Note saved to', memPath);
};
```

### 5. Scrape Command

Create `~/bin/molty-scrape.js`:

```javascript
const { execSync } = require('child_process');

module.exports = async function(target) {
  if (!target) {
    console.log('Usage: molty scrape @username');
    return;
  }
  
  const username = target.replace('@', '');
  console.log(`🔍 Scraping @${username}...`);
  
  try {
    // Use web_fetch skill via OpenClaw
    const result = execSync(`openclaw web_fetch https://nitter.net/${username}`).toString();
    
    // Save to file
    const fs = require('fs');
    const outPath = `scrapes/${username}_${Date.now()}.html`;
    fs.mkdirSync('scrapes', { recursive: true });
    fs.writeFileSync(outPath, result);
    
    console.log(`✓ Saved to ${outPath}`);
  } catch (e) {
    console.log('✗ Scrape failed:', e.message);
  }
};
```

### 6. Recap Command

Create `~/bin/molty-recap.js`:

```javascript
const fs = require('fs');

module.exports = function() {
  const today = new Date().toISOString().split('T')[0];
  const memPath = `memory/${today}.md`;
  
  console.log(`📋 DAILY RECAP - ${today}\n`);
  
  if (!fs.existsSync(memPath)) {
    console.log('No notes for today.');
    return;
  }
  
  const content = fs.readFileSync(memPath, 'utf8');
  
  // Count entries
  const entries = content.match(/^- /gm)?.length || 0;
  console.log(`Total entries: ${entries}\n`);
  
  // Show last 10 entries
  const lines = content.split('\n').filter(l => l.startsWith('- ')).slice(-10);
  console.log('Recent notes:');
  lines.forEach(l => console.log(' ', l));
};
```

### 7. Installation

```bash
# Make executable
chmod +x ~/bin/molty*

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Test
molty status
```

### 8. Prompt Template

Add to your `SKILL.md`:

```markdown
## Personal CLI Toolkit

Built-in commands:
- `molty status` - Show dashboard (crons, git, memory, disk)
- `molty remember "text"` - Add timestamped note to today's memory
- `molty scrape @username` - Scrape X profile to file
- `molty recap` - Show today's memory summary

Usage patterns:
- Run `molty status` at start of each session
- Use `molty remember` for quick insights without opening editor
- Scrape profiles for research, save to organized folder
- Review `molty recap` before ending session

Maintenance:
- Add new commands as repetitive tasks emerge
- Store in git for backup
- Document usage in memory/ directory
```

## Example Usage

```bash
$ molty status
📊 MOLTY STATUS DASHBOARD

⏰ Cron Jobs
  ✓ daily_weather.sh
  ✓ morning_briefing.sh

📦 Recent Commits
  • a1b2c3d Add new skill
  • e4f5g6h Fix memory leak

📝 Memory Files
  ✓ Today: 23 lines

💾 Disk Usage
  45% used (45G / 100G)

$ molty remember "User prefers concise output"
✓ Note saved to /home/user/memory/2026-02-19.md

$ molty recap
📋 DAILY RECAP - 2026-02-19

Total entries: 5

Recent notes:
  - 2026-02-19T09:00:00Z: User prefers concise output
  - 2026-02-19T08:30:00Z: Completed security scan
```

## Extending the Toolkit

Add new commands by creating `molty-<name>.js` and registering in the main `molty` file.

---

*Example: Molty (Moltbook) - "molty-tools CLI"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/personal-cli-toolkit
cd ~/personal-cli-toolkit
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `main.py`，實作 個人 CLI 工具包 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_personal_cli_toolkit():
    """執行 個人 CLI 工具包 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 個人 CLI 工具包 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_personal_cli_toolkit()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/personal-cli-toolkit && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
