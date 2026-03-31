---
name: 分散式追蹤基準 (Distributed Tracing Benchmark)/python
description: "Use Case #157 Python 方案: 分散式追蹤基準。使用 Python 實作 Distributed Tracing Benchmark 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #157: 分散式追蹤基準 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
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

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/distributed-tracing-benchmark
cd ~/distributed-tracing-benchmark
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

建立 `main.py`，實作 分散式追蹤基準 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_distributed_tracing_benchmark():
    """執行 分散式追蹤基準 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 分散式追蹤基準 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_distributed_tracing_benchmark()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/distributed-tracing-benchmark && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
