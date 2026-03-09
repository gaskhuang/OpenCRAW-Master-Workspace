#!/bin/bash
set -euo pipefail

export PATH="/Users/user/.local/bin:/Users/user/.npm-global/bin:/Users/user/bin:/Users/user/.volta/bin:/Users/user/.asdf/shims:/Users/user/.bun/bin:/Users/user/Library/Application Support/fnm/aliases/default/bin:/Users/user/.fnm/aliases/default/bin:/Users/user/Library/pnpm:/Users/user/.local/share/pnpm:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/user"

WORKSPACE="/Users/user"
LOG_FILE="$WORKSPACE/openclaw_memory_guard.log"
FLUSH_SCRIPT="$WORKSPACE/scripts/prepare_context_flush.py"
TODAY=$(date '+%Y-%m-%d')
FLUSH_REPORT="$WORKSPACE/reports/context-flush/context-flush-$TODAY.md"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" | tee -a "$LOG_FILE"
}

log "Lobster Memory Guard v2 開始"

if [ -x "$FLUSH_SCRIPT" ] || [ -f "$FLUSH_SCRIPT" ]; then
  python3 "$FLUSH_SCRIPT" >/dev/null 2>&1 || true
  log "已執行 pre-compact context flush：$FLUSH_REPORT"
else
  log "找不到 flush 腳本，略過 pre-compact flush"
fi

STATUS_TEXT=$(openclaw status 2>&1 || true)
printf "%s\n" "$STATUS_TEXT" >> "$LOG_FILE"

SESSION_LINE=$(printf "%s\n" "$STATUS_TEXT" | grep 'agent:hq:telegram:direct:' | head -n 1 || true)
PERCENT=$(printf "%s\n" "$SESSION_LINE" | sed -n 's/.*(\([0-9][0-9]*\)%).*/\1/p')

if [ -z "$PERCENT" ]; then
  PERCENT=0
fi

log "目前主 session 使用率：約 ${PERCENT}%"

if [ "$PERCENT" -ge 80 ]; then
  log "達到 compact 建議門檻，送出提醒"
  openclaw message send \
    --channel telegram \
    --account default \
    --target 7132792298 \
    --message "🦞 Lobster Memory Guard\n目前主 session 約 ${PERCENT}% 使用率。\n已完成 pre-compact flush：$FLUSH_REPORT\n建議現在執行 /compact" \
    --silent >/dev/null 2>&1 || true
else
  log "未達 compact 門檻，僅完成 flush 與紀錄"
fi

log "Lobster Memory Guard v2 結束"
