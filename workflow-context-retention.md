# 龍蝦 Context Retention Workflow

目標：把「不會忘記上下文」直接落地到目前 OpenClaw / 夜班 / 監控 / GitHub 同步流程。

## 核心原則

1. **短期上下文只留當前要做事的內容**
2. **任務狀態不要只留在聊天，必須寫入 `memory/TASK_STATE.json`**
3. **重要決策 / 偏好 / 規則先寫入 `memory/YYYY-MM-DD.md`，再 compact**
4. **長任務不要直跑短 timeout，改背景任務 / 長 timeout**
5. **報告類任務先分段整理，再總結，不要一次硬吃全部內容**
6. **所有新寫或修改的 md / config 檔案，去敏感後同步 GitHub**

## 每輪工作流程

### 1. 開始前

- 讀 `memory/TASK_STATE.json`
- 確認目前：
  - current_goal
  - current_workflow
  - active_tasks
  - blockers
  - next_actions

### 2. 執行中

將資訊分三層：

#### A. 短期上下文
- 當前工具輸出
- 頁面 DOM / 臨時 log / 單輪分析
- 不需要持久保存的內容

#### B. 每日記憶 `memory/YYYY-MM-DD.md`
- 新規則
- 當日決策
- 新 workflow
- 成功 / 失敗的關鍵結論
- 值得延續到今天稍後的任務狀態

#### C. 長期記憶 `MEMORY.md`
- 穩定偏好
- 工具分工協議
- SOP / 鐵律
- 已反覆驗證的流程

## Compact 前流程

### 一律先做 pre-compact memory flush

執行：

```bash
python3 /Users/user/scripts/prepare_context_flush.py
```

檢查輸出後，確認以下四件事是否已寫入 daily note：

1. 使用者新偏好
2. 新決策 / 新規則
3. 任務狀態變更
4. blocker 與下一步

然後才 compact。

## 任務狀態機規則

統一使用：`memory/TASK_STATE.json`

必填欄位：
- `current_goal`
- `current_workflow`
- `active_tasks`
- `blockers`
- `next_actions`
- `last_updated`

### 何時更新

- 使用者改優先順序
- 任務切換
- 成功完成一段流程
- 出現 blocker
- 進入新一輪夜班 / cron 交接

## 長任務規則

以下任務視為長任務：
- NotebookLM
- browser automation
- 大型爬站 / 監控
- 圖片批次生成
- 長時間下載 / 轉檔
- 多步驟 GitHub / 報告流程

### 規則
- 不預設走短 timeout
- 優先背景執行 / 長 timeout
- 回報至少包含：
  - 狀態（running / done / blocked）
  - 產出路徑
  - blocker
  - next action

## 報告類任務規則

適用：FB / Reddit / Threads / X / 夜班報告

### 流程
1. 採集原始資料
2. 先整理結構化重點
3. 再生成中文摘要
4. 再輸出 md / html
5. GitHub 同步

### 不可直接做的事
- 一次把全部原始資料直接塞進模型做單次超長總結
- 無來源地虛構摘要
- 沒寫 blocker 就當成功

## Tool 結果整理規則

每個工具結果最少要沉澱成：
- `status`
- `why`
- `output`
- `next`

不要只留下原始 log。

## 阿蓋三號交接規則

凡是定時任務 / 夜班 / 背景監控：
- 必須從 `memory/TASK_STATE.json` 讀目前目標
- 執行後把新 blocker / 新進度寫回 daily note
- 產生 md / config 後同步 GitHub

## 目前先落地的 5 個地方

1. `memory/TASK_STATE.json` 狀態機
2. `memory/YYYY-MM-DD.md` 每日決策存檔
3. `scripts/prepare_context_flush.py` compact 前整理
4. 長任務改 background / 長 timeout 思維
5. md / config → GitHub 同步
