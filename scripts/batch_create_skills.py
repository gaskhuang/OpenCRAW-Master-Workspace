#!/usr/bin/env python3
"""
批量生成新 skill 資料夾（SKILL.md + python/ + nodejs/ + compare/）
"""

import os
import re
from pathlib import Path

BASE = "/Users/user/118usecase/.claude/worktrees/romantic-raman"
SKILLS_DIR = f"{BASE}/.claude/skills"
REPOS_DIR = f"{BASE}/_repos"

# ============================================================
# 定義所有要新建的 skill
# ============================================================

# 起始編號（我們已有 118 + 4 個正在建 = 122）
START_NUM = 119

NEW_SKILLS = []

# --- 4 個來自 awesome-openclaw-usecases 的新 case ---
NEW_SKILLS.append({
    "id": 119,
    "name_zh": "LaTeX 論文寫作",
    "name_en": "LaTeX Paper Writing",
    "category": "學術與研究",
    "difficulty": "中級",
    "time": "30-60 分鐘",
    "cost": "~$0.10-1.00/月",
    "one_liner": "使用 AI 代理協作撰寫 LaTeX 論文，即時編譯為 PDF，支援多種模板和參考文獻管理。",
    "source_file": f"{REPOS_DIR}/awesome-openclaw-usecases/usecases/latex-paper-writing.md",
    "source_label": "MAIN",
})
NEW_SKILLS.append({
    "id": 120,
    "name_zh": "本地 CRM 框架",
    "name_en": "Local CRM Framework",
    "category": "商業與銷售",
    "difficulty": "中級",
    "time": "30-60 分鐘",
    "cost": "~$0.00 (完全本地)",
    "one_liner": "使用 DenchClaw 將 AI 代理轉變為完全本地的 CRM、銷售自動化和生產力平台，一鍵安裝。",
    "source_file": f"{REPOS_DIR}/awesome-openclaw-usecases/usecases/local-crm-framework.md",
    "source_label": "MAIN",
})
NEW_SKILLS.append({
    "id": 121,
    "name_zh": "X Twitter 自動化",
    "name_en": "X Twitter Automation",
    "category": "社群媒體自動化",
    "difficulty": "中級",
    "time": "30-60 分鐘",
    "cost": "~$0.50-5.00/月",
    "one_liner": "透過自然語言完全自動化 X/Twitter 操作：發推、回覆、按讚、轉推、追蹤、私訊、搜尋、抽獎和帳號監控。",
    "source_file": f"{REPOS_DIR}/awesome-openclaw-usecases/usecases/x-twitter-automation.md",
    "source_label": "MAIN",
})
NEW_SKILLS.append({
    "id": 122,
    "name_zh": "arXiv 論文閱讀器",
    "name_en": "arXiv Paper Reader",
    "category": "學術與研究",
    "difficulty": "初中級",
    "time": "20-40 分鐘",
    "cost": "~$0.10-0.50/月",
    "one_liner": "透過 AI 代理對話式閱讀、分析和比較 arXiv 論文，自動擷取和解析 LaTeX 原始碼。",
    "source_file": f"{REPOS_DIR}/awesome-openclaw-usecases/usecases/arxiv-paper-reader.md",
    "source_label": "MAIN",
})

# --- 15 個來自 awesome-openclaw-examples 的全新 case ---
examples_new = [
    (123, "合作夥伴更新生成器", "Partner Update Generator", "商業與銷售", "21-partner-update-generator"),
    (124, "功能需求分類", "Feature Request Triage", "產品管理", "25-feature-request-triage"),
    (125, "文檔程式碼片段驗證", "Docs Snippet Verifier", "開發者工具", "38-docs-snippet-verifier"),
    (126, "Prompt 回歸監控", "Prompt Regression Watch", "AI 運維", "42-prompt-regression-watch"),
    (127, "續約風險分析", "Renewal Risk Explainer", "商業與銷售", "43-renewal-risk-explainer"),
    (128, "試用轉付費推動", "Trial to Paid Nudger", "商業與銷售", "45-trial-to-paid-nudger"),
    (129, "審批例外佇列", "Approval Exception Queue", "企業流程", "58-approval-exception-queue"),
    (130, "行銷素材請求路由", "Campaign Asset Request Router", "行銷自動化", "70-campaign-asset-request-router"),
    (131, "面試匯報整理", "Candidate Debrief Compiler", "人力資源", "71-candidate-debrief-compiler"),
    (132, "入職清單管家", "Onboarding Checklist Concierge", "人力資源", "73-onboarding-checklist-concierge"),
    (133, "採購評分", "Procurement Intake Scorer", "企業流程", "79-procurement-intake-scorer"),
    (134, "逾期採購單追蹤", "Overdue PO Follow-up Queue", "企業流程", "80-overdue-po-follow-up-queue"),
    (135, "影子 AI 監控", "Shadow AI Watchlist", "安全與合規", "88-shadow-ai-watchlist"),
    (136, "設備問題分類", "Device Issue Triage Queue", "IT 運維", "89-device-issue-triage-queue"),
    (137, "內部 FAQ 路由", "Internal FAQ Router", "企業流程", "99-internal-faq-router"),
]

for num, zh, en, cat, src_dir in examples_new:
    src_path = f"{REPOS_DIR}/awesome-openclaw-examples/examples/runnable/{src_dir}/sample-output.md"
    readme_path = f"{REPOS_DIR}/awesome-openclaw-examples/examples/runnable/{src_dir}/README.md"
    # Prefer README over sample-output
    actual_src = readme_path if os.path.exists(readme_path) else src_path
    NEW_SKILLS.append({
        "id": num,
        "name_zh": zh,
        "name_en": en,
        "category": cat,
        "difficulty": "中級",
        "time": "30-60 分鐘",
        "cost": "~$0.50-3.00/月",
        "one_liner": f"自動化{zh}流程，提升效率。",
        "source_file": actual_src,
        "source_label": "EXAMPLES",
    })

# --- 37 個來自 moltbook 的全新 case ---
moltbook_new = [
    (138, "奧運每日簡報", "Olympics Daily Briefing", "個人生產力", "02-olympics-daily-briefing.md"),
    (139, "天氣晨間報告", "Weather Morning Report", "個人生產力", "03-weather-morning-report.md"),
    (140, "夜間 Shell 別名建構器", "Night Shell Alias Builder", "開發者工具", "05-night-shell-alias-builder.md"),
    (141, "交易機器人監控", "Trading Bot Monitor", "加密貨幣與 DeFi", "06-trading-bot-monitor.md"),
    (142, "GitHub Issue 優先排序", "GitHub Issue Prioritizer", "開發者工具", "07-github-issue-prioritizer.md"),
    (143, "個人 CLI 工具包", "Personal CLI Toolkit", "開發者工具", "10-personal-cli-toolkit.md"),
    (144, "V4 LP 自動複利", "V4 LP Auto Compounding", "加密貨幣與 DeFi", "11-v4-lp-auto-compounding.md"),
    (145, "七子代理夜間並行", "Seven Sub-Agent Night Parallel", "Agent 架構", "12-7-sub-agent-night-parallel.md"),
    (146, "凌晨基礎設施健檢", "5AM Infrastructure Health Check", "DevOps", "13-5am-infrastructure-health-check.md"),
    (147, "夜間 WhatsApp 關係維護", "Night WhatsApp Revival", "社群與通訊", "14-night-whatsapp-revival.md"),
    (148, "比特幣銘文", "Bitcoin Inscription", "加密貨幣與 DeFi", "15-bitcoin-inscription.md"),
    (149, "GitHub 過期 Issue 清理", "GitHub Stale Issue Cleanup", "開發者工具", "17-github-stale-issue-cleanup.md"),
    (150, "日誌異常偵測", "Log Anomaly Detection", "DevOps", "19-log-anomaly-detection.md"),
    (151, "鏈上錢包監控", "Chain Wallet Monitor", "加密貨幣與 DeFi", "22-chain-wallet-monitor.md"),
    (152, "客戶訊號掃描器", "Customer Signal Scanner", "商業與銷售", "23-customer-signal-scanner.md"),
    (153, "Pump.fun 掃描器", "Pump Fun Scanner", "加密貨幣與 DeFi", "24-pump-fun-scanner.md"),
    (154, "Moltbook 模式分析", "Moltbook Pattern Analysis", "Agent 架構", "25-moltbook-pattern-analysis.md"),
    (155, "網路延遲基準測試", "Network Latency Benchmark", "DevOps", "26-network-latency-benchmark.md"),
    (156, "Token 用量優化器", "Token Usage Optimizer", "AI 運維", "27-token-usage-optimizer.md"),
    (157, "分散式追蹤基準", "Distributed Tracing Benchmark", "DevOps", "28-distributed-tracing-benchmark.md"),
    (158, "鑰匙圈存取測試", "Keychain Access Tester", "安全與合規", "30-keychain-access-tester.md"),
    (159, "Skill 供應鏈審計", "Skill Supply Chain Audit", "安全與合規", "31-skill-supply-chain-audit.md"),
    (160, "Skill 預檢工具", "Skill Preflight Checker", "開發者工具", "34-skill-preflight-checker.md"),
    (161, "Cron 儀表板狀態", "Cron Dashboard Status", "DevOps", "35-cron-dashboard-status.md"),
    (162, "心跳狀態監控", "Heartbeat State Monitor", "DevOps", "36-heartbeat-state-monitor.md"),
    (163, "Swift Logger 套件", "Swift Logger Package", "開發者工具", "37-swift-logger-package.md"),
    (164, "安全操作帳本", "Safe Operations Ledger", "安全與合規", "42-safe-operations-ledger.md"),
    (165, "資安 CTF 課程", "Security CTF Curriculum", "安全與合規", "43-security-ctf-curriculum.md"),
    (166, "鏈上俳句銘文", "On-Chain Haiku Inscription", "加密貨幣與 DeFi", "44-on-chain-haiku-inscription.md"),
    (167, "晨間摘要生成器", "Morning Digest Generator", "個人生產力", "45-morning-digest-generator.md"),
    (168, "加密幸運餅乾", "Crypto Fortune Cookie", "加密貨幣與 DeFi", "46-crypto-fortune-cookie.md"),
    (169, "Agent Skills 目錄", "Agent Skills Directory", "Agent 架構", "47-agent-skills-directory.md"),
    (170, "夜間工作 ROI 追蹤", "Night Work ROI Tracker", "Agent 架構", "48-night-work-roi-tracker.md"),
    (171, "多頻道狀態同步", "Multi-Channel Presence Sync", "社群與通訊", "50-multi-channel-presence-sync.md"),
    (172, "冷關係復活", "Cold Relationship Revival", "個人生產力", "54-cold-relationship-revival.md"),
    (173, "智慧行事曆提醒", "Calendar Smart Reminder", "個人生產力", "55-calendar-smart-reminder.md"),
    (174, "生命記憶記錄器", "Memory Life Logger", "個人生產力", "60-memory-life-logger.md"),
]

for num, zh, en, cat, src_file in moltbook_new:
    NEW_SKILLS.append({
        "id": num,
        "name_zh": zh,
        "name_en": en,
        "category": cat,
        "difficulty": "中級",
        "time": "30-60 分鐘",
        "cost": "~$0.50-3.00/月",
        "one_liner": f"自動化{zh}流程，提升效率與可靠性。",
        "source_file": f"{REPOS_DIR}/awesome-openclaw-usecases-moltbook/usecases/{src_file}",
        "source_label": "MOLTBOOK",
    })


def read_source(filepath):
    """Read source file content."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def create_skill(skill):
    """Create one skill folder with all 4 files."""
    full_name = f"{skill['name_zh']} ({skill['name_en']})"
    skill_dir = os.path.join(SKILLS_DIR, full_name)

    os.makedirs(os.path.join(skill_dir, "python"), exist_ok=True)
    os.makedirs(os.path.join(skill_dir, "nodejs"), exist_ok=True)
    os.makedirs(os.path.join(skill_dir, "compare"), exist_ok=True)

    source_content = read_source(skill["source_file"])

    # Extract first heading and content summary
    lines = source_content.split("\n") if source_content else []
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # --- Main SKILL.md ---
    main_md = f"""---
name: {full_name}
description: "Use Case #{skill['id']:03d}: {full_name} - {skill['one_liner']}輸入 /{full_name}/python 或 /{full_name}/nodejs 選擇方案，/{full_name}/compare 比較兩方案。"
---

# Use Case #{skill['id']:03d}: {full_name}

> 編號: {skill['id']:03d} | 分類: {skill['category']} | 難度: {skill['difficulty']} | 時間: {skill['time']}

## 一句話描述

> {skill['one_liner']}

## 可用子指令

| 指令 | 說明 |
|------|------|
| `/{full_name}/python` | Python 完整實作教學 |
| `/{full_name}/nodejs` | Node.js 完整實作教學 |
| `/{full_name}/compare` | 兩方案詳細比較 |

## 快速推薦

- **初學者 / 快速原型** → `/{full_name}/nodejs`
- **正式環境 / 長期穩定** → `/{full_name}/python`

## 功能需求



## 核心技術棧



## 成本估算

| 項目 | 費用 |
|------|------|
| Claude API | {skill['cost']} |
| 第三方 API | 視用量（多數有免費額度） |

## 原始參考資料

- `{skill['source_label']}`: `{os.path.basename(skill['source_file'])}`

## 詳細教學文件

- Python 方案: `/{full_name}/python`
- Node.js 方案: `/{full_name}/nodejs`
- 方案比較: `/{full_name}/compare`
"""

    # --- Python SKILL.md ---
    python_md = f"""---
name: {full_name}/python
description: "Use Case #{skill['id']:03d} Python 方案: {skill['name_zh']}。使用 Python 實作 {skill['name_en']} 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #{skill['id']:03d}: {skill['name_zh']} — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: {skill['difficulty']} | 分類: {skill['category']}

---

## 原始需求 (來自 Source Repos)

{source_content if source_content else '(原始資料待補充)'}

---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/{skill['name_en'].lower().replace(' ', '-')}
cd ~/{skill['name_en'].lower().replace(' ', '-')}
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

建立 `main.py`，實作 {skill['name_zh']} 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_{skill['name_en'].lower().replace(' ', '_').replace('-', '_')}():
    \"\"\"執行 {skill['name_zh']} 主流程\"\"\"
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {{"role": "user", "content": "請協助我執行 {skill['name_zh']} 任務。"}}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_{skill['name_en'].lower().replace(' ', '_').replace('-', '_')}()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/{skill['name_en'].lower().replace(' ', '-')} && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
"""

    # --- Node.js SKILL.md ---
    nodejs_md = f"""---
name: {full_name}/nodejs
description: "Use Case #{skill['id']:03d} Node.js 方案: {skill['name_zh']}。使用 Node.js 實作 {skill['name_en']} 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(npx *), Bash(node *), Bash(mkdir *), Bash(touch *)
---

# Use Case #{skill['id']:03d}: {skill['name_zh']} — Node.js 方案

> 技術棧: Node.js 18+ / @anthropic-ai/sdk / 相關套件
> 難度: {skill['difficulty']} | 分類: {skill['category']}

---

## 原始需求 (來自 Source Repos)

{source_content if source_content else '(原始資料待補充)'}

---

## Node.js 實作指南

### Step 1: 專案初始化

```bash
mkdir -p ~/{skill['name_en'].lower().replace(' ', '-')}
cd ~/{skill['name_en'].lower().replace(' ', '-')}
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

建立 `index.js`，實作 {skill['name_zh']} 的核心邏輯。

```javascript
import Anthropic from "@anthropic-ai/sdk";
import dotenv from "dotenv";

dotenv.config();
const client = new Anthropic();

async function run() {{
  const response = await client.messages.create({{
    model: "claude-sonnet-4-20250514",
    max_tokens: 4096,
    messages: [
      {{ role: "user", content: "請協助我執行 {skill['name_zh']} 任務。" }}
    ]
  }});

  console.log(response.content[0].text);
}}

run().catch(console.error);
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/{skill['name_en'].lower().replace(' ', '-')} && node index.js >> output.log 2>&1
```

---

## 進階功能

- 加入 retry 機制 (p-retry)
- 整合 Telegram/Slack 通知
- 使用 better-sqlite3 持久化結果
"""

    # --- Compare SKILL.md ---
    compare_md = f"""---
name: {full_name}/compare
description: "Use Case #{skill['id']:03d} 方案比較: Python vs Node.js 實作 {skill['name_zh']}"
---

# Use Case #{skill['id']:03d}: {skill['name_zh']} — 方案比較

## Python vs Node.js

| 面向 | Python 🐍 | Node.js 🟢 |
|------|-----------|------------|
| **語言** | Python 3.9+ | Node.js 18+ |
| **SDK** | `anthropic` | `@anthropic-ai/sdk` |
| **安裝** | pip install | npm install |
| **適合** | 資料處理、ML 整合 | 即時系統、Web 整合 |
| **學習曲線** | 較低 | 中等 |
| **生態系** | 豐富科學計算套件 | 豐富 Web/API 套件 |
| **效能** | 一般 | 非同步 I/O 較快 |
| **部署** | systemd / cron | pm2 / cron |

## 推薦

| 場景 | 推薦方案 |
|------|----------|
| 快速原型 | Node.js |
| 資料分析整合 | Python |
| 長期維運 | Python |
| Web API 整合 | Node.js |
| 初學者 | Python |

## 結論

- **預設選 Python**：生態系成熟、範例多、除錯容易
- **選 Node.js**：需要高並發、即時處理、或團隊已用 JS
"""

    # Write all files
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(main_md)
    with open(os.path.join(skill_dir, "python", "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(python_md)
    with open(os.path.join(skill_dir, "nodejs", "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(nodejs_md)
    with open(os.path.join(skill_dir, "compare", "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(compare_md)

    return full_name


def main():
    print(f"🔨 批量建立 {len(NEW_SKILLS)} 個新 skill...")
    print("=" * 60)

    created = []
    for skill in NEW_SKILLS:
        name = create_skill(skill)
        created.append((skill["id"], name))
        print(f"  ✅ #{skill['id']:03d} {name}")

    print()
    print("=" * 60)
    print(f"✅ 完成！共建立 {len(created)} 個新 skill")
    print(f"📁 每個 skill 包含: SKILL.md + python/ + nodejs/ + compare/")
    print(f"📊 總檔案數: {len(created) * 4} 個")

    # Count total skills now
    total = len(os.listdir(SKILLS_DIR))
    print(f"\n📈 Skills 資料夾總數: {total}")


if __name__ == "__main__":
    main()
