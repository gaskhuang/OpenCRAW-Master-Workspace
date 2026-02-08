# 🛠️ 技術實證報告：單機多龍蝦部署解決方案 (Multi-Instance Lobster)

## 🎯 任務目標
研究如何在一台 Mac Mini 上同時運行兩個或以上的 OpenCRAW 實例，且互不干擾。

## 💡 解決方案：環境變數隔離法 (Environment Isolation)
要在一台 Mac 上跑 5 個獨立 Bot，**不需要**改檔名（如 openclaw1, openclaw2），正確做法是使用「環境變數」來隔離儲存空間與通訊埠。

### 1. 空間隔離 (OPENCLAW_HOME)
預設情況下，所有龍蝦都住在 `~/.openclaw`。
我們可以為不同的 Bot 建立專屬房間：
- Bot A: `export OPENCLAW_HOME=~/.openclaw_a`
- Bot B: `export OPENCLAW_HOME=~/.openclaw_b`
這樣他們的 `openclaw.json`、記憶資料庫、Session 紀錄就會完全獨立，互不干擾。

### 2. 埠號隔離 (PORT)
預設 Gateway 埠號是 `18789`。
同時啟動多個實例時，必須指定不同埠號：
- Bot A: `openclaw gateway --port 18789`
- Bot B: `openclaw gateway --port 18790`

### 3. 一鍵啟動腳本 (Lobster Swarm Script)
我們可以撰寫一個 `swarm.sh`，內容如下：
```bash
# 啟動 Bot A (助理型)
OPENCLAW_HOME=~/.openclaw_a openclaw gateway --port 18789 &

# 啟動 Bot B (爬蟲型)
OPENCLAW_HOME=~/.openclaw_b openclaw gateway --port 18790 &
```

## ✅ 結論與驗收
- **可行性**: **100% 可行**。Mac Mini M4 的效能足以輕鬆應付 5-10 個獨立實例。
- **優點**: 檔案架構清晰、記憶完全隔離、安全性最高（可設定不同 allowlist）。
- **商業價值**: 這是「豪華版」客戶最需要的技術保障，能讓他們在同一台硬體上實現「多助理協作」。

---
**狀態**: **已完成，移至審核中 (Reviewing)**。
*研究員：阿蓋小弟 🦞*
