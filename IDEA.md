# 執行中項目 (Executing Ideas)

## 🐉 BNI 華資數字追蹤專案 (Hua Tech Tracking)
- **目標**: 自動化追蹤 BNI 華資分會數據，分析 2026-01 起的紅綠燈變化趨勢。
- **阿蓋小弟建議**: 實作 OCR 腳本（使用 Gemini-Flash）解析最新報表圖片並更新 Markdown。
- **分數**: 8/10
- **狀態**: 🚀 處理中 (Moving to In Progress)

## 📑 案例自動化撰寫與發布系統 (Automated Case Study System)
- **目標**: 自動讀取 NAS 照片、GDrive 報價單，生成「蓋斯克風格」案例並發布至 WordPress。
- **阿蓋小弟建議**: 建立「目錄監測器」，偵測到新照片即自動抓取相關 GDrive 檔案並產出草稿。
- **分數**: 9/10
- **狀態**: 🚀 處理中 (Moving to In Progress)

## 🎙️ 連續免提語音交互方案 (Hands-Free Continuous Voice)
- **目標**: 解決開車場景下的「無需點擊」語音對話。
- **阿蓋小弟建議**: 測試 `voice-call` 插件，或實作「iMessage 指令轉接」方案（Hacker News 實測最穩方案）。
- **分數**: 10/10
- **狀態**: 🚀 處理中 (Moving to In Progress)

## 🦞 雙龍蝦 HA 實作部署 (Double Lobster High Availability)
- **目標**: 實作「單機雙實例」架構，確保高可用性。
- **阿蓋小弟建議**: 完善 `swarm.sh` 的健康檢查機制，斷線自動重啟。
- **分數**: 7/10
- **狀態**: 🚀 執行中 (In Progress)

## 📡 OpenCRAW 3小時情報哨兵 (Intelligence Sentinel)
- **目標**: 每 3 小時自動掃描 X/Reddit/Threads。
- **阿蓋小弟建議**: 加入 "Claude Code", "Windsurf" 等熱門 Builder 關鍵字。
- **分數**: 8/10
- **狀態**: 🚀 全自動執行中 (Scheduled)

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
