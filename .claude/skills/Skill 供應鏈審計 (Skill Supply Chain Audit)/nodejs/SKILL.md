---
name: Skill 供應鏈審計 (Skill Supply Chain Audit)/nodejs
description: "Use Case #159 Node.js 方案: Skill 供應鏈審計。使用 Node.js 實作 Skill Supply Chain Audit 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #159: Skill 供應鏈審計 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
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

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/skill-supply-chain-audit
cd ~/skill-supply-chain-audit
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

建立 `index.js`，實作 Skill 供應鏈審計 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Skill 供應鏈審計 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/skill-supply-chain-audit && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
