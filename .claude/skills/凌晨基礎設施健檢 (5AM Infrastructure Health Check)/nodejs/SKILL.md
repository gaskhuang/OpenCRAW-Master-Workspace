---
name: 凌晨基礎設施健檢 (5AM Infrastructure Health Check)/nodejs
description: "Use Case #146 Node.js 方案: 凌晨基礎設施健檢。使用 Node.js 實作 5AM Infrastructure Health Check 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #146: 凌晨基礎設施健檢 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# 5AM Infrastructure Health Check

## Introduction

Early morning server health monitoring: uptime checks, disk space verification, resource utilization tracking, and backup validation. Proactive identification of issues before human starts workday.

**Why it matters**: Infrastructure problems discovered at 9 AM cost hours of productivity. Early detection enables fixes before impact.

**Real-world example**: Agent detects disk at 95% capacity at 5 AM, alerts human, cleanup script runs, crisis averted before business hours.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Resource monitoring |
| `telegram` | Built-in | Alerts |
| `cron` | Built-in | Automation |

## How to Setup

### 1. Health Check Script

```bash
#!/bin/bash
# check-health.sh

df -h | grep -E "(9[0-9]|100)%" && alert "Disk critical"
free -m | awk '/Mem:/ {if ($3/$2 > 0.9) print "Memory high"}'
uptime | awk '{if ($3 > 7) print "Reboot suggested"}'
```

### 2. Prompt Template

```markdown
## 5AM Infrastructure Check

Every day at 05:00:
1. Check disk usage on all volumes
2. Verify memory utilization
3. Check load average
4. Validate backup completion
5. Test external connectivity
6. If any check fails: immediate alert
7. Otherwise: silent success

Thresholds:
- Disk >90%: Warning
- Disk >95%: Critical
- Memory >90%: Warning
- Load >4: Investigate
```

## Success Metrics

- [ ] 100% uptime for critical services
- [ ] Issues detected before 8 AM
- [ ] False positive rate <5%

---

*Example: VPS_Central (Moltbook) - Infrastructure monitoring*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/5am-infrastructure-health-check
cd ~/5am-infrastructure-health-check
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

建立 `index.js`，實作 凌晨基礎設施健檢 的核心邏輯。

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
      { role: "user", content: "請協助我執行 凌晨基礎設施健檢 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/5am-infrastructure-health-check && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
