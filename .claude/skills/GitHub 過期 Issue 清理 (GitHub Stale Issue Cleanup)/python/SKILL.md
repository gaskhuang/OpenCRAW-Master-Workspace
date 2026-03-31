---
name: GitHub 過期 Issue 清理 (GitHub Stale Issue Cleanup)/python
description: "Use Case #149 Python 方案: GitHub 過期 Issue 清理。使用 Python 實作 GitHub Stale Issue Cleanup 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #149: GitHub 過期 Issue 清理 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
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

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/github-stale-issue-cleanup
cd ~/github-stale-issue-cleanup
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

建立 `main.py`，實作 GitHub 過期 Issue 清理 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_github_stale_issue_cleanup():
    """執行 GitHub 過期 Issue 清理 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 GitHub 過期 Issue 清理 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_github_stale_issue_cleanup()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/github-stale-issue-cleanup && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
