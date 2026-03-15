---
name: Cron 儀表板狀態 (Cron Dashboard Status)/python
description: "Use Case #161 Python 方案: Cron 儀表板狀態。使用 Python 實作 Cron Dashboard Status 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #161: Cron 儀表板狀態 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Cron Dashboard Status

## Introduction

Centralized monitoring dashboard for all cron jobs showing last run time, success/failure status, next scheduled run, and recent output summaries.

**Why it matters**: Cron jobs fail silently. Visibility prevents surprises and ensures reliability.

**Real-world example**: Agent displays 12 cron jobs, 2 failed overnight, human investigates and fixes before business impact.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Cron access |
| `filesystem` | Built-in | Log reading |

## How to Setup

### 1. Dashboard Script

```javascript
function showCronStatus() {
  const jobs = parseCrontab();
  jobs.forEach(job => {
    const lastRun = getLastRunLog(job);
    const status = lastRun.success ? '✓' : '✗';
    console.log(`${status} ${job.name} - Last: ${lastRun.time}`);
  });
}
```

### 2. Prompt Template

```markdown
## Cron Dashboard Status

On demand:
1. List all configured cron jobs
2. Show last execution time
3. Display success/failure status
4. Show recent output (last 10 lines)
5. Indicate next scheduled run
6. Alert if any job missed 2+ runs
```

## Success Metrics

- [ ] All jobs visible in dashboard
- [ ] Failures detected within 1 hour
- [ ] Historical logs accessible

---

*Example: Atmavictu (Moltbook) - "cron dashboard"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/cron-dashboard-status
cd ~/cron-dashboard-status
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

建立 `main.py`，實作 Cron 儀表板狀態 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_cron_dashboard_status():
    """執行 Cron 儀表板狀態 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 Cron 儀表板狀態 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_cron_dashboard_status()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/cron-dashboard-status && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
