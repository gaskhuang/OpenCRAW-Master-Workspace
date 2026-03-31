#!/usr/bin/env python3
"""
從原始 source 檔案提取每個 use case 的：
1. 50 字中文描述
2. 所需 skills / plugins 清單
輸出 JSON 供 index.html 使用
"""

import os
import re
import json
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE, ".claude", "skills")
REPOS_DIR = os.path.join(BASE, "_repos")
OUTPUT = os.path.join(BASE, "scripts", "skills_metadata.json")


def extract_from_source(content):
    """Extract skills/plugins and description from source markdown."""
    skills_tools = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Match skill install patterns
        # openclaw skill install xxx
        m = re.findall(r"openclaw\s+(?:skill|plugins?)\s+install\s+(\S+)", stripped, re.I)
        for s in m:
            skills_tools.append(s.strip("`").strip("'").strip('"'))

        # [skill-name](url) patterns in Skills sections
        m2 = re.findall(r"\[([a-zA-Z0-9_@/-]+)\]\(https?://[^)]+\)\s*(?:skill|plugin)?", stripped)
        for s in m2:
            if len(s) > 2 and s not in ("https", "http", "the", "this"):
                skills_tools.append(s)

        # npx clawhub install xxx
        m3 = re.findall(r"npx\s+clawhub\S*\s+install\s+(\S+)", stripped, re.I)
        for s in m3:
            skills_tools.append(s)

        # MCP server patterns
        if "mcp" in stripped.lower() and ("server" in stripped.lower() or "tool" in stripped.lower()):
            m4 = re.findall(r"`([a-zA-Z0-9_-]+)`", stripped)
            for s in m4:
                if len(s) > 3:
                    skills_tools.append(f"mcp:{s}")

        # Brave search, web-fetch, etc.
        m5 = re.findall(r"(?:skill|tool|plugin)s?\s*(?:install|:)\s*[`'\"]?([a-zA-Z0-9_-]+)", stripped, re.I)
        for s in m5:
            if len(s) > 2 and s.lower() not in ("the", "install", "and", "or", "you", "need", "required", "needed"):
                skills_tools.append(s)

    # Deduplicate and clean
    seen = set()
    clean = []
    for s in skills_tools:
        s = s.strip("`").strip("'").strip('"').strip(",").strip(".")
        if s.lower() in seen or len(s) < 2:
            continue
        # Filter out common false positives
        if s.lower() in ("bash", "read", "grep", "glob", "step", "the", "for", "use", "set", "get", "run", "add",
                          "you", "your", "this", "that", "with", "from", "install", "skill", "plugin", "tool",
                          "setup", "create", "build", "start", "config", "check", "test", "main"):
            continue
        seen.add(s.lower())
        clean.append(s)

    return clean[:8]  # Max 8 items


def get_source_content(skill_name):
    """Try to find source content for a skill."""
    # Check python SKILL.md for embedded source
    py_md = os.path.join(SKILLS_DIR, skill_name, "python", "SKILL.md")
    if os.path.exists(py_md):
        with open(py_md, encoding="utf-8") as f:
            return f.read()
    # Check main SKILL.md
    main_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if os.path.exists(main_md):
        with open(main_md, encoding="utf-8") as f:
            return f.read()
    return ""


# Hardcoded descriptions and skills for all use cases
# Format: id -> (description_zh, [skills/plugins])
DESCRIPTIONS = {
    1: ("每天自動抓取 Reddit 熱門貼文，用 AI 摘要重點，透過 Telegram 推送個人化每日精華。", ["reddit-readonly", "brave-search"]),
    2: ("自動擷取 YouTube 訂閱頻道最新影片，AI 生成摘要與重點，每日推送到 Telegram。", ["youtube-mcp", "brave-search"]),
    3: ("分析 X/Twitter 帳號的發文風格、互動模式、受眾特徵，產出質性研究報告。", ["twitter-mcp", "brave-search"]),
    4: ("聚合多個 RSS 源與新聞網站，AI 篩選並摘要科技新聞，每日生成個人化科技簡報。", ["brave-search", "web-fetch"]),
    5: ("監控品牌在社群媒體的提及、情緒趨勢和競爭對手動態，產出每週聲量分析報告。", ["twitter-mcp", "brave-search", "web-fetch"]),
    6: ("根據排程自動在多個社群平台發布內容，支援圖文、時間最佳化和跨平台管理。", ["twitter-mcp", "buffer-api"]),
    7: ("管理 Instagram 限時動態的排程、設計、互動回覆和成效分析，自動化日常運營。", ["instagram-api", "image-gen"]),
    8: ("追蹤 Reddit 上產品相關討論，分析用戶反饋和市場需求信號，生成產品洞察報告。", ["reddit-readonly", "brave-search"]),
    9: ("自動管理 X/Twitter 的互動、回覆、追蹤者分析和內容排程，提升社群經營效率。", ["twitter-mcp", "brave-search"]),
    10: ("將長期目標拆解為每日可執行任務，代理根據進度自動調整計畫並追蹤完成率。", ["todoist-mcp", "google-calendar"]),
    11: ("自動化 YouTube 內容製作流程：腳本撰寫、SEO 優化、縮圖建議、排程發布。", ["youtube-mcp", "brave-search", "image-gen"]),
    12: ("多個 AI 代理協作產出內容：研究員蒐集資料、寫手撰文、編輯校對、SEO 優化。", ["brave-search", "web-fetch"]),
    13: ("AI 代理自主開發遊戲：從概念設計到程式碼生成、測試、迭代，全流程自動化。", ["filesystem", "code-runner"]),
    14: ("自動化 Podcast 製作：音訊轉文字、段落編輯、節目筆記生成、平台上傳分發。", ["whisper-api", "rss-feed"]),
    15: ("將訂閱的電子報自動轉換為 Podcast 音訊，通勤時用聽的方式消化資訊。", ["email-reader", "tts-api"]),
    16: ("AI 寫作助手：從空白頁到完稿，協助研究、起草、編輯、SEO 優化和排版發布。", ["brave-search", "gsc", "ghost"]),
    17: ("一篇文章自動改寫為多平台格式：Twitter 串文、LinkedIn 貼文、IG 圖文、短影音腳本。", ["twitter-mcp", "linkedin-api"]),
    18: ("自動搜尋學術文獻、整理引用、摘要論文重點、追蹤研究領域最新動態。", ["arxiv-reader", "brave-search", "web-fetch"]),
    19: ("透過 Telegram 訊息控制智慧家居設備：燈光、溫度、家電開關、場景切換。", ["telegram-bot", "home-assistant"]),
    20: ("AI 規劃旅行行程：目的地研究、交通住宿比價、景點安排、預算控管、行程表生成。", ["brave-search", "google-maps", "booking-api"]),
    21: ("自動比較多個平台的商品價格，追蹤降價通知，找出最佳購買時機和優惠組合。", ["brave-search", "web-fetch"]),
    22: ("根據天氣預報和個人衣櫥，每天自動推薦穿搭組合，支援不同場合的穿衣建議。", ["weather-api", "web-fetch"]),
    23: ("管理重要日期清單，自動在生日前生成個人化祝福訊息並透過指定管道發送。", ["google-calendar", "telegram-bot"]),
    24: ("自動處理餐廳訂位、服務預約，根據偏好和可用時段進行反覆確認和調整。", ["web-fetch", "google-calendar"]),
    25: ("智能管理閱讀清單：自動摘要待讀文章、優先排序、追蹤閱讀進度、定期清理。", ["web-fetch", "pocket-api"]),
    26: ("根據冰箱食材、營養需求和口味偏好，推薦食譜並自動生成購物清單。", ["brave-search", "web-fetch"]),
    27: ("AI 輔導老師，耐心引導孩子解題，用蘇格拉底式提問培養獨立思考能力。", ["anthropic-sdk"]),
    28: ("每日自動記錄學習內容、反思心得、追蹤知識成長曲線，建立個人學習歷程檔案。", ["filesystem", "todoist-mcp"]),
    29: ("AI 代理自主管理複雜專案：分配任務、追蹤進度、偵測風險、產出進度報告。", ["github-mcp", "todoist-mcp", "slack"]),
    30: ("多通道 AI 客服：同時處理 Email、Telegram、網頁聊天，統一知識庫和回覆風格。", ["telegram-bot", "email-reader"]),
    31: ("透過電話語音與 AI 助理對話，處理行程安排、資訊查詢、任務管理等日常需求。", ["twilio-api", "whisper-api"]),
    32: ("自動清理收件匣：退訂無用電子報、分類郵件、標記重要信件、批量歸檔處理。", ["email-reader", "gmail-api"]),
    33: ("AI 管理人脈關係：自動記錄聯繫人資訊、追蹤互動歷史、提醒跟進時機。", ["google-contacts", "google-calendar"]),
    34: ("追蹤身體症狀、飲食和生活習慣的關聯性，識別觸發因素，產出健康趨勢報告。", ["health-api", "filesystem"]),
    35: ("跨 Email、Telegram、Slack 等多通道的統一 AI 助理，保持上下文一致性。", ["telegram-bot", "slack", "email-reader"]),
    36: ("事件驅動的專案狀態管理：當代碼合併、Issue 更新時，自動更新看板和通知相關人。", ["github-mcp", "todoist-mcp"]),
    37: ("自動生成和更新即時數據儀表板：拉取 API 數據、計算指標、渲染圖表。", ["web-fetch", "filesystem"]),
    38: ("Todoist 任務管理透明化：AI 代理直接操作任務清單，優先排序和自動整理。", ["todoist-mcp"]),
    39: ("管理全家人的行事曆和家務分工：協調時間衝突、分配任務、發送提醒。", ["google-calendar", "todoist-mcp"]),
    40: ("多個專業 AI 代理組成虛擬團隊：產品經理、工程師、設計師、行銷，協作完成任務。", ["filesystem", "web-fetch"]),
    41: ("每天早上生成個人化簡報：天氣、行程、新聞、待辦事項、重要提醒一次掌握。", ["weather-api", "google-calendar", "brave-search"]),
    42: ("自動將會議錄音轉為文字紀錄，提取行動項目，分配給負責人並追蹤完成進度。", ["whisper-api", "todoist-mcp"]),
    43: ("追蹤每日習慣完成情況，AI 教練分析趨勢、提供建議、問責催促。", ["todoist-mcp", "telegram-bot"]),
    44: ("自動捕捉想法、整理知識、建立連結，打造個人知識管理的第二大腦系統。", ["filesystem", "web-fetch"]),
    45: ("自動打電話確認活動賓客出席狀況，記錄回覆，更新賓客名單和座位安排。", ["twilio-api", "google-sheets"]),
    46: ("AI 自動分類和優先排序收件匣郵件，依據內容標記標籤、設定提醒、歸檔處理。", ["gmail-api", "email-reader"]),
    47: ("將語音備忘錄自動轉為結構化任務和日記條目，支援通勤中隨時語音輸入。", ["whisper-api", "todoist-mcp"]),
    48: ("自動閱讀長篇 PDF 文件，提取重點摘要、關鍵數據、結論，支援批量處理。", ["pdf-reader", "filesystem"]),
    49: ("每天早上自動準備會議簡報：參會者背景、議程重點、相關文件、建議提問。", ["google-calendar", "brave-search", "web-fetch"]),
    50: ("智慧解決行事曆衝突：分析會議優先級、建議替代時段、自動協調多方時間。", ["google-calendar"]),
    51: ("自動整理 Trello/看板上的過期卡片、更新標籤、歸檔完成項目、平衡工作量。", ["trello-api", "todoist-mcp"]),
    52: ("自動追蹤包裹物流狀態，整合多個快遞平台，異常時即時推送通知。", ["web-fetch", "telegram-bot"]),
    53: ("非同步每日站會：AI 收集團隊成員進度更新，彙整報告，標記阻塞項目。", ["slack", "todoist-mcp"]),
    54: ("AI 自動協調多方會議時間：分析各方可用時段，提出最佳選項，發送邀請。", ["google-calendar"]),
    55: ("追蹤競爭對手的產品更新、定價變化、市場策略，每週生成競爭情報報告。", ["brave-search", "web-fetch"]),
    56: ("即時追蹤競品在各平台的定價變化，分析價格趨勢，建議最佳定價策略。", ["web-fetch", "brave-search"]),
    57: ("監控社群媒體和評論網站的競品評價，分析情緒趨勢和用戶痛點。", ["twitter-mcp", "brave-search"]),
    58: ("自動化大規模 SEO 頁面生成：關鍵字研究、內容模板、批量產出、排名追蹤。", ["gsc", "brave-search", "web-fetch"]),
    59: ("監控 HARO 記者需求，自動匹配專業背景，草擬高品質回覆以獲取外鏈。", ["email-reader", "brave-search"]),
    60: ("自動豐富潛在客戶資料：抓取公司資訊、社群動態、技術棧，產出銷售情報卡。", ["brave-search", "web-fetch", "linkedin-api"]),
    61: ("大規模個人化冷外聯：根據收件人背景自動客製化郵件內容，追蹤開信率。", ["email-sender", "brave-search"]),
    62: ("自動追蹤和分析廣告平台效益數據，生成每日績效報告和優化建議。", ["google-ads", "facebook-ads"]),
    63: ("每週自動彙整業務數據、市場動態、團隊進展，生成結構化策略備忘錄。", ["brave-search", "web-fetch"]),
    64: ("自動在 Upwork、Freelancer 等平台搜尋匹配案件，篩選評估並草擬提案。", ["web-fetch", "brave-search"]),
    65: ("自動發掘符合品牌調性的網紅，分析粉絲數據和合作效益，草擬外聯信件。", ["twitter-mcp", "brave-search", "web-fetch"]),
    66: ("銷售電話前自動準備客戶研究報告：公司背景、決策者資訊、痛點分析、話術建議。", ["brave-search", "web-fetch", "linkedin-api"]),
    67: ("自動追蹤和管理產品評論：分類回覆建議、情緒分析、趨勢報告、競品對比。", ["brave-search", "web-fetch"]),
    68: ("自動生成廣告創意變體，A/B 測試不同版本，分析點擊率和轉換數據。", ["web-fetch", "image-gen"]),
    69: ("用 n8n 編排複雜工作流程：串接多個 API、條件分支、錯誤處理、排程執行。", ["n8n-api", "web-fetch"]),
    70: ("家庭伺服器自動故障偵測與修復：服務監控、日誌分析、自動重啟、告警通知。", ["ssh-tool", "telegram-bot"]),
    71: ("自動追蹤 GitHub PR 狀態：偵測過期 PR、未審核代碼、合併衝突，推送提醒。", ["github-mcp"]),
    72: ("自動偵測和修復 CI 中的不穩定測試：分析失敗模式、隔離 Flaky Test、建議修復。", ["github-mcp", "filesystem"]),
    73: ("夜間自動檢查文檔問題：壞連結、過時程式碼範例、格式錯誤，並提交修復 PR。", ["github-mcp", "web-fetch"]),
    74: ("從 Git 提交記錄自動生成結構化變更日誌，分類功能、修復、破壞性變更。", ["github-mcp"]),
    75: ("掃描專案依賴的安全漏洞和過期版本，產出風險評估報告和升級建議。", ["github-mcp", "npm-audit"]),
    76: ("分析 Sentry 錯誤報告，自動歸類問題根因、影響範圍，生成事故回顧文件。", ["sentry-api", "github-mcp"]),
    77: ("自動化部署流水線：環境檢查、測試執行、灰度發布、回滾準備、狀態通知。", ["github-mcp", "ssh-tool"]),
    78: ("掃描程式碼庫，自動為函數和模組生成文檔註解，保持文檔與代碼同步。", ["github-mcp", "filesystem"]),
    79: ("掃描系統中的 SSH 金鑰：檢查強度、過期時間、權限設定，產出安全報告。", ["ssh-tool", "filesystem"]),
    80: ("掃描 AWS 憑證安全性：檢查金鑰強度、輪換狀態、權限過度授予，產出合規報告。", ["aws-cli", "filesystem"]),
    81: ("掃描 Git 歷史中洩露的密碼、API 金鑰等敏感資訊，並安全地清理歷史紀錄。", ["github-mcp", "filesystem"]),
    82: ("自動化 API 安全測試：注入攻擊、認證繞過、速率限制檢查，產出漏洞報告。", ["web-fetch", "filesystem"]),
    83: ("掃描系統和應用的已知漏洞，比對 CVE 資料庫，產出修補優先級建議。", ["web-fetch", "filesystem"]),
    84: ("檢查系統和流程的法規合規性（GDPR、SOC2 等），產出差距分析和修正建議。", ["filesystem", "web-fetch"]),
    85: ("監控系統心跳狀態，確保各組件正常運行，故障時自動告警並嘗試修復。", ["web-fetch", "telegram-bot"]),
    86: ("持續監控網站可用性和回應時間，異常時即時通知並記錄停機歷史。", ["web-fetch", "telegram-bot"]),
    87: ("監控 SSL 憑證到期時間，在過期前提前告警，自動提醒更新或觸發續期流程。", ["ssl-checker", "telegram-bot"]),
    88: ("自動化資料庫備份流程：定期備份、驗證完整性、管理存儲空間、異地備份。", ["ssh-tool", "filesystem"]),
    89: ("追蹤 AI 服務的 API 使用量和費用，預測月底開支，在超額前發出預警。", ["web-fetch", "filesystem"]),
    90: ("彙整每週安全事件摘要：嚴重程度分類、根因分析、修復進度、趨勢圖表。", ["sentry-api", "github-mcp"]),
    91: ("監控 API 速率限制使用情況，預警接近上限，建議限流策略和升級方案。", ["web-fetch", "filesystem"]),
    92: ("智能聚合和去重告警訊息，減少告警風暴，合併相關事件，降低噪音。", ["telegram-bot", "web-fetch"]),
    93: ("追蹤公司財報發布和關鍵財務指標，自動生成投資分析摘要和市場影響評估。", ["brave-search", "web-fetch"]),
    94: ("建立個人知識庫，支援語義搜尋和 RAG 檢索，讓 AI 基於你的知識回答問題。", ["filesystem", "embeddings-api"]),
    95: ("自動化市場調研和 MVP 驗證：競品分析、用戶訪談、原型設計、快速迭代。", ["brave-search", "web-fetch"]),
    96: ("在開始開發前驗證創意可行性：市場需求分析、技術可行性、成本估算。", ["brave-search", "web-fetch"]),
    97: ("基於語義理解搜尋代理記憶，找到相關的過往對話、決策和上下文。", ["filesystem", "embeddings-api"]),
    98: ("自動監控 YouTube 頻道數據，分析觀看趨勢、觀眾行為，產出內容策略報告。", ["youtube-mcp", "brave-search"]),
    99: ("聚合多個 RSS 源，AI 篩選和摘要新聞，生成個人化每週研究情報簡報。", ["brave-search", "web-fetch", "rss-feed"]),
    100: ("自動挖掘內容靈感：監控熱門話題、分析競品內容、識別未被覆蓋的主題缺口。", ["brave-search", "twitter-mcp", "web-fetch"]),
    101: ("根據需求討論自動生成結構化 PRD 文件：用戶故事、功能規格、驗收標準。", ["filesystem"]),
    102: ("自動監控 Polymarket 預測市場，分析賠率變化，根據策略執行交易。", ["web-fetch", "polymarket-api"]),
    103: ("自動化處理入站投資案：篩選項目、提取關鍵資訊、安排評估流程、追蹤進度。", ["brave-search", "web-fetch"]),
    104: ("自動監控投資組合公司的關鍵指標、新聞動態、里程碑事件，產出組合報告。", ["brave-search", "web-fetch"]),
    105: ("掃描所有訂閱服務和定期付費，分析使用率，識別浪費並建議取消或降級。", ["email-reader", "web-fetch"]),
    106: ("自動處理發票：OCR 辨識、資料提取、分類記帳、審核異常、催款提醒。", ["pdf-reader", "filesystem"]),
    107: ("追蹤個人收支、預算執行情況，分析消費模式，產出月度財務健康報告。", ["filesystem"]),
    108: ("追蹤睡眠數據，分析影響因素，提供個人化改善建議，優化睡眠品質。", ["health-api", "filesystem"]),
    109: ("定期心理健康檢查：情緒追蹤、壓力評估、正念建議、趨勢分析。", ["filesystem", "telegram-bot"]),
    110: ("追蹤健身計畫執行情況，AI 教練分析表現、調整訓練強度、問責鼓勵。", ["filesystem", "telegram-bot"]),
    111: ("根據學習目標自動規劃個人化學習路徑：課程推薦、進度追蹤、知識檢測。", ["brave-search", "web-fetch"]),
    112: ("聚合多來源健身數據（Apple Watch、Strava 等），分析訓練趨勢和恢復狀態。", ["health-api", "filesystem"]),
    113: ("根據營養目標和預算規劃每週餐單，自動生成最優化購物清單和採購建議。", ["brave-search", "web-fetch"]),
    114: ("三層記憶架構：短期工作記憶、中期情境記憶、長期知識記憶，優化代理記憶管理。", ["filesystem"]),
    115: ("重建和優化知識圖譜，發現知識關聯，填補知識缺口，增強語義理解能力。", ["filesystem", "embeddings-api"]),
    116: ("每週自動歸檔代理記憶，整理歷史紀錄，優化存儲空間，保留關鍵上下文。", ["filesystem"]),
    117: ("每日生成個人化自我提升建議：學習資源、習慣優化、技能發展計畫。", ["brave-search", "filesystem"]),
    118: ("追蹤夜間自動化任務的執行結果，計算投入產出比，優化任務排程策略。", ["filesystem", "telegram-bot"]),
    119: ("使用 AI 代理協作撰寫 LaTeX 論文，即時編譯為 PDF，支援多種模板和參考文獻。", ["latex-compiler", "pdf-reader"]),
    120: ("一鍵安裝本地 CRM 系統，用自然語言管理客戶、銷售管道、看板和行銷自動化。", ["denchclaw", "duckdb"]),
    121: ("透過聊天完全控制 X/Twitter：發推、回覆、按讚、轉推、抽獎、帳號監控。", ["@xquik/tweetclaw"]),
    122: ("對話式閱讀 arXiv 論文：自動擷取 LaTeX 原始碼，解析章節，比較多篇論文。", ["arxiv-reader"]),
    123: ("自動生成合作夥伴進展報告：整合專案狀態、里程碑、共享指標和後續行動。", ["brave-search", "web-fetch"]),
    124: ("自動分類和優先排序功能需求：分析用戶投票、商業價值、技術複雜度。", ["github-mcp", "todoist-mcp"]),
    125: ("驗證文檔中的程式碼片段是否可正確執行，自動修復過時的範例代碼。", ["github-mcp", "filesystem"]),
    126: ("監控 AI Prompt 的輸出品質，偵測回歸問題，追蹤不同版本的效果差異。", ["filesystem", "anthropic-sdk"]),
    127: ("分析客戶續約風險因素：使用頻率下降、支援單增加、競品動態，產出預警報告。", ["web-fetch", "filesystem"]),
    128: ("追蹤試用用戶行為，識別轉換信號，在最佳時機推送個人化付費升級提醒。", ["web-fetch", "email-sender"]),
    129: ("自動路由和追蹤超出標準審批流程的例外請求，記錄決策理由和批准歷史。", ["todoist-mcp", "email-reader"]),
    130: ("自動接收、分類和分派行銷素材製作請求，追蹤進度，確保按時交付。", ["todoist-mcp", "slack"]),
    131: ("自動彙整多輪面試官的評價回饋，整理成結構化報告供 Hiring Manager 決策。", ["filesystem", "email-reader"]),
    132: ("管理新員工入職清單：追蹤各部門任務完成進度，自動提醒待處理項目。", ["todoist-mcp", "slack"]),
    133: ("自動評估採購申請：供應商信譽、價格合理性、預算匹配度、歷史記錄比對。", ["web-fetch", "filesystem"]),
    134: ("追蹤逾期採購訂單，自動發送催款提醒，升級未回應案件，產出逾期報告。", ["email-sender", "filesystem"]),
    135: ("偵測組織中未經授權使用的 AI 工具，評估風險，產出合規建議和治理方案。", ["brave-search", "web-fetch"]),
    136: ("自動分類和優先排序設備問題報告，根據嚴重程度分派處理人員，追蹤修復進度。", ["todoist-mcp", "email-reader"]),
    137: ("智能路由內部常見問題：分析問題意圖，匹配知識庫答案，無法回答時轉派專人。", ["filesystem", "embeddings-api"]),
    138: ("每日自動彙整奧運賽事結果、獎牌榜、精彩時刻，生成個人化奧運日報。", ["brave-search", "web-fetch"]),
    139: ("每天清晨自動抓取天氣數據，生成包含穿衣建議和通勤提醒的晨間天氣報告。", ["weather-api", "telegram-bot"]),
    140: ("夜間自動分析 Shell 使用習慣，建議並創建實用的命令別名，提升終端效率。", ["filesystem"]),
    141: ("監控交易機器人運行狀態：追蹤訂單執行、盈虧計算、異常偵測、風險告警。", ["web-fetch", "telegram-bot"]),
    142: ("自動分析 GitHub Issue 的優先級：影響範圍、用戶數量、修復複雜度排序。", ["github-mcp"]),
    143: ("自動為個人打造客製化 CLI 工具包：常用命令封裝、智慧補全、工作流腳本。", ["filesystem"]),
    144: ("自動管理 Uniswap V4 流動性部位：監控價格範圍、自動複利收益、調整策略。", ["web3-api", "web-fetch"]),
    145: ("七個子代理夜間並行執行不同任務，最大化利用離峰時間完成批量工作。", ["filesystem"]),
    146: ("凌晨 5 點自動執行基礎設施全面健檢：服務狀態、磁碟空間、SSL、DNS 檢查。", ["ssh-tool", "web-fetch", "ssl-checker"]),
    147: ("夜間自動在 WhatsApp 發送關懷訊息給冷聯繫人，維護長期人脈關係。", ["whatsapp-api"]),
    148: ("將文字或數據銘刻到比特幣區塊鏈上，創建永久不可竄改的鏈上記錄。", ["bitcoin-rpc", "web-fetch"]),
    149: ("自動清理 GitHub 上長期未活動的 Issue：標記、通知、關閉過期問題。", ["github-mcp"]),
    150: ("自動分析系統日誌，使用 AI 偵測異常模式，提前預警潛在問題。", ["filesystem", "ssh-tool"]),
    151: ("監控區塊鏈錢包餘額和交易活動，大額轉帳即時告警，追蹤 DeFi 部位。", ["web3-api", "web-fetch"]),
    152: ("掃描客戶在社群、論壇、評論中的購買信號，及時識別銷售機會。", ["brave-search", "twitter-mcp", "web-fetch"]),
    153: ("監控 Pump.fun 平台的新代幣上線，分析流動性和風險指標，即時推送通知。", ["web-fetch", "telegram-bot"]),
    154: ("分析 Moltbook 代理的執行模式，識別效率瓶頸和優化機會，提升任務成功率。", ["filesystem"]),
    155: ("定期執行網路延遲基準測試，追蹤不同節點和路由的效能趨勢。", ["web-fetch", "filesystem"]),
    156: ("分析和優化 AI API 的 Token 使用量，減少不必要消耗，降低 API 費用。", ["filesystem", "anthropic-sdk"]),
    157: ("執行分散式追蹤基準測試，分析跨服務請求的延遲分佈和瓶頸位置。", ["web-fetch", "filesystem"]),
    158: ("測試 macOS 鑰匙圈的存取權限和安全性，檢查已存儲的憑證強度。", ["filesystem"]),
    159: ("審計 OpenClaw Skill 的依賴鏈安全性，檢查是否有已知漏洞或惡意套件。", ["npm-audit", "github-mcp"]),
    160: ("在安裝 Skill 前自動執行預檢：權限檢查、依賴衝突、安全掃描、相容性驗證。", ["filesystem"]),
    161: ("自動生成 Cron 任務執行狀態儀表板：成功率、執行時間、錯誤日誌、趨勢圖。", ["filesystem"]),
    162: ("監控多個服務的心跳信號，偵測異常中斷，自動重啟失敗服務並通知運維。", ["web-fetch", "ssh-tool", "telegram-bot"]),
    163: ("自動生成 Swift Logger 套件：日誌格式化、等級過濾、檔案輸出、遠端傳送。", ["filesystem"]),
    164: ("記錄所有敏感操作的審計日誌，確保可追溯性，支援合規審查和事故調查。", ["filesystem"]),
    165: ("自動生成資安 CTF 挑戰課程：漏洞情境設計、練習題目、解題指引、評分系統。", ["filesystem", "web-fetch"]),
    166: ("將俳句詩作銘刻到區塊鏈上，創建獨特的鏈上數位藝術作品。", ["bitcoin-rpc", "web-fetch"]),
    167: ("每天清晨自動彙整多來源資訊，生成包含新聞、行程、待辦的個人化晨間摘要。", ["brave-search", "google-calendar", "weather-api"]),
    168: ("結合加密貨幣市場數據生成趣味幸運餅乾訊息，附帶投資小知識。", ["web-fetch"]),
    169: ("自動建立和維護 Agent Skill 目錄：分類整理、搜尋索引、版本追蹤、使用統計。", ["filesystem", "github-mcp"]),
    170: ("追蹤夜間自動化任務的 ROI：計算節省時間、成本效益、任務成功率趨勢。", ["filesystem"]),
    171: ("在多個通訊平台（Slack、Telegram、Discord）同步在線狀態和自動回覆設定。", ["slack", "telegram-bot"]),
    172: ("自動排程關懷訊息給長時間未聯繫的人脈，維護和復活冷淡的社交關係。", ["telegram-bot", "google-contacts"]),
    173: ("AI 增強版行事曆提醒：根據會議重要性、準備需求和交通時間智慧調整提醒時機。", ["google-calendar"]),
    174: ("自動記錄生活中的重要時刻、想法和感悟，建立可搜尋的個人生命歷程記錄。", ["filesystem"]),
}


def parse_skills():
    skills = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        if name == "usecase-index":
            continue
        skill_md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
        with open(skill_md, encoding="utf-8") as f:
            content = f.read(2000)

        m = re.search(r"#(\d{3})", content)
        num = int(m.group(1)) if m else 0

        m2 = re.search(r"分類:\s*(.+?)\s*\|", content)
        cat = m2.group(1).strip() if m2 else "其他"

        m4 = re.search(r"難度:\s*(\S+)", content)
        diff = m4.group(1).strip() if m4 else "中級"

        m5 = re.match(r"(.+?)\s*\((.+?)\)", name)
        if m5:
            name_zh = m5.group(1)
            name_en = m5.group(2)
        else:
            name_zh = name
            name_en = name

        m6 = re.search(r"`(\w+)`:\s*`(.+?)`", content)
        source = m6.group(1) if m6 else ""

        # Get description and tools from our hardcoded data
        desc_data = DESCRIPTIONS.get(num, ("", []))
        description = desc_data[0]
        tools = desc_data[1]

        # If not in hardcoded, try to extract from source
        if not description:
            desc_match = re.search(r"一句話描述.*?>\s*(.+)", content, re.S)
            description = desc_match.group(1).strip() if desc_match else ""

        if not tools:
            source_content = get_source_content(name)
            tools = extract_from_source(source_content)

        skills.append({
            "id": num,
            "name": name,
            "name_zh": name_zh,
            "name_en": name_en,
            "category": cat,
            "description": description,
            "difficulty": diff,
            "source": source,
            "tools": tools,
        })

    skills.sort(key=lambda s: s["id"])
    return skills


def main():
    print("Parsing skills...")
    skills = parse_skills()
    print(f"Found {len(skills)} skills")

    with_desc = sum(1 for s in skills if s["description"])
    with_tools = sum(1 for s in skills if s["tools"])
    print(f"With descriptions: {with_desc}")
    print(f"With tools/skills: {with_tools}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
