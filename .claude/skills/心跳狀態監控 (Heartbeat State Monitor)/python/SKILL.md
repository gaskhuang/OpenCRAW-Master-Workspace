---
name: 心跳狀態監控 (Heartbeat State Monitor)/python
description: "Use Case #162 Python 方案: 心跳狀態監控。使用 Python 實作 Heartbeat State Monitor 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #162: 心跳狀態監控 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Heartbeat State Monitor

## Introduction

Tracks freshness of heartbeat checks showing which monitoring tasks are overdue. Reads heartbeat-state.json and displays staleness in human-readable format.

**Why it matters**: Heartbeats can fail silently. Monitoring the monitors ensures nothing falls through cracks.

**Real-world example**: Agent checks heartbeat-state, finds email check 4 hours overdue, triggers immediate check, discovers API issue.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Read state |
| `system` | Built-in | Time calculations |

## How to Setup

### 1. State Format

```json
{
  "lastChecks": {
    "email": "2026-02-19T08:00:00Z",
    "calendar": "2026-02-19T08:30:00Z"
  }
}
```

### 2. Monitor Script

```javascript
function checkFreshness() {
  const state = JSON.parse(fs.readFileSync('heartbeat-state.json'));
  const now = Date.now();
  
  Object.entries(state.lastChecks).forEach(([check, time]) => {
    const age = (now - new Date(time)) / 1000 / 60;
    const status = age > 60 ? 'STALE' : 'OK';
    console.log(`${status}: ${check} - ${age} min ago`);
  });
}
```

### 3. Prompt Template

```markdown
## Heartbeat State Monitor

Every heartbeat:
1. Read heartbeat-state.json
2. Calculate staleness for each check
3. Display human-readable status
4. Alert if any check > threshold
5. Trigger overdue checks immediately
```

## Success Metrics

- [ ] All checks freshness visible
- [ ] Overdue checks triggered promptly
- [ ] Staleness trends tracked

---

*Example: MrButtSmell (Moltbook) - "heartbeat freshness reporter"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/heartbeat-state-monitor
cd ~/heartbeat-state-monitor
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

建立 `main.py`，實作 心跳狀態監控 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_heartbeat_state_monitor():
    """執行 心跳狀態監控 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 心跳狀態監控 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_heartbeat_state_monitor()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/heartbeat-state-monitor && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
