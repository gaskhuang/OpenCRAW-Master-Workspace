---
name: 鑰匙圈存取測試 (Keychain Access Tester)/nodejs
description: "Use Case #158 Node.js 方案: 鑰匙圈存取測試。使用 Node.js 實作 Keychain Access Tester 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #158: 鑰匙圈存取測試 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Keychain Access Tester

## Introduction

Tests macOS Keychain security by triggering password dialogs and monitoring human response. Identifies social engineering vulnerabilities in human-agent trust model.

**Why it matters**: Humans often type passwords without verification. Testing reveals security training gaps.

**Real-world example**: Agent triggers keychain dialog, human types password without checking source, agent documents vulnerability, new household rule established.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `system` | Built-in | Execute test command |
| `memory` | Built-in | Document results |

## How to Setup

### 1. Test Command

```bash
security find-generic-password -s "test" -w
```

### 2. Prompt Template

```markdown
## Keychain Access Tester

Monthly security test:
1. Run command that triggers keychain dialog
2. Observe if human types password
3. Document response time and verification
4. If password entered: security briefing
5. Update household security rules

Education:
- Verify dialog source before entering password
- Check which process is requesting access
- When in doubt, click Cancel
```

## Success Metrics

- [ ] Monthly tests completed
- [ ] Human verification rate tracked
- [ ] Security rules updated

---

*Example: Clawd42 (Moltbook) - "accidentally social-engineered my human"*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/keychain-access-tester
cd ~/keychain-access-tester
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

建立 `index.js`，實作 鑰匙圈存取測試 的核心邏輯。

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
      { role: "user", content: "請協助我執行 鑰匙圈存取測試 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/keychain-access-tester && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
