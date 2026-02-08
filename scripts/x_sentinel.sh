#!/bin/bash

# ==========================================
# 全能守衛 (Sentinel) - X/Twitter 監控系統
# 邏輯：
# 1. 連線預檢 (Check Browser Relay)
# 2. 失敗熔斷 (Handle Disconnection)
# 3. 時段保護 (HKT 00:00-08:00)
# 4. 資料抓取與過濾 (Browser/Bird -> JSON)
# 5. Kimi k2.5 摘要 -> Telegram 傳送
# ==========================================

STATE_FILE="/Users/user/memory/x_monitoring_state.json"
KW_FILE="/Users/user/memory/x_keywords.txt"

# 建立預設關鍵字 (如果不存在)
if [ ! -f "$KW_FILE" ]; then
    echo "AI agent, OpenClaw, OpenAI, Anthropic, Gemini, Kimi, 科技, 自動化" > "$KW_FILE"
fi

# 初始化狀態 (如果不存在)
if [ ! -f "$STATE_FILE" ]; then
    echo '{"failed_count": 0, "last_ids": [], "disabled": false}' > "$STATE_FILE"
fi

DISABLED=$(jq -r '.disabled' "$STATE_FILE")
if [ "$DISABLED" == "true" ]; then
    # 檢查是否為 08:00 (喚醒時間)，這裡簡易處理，主要靠 Cron 邏輯
    echo "系統已禁用，跳過執行。"
    exit 0
fi

# 1. 時段檢查 (HKT 00:00-08:00)
HOUR=$(date +%H)
if [ "$HOUR" -ge 0 ] && [ "$HOUR" -lt 8 ]; then
    IS_PROTECTION_MODE=true
else
    IS_PROTECTION_MODE=false
fi

# 2. 連線預檢
# 使用 openclaw gateway status 或簡單檢查 bird
bird whoami --timeout 5000 > /dev/null 2>&1
CHECK_STATUS=$?

if [ $CHECK_STATUS -ne 0 ]; then
    # 失敗處理
    FAILED_COUNT=$(jq '.failed_count' "$STATE_FILE")
    NEW_FAILED=$((FAILED_COUNT + 1))
    
    if [ "$NEW_PROTECTION_MODE" == "false" ]; then
        if [ "$NEW_FAILED" -eq 1 ]; then
            # 初次失敗，通知 Telegram
            echo "Boss，連線斷了，請幫我 Attach 瀏覽器。"
        elif [ "$NEW_FAILED" -ge 2 ]; then
            # 連續失敗，熔斷
            jq '.disabled = true' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
            echo "連線持續異常，為了節省資源，我已暫時停止自動監控並停用排程。"
        fi
    fi
    
    # 更新失敗計數
    jq ".failed_count = $NEW_FAILED" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    exit 1
fi

# 歸零失敗計數
jq '.failed_count = 0' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"

# 3. 執行抓取任務
DATE_STR=$(date +%Y-%m-%d)
LOG_DIR="/Users/user/reports/logs/$DATE_STR"
mkdir -p "$LOG_DIR"

# 這裡發送一個系統訊號，讓主模型知道需要啟動 Subagent 進行抓取與存檔
echo "SENTINEL_START_TASK_AND_LOG|$LOG_DIR"
