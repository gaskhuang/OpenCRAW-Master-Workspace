---
name: 文檔程式碼片段驗證 (Docs Snippet Verifier)/python
description: "Use Case #125 Python 方案: 文檔程式碼片段驗證。使用 Python 實作 Docs Snippet Verifier 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #125: 文檔程式碼片段驗證 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# 38 - Docs Snippet Verifier

Builds a recurring docs verification packet from documentation snippets that may no longer match shipped behavior.

## Skill Stack

```bash
npx clawhub@latest install github
npx clawhub@latest install notion
npx clawhub@latest install summarize
```

## What It Does

- Scans documentation snippets that may no longer match shipped behavior across configured engineering tools
- Ranks issues by risk, recurrence, and delivery impact
- Produces a docs verification packet for operator review

## Setup

```bash
export TARGET_SCOPE='developer docs'
export LOOKBACK_DAYS='7'
export DELIVERY_CHANNEL='slack'
export DELIVERY_TARGET='channel:C1234567890'
export CRON_EXPR='26 14 * * 4'
export CRON_NAME='Docs Snippet Verifier'
```

```bash
bash examples/runnable/38-docs-snippet-verifier/scripts/check_prereqs.sh
bash examples/runnable/38-docs-snippet-verifier/scripts/install_cron.sh
```

## Smoke Test

- Run once and verify the docs verification packet includes evidence-backed prioritization.
- Confirm no external action is taken automatically and any draft output stays reviewable.

## KPI

- docs mismatches caught pre-release
- triage latency
- repeat issue escape rate

## Security Notes

- Use read-only repository or analytics scopes for the first rollout.
- Deliver only to trusted engineering channels and require human review for follow-up writes.

## Failure Modes

- Missing repository scopes can hide critical context.
- Noisy data can over-rank low-value issues unless thresholds are tuned.

## Rollback

```bash
openclaw cron delete <job-id>
```


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/docs-snippet-verifier
cd ~/docs-snippet-verifier
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

建立 `main.py`，實作 文檔程式碼片段驗證 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_docs_snippet_verifier():
    """執行 文檔程式碼片段驗證 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 文檔程式碼片段驗證 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_docs_snippet_verifier()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/docs-snippet-verifier && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
