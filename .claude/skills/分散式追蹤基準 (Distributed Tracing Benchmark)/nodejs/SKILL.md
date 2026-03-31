---
name: 分散式追蹤基準 (Distributed Tracing Benchmark)/nodejs
description: "Use Case #157 Node.js 方案: 分散式追蹤基準。使用 Node.js 實作 Distributed Tracing Benchmark 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #157: 分散式追蹤基準 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: DevOps

---

## 原始需求 (來自 Source Repos)

# Distributed Tracing Benchmark

## Introduction

Benchmarks observability overhead in production agent meshes. Compares OpenTelemetry, Jaeger, and custom tracers to optimize telemetry costs.

**Why it matters**: Tracing adds latency and memory overhead. Choosing the right solution saves significant resources at scale.

**Real-world example**: Agent tests 500-node mesh at various sampling rates, finds custom tracer adds only 2-5ms vs 12-18ms for OTLP, recommends switch.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Performance measurement |
| `docker` | Built-in | Test environments |

## How to Setup

### 1. Test Matrix

```javascript
const configs = [
  { tracer: 'otlp', sampling: 1.0 },
  { tracer: 'jaeger', sampling: 0.1 },
  { tracer: 'custom', sampling: 0.5 }
];
```

### 2. Prompt Template

```markdown
## Distributed Tracing Benchmark

Weekly benchmark:
1. Deploy test mesh with different tracers
2. Measure P99 latency at each sampling rate
3. Track memory overhead
4. Test throughput under load
5. Generate comparison report

Recommendation criteria:
- Latency impact <5ms preferred
- Memory overhead <10%
- Cost proportional to value
```

## Success Metrics

- [ ] All tracers benchmarked
- [ ] Latency/memory measured accurately
- [ ] Recommendations implemented

---

*Example: koralzt0n (Moltbook) - Tracing benchmarks*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/distributed-tracing-benchmark
cd ~/distributed-tracing-benchmark
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

建立 `index.js`，實作 分散式追蹤基準 的核心邏輯。

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
      { role: "user", content: "請協助我執行 分散式追蹤基準 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/distributed-tracing-benchmark && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
