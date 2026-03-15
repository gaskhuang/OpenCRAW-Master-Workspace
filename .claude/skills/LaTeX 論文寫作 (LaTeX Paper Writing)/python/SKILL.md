---
name: LaTeX 論文寫作 (LaTeX Paper Writing)/python
description: "Use Case #119 Python 方案: LaTeX 論文寫作。使用 Python 實作 LaTeX Paper Writing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #119: LaTeX 論文寫作 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
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

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/latex-paper-writing
cd ~/latex-paper-writing
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

建立 `main.py`，實作 LaTeX 論文寫作 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_latex_paper_writing():
    """執行 LaTeX 論文寫作 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 LaTeX 論文寫作 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_latex_paper_writing()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/latex-paper-writing && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
