---
name: 日誌異常偵測 (Log Anomaly Detection)/nodejs
description: "Use Case #150 Node.js 方案: 日誌異常偵測。使用 Node.js 實作 Log Anomaly Detection 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #150: 日誌異常偵測 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/log-anomaly-detection
cd ~/log-anomaly-detection
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

建立 `index.js`，實作 日誌異常偵測 的核心邏輯。

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
      { role: "user", content: "請協助我執行 日誌異常偵測 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/log-anomaly-detection && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
