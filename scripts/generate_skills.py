#!/usr/bin/env python3
"""
generate_skills.py - Batch-generate the skill directory structure for all 118 use cases.

Creates the following structure for each use case:
  .claude/skills/usecase-{NNN}/
  ├── SKILL.md          (main overview)
  ├── python/
  │   └── SKILL.md      (Python implementation)
  ├── nodejs/
  │   └── SKILL.md      (Node.js implementation)
  └── compare/
      └── SKILL.md      (comparison)

Skips usecase-001 (already done).
"""

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# All 118 use cases: (number, chinese_name, english_name, category, difficulty)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "social-media": "社群媒體",
    "creative-content": "創意與內容製作",
    "daily-life": "日常生活自動化",
    "productivity": "生產力工具",
    "business-marketing": "商業、行銷與銷售",
    "devops-engineering": "DevOps 與工程",
    "security-compliance": "安全與合規",
    "monitoring-ops": "監控與維運",
    "research-learning": "研究與學習",
    "finance-trading": "金融與交易",
    "health-growth": "健康與個人成長",
    "ai-memory-agent": "AI 記憶與代理架構",
}

USE_CASES = [
    # --- 社群媒體 (001-009) ---
    (1,   "每日 Reddit 摘要",           "Daily Reddit Digest",                  "social-media",        "初中級"),
    (2,   "每日 YouTube 摘要",          "Daily YouTube Digest",                 "social-media",        "初中級"),
    (3,   "X 帳號質性分析",             "X Account Qualitative Analysis",       "social-media",        "中級"),
    (4,   "多來源科技新聞摘要",         "Multi-Source Tech News Digest",        "social-media",        "中級"),
    (5,   "品牌社群監控",               "Brand Social Monitoring",              "social-media",        "中級"),
    (6,   "自動排程社群發文",           "Auto-Schedule Social Posts",           "social-media",        "中級"),
    (7,   "Instagram 限時動態管理",     "Instagram Stories Management",         "social-media",        "中高級"),
    (8,   "Reddit 產品聲量追蹤",        "Reddit Product Buzz Tracking",         "social-media",        "中級"),
    (9,   "X 互動管理助手",             "X Engagement Manager",                 "social-media",        "中級"),

    # --- 創意與內容製作 (010-018) ---
    (10,  "目標驅動自主任務",           "Goal-Driven Autonomous Tasks",         "creative-content",    "高級"),
    (11,  "YouTube 內容產線",           "YouTube Content Pipeline",             "creative-content",    "中高級"),
    (12,  "多代理內容工廠",             "Multi-Agent Content Factory",          "creative-content",    "高級"),
    (13,  "自主遊戲開發流水線",         "Autonomous Game Dev Pipeline",         "creative-content",    "高級"),
    (14,  "Podcast 製作流水線",         "Podcast Production Pipeline",          "creative-content",    "中高級"),
    (15,  "電子報轉 Podcast",           "Newsletter to Podcast",               "creative-content",    "中級"),
    (16,  "AI 寫作助手",               "AI Writing Assistant",                 "creative-content",    "初中級"),
    (17,  "一文多平台內容複製",         "Cross-Platform Content Repurposing",   "creative-content",    "中級"),
    (18,  "學術研究助手",               "Academic Research Assistant",          "creative-content",    "中高級"),

    # --- 日常生活自動化 (019-028) ---
    (19,  "Telegram 智慧家居控制",      "Telegram Smart Home Control",          "daily-life",          "中高級"),
    (20,  "旅遊行程規劃",               "Travel Itinerary Planner",            "daily-life",          "中級"),
    (21,  "跨平台比價購物",             "Cross-Platform Price Comparison",      "daily-life",          "中級"),
    (22,  "天氣穿搭建議",               "Weather-Based Outfit Suggestions",    "daily-life",          "初中級"),
    (23,  "生日祝福自動發送",           "Auto Birthday Wishes",                "daily-life",          "初級"),
    (24,  "自動預訂代理",               "Auto Booking Agent",                  "daily-life",          "中高級"),
    (25,  "閱讀清單智慧管理",           "Smart Reading List Manager",          "daily-life",          "中級"),
    (26,  "食譜推薦與購物清單",         "Recipe & Shopping List",              "daily-life",          "初中級"),
    (27,  "耐心作業輔導老師",           "Patient Homework Tutor",              "daily-life",          "中級"),
    (28,  "每日學習日誌",               "Daily Learning Journal",              "daily-life",          "初級"),

    # --- 生產力工具 (029-054) ---
    (29,  "自主專案管理",               "Autonomous Project Management",       "productivity",        "高級"),
    (30,  "多通道 AI 客服",             "Multi-Channel AI Customer Service",   "productivity",        "中高級"),
    (31,  "電話語音個人助理",           "Phone Voice Personal Assistant",      "productivity",        "高級"),
    (32,  "收件匣清理器",               "Inbox Cleaner",                       "productivity",        "中級"),
    (33,  "個人 CRM",                   "Personal CRM",                        "productivity",        "中級"),
    (34,  "健康與症狀追蹤器",           "Health & Symptom Tracker",            "productivity",        "中級"),
    (35,  "多通道個人助理",             "Multi-Channel Personal Assistant",    "productivity",        "中高級"),
    (36,  "事件驅動專案狀態管理",       "Event-Driven Project Status",         "productivity",        "中高級"),
    (37,  "動態即時儀表板",             "Dynamic Real-Time Dashboard",         "productivity",        "中高級"),
    (38,  "Todoist 透明任務管理",       "Todoist Transparent Task Management", "productivity",        "中級"),
    (39,  "家庭行事曆與家務助理",       "Family Calendar & Chore Assistant",   "productivity",        "中級"),
    (40,  "多代理專業團隊",             "Multi-Agent Professional Team",       "productivity",        "高級"),
    (41,  "客製化晨間簡報",             "Custom Morning Briefing",             "productivity",        "中級"),
    (42,  "自動會議紀錄與行動項目",     "Auto Meeting Notes & Action Items",   "productivity",        "中高級"),
    (43,  "習慣追蹤與問責教練",         "Habit Tracker & Accountability Coach","productivity",        "中級"),
    (44,  "第二大腦",                   "Second Brain",                        "productivity",        "中高級"),
    (45,  "活動賓客電話確認",           "Event Guest Phone Confirmation",      "productivity",        "中高級"),
    (46,  "郵件自動分類器",             "Email Auto Classifier",               "productivity",        "中級"),
    (47,  "語音筆記轉任務",             "Voice Notes to Tasks",                "productivity",        "中級"),
    (48,  "PDF 文件處理中心",           "PDF Document Processing Hub",         "productivity",        "中級"),
    (49,  "會議前情報準備",             "Pre-Meeting Intel Prep",              "productivity",        "中級"),
    (50,  "行事曆衝突排解",             "Calendar Conflict Resolution",        "productivity",        "中級"),
    (51,  "看板自動整理",               "Kanban Auto Organizer",               "productivity",        "中級"),
    (52,  "包裹追蹤自動化",             "Package Tracking Automation",         "productivity",        "初中級"),
    (53,  "異步站會機器人",             "Async Standup Bot",                   "productivity",        "中級"),
    (54,  "會議時間自動協調",           "Meeting Time Auto Coordination",      "productivity",        "中級"),

    # --- 商業、行銷與銷售 (055-068) ---
    (55,  "競爭對手情報週報",           "Competitor Intelligence Weekly",      "business-marketing",  "中高級"),
    (56,  "競品定價即時追蹤",           "Competitor Pricing Tracker",          "business-marketing",  "中級"),
    (57,  "競品情緒分析",               "Competitor Sentiment Analysis",       "business-marketing",  "中高級"),
    (58,  "程式化 SEO",                 "Programmatic SEO",                    "business-marketing",  "中高級"),
    (59,  "HARO 外鏈建設",             "HARO Link Building",                  "business-marketing",  "中級"),
    (60,  "潛在客戶資料豐富",           "Lead Enrichment",                     "business-marketing",  "中級"),
    (61,  "冷外聯自動化",               "Cold Outreach Automation",            "business-marketing",  "中級"),
    (62,  "廣告效益每日報告",           "Ad Performance Daily Report",         "business-marketing",  "中級"),
    (63,  "每週策略備忘錄",             "Weekly Strategy Memo",                "business-marketing",  "中級"),
    (64,  "自由工作者案源開發",         "Freelancer Lead Generation",          "business-marketing",  "中級"),
    (65,  "網紅發掘與外聯",             "Influencer Discovery & Outreach",     "business-marketing",  "中級"),
    (66,  "銷售電話準備助手",           "Sales Call Prep Assistant",           "business-marketing",  "中級"),
    (67,  "評論追蹤管理",               "Review Tracking Manager",             "business-marketing",  "中級"),
    (68,  "廣告創意 A/B 測試",         "Ad Creative A/B Testing",             "business-marketing",  "中高級"),

    # --- DevOps 與工程 (069-078) ---
    (69,  "n8n 工作流程編排",           "n8n Workflow Orchestration",          "devops-engineering",  "中高級"),
    (70,  "自我修復家庭伺服器",         "Self-Healing Home Server",            "devops-engineering",  "高級"),
    (71,  "PR 追蹤雷達",               "PR Tracking Radar",                   "devops-engineering",  "中級"),
    (72,  "CI 不穩定測試修復",          "CI Flaky Test Fix",                   "devops-engineering",  "中高級"),
    (73,  "文件漂移哨兵",               "Doc Drift Sentinel",                  "devops-engineering",  "中級"),
    (74,  "變更日誌自動化",             "Changelog Automation",                "devops-engineering",  "中級"),
    (75,  "依賴套件審計",               "Dependency Audit",                    "devops-engineering",  "中級"),
    (76,  "Sentry 事故回顧報告",        "Sentry Incident Retrospective",       "devops-engineering",  "中高級"),
    (77,  "部署自動化流水線",           "Deployment Automation Pipeline",      "devops-engineering",  "高級"),
    (78,  "程式碼自動文件化",           "Code Auto Documentation",             "devops-engineering",  "中級"),

    # --- 安全與合規 (079-084) ---
    (79,  "SSH 金鑰安全掃描",          "SSH Key Security Scan",               "security-compliance", "中級"),
    (80,  "AWS 憑證安全掃描",           "AWS Credential Security Scan",        "security-compliance", "中級"),
    (81,  "Git 歷史敏感資訊清理",       "Git History Sensitive Data Cleanup",  "security-compliance", "中高級"),
    (82,  "API 安全測試",               "API Security Testing",                "security-compliance", "中高級"),
    (83,  "漏洞自動掃描",               "Vulnerability Auto Scan",             "security-compliance", "中高級"),
    (84,  "法規合規性自動檢查",         "Regulatory Compliance Auto Check",    "security-compliance", "高級"),

    # --- 監控與維運 (085-092) ---
    (85,  "SLA 守護者",                "SLA Guardian",                        "monitoring-ops",      "中高級"),
    (86,  "網站可用性監控",             "Website Uptime Monitor",              "monitoring-ops",      "中級"),
    (87,  "SSL 憑證到期監控",           "SSL Certificate Expiry Monitor",      "monitoring-ops",      "初中級"),
    (88,  "資料庫自動備份",             "Database Auto Backup",                "monitoring-ops",      "中級"),
    (89,  "AI 模型費用追蹤中心",        "AI Model Cost Tracker",               "monitoring-ops",      "中級"),
    (90,  "每週事故摘要",               "Weekly Incident Summary",             "monitoring-ops",      "中級"),
    (91,  "API 速率限制監控",           "API Rate Limit Monitor",              "monitoring-ops",      "中級"),
    (92,  "智慧警報彙整去重",           "Smart Alert Aggregation & Dedup",     "monitoring-ops",      "中高級"),

    # --- 研究與學習 (093-101) ---
    (93,  "AI 財報追蹤器",             "AI Financial Report Tracker",         "research-learning",   "中高級"),
    (94,  "個人知識庫 (RAG)",           "Personal Knowledge Base (RAG)",       "research-learning",   "高級"),
    (95,  "市場調研與 MVP 工廠",        "Market Research & MVP Factory",       "research-learning",   "高級"),
    (96,  "建造前點子驗證器",           "Pre-Build Idea Validator",            "research-learning",   "中級"),
    (97,  "語義記憶搜尋",               "Semantic Memory Search",              "research-learning",   "中高級"),
    (98,  "YouTube 研究分析桌",         "YouTube Research Desk",               "research-learning",   "中級"),
    (99,  "每週研究情報摘要",           "Weekly Research Intel Summary",       "research-learning",   "中級"),
    (100, "內容靈感挖掘機",             "Content Inspiration Miner",           "research-learning",   "中級"),
    (101, "產品需求文件起草",           "Product Requirements Doc Draft",      "research-learning",   "中級"),

    # --- 金融與交易 (102-107) ---
    (102, "Polymarket 自動交易",        "Polymarket Auto Trading",             "finance-trading",     "高級"),
    (103, "投資案流程管理",             "Investment Deal Pipeline",            "finance-trading",     "中高級"),
    (104, "投資組合監控",               "Portfolio Monitor",                   "finance-trading",     "中高級"),
    (105, "訂閱費用審計",               "Subscription Cost Audit",             "finance-trading",     "中級"),
    (106, "發票處理自動化",             "Invoice Processing Automation",       "finance-trading",     "中級"),
    (107, "個人財務追蹤",               "Personal Finance Tracker",            "finance-trading",     "中級"),

    # --- 健康與個人成長 (108-113) ---
    (108, "睡眠品質優化",               "Sleep Quality Optimizer",             "health-growth",       "中級"),
    (109, "心理健康定期打卡",           "Mental Health Check-In",              "health-growth",       "初中級"),
    (110, "健身打卡問責系統",           "Fitness Accountability System",       "health-growth",       "中級"),
    (111, "個人學習路徑規劃",           "Personal Learning Path Planner",      "health-growth",       "中級"),
    (112, "健身數據彙整分析",           "Fitness Data Aggregation",            "health-growth",       "中級"),
    (113, "採購與營養優化",             "Grocery & Nutrition Optimizer",       "health-growth",       "中級"),

    # --- AI 記憶與代理架構 (114-118) ---
    (114, "三層記憶架構系統",           "Three-Tier Memory Architecture",      "ai-memory-agent",     "高級"),
    (115, "知識圖譜重建",               "Knowledge Graph Reconstruction",      "ai-memory-agent",     "高級"),
    (116, "每週記憶封存",               "Weekly Memory Archive",               "ai-memory-agent",     "中高級"),
    (117, "每日自我提升 Cron",          "Daily Self-Improvement Cron",         "ai-memory-agent",     "中級"),
    (118, "夜間自動化回報追蹤",         "Nightly Automation Report Tracker",   "ai-memory-agent",     "中級"),
]

# ---------------------------------------------------------------------------
# Determine time estimate based on difficulty
# ---------------------------------------------------------------------------
DIFFICULTY_TIME = {
    "初級":   "15-30 分鐘",
    "初中級": "30-45 分鐘",
    "中級":   "45-90 分鐘",
    "中高級": "1-2 小時",
    "高級":   "2-4 小時",
}

# ---------------------------------------------------------------------------
# Template: Main SKILL.md
# ---------------------------------------------------------------------------
def gen_main_skill(num, cn_name, en_name, cat_key, difficulty):
    nnn = f"{num:03d}"
    cat_cn = CATEGORIES[cat_key]
    time_est = DIFFICULTY_TIME.get(difficulty, "45-90 分鐘")

    return f"""---
name: usecase-{nnn}
description: "Use Case #{nnn}: {cn_name} ({en_name}) - TODO: 填入一句話描述。輸入 /usecase-{nnn}/python 或 /usecase-{nnn}/nodejs 選擇方案，/usecase-{nnn}/compare 比較兩方案。"
---

# Use Case #{nnn}: {cn_name} ({en_name})

> 編號: {nnn} / 118 | 分類: {cat_cn} | 難度: {difficulty} | 時間: {time_est}

## 一句話描述

<!-- TODO: 用一句話描述此 use case 的核心功能 -->

## 可用子指令

| 指令 | 說明 |
|------|------|
| `/usecase-{nnn}/python` | Python 完整實作教學 |
| `/usecase-{nnn}/nodejs` | Node.js 完整實作教學 |
| `/usecase-{nnn}/compare` | 兩方案詳細比較 |

## 快速推薦

- **初學者 / 快速原型** → `/usecase-{nnn}/nodejs`
- **正式環境 / 長期穩定** → `/usecase-{nnn}/python`

## 功能需求

<!-- TODO: 列出 4-6 項核心功能需求 -->
1. TODO
2. TODO
3. TODO
4. TODO

## 核心技術棧

<!-- TODO: 列出此 use case 會用到的核心技術 -->
- Anthropic Claude API (AI 核心)
- TODO: 主要資料來源 API
- TODO: 推送/輸出管道
- TODO: 排程/觸發機制

## 成本估算

| 項目 | 費用 |
|------|------|
| Claude API | ~$TODO/月 |
| TODO: 其他服務 | TODO |

## 詳細教學文件

- Python 方案: `/usecase-{nnn}/python`
- Node.js 方案: `/usecase-{nnn}/nodejs`
- 方案比較: `/usecase-{nnn}/compare`
"""


# ---------------------------------------------------------------------------
# Template: Python SKILL.md
# ---------------------------------------------------------------------------
def gen_python_skill(num, cn_name, en_name, cat_key, difficulty):
    nnn = f"{num:03d}"
    time_est = DIFFICULTY_TIME.get(difficulty, "45-90 分鐘")

    return f"""---
name: usecase-{nnn}/python
description: "Use Case #{nnn} Python 方案: {cn_name}。TODO: 填入 Python 方案的一句話描述。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *), Bash(chmod *)
---

# Use Case #{nnn}: {cn_name} -- Python 方案

> 技術棧: Python 3.9+ / TODO: 列出主要套件
> 難度: {difficulty} | 時間: {time_est}

---

## 所需套件

```txt
# TODO: 列出 Python 套件及版本
anthropic==0.43.0        # Claude AI
python-dotenv==1.0.1     # 環境變數管理
```

安裝指令:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 前置準備 Checklist

<!-- TODO: 列出所有必要的前置準備項目 -->
- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] TODO: 其他需要的 API Key / Token

---

## 專案結構

```
usecase-{nnn}/
├── .env                    # 環境變數 (勿 commit)
├── requirements.txt        # Python 依賴
├── run.py                  # 執行入口
└── src/
    ├── __init__.py
    ├── config.py           # 設定管理
    └── main.py             # 主流程
```

<!-- TODO: 根據實際需求調整專案結構 -->

---

## 實作流程 (Step by Step)

### Step 1: 建立專案與環境

```bash
mkdir -p usecase-{nnn}/src
cd usecase-{nnn}
python3 -m venv venv && source venv/bin/activate
```

### Step 2: 設定環境變數

建立 `.env`:
```bash
# Claude
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# TODO: 加入其他環境變數
```

### Step 3: 核心邏輯實作

<!-- TODO: 逐步實作教學 -->

```python
# TODO: 核心程式碼
```

---

## 測試步驟

| 階段 | 測試什麼 | 指令 | 預期結果 |
|------|---------|------|---------|
| 1 | 環境變數 | TODO | 無錯誤 |
| 2 | 核心功能 | TODO | TODO |
| 3 | 完整流程 | `python run.py` | TODO |

---

## 常見陷阱

<!-- TODO: 列出常見問題與解法 -->

| 問題 | 原因 | 解法 |
|------|------|------|
| TODO | TODO | TODO |

---

## 完整參考

<!-- TODO: 加入參考文件連結 -->
"""


# ---------------------------------------------------------------------------
# Template: Node.js SKILL.md
# ---------------------------------------------------------------------------
def gen_nodejs_skill(num, cn_name, en_name, cat_key, difficulty):
    nnn = f"{num:03d}"
    time_est = DIFFICULTY_TIME.get(difficulty, "45-90 分鐘")

    return f"""---
name: usecase-{nnn}/nodejs
description: "Use Case #{nnn} Node.js 方案: {cn_name}。TODO: 填入 Node.js 方案的一句話描述。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *), Bash(touch *), Bash(chmod *)
---

# Use Case #{nnn}: {cn_name} -- Node.js 方案

> 技術棧: Node.js 18+ / TODO: 列出主要套件
> 難度: {difficulty} | 時間: {time_est}

---

## 方案特色

| 優勢 | 說明 |
|------|------|
| TODO | TODO |

---

## 所需套件

```json
{{
  "dependencies": {{
    "@anthropic-ai/sdk": "^0.39.0",
    "dotenv": "^16.4.7"
  }}
}}
```

<!-- TODO: 根據實際需求補充套件 -->

安裝指令:
```bash
mkdir usecase-{nnn} && cd usecase-{nnn}
npm init -y
npm install @anthropic-ai/sdk dotenv
```

---

## 前置準備 Checklist

<!-- TODO: 列出所有必要的前置準備項目 -->
- [ ] Node.js 18+ 已安裝 (`node --version`)
- [ ] Claude API Key (console.anthropic.com)
- [ ] TODO: 其他需要的 API Key / Token

---

## 專案結構

```
usecase-{nnn}/
├── .env                    # 環境變數 (勿 commit)
├── package.json
└── src/
    ├── index.js            # 主程式入口
    └── config.js           # 設定管理
```

<!-- TODO: 根據實際需求調整專案結構 -->

---

## 實作流程 (Step by Step)

### Step 1: 建立專案

```bash
mkdir -p usecase-{nnn}/src
cd usecase-{nnn}
npm init -y
npm install @anthropic-ai/sdk dotenv
```

在 `package.json` 加入 `"type": "module"` 以使用 ES Modules。

### Step 2: 設定環境變數

建立 `.env`:
```bash
# Claude
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# TODO: 加入其他環境變數
```

### Step 3: 核心邏輯實作

<!-- TODO: 逐步實作教學 -->

```javascript
// TODO: 核心程式碼
```

---

## 測試步驟

| 階段 | 測試什麼 | 指令 | 預期結果 |
|------|---------|------|---------|
| 1 | 環境變數 | TODO | 無錯誤 |
| 2 | 核心功能 | TODO | TODO |
| 3 | 完整流程 | `node src/index.js` | TODO |

---

## 常見陷阱

<!-- TODO: 列出常見問題與解法 -->

| 問題 | 原因 | 解法 |
|------|------|------|
| TODO | TODO | TODO |

---

## 完整參考

<!-- TODO: 加入參考文件連結 -->
"""


# ---------------------------------------------------------------------------
# Template: Compare SKILL.md
# ---------------------------------------------------------------------------
def gen_compare_skill(num, cn_name, en_name, cat_key, difficulty):
    nnn = f"{num:03d}"

    return f"""---
name: usecase-{nnn}/compare
description: "Use Case #{nnn} 方案比較: {cn_name}。Python vs Node.js 兩方案的完整對照分析。"
---

# Use Case #{nnn}: {cn_name} -- 方案比較

> 兩方案的完整比較分析。

---

## 總覽比較

| 比較項目 | Python 方案 | Node.js 方案 |
|---------|------------|-------------|
| **語言** | Python 3.9+ | Node.js 18+ |
| **主要套件** | TODO | TODO |
| **AI 引擎** | Anthropic Python SDK | Anthropic JS SDK |
| **排程** | TODO | TODO |

---

## 關鍵差異

### 1. 核心 API 存取

<!-- TODO: 比較兩方案在主要 API 存取方式上的差異 -->

| | Python | Node.js |
|---|--------|---------|
| TODO | TODO | TODO |

### 2. 程式碼架構

<!-- TODO: 比較程式碼架構 -->

| | Python | Node.js |
|---|--------|---------|
| **模組數** | TODO | TODO |
| **程式碼行數** | TODO | TODO |

### 3. 部署與維運

<!-- TODO: 比較部署方式 -->

| | Python | Node.js |
|---|--------|---------|
| TODO | TODO | TODO |

---

## 效能比較

<!-- TODO: 填入效能比較數據 -->

| 指標 | Python | Node.js |
|------|--------|---------|
| TODO | TODO | TODO |

---

## 成本比較

<!-- TODO: 填入成本比較 -->

| 項目 | 費用 |
|------|------|
| TODO | TODO |

---

## 推薦選擇

### 選 Python 如果你...
<!-- TODO: 列出選擇 Python 的理由 -->
- TODO

### 選 Node.js 如果你...
<!-- TODO: 列出選擇 Node.js 的理由 -->
- TODO

### 最終推薦

| 使用場景 | 推薦 |
|---------|------|
| **初學者 / 課程教學** | Node.js |
| **快速原型 / PoC** | Node.js |
| **正式環境 / Production** | Python |

---

## 開始實作

- 選擇 Python → `/usecase-{nnn}/python`
- 選擇 Node.js → `/usecase-{nnn}/nodejs`
- 回到總覽 → `/usecase-{nnn}`
"""


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------
def main():
    # Determine the project root (the repo root, where .claude/ lives)
    script_dir = Path(__file__).resolve().parent
    # Navigate up from scripts/ to repo root
    repo_root = script_dir.parent
    skills_dir = repo_root / ".claude" / "skills"

    print(f"=== Generate Skills for 118 Use Cases ===")
    print(f"Repository root : {repo_root}")
    print(f"Skills directory: {skills_dir}")
    print()

    created_dirs = 0
    created_files = 0
    skipped = 0

    for num, cn_name, en_name, cat_key, difficulty in USE_CASES:
        nnn = f"{num:03d}"
        uc_dir = skills_dir / f"usecase-{nnn}"

        # Skip usecase-001 (already done)
        if num == 1:
            print(f"[SKIP] usecase-{nnn}: {cn_name} ({en_name}) -- already exists")
            skipped += 1
            continue

        print(f"[{nnn}/118] {cn_name} ({en_name}) [{CATEGORIES[cat_key]}]")

        # Create directory structure
        for subdir in ["", "python", "nodejs", "compare"]:
            d = uc_dir / subdir if subdir else uc_dir
            d.mkdir(parents=True, exist_ok=True)
            created_dirs += 1

        # Generate SKILL.md files
        files_to_write = {
            uc_dir / "SKILL.md": gen_main_skill(num, cn_name, en_name, cat_key, difficulty),
            uc_dir / "python" / "SKILL.md": gen_python_skill(num, cn_name, en_name, cat_key, difficulty),
            uc_dir / "nodejs" / "SKILL.md": gen_nodejs_skill(num, cn_name, en_name, cat_key, difficulty),
            uc_dir / "compare" / "SKILL.md": gen_compare_skill(num, cn_name, en_name, cat_key, difficulty),
        }

        for filepath, content in files_to_write.items():
            filepath.write_text(content, encoding="utf-8")
            created_files += 1

        print(f"         -> Created 4 SKILL.md files in usecase-{nnn}/")

    print()
    print(f"=== Summary ===")
    print(f"  Use cases processed: {len(USE_CASES) - skipped}")
    print(f"  Use cases skipped  : {skipped}")
    print(f"  Directories created: {created_dirs}")
    print(f"  Files created      : {created_files}")
    print(f"  Total skill files  : {created_files} ({created_files // 4} use cases x 4 files)")
    print()
    print("Done! All skeleton SKILL.md files have been generated with TODO markers.")


if __name__ == "__main__":
    main()
