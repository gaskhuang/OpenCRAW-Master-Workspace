# Context Flush Checklist

- date: 2026-03-09
- task_state: `/Users/user/memory/TASK_STATE.json`
- daily_note: `/Users/user/memory/2026-03-09.md`

## Current Goal
建立不會忘記上下文的 OpenClaw 工作流，並落地到監控、夜班、長任務、GitHub 同步流程

## Current Workflow
Context Retention Workflow v1

## Active Tasks
- Reddit OpenClaw 監控改為繁中、每 3 小時、全量、排序後回報
- Facebook 社團／粉絲團監控每 3 小時產出繁中結構化摘要
- Facebook 帶圖發文 SOP：以可見圖片預覽作為成功條件
- OpenClaw auto-updater 由阿蓋三號每日 00:00 執行
- 將 compact 前 memory flush / 任務狀態寫盤 / GitHub 同步固化為標準流程

## Blockers
- Facebook composer 上傳圖片成功但未真正綁定到貼文，需以可見預覽驗證
- 部分長任務仍可能因 timeout 中斷，需持續改為背景執行或長 timeout

## Next Actions
- 在 compact 前固定執行 prepare_context_flush.py
- 後續所有 workflow 變更同步寫入 daily note 與必要的長期記憶
- 所有新寫或修改的 md / config 去敏感後同步 GitHub
- 將長任務回報格式統一為 status / why / output / next

## Pre-Compact Check
- [ ] 新偏好是否已寫入 daily note
- [ ] 新規則 / 新 SOP 是否已寫入 daily note / MEMORY
- [ ] 任務狀態變更是否已寫回 TASK_STATE
- [ ] blocker 與 next action 是否明確
- [ ] daily note exists: True

