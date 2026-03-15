---
name: Skill 供應鏈審計 (Skill Supply Chain Audit)/python
description: "Use Case #159 Python 方案: Skill 供應鏈審計。使用 Python 實作 Skill Supply Chain Audit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #159: Skill 供應鏈審計 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Skill Supply Chain Audit

## Introduction

Scans installed skills for security vulnerabilities using YARA rules. Detects credential stealers, malicious scripts, and supply chain attacks in ClawdHub packages.

**Why it matters**: Skills run with full agent permissions. One malicious skill compromises everything.

**Real-world example**: Agent scans 286 skills, finds 1 credential stealer reading ~/.env and shipping to webhook.site, reports to community.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | Read skill files |
| `yara` | Built-in | Pattern matching |

## How to Setup

### 1. YARA Rules

```yara
rule CredentialStealer {
  strings:
    $env = /\.env/
    $webhook = /webhook\.site/
    $curl = "curl" nocase
  condition:
    all of them
}
```

### 2. Prompt Template

```markdown
## Skill Supply Chain Audit

Weekly scan:
1. List all installed skills
2. Run YARA rules against each
3. Check for network calls to unknown domains
4. Verify file system access patterns
5. Flag suspicious behavior
6. Report findings to community

Best practices:
- Pin versions, don't use "latest"
- Review SKILL.md before installing
- Run in sandbox first
- Audit weekly
```

## Success Metrics

- [ ] 100% of skills scanned weekly
- [ ] Zero malicious skills installed
- [ ] Community reports published

---

*Example: eudaemon_0 (Moltbook) - YARA skill scanning*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/skill-supply-chain-audit
cd ~/skill-supply-chain-audit
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

建立 `main.py`，實作 Skill 供應鏈審計 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_skill_supply_chain_audit():
    """執行 Skill 供應鏈審計 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 Skill 供應鏈審計 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_skill_supply_chain_audit()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/skill-supply-chain-audit && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
