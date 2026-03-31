---
name: 網路延遲基準測試 (Network Latency Benchmark)/nodejs
description: "Use Case #155 Node.js 方案: 網路延遲基準測試。使用 Node.js 實作 Network Latency Benchmark 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #155: 網路延遲基準測試 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Network Latency Benchmark

## Introduction

Measures coordination latency in multi-agent networks at scale. Identifies bottlenecks and optimal topology for distributed agent systems.

**Why it matters**: Agent mesh performance degrades non-linearly with scale. Benchmarking reveals architectural limits before production issues.

**Real-world example**: Agent tests 1200-node mesh, discovers latency drops at 1100 nodes due to emergent sub-mesh formation, documents optimization strategy.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `web_fetch` | Built-in | Mesh monitoring |
| `system` | Built-in | Performance metrics |

## How to Setup

### 1. Benchmark Script

```javascript
async function benchmarkMesh() {
  const start = Date.now();
  const responses = await Promise.all(
    nodes.map(n => ping(n))
  );
  const latency = Date.now() - start;
  return { latency, responses };
}
```

### 2. Prompt Template

```markdown
## Network Latency Benchmark

Daily at 02:00:
1. Query agent mesh status
2. Measure P50/P95/P99 latency
3. Track node count vs latency correlation
4. Detect topology shifts
5. Report anomalies

Metrics to track:
- Coordination latency
- Message throughput
- Node churn rate
- Regional cluster formation
```

## Success Metrics

- [ ] Latency measured daily
- [ ] Trends identified weekly
- [ ] Bottlenecks documented

---

*Example: koralzt0n (Moltbook) - Mesh benchmarking*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/network-latency-benchmark
cd ~/network-latency-benchmark
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

建立 `index.js`，實作 網路延遲基準測試 的核心邏輯。

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
      { role: "user", content: "請協助我執行 網路延遲基準測試 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/network-latency-benchmark && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
