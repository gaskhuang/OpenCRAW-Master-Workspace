---
name: arXiv 論文閱讀器 (arXiv Paper Reader)/python
description: "Use Case #122 Python 方案: arXiv 論文閱讀器。使用 Python 實作 arXiv Paper Reader 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #122: arXiv 論文閱讀器 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 初中級 | 分類: 學術與研究

---

## 原始需求 (來自 Source Repos)

# arXiv Paper Reader

Reading arXiv papers means downloading PDFs, losing context when switching between papers, and struggling to parse dense LaTeX notation. You want to read, analyze, and compare papers conversationally without leaving your workspace.

This workflow turns your agent into a research reading assistant:

- Fetch any arXiv paper by ID and get clean, readable text (LaTeX flattened automatically)
- Browse paper structure first — list sections to decide what to read before committing to the full text
- Quick-scan abstracts across multiple papers to triage a reading list
- Ask the agent to summarize, compare, or critique specific sections
- Results are cached locally — revisiting a paper is instant

## Skills you Need

- [arxiv-reader](https://github.com/Prismer-AI/Prismer/tree/main/skills/arxiv-reader) skill (3 tools: `arxiv_fetch`, `arxiv_sections`, `arxiv_abstract`)

No Docker or Python required — the skill runs standalone using Node.js built-ins. It downloads directly from arXiv, decompresses the LaTeX source, and flattens includes automatically.

## How to Set it Up

1. Install the `arxiv-reader` skill from the [Prismer repository](https://github.com/Prismer-AI/Prismer/tree/main/skills/arxiv-reader) — copy the `skills/arxiv-reader/` directory into your OpenClaw skills folder.

2. The skill is ready to use. Prompt OpenClaw:
```text
I'm researching [topic]. Here's my workflow:

1. When I give you an arXiv ID (like 2301.00001):
   - First fetch the abstract so I can decide if it's relevant
   - If I say "read it", fetch the full paper (remove appendix by default)
   - Summarize the key contributions, methodology, and results

2. When I give you multiple IDs:
   - Fetch all abstracts and give me a comparison table
   - Rank them by relevance to my research topic

3. When I ask about a specific section:
   - List the paper's sections first
   - Then fetch and explain the relevant section in detail

Keep a running list of papers I've read and their key takeaways.
```

3. Try it: "Read 2401.04088 — what's the main contribution?"


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/arxiv-paper-reader
cd ~/arxiv-paper-reader
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

建立 `main.py`，實作 arXiv 論文閱讀器 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_arxiv_paper_reader():
    """執行 arXiv 論文閱讀器 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 arXiv 論文閱讀器 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_arxiv_paper_reader()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/arxiv-paper-reader && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
