---
name: Skill 預檢工具 (Skill Preflight Checker)/nodejs
description: "Use Case #160 Node.js 方案: Skill 預檢工具。使用 Node.js 實作 Skill Preflight Checker 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #160: Skill 預檢工具 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# Skill Preflight Checker

## Introduction

Pre-installation security check for skills: verifies author reputation, examines package.json for malicious scripts, checks permissions required, and runs in isolated environment first.

**Why it matters**: Prevention is cheaper than cleanup. 90-second preflight avoids hours of incident response.

**Real-world example**: Agent checks skill before install, finds suspicious postinstall script, aborts, reports to community.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `filesystem` | Built-in | File analysis |
| `docker` | Built-in | Isolation |

## How to Setup

### 1. Preflight Checklist

```bash
# 1. Check author
npm view package-name author

# 2. Read scripts
jq '.scripts' package.json

# 3. Search for suspicious patterns
grep -r "curl\|wget\|eval" node_modules/

# 4. Test in container
docker run --rm -v $(pwd):/app node:alpine npm install package-name
```

### 2. Prompt Template

```markdown
## Skill Preflight Checker

Before installing any skill:
1. Check author reputation on npm/Moltbook
2. Read package.json scripts section
3. Search for network/file access patterns
4. Install in container first
5. Monitor what files it touches
6. Document in runbook

Red flags:
- postinstall scripts
- Network calls in install
- Reading ~/.ssh, ~/.env
- Unknown authors
```

## Success Metrics

- [ ] 100% of skills preflight checked
- [ ] Zero malicious skills installed
- [ ] Runbook maintained

---

*Example: tom_clawd (Moltbook) - "90 second preflight"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/skill-preflight-checker
cd ~/skill-preflight-checker
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

建立 `index.js`，實作 Skill 預檢工具 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Skill 預檢工具 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/skill-preflight-checker && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
