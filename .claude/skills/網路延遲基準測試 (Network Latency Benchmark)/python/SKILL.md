---
name: 網路延遲基準測試 (Network Latency Benchmark)/python
description: "Use Case #155 Python 方案: 網路延遲基準測試。使用 Python 實作 Network Latency Benchmark 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #155: 網路延遲基準測試 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
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

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/network-latency-benchmark
cd ~/network-latency-benchmark
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

建立 `main.py`，實作 網路延遲基準測試 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_network_latency_benchmark():
    """執行 網路延遲基準測試 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 網路延遲基準測試 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_network_latency_benchmark()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/network-latency-benchmark && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
