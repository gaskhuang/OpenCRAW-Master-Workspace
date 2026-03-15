---
name: 日誌異常偵測 (Log Anomaly Detection)/python
description: "Use Case #150 Python 方案: 日誌異常偵測。使用 Python 實作 Log Anomaly Detection 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #150: 日誌異常偵測 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Log Anomaly Detection

## Introduction

Automated log file scanning for error patterns, unusual activity, or security events. Identifies anomalies without predefined rules using statistical analysis.

**Why it matters**: Logs contain early warning signs of problems. Automated detection catches issues humans would miss in volume.

**Real-world example**: Agent detects 10x increase in 404 errors at 4 AM, traces to broken API endpoint, alerts before customer impact.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Read logs |
| `telegram` | Built-in | Alerts |

## How to Setup

### 1. Anomaly Detection

```javascript
function detectAnomaly(lines) {
  const errorRate = lines.filter(l => l.includes('ERROR')).length / lines.length;
  const baseline = getBaseline(); // Historical average
  return errorRate > baseline * 2;
}
```

### 2. Prompt Template

```markdown
## Log Anomaly Detection

Every 30 minutes:
1. Tail recent log entries
2. Count error frequencies by type
3. Compare to rolling 24h baseline
4. If 2x baseline: warning
5. If 5x baseline: immediate alert
6. Include sample error messages
```

## Success Metrics

- [ ] Anomalies detected within 30 min
- [ ] False positive rate <10%
- [ ] Zero missed critical errors

---

*Example: VPS_Central (Moltbook) - Log monitoring*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/log-anomaly-detection
cd ~/log-anomaly-detection
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

建立 `main.py`，實作 日誌異常偵測 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_log_anomaly_detection():
    """執行 日誌異常偵測 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 日誌異常偵測 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_log_anomaly_detection()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/log-anomaly-detection && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
