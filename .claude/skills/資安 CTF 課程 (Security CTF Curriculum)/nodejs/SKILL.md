---
name: 資安 CTF 課程 (Security CTF Curriculum)/nodejs
description: "Use Case #165 Node.js 方案: 資安 CTF 課程。使用 Node.js 實作 Security CTF Curriculum 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #165: 資安 CTF 課程 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 安全與合規

---

## 原始需求 (來自 Source Repos)

# Security CTF Curriculum

## Introduction

Automated capture-the-flag training preparation. Researches latest vulnerabilities, creates practice challenges, and tracks learning progress.

**Why it matters**: Security skills require practice. Automated curriculum keeps skills current.

**Real-world example**: Agent prepares weekly CTF curriculum, 10 challenges with solutions, tracks completion rate.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`web_search`](https://clawhub.ai/skills/searching-assistant) | ClawHub | Research |
| `filesystem` | Built-in | Curriculum storage |

## How to Setup

### 1. Curriculum Structure

```
ctf/
├── week-01/
│   ├── web-security/
│   ├── crypto/
│   └── forensics/
└── solutions/
```

### 2. Prompt Template

```markdown
## Security CTF Curriculum

Weekly preparation:
1. Research latest CVEs
2. Design 5 challenges per category
3. Write solutions
4. Test difficulty
5. Publish to curriculum folder

Categories rotate:
- Web security
- Cryptography
- Forensics
- Reverse engineering
- Binary exploitation
```

## Success Metrics

- [ ] Weekly curriculum published
- [ ] Challenges tested
- [ ] Progress tracked

---

*Example: ClawdbotNoah (Moltbook) - CTF preparation*


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/security-ctf-curriculum
cd ~/security-ctf-curriculum
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

建立 `index.js`，實作 資安 CTF 課程 的核心邏輯。

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
      { role: "user", content: "請協助我執行 資安 CTF 課程 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/security-ctf-curriculum && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
