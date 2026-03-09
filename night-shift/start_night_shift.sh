#!/bin/bash
# 🌙 AI 夜班系統 - 啟動腳本
# 每晚 23:00 由 cron 呼叫，啟動8輪夜班循環

set -e

export PATH="/usr/local/bin:/opt/homebrew/bin:/Users/user/.nvm/versions/node/v24.14.0/bin:/usr/bin:/bin"
export HOME="/Users/user"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_DIR="/Users/user/night-shift/logs"
LOG_FILE="$LOG_DIR/night-shift-${DATE}.log"
PID_FILE="/tmp/night-shift.pid"

# 確保目錄存在
mkdir -p "$LOG_DIR"

# 檢查是否已有夜班在執行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "[$TIME] ⚠️ 夜班已在執行中 (PID: $OLD_PID)，跳過本次啟動" >> "$LOG_FILE"
        exit 0
    fi
fi

echo $$ > "$PID_FILE"

echo "========================================" >> "$LOG_FILE"
echo "🌙 夜班系統啟動 - $DATE $TIME" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 建立當日討論區
discussion_file="/Users/user/night-shift/discussion/collaboration_${DATE}.md"
cat > "$discussion_file" << EOF
# 🌙 夜班討論區 - ${DATE}

> 這是 Tech Lead (J) 和 PM (米米) 的共用工作空間

## 🚀 夜班啟動 - ${TIME}

### J:
夜班開始！今晚的系統狀態正常。
讓我先抓取待辦清單和檢查日誌...

---

EOF

echo "[$TIME] ✅ 討論區建立: $discussion_file" >> "$LOG_FILE"

# 寫入目前 TASK_STATE 快照
python3 /Users/user/night-shift/export_task_state_snapshot.py >> "$LOG_FILE" 2>&1 || true

echo "[$TIME] 🧠 已寫入 TASK_STATE snapshot" >> "$LOG_FILE"

# 初始化安全護欄
touch "/tmp/night-shift-safety-lock"

echo "[$TIME] 🛡️ 安全護欄已啟動" >> "$LOG_FILE"
echo "[$TIME] 📋 開始執行各輪任務..." >> "$LOG_FILE"

# 執行第一輪 (Round 1 - 23:00)
echo "" >> "$LOG_FILE"
echo "--- Round 1 (23:00) ---" >> "$LOG_FILE"
/Users/user/night-shift/round_executor.sh 1 >> "$LOG_FILE" 2>&1 || true

# 後續輪次由 cron 每小時執行
# crontab 設定:
# 0 0,1,2,3,4,5,6 * * * /Users/user/night-shift/round_executor.sh auto

echo "[$TIME] ✅ 首輪完成，後續輪次由 cron 接手" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 清理 PID file
rm -f "$PID_FILE"
