#!/bin/bash
set -euo pipefail

export PATH="/Users/user/.local/bin:/Users/user/.npm-global/bin:/Users/user/bin:/Users/user/.volta/bin:/Users/user/.asdf/shims:/Users/user/.bun/bin:/Users/user/Library/Application Support/fnm/aliases/default/bin:/Users/user/.fnm/aliases/default/bin:/Users/user/Library/pnpm:/Users/user/.local/share/pnpm:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/user"

WORKSPACE="/Users/user"
LOG_FILE="$WORKSPACE/openclaw_update.log"
REPORT_DIR="$WORKSPACE/reports/openclaw-updates"
DATE=$(date '+%Y-%m-%d')
STAMP=$(date '+%Y%m%d_%H%M%S')
REPORT_FILE="$REPORT_DIR/openclaw-auto-update-$DATE.md"
TMP_FILE="/tmp/openclaw_auto_update_$STAMP.tmp"

mkdir -p "$REPORT_DIR"

after_or_unknown() {
  "$@" 2>/dev/null || true
}

safe_append() {
  printf "%s\n" "$1" >> "$TMP_FILE"
}

echo "=== OpenClaw Auto Update 開始: $(date) ===" >> "$LOG_FILE"

OPENCLAW_BEFORE=$(after_or_unknown openclaw --version | head -1)
NODE_VERSION=$(after_or_unknown node -v | head -1)
NPM_VERSION=$(after_or_unknown npm -v | head -1)

{
  echo "# OpenClaw Auto Update 報告"
  echo
  echo "- 日期：$DATE"
  echo "- 執行時間：$(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- Node：$NODE_VERSION"
  echo "- npm：$NPM_VERSION"
  echo "- OpenClaw（更新前）：${OPENCLAW_BEFORE:-unknown}"
  echo
  echo "## 1. OpenClaw 更新"
} > "$TMP_FILE"

OPENCLAW_UPDATE_OUTPUT=$(openclaw update 2>&1 || true)
printf "%s\n" "$OPENCLAW_UPDATE_OUTPUT" >> "$LOG_FILE"
OPENCLAW_AFTER=$(after_or_unknown openclaw --version | head -1)
{
  echo '- 更新指令：`openclaw update`'
  echo '- 更新前：'
  printf '  - `%s`\n' "${OPENCLAW_BEFORE:-unknown}"
  echo '- 更新後：'
  printf '  - `%s`\n' "${OPENCLAW_AFTER:-unknown}"
  echo
  echo '```text'
  printf "%s\n" "$OPENCLAW_UPDATE_OUTPUT" | tail -n 40
  echo '```'
  echo
  echo "## 2. ~/skills 更新"
} >> "$TMP_FILE"

SKILLS_UPDATED=0
if [ -d "$WORKSPACE/skills" ]; then
  while IFS= read -r -d '' dir; do
    REPO_NAME=$(basename "$dir")
    if [ -d "$dir/.git" ]; then
      BEFORE=$(git -C "$dir" rev-parse --short HEAD 2>/dev/null || echo unknown)
      BRANCH=$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)
      PULL_OUT=$(git -C "$dir" pull origin "$BRANCH" 2>&1 || git -C "$dir" pull origin main 2>&1 || git -C "$dir" pull origin master 2>&1 || true)
      AFTER=$(git -C "$dir" rev-parse --short HEAD 2>/dev/null || echo unknown)
      {
        echo "### $REPO_NAME"
        echo "- branch: $BRANCH"
        echo "- commit: $BEFORE -> $AFTER"
        echo '```text'
        printf "%s\n" "$PULL_OUT" | tail -n 20
        echo '```'
        echo
      } >> "$TMP_FILE"
      printf "[%s] %s\n" "$REPO_NAME" "$PULL_OUT" >> "$LOG_FILE"
      SKILLS_UPDATED=$((SKILLS_UPDATED + 1))
    fi
  done < <(find "$WORKSPACE/skills" -mindepth 1 -maxdepth 1 -type d -print0)
fi

{
  echo "## 3. /Users/user/openclaw repo 更新"
} >> "$TMP_FILE"
if [ -d "$WORKSPACE/openclaw/.git" ]; then
  OC_BEFORE=$(git -C "$WORKSPACE/openclaw" rev-parse --short HEAD 2>/dev/null || echo unknown)
  OC_BRANCH=$(git -C "$WORKSPACE/openclaw" rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)
  OC_PULL=$(git -C "$WORKSPACE/openclaw" pull origin "$OC_BRANCH" 2>&1 || git -C "$WORKSPACE/openclaw" pull origin main 2>&1 || true)
  OC_AFTER=$(git -C "$WORKSPACE/openclaw" rev-parse --short HEAD 2>/dev/null || echo unknown)
  {
    echo "- branch: $OC_BRANCH"
    echo "- commit: $OC_BEFORE -> $OC_AFTER"
    echo '```text'
    printf "%s\n" "$OC_PULL" | tail -n 20
    echo '```'
    echo
  } >> "$TMP_FILE"
else
  echo '- 未偵測到 git repo，略過。' >> "$TMP_FILE"
  echo >> "$TMP_FILE"
fi

STATUS_OUTPUT=$(openclaw status 2>&1 || true)
{
  echo "## 4. 健康檢查"
  echo '```text'
  printf "%s\n" "$STATUS_OUTPUT" | tail -n 80
  echo '```'
  echo
  echo "## 5. 總結"
  echo "- 已更新 OpenClaw 與技能庫"
  echo "- skills repo 檢查數量：$SKILLS_UPDATED"
  echo "- 本報告由 OpenClaw 版 auto-updater 自動生成"
} >> "$TMP_FILE"

mv "$TMP_FILE" "$REPORT_FILE"
echo "報告產出：$REPORT_FILE" >> "$LOG_FILE"

cd "$WORKSPACE"
git add "$REPORT_FILE" \
        "/Users/user/skills/openclaw-auto-updater/SKILL.md" \
        "/Users/user/Library/LaunchAgents/com.agaikid.openclaw-auto-update.plist" 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "🔄 add OpenClaw auto-updater workflow and daily update report" >/dev/null 2>&1 || true
  git push origin HEAD >/dev/null 2>&1 || true
fi

openclaw message send \
  --channel telegram \
  --account default \
  --target 7132792298 \
  --message "🦀 阿蓋三號｜OpenClaw 自動更新完成\n- 報告：$REPORT_FILE\n- skills 檢查數量：$SKILLS_UPDATED\n- 已同步 GitHub" \
  --silent >/dev/null 2>&1 || true

echo "=== OpenClaw Auto Update 結束: $(date) ===" >> "$LOG_FILE"
