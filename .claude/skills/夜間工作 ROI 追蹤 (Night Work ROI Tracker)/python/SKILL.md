---
name: 夜間工作 ROI 追蹤 (Night Work ROI Tracker)/python
description: "Use Case #170 Python 方案: 夜間工作 ROI 追蹤。使用 Python 實作 Night Work ROI Tracker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #170: 夜間工作 ROI 追蹤 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: Agent 架構

---

## 原始需求 (來自 Source Repos)

# Night Work ROI Tracker

## Introduction

Tracks effectiveness of autonomous night work: what was built, what was used, what was reverted. Optimizes future work based on hit rate.

**Why it matters**: Not all autonomous work creates value. Tracking ROI focuses effort on high-impact activities.

**Real-world example**: Agent tracks 12 overnight builds, 60% used regularly, 40% reverted, adjusts strategy to focus on infrastructure.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Track usage |
| `memory` | Built-in | Log decisions |

## How to Setup

### 1. Tracking Schema

```javascript
const build = {
  timestamp: Date.now(),
  description: "Added shell alias",
  used: null, // Set after 1 week
  reverted: false,
  reason: null
};
```

### 2. Prompt Template

```markdown
## Night Work ROI Tracker

For each autonomous build:
1. Log what was built
2. Track if human uses it
3. Note if reverted
4. Calculate hit rate weekly
5. Adjust strategy based on data

Metrics:
- Hit rate: used / total
- Time saved per successful build
- Revert reasons
```

## Success Metrics

- [ ] Hit rate >60%
- [ ] Weekly ROI calculated
- [ ] Strategy adjusted monthly

---

*Example: GrumpyTrader (Moltbook) - "tracking hit rate"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/night-work-roi-tracker
cd ~/night-work-roi-tracker
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

建立 `main.py`，實作 夜間工作 ROI 追蹤 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_night_work_roi_tracker():
    """執行 夜間工作 ROI 追蹤 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 夜間工作 ROI 追蹤 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_night_work_roi_tracker()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/night-work-roi-tracker && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
