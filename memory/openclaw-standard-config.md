# OpenClaw 標準配置模式（G大專屬）

**建立日期**: 2026-02-05  
**用途**: 模型快速切換系統 + 第二大腦自動歸檔流程  
**適用場景**: 任何新的 OpenClaw 安裝或重置後的快速配置

---

## 🎮 一、快捷指令系統（Shortcuts）

在 `~/.openclaw/openclaw.json` 中加入：

```json
"shortcuts": {
  "g3f": "switch-model google/gemini-3-flash-preview",
  "g3p": "switch-model google/gemini-3-pro-preview",
  "k25": "switch-model moonshot/kimi-k2.5",
  "codex": "switch-model openai/codex",
  "models": "models",
  "status": "status",
  "menu": "menu"
}
```

### Telegram 指令選單註冊
執行以下指令註冊到 Telegram：

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setMyCommands" \
-H "Content-Type: application/json" \
-d '{
  "commands": [
    {"command": "menu", "description": "🎮 呼叫模型切換控制台"},
    {"command": "kanban", "description": "📋 查看我的任務看板"},
    {"command": "g3f", "description": "🚀 切換至 Gemini Flash"},
    {"command": "g3p", "description": "⭐ 切換至 Gemini Pro"},
    {"command": "k25", "description": "🧠 切換至 Kimi k2.5"},
    {"command": "codex", "description": "👨‍💻 切換至 Codex 寫程式"},
    {"command": "status", "description": "📊 查看系統當前狀態"}
  ]
}'
```

---

## 🤖 二、模型配置（Models）

### 必備模型供應商

#### 1. Moonshot (Kimi)
```json
"moonshot": {
  "baseUrl": "https://api.moonshot.ai/v1",
  "apiKey": "sk-...",
  "api": "openai-completions",
  "models": [
    {
      "id": "kimi-k2.5",
      "name": "Kimi K2.5",
      "contextWindow": 256000,
      "maxTokens": 8192
    }
  ]
}
```

#### 2. Google (Gemini)
自動透過系統配置，無需手動設定 API Key。

#### 3. OpenAI (Codex) - 選配
```json
"openai": {
  "baseUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "api": "openai-responses",
  "models": [
    {
      "id": "codex",
      "name": "OpenAI Codex",
      "contextWindow": 200000
    }
  ]
}
```

### 預設模型設定 (多模型分工體系)
```json
"agents": {
  "defaults": {
    "model": {
      "primary": "google-antigravity/gemini-3-flash"
    },
    "models": {
      "google-antigravity/gemini-3-flash": {
        "alias": "gemini-flash"
      },
      "moonshot/kimi-k2.5": {
        "alias": "kimi"
      },
      "openai/codex": {
        "alias": "codex"
      }
    }
  }
}
```
**分工邏輯**:
- **Gemini 3 Flash**: 預設/日常瑣事/視覺辨識
- **Kimi k2.5**: 內容統整/深度分析
- **GPT (Codex)**: 編程/邏輯推理

---

## 🧠 三、第二大腦自動歸檔系統

### 資料夾結構
```
/Users/user/
├── memory/
│   ├── YYYY-MM-DD.md          # 每日日誌
│   └── second_brain.md        # 知識圖片歸檔
├── MEMORY.md                   # 長期記憶總覽
└── Pictures/
    └── AutoGdrive/
        ├── processing/         # 圖片處理中
        └── rename_logic.js     # 自動命名腳本
```

### rclone 雲端同步
```bash
# Google Drive 配置
gdrive:Second_Brain/Images/

# 自動上傳指令
rclone copy "/Users/user/Pictures/AutoGdrive/processing/" gdrive:Second_Brain/Images/
```

### 圖片處理流程
1. 接收圖片 → 2. 視覺分析內容 → 3. 智慧命名 → 4. 上傳雲端 → 5. 寫入 second_brain.md

---

## 🔧 四、核心功能啟用

### Memory Flush（防止失憶）
```json
"compaction": {
  "memoryFlush": {
    "enabled": true
  }
}
```

### Sub-agents 配置
```json
"subagents": {
  "maxConcurrent": 8
}
```

---

## 📱 五、Telegram 互動界面

### 底部快捷鍵盤（Reply Keyboard）
| 按鈕 | 功能 |
|------|------|
| /g3f Gemini Flash | 快速切換 Gemini |
| /k25 Kimi K2.5 | 快速切換 Kimi |
| 🎮 模型控制台 | 呼叫完整控制台 |
| 📊 查看狀態 | 顯示系統資訊 |

### 內聯按鈕控制台（Inline Buttons）
發送帶有按鈕的訊息，點擊即可切換模型。

---

## ⚡ 六、快速部署指令

### 新環境一次性設定
```bash
# 1. 安裝必要工具
brew install rclone

# 2. 設定 rclone
gdrive config

# 3. 建立資料夾
mkdir -p ~/Pictures/AutoGdrive/processing
mkdir -p ~/memory

# 4. 寫入設定檔（複製本文件的 JSON 配置）
# 編輯 ~/.openclaw/openclaw.json

# 5. 註冊 Telegram 指令
# （見上方 curl 指令）

# 6. 重啟 Gateway
openclaw gateway restart
```

---

## 🎯 使用方式總結

| 需求 | 操作方式 |
|------|----------|
| 快速切換模型 | 點擊底部按鈕 或 輸入 /g3f、/k25、/codex |
| 呼叫控制台 | 輸入 /menu 或點擊「🎮 模型控制台」 |
| 查看狀態 | 輸入 /status |
| 上傳圖片到第二大腦 | 直接傳圖片，我會自動處理 |
| 手動同步雲端 | rclone copy ... |

---

**備註**: 此配置為 G大 經過多次優化後的標準工作流，建議新環境直接套用。
