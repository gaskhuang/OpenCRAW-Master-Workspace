# OpenCRAW Skill 獵人計畫 (Skill Hunter Project)

## 🎯 任務目標
建立一套自動化流程，從全球開源社群（X, Reddit, GitHub, MCP Directory）挖掘高效能的 Skill 與 MCP 插件，並由 G大 親自驗證後納入 OpenCRAW 官方技能庫。

## 🛠️ 執行狀態機 (State Machine)
1. **[自動化] 收集 (Collect)**: 每日從網路抓取潛在好用的 Skill 資訊。
2. **[自動化] 預審 (Pre-audit)**: 小弟初步分析該 Skill 的功能、安全性與相容性。
3. **[人工] 驗證 (Verify)**: 由 G大 親自試用並決定是否採納。
4. **[自動化] 歸檔 (Archive)**: 驗證通過後，正式納入「Skill SaaS 同步庫」。

## 📅 排程配置 (Cron Jobs)
- **收集任務**: 每日 08:00 AM 啟動（同步 X Threads Digest）。
- **彙整報告**: 每週日晚間 09:00 PM 生成「本週推薦 Skill 試用報告」。

---
## 📝 待辦事項 (Backlog)
- [ ] 撰寫第一版 `skill_hunter.sh` 腳本，監控 Reddit r/AIAgents 與 GitHub 相關標籤。
- [ ] 在 `sentinel-intelligence-hub` 建立「Skill 推薦專區」。
- [ ] 整合 MCP Directory (https://mcp-directory.com) 的自動抓取。
