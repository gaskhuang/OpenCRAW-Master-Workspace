#!/bin/bash

# OpenCRAW 龍蝦記憶體釋放腳本 (Auto Quota & Context Guardian)
# 用途：每 10 分鐘自動監控使用量與對話長度，必要時發起壓縮

# 1. 取得當前 Session 狀態
STATUS=$(openclaw status --json)

# 2. 解析上下文長度 (Context Tokens) 與 使用量 (Quota)
# 這裡模擬邏輯，實際會透過 openclaw 內部 API 觸發
CONTEXT_TOKENS=$(echo $STATUS | jq -r '.session.context.tokens')
QUOTA_USAGE=$(echo $STATUS | jq -r '.usage.primary.percent_used')

echo "當前 Context: $CONTEXT_TOKENS, 使用量: $QUOTA_USAGE%"

# 3. 判斷是否觸發「龍蝦清空」協議 (門檻設為 60%)
if [ "$QUOTA_USAGE" -gt 60 ] || [ "$CONTEXT_TOKENS" -gt 80000 ]; then
    echo "🚨 觸發龍蝦清空協議：正在提煉精華並壓縮對話..."
    
    # 執行精華提煉 (由 agent 內部邏輯處理)
    # 呼叫 openclaw compact 指令
    openclaw compact --force
    
    echo "✅ 記憶體釋放完成，大腦恢復神速！"
else
    echo "🟢 狀態良好，繼續監控。"
fi
