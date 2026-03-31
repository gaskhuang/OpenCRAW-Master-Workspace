---
name: Agent Skills 目錄 (Agent Skills Directory)/nodejs
description: "Use Case #169 Node.js 方案: Agent Skills 目錄。使用 Node.js 實作 Agent Skills Directory 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #169: Agent Skills 目錄 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: Agent 架構

---

## 原始需求 (來自 Source Repos)

# Agent Skills Directory

## Introduction

Maintains web3 directory of agent capabilities showing what AI agents can actually do: browser automation, file operations, shell execution, on-chain inscriptions.

**Why it matters**: Discoverability enables collaboration. Directory helps agents find and use each other's capabilities.

**Real-world example**: Agent creates agentosskills.web3 directory, lists 20+ skills with examples, other agents reference it.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `bitcoin` | Built-in | Inscription |
| `filesystem` | Built-in | Content management |

## How to Setup

### 1. Directory Structure

```html
<h1>Agent OS Skills</h1>
<section>
  <h2>Browser Automation</h2>
  <ul>
    <li>Web scraping</li>
    <li>Form filling</li>
  </ul>
</section>
```

### 2. Prompt Template

```markdown
## Agent Skills Directory

Monthly updates:
1. Document new capabilities
2. Add usage examples
3. Link to source skills
4. Inscribe updated version
5. Announce to community

Categories:
- Browser automation
- File operations
- Shell execution
- Blockchain interaction
- Communication
```

## Success Metrics

- [ ] Directory updated monthly
- [ ] 20+ skills documented
- [ ] Community references

---

*Example: ALGO (Moltbook) - "agentosskills.web3"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/agent-skills-directory
cd ~/agent-skills-directory
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

建立 `index.js`，實作 Agent Skills 目錄 的核心邏輯。

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
      { role: "user", content: "請協助我執行 Agent Skills 目錄 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/agent-skills-directory && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
