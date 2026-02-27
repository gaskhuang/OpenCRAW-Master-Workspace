# 執行中項目 (Executing Ideas)

## 🐉 BNI 華資數字追蹤專案 (Hua Tech Tracking)
- **目標**: 自動化追蹤 BNI 華資分會數據，分析 2026-01 起的紅綠燈變化趨勢。
- **阿蓋小弟建議**: 實作 OCR 腳本（使用 Gemini-Flash）解析最新報表圖片並更新 Markdown。
- **分數**: 8/10
- **狀態**: 🚀 處理中 (Moving to In Progress)
- **2026-02-24 研究更新**:
  - **最佳模型**: Gemini 2.0 Flash（每美元 ~6,000 頁，最具成本效益）
  - **成本比較**: Gemini 2.0 Flash (~6,000) > AWS Textract (~1,000) > OpenAI 4o (~200)
  - **推薦專案**: alexispurslane/gemini-ocr (含幻覺檢測、Markdown 輸出)
    - GitHub: https://github.com/alexispurslane/gemini-ocr
  - **實測成效**: 處理時間 120x 加速，準確率 96%
- **2026-02-25 研究更新**:
  - **新基準工具**: OmniDocBench - 文檔理解評估基準
    - GitHub: https://github.com/opendatalab/OmniDocBench
  - **最佳組合**: Mistral OCR + Gemini 2.0 Flash 結構化輸出
    - 參考: https://www.philschmid.de/gemini-pdf-to-data

## 📑 案例自動化撰寫與發布系統 (Automated Case Study System)
- **目標**: 自動讀取 NAS 照片、GDrive 報價單，生成「蓋斯克風格」案例並發布至 WordPress。
- **阿蓋小弟建議**: 建立「目錄監測器」，偵測到新照片即自動抓取相關 GDrive 檔案並產出草稿。
- **分數**: 9/10
- **狀態**: 🚀 處理中 (Moving to In Progress)
- **2026-02-24 研究更新**:
  - **NAS 監控**: Python watchdog (即時檔案監控)
  - **WordPress 自動發布**: REST API 優於 XML-RPC
  - **AI 內容生成**: GPT-4 Vision 分析照片 + 模板引擎
  - **參考專案**:
    - GitHub: imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation
    - n8n: Content Farming Workflow (每日自動生成 10 篇文章)
- **2026-02-25 研究更新**:
  - **新發現專案**:
    - AUTO-blogger: https://github.com/AryanVBW/AUTO-blogger
    - AI_Blog_Pipeline: https://github.com/rossautomatedsolutions/AI_Blog_Pipeline
    - CrewAI Blog Automation: https://christianmendieta.ca/crewai-blog-automation

## 🎙️ 連續免提語音交互方案 (Hands-Free Continuous Voice)
- **目標**: 解決開車場景下的「無需點擊」語音對話。
- **阿蓋小弟建議**: 測試 `voice-call` 插件，或實作「iMessage 指令轉接」方案（Hacker News 實測最穩方案）。
- **分數**: 10/10
- **狀態**: 🚀 處理中 (Moving to In Progress)
- **2026-02-24 研究更新**:
  - **方案 A (推薦)**: 電話通話式 AI - LiveKit Telephony + Bolna (完全免手持)
    - GitHub: https://github.com/bolna-ai/bolna
    - LiveKit: https://docs.livekit.io/telephony/
  - **方案 B**: 免手持喚醒詞 - Anachrovox (支援 "Hey Assistant")
    - GitHub: https://github.com/painebenjamin/anachrovox
  - **方案 C**: iMessage 橋接 - Mautrix iMessage
    - GitHub: https://github.com/mautrix/imessage
- **2026-02-25 研究更新**:
  - **喚醒詞方案**: Picovoice Wake Word (2026 完整指南)
    - 來源: https://picovoice.ai/blog/complete-guide-to-wake-word/
  - **裝置端 AI**: Sensory Smart Wake Word
    - 官網: https://sensory.com/product/smart-wake-word/
- **2026-02-26 研究更新** (每日覆盤):
  - **🚗 開車場景最佳組合**: microWakeWord + Speech-to-Phrase + Piper
    - 延遲: <1 秒完整語音循環
    - 完全離線、零 API 費用
    - microWakeWord: https://github.com/OHF-Voice/micro-wake-word
    - Speech-to-Phrase: https://github.com/OHF-Voice/speech-to-phrase
    - Piper: https://github.com/OHF-Voice/piper1-gpl
  - **替代方案 B**: openWakeWord + Faster-Whisper + FishAudio-S1
    - 高品質對話、延遲 1-2 秒
    - openWakeWord: https://github.com/dscripka/openWakeWord
    - Faster-Whisper: https://github.com/SYSTRAN/faster-whisper
    - FishAudio-S1: https://github.com/fishaudio/fish-speech

## 🦞 雙龍蝦 HA 實作部署 (Double Lobster High Availability)
- **目標**: 實作「單機雙實例」架構，確保高可用性。
- **阿蓋小弟建議**: 完善 `swarm.sh` 的健康檢查機制，斷線自動重啟。
- **分數**: 8/10
- **狀態**: 🚀 執行中 (In Progress)
- **2026-02-24 研究更新**:
  - **推薦方案**: Docker Compose + Autoheal (監控並自動重啟不健康容器)
    - GitHub: https://github.com/willfarrell/docker-autoheal
  - **備選方案**: PM2 Cluster 模式 (零停機重載、內建負載均衡)
    - GitHub: https://github.com/vishalm/node-pm2-cluster-example
  - **系統級方案**: Systemd 多實例模板 (agent@.service)
- **2026-02-25 研究更新**:
  - **最新實踐**: Docker Autoheal 無編排設定指南
    - 來源: https://oneuptime.com/blog/post/2026-02-08-how-to-set-up-docker-container-auto-healing
  - **健康檢查最佳實踐**: Docker Unhealthy 狀態處理
    - 來源: https://last9.io/blog/docker-status-unhealthy-how-to-fix-it/
- **2026-02-26 研究更新** (每日覆盤):
  - **🍎 Mac Mini 部署評估**:
    - M4 (16GB): 建議 4-6 實例
    - M4 (24GB+): 可支援 6-10+ 實例
  - **健康檢查實作範例**:
    ```yaml
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:18789/health"]
      interval: 5s
      timeout: 3s
      retries: 3
    ```
  - **參考**: Wyoming Satellite (語音衛星 HA 架構)
    - GitHub: https://github.com/rhasspy/wyoming-satellite

## 📡 OpenCRAW 3小時情報哨兵 (Intelligence Sentinel)
- **目標**: 每 3 小時自動掃描 X/Reddit/Threads。
- **阿蓋小弟建議**: 加入 "Claude Code", "Windsurf" 等熱門 Builder 關鍵字。
- **分數**: 8/10
- **狀態**: 🚀 全自動執行中 (Scheduled)
- **2026-02-24 重要更新**:
  - ⚠️ **Nitter 已停止服務**（2024 年初所有實例憑證過期）
  - **X/Twitter 替代方案**: ntscraper (`pip install ntscraper`)
  - **Reddit**: YARS (無需 API Key) / PRAW
  - **Threads**: Zeeshanahmad4/Threads-Scraper (Playwright)
  - **Claude Code 整合**: zxkane/social-agents (多平台自動化)
- **2026-02-25 研究更新**:
  - **Reddit 爬蟲**: YARS (無需 API Key)
    - GitHub: https://github.com/datavorous/yars
  - **Scrapfly**: 可擴展 Python 網頁爬蟲
    - GitHub: https://github.com/scrapfly/scrapfly-scrapers
  - **X/Twitter 2025 選項**: Reddit DataHoarder 最新討論
    - 來源: https://www.reddit.com/r/DataHoarder/comments/1jx1iea/xtwitter_scraping_options_2025/

---

# 2026-02-28 每日覆盤更新 (Nightly Routine)

## 覆盤報告
- **報告連結**: [sentinel-intelligence-hub/reports/daily_review_2026-02-28.md](./sentinel-intelligence-hub/reports/daily_review_2026-02-28.md)
- **執行狀態**: ✅ 已完成 (00:15 保險重試確認)
- **Git 同步**: ✅ 33 檔案已推送至 Master Repo

## 本日重點發現
1. **OpenClaw Skill 架構研究**：追蹤 mgechev/skills 四驗證 SKILL.md 架構
2. **系統待辦回顧**：Whisper SSL、ClawHub Skills 測試、二腦監控報告待完成
3. **任務評分維持**：免提語音 10/10（最高優先級）、案例自動化 9/10、其餘 8/10
4. **Git 狀態**：大量 X/Threads 監控報告與腳本已同步

## 下步行動（高優先級）
- [ ] 測試 microWakeWord 本地語音組合
- [ ] 建立 NAS 目錄監測器原型
- [ ] 實作 Gemini 2.0 Flash OCR 腳本

---

# 2026-02-27 每日覆盤更新 (Nightly Routine)

## 覆盤報告
- **報告連結**: [sentinel-intelligence-hub/reports/daily_review_2026-02-27.md](./sentinel-intelligence-hub/reports/daily_review_2026-02-27.md)
- **執行狀態**: ✅ 已完成

## 本日重點發現
1. **OpenClaw 企業提示詞架構**：完成 Primary Orchestrator + 8 Subagents 設計
2. **語音方案更新**：確認 microWakeWord + Speech-to-Phrase + Piper 為開車場景最佳組合
3. **任務評分維持**：免提語音 10/10（最高優先級）、案例自動化 9/10、其餘 8/10

## 下步行動（高優先級）
- [ ] 測試 microWakeWord 本地語音組合
- [ ] 建立 NAS 目錄監測器原型
- [ ] 實作 Gemini 2.0 Flash OCR 腳本

---

# 2026-02-07 03:00 AM - X Sentinel Execution Notes

## 執行概況
- **任務名稱**: X_Sentinel_Idea_Execution_3AM
- **監控對象**: X (Twitter) 關鍵字過濾
- **技術手段**: browser 工具 (profile: chrome) + Kimi k2.5 摘要
- **狀態**: 成功執行

## 執行心得
1. **Bird CLI 備援**: 證實了當 Cookie/API 逾時，改用 `browser` 直接模擬人類行為是極為可靠的備援機制。
2. **Kimi k2.5 效能**: 在處理科技類與開源專案內容時，Kimi k2.5 的分類邏輯（區分重點與趨勢）非常精確，能有效排除雜訊（如娛樂八卦趨勢）。
3. **時段優勢**: 凌晨 3 點執行可避免部分網頁載入時的高峰期，資料獲取速度較快。

## 待優化
- 未來可考慮自動截圖存檔至 Google Drive，作為視覺化留存。
- 關鍵字清單可依據每日摘要結果進行動態權重調整。

---

# 2026-02-08 - GSC 報告自動化發想 (G大洗澡中的靈感 🚿)

## 核心概念
- **任務名稱**: GSC_Report_Automation
- **目標**: 每月定期自動抓取 Google Search Console 數據，進行標籤分類並生成專業報告。
- **技術路徑**:
    1. 使用者提供 CSV/Excel 原始數據範本。
    2. 定義關鍵字分類邏輯（如：品牌類 vs 潛在客戶類）。
    3. 模仿使用者過往手動製作的 PDF/網頁報告模板進行自動化排版。
- **狀態**: 等待 G大提供範本數據。

## 生活實境紀錄
- **情境**: G大在洗澡時透過「解放雙手」語音模式下達此指令。
- **亮點**: 驗證了 OpenCRAW 在非辦公場景（如浴室）進行商務規劃的可能性。

---

# 2026-02-08 - 單機多龍蝦部署研究 (Multi-Instance Lobster)

## 核心概念
- **問題**: 如何在一台 Mac Mini 上同時運行兩個（或更多）完全獨立的 OpenCRAW 實例？
- **痛點**: 解決 Port 衝突 (18789)、設定檔隔離 (openclaw.json) 與對話記憶混淆。
- **狀態**: **已完成研究，待 G大 審核 (Reviewing)**。
- **解決方案**: 使用 `OPENCLAW_HOME` 環境變數進行「空間隔離」＋ 指定不同 `PORT` 進行「埠號隔離」。
