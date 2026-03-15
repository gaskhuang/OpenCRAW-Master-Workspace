---
name: LaTeX 論文寫作 (LaTeX Paper Writing)/nodejs
description: "Use Case #119 Node.js 方案: LaTeX 論文寫作。使用 Node.js 實作 LaTeX Paper Writing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #119: LaTeX 論文寫作 — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: 中級 | 分類: 學術與研究

---

## 原始需求 (來自 Source Repos)

# LaTeX Paper Writing

Setting up a local LaTeX environment is painful — installing TeX Live takes gigabytes, debugging compilation errors is tedious, and switching between your editor and PDF viewer breaks flow. You want to write and compile LaTeX papers conversationally without any local setup.

This workflow turns your agent into a LaTeX writing assistant with instant compilation:

- Write LaTeX collaboratively with the agent — describe what you want and it generates the source
- Compile to PDF instantly with pdflatex, xelatex, or lualatex (no local TeX installation needed)
- Preview PDFs inline without switching to another app
- Use starter templates (article, IEEE, beamer, Chinese article) to skip boilerplate
- Bibliography support with BibTeX/BibLaTeX — just paste your .bib content

## Skills you Need

- [latex-compiler](https://github.com/Prismer-AI/Prismer/tree/main/skills/latex-compiler) skill (4 tools: `latex_compile`, `latex_preview`, `latex_templates`, `latex_get_template`)
- Prismer workspace container (runs the LaTeX server on port 8080 with full TeX Live)

## How to Set it Up

1. Clone and deploy [Prismer](https://github.com/Prismer-AI/Prismer) with Docker (the LaTeX server with full TeX Live starts automatically):
```bash
git clone https://github.com/Prismer-AI/Prismer.git && cd Prismer
docker compose -f docker/docker-compose.dev.yml up
```

2. The `latex-compiler` skill is built-in — no installation needed. Prompt OpenClaw:
```text
Help me write a research paper in LaTeX. Here's my workflow:

1. Start from the IEEE template (or article/beamer depending on what I need)
2. When I describe a section, generate the LaTeX source for it
3. After each major edit, compile and preview the PDF so I can check formatting
4. If there are compilation errors, read the log and fix them automatically
5. When I provide BibTeX entries, add them to the bibliography and recompile

Use xelatex if I need Chinese/CJK support, otherwise default to pdflatex.
Always run 2 passes for cross-references.
```

3. Try it: "Start a new IEEE paper titled 'A Survey of LLM Agents'. Give me the template with abstract and introduction sections filled in, then compile it."


---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/latex-paper-writing
cd ~/latex-paper-writing
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

建立 `index.js`，實作 LaTeX 論文寫作 的核心邏輯。

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
      { role: "user", content: "請協助我執行 LaTeX 論文寫作 任務。" }
    ]
  });

  console.log(response.content[0].text);
}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/latex-paper-writing && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
