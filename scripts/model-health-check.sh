#!/bin/zsh
# Model Health Check + Auto-Fallback Script
# Run: ./model-health-check.sh [test_query]

set -e

TEST_QUERY=${1:-"test"}
WORKING_MODELS=()
FAILED_MODELS=()

echo "🧠 模型健康檢查開始..."

# List preferred models from USER.md
PREFERRED=( "google-antigravity/gemini-3-flash" "moonshot/kimi-k2.5" "openai/codex" "xai/grok-4-1-fast-reasoning" "gmi/glm-5" )

for model in ${PREFERRED[@]}; do
  echo "測試 $model..."
  if sessions_status model=$model "健康檢查: $TEST_QUERY" &>/dev/null; then
    WORKING_MODELS+=($model)
    echo "✅ $model OK"
  else
    FAILED_MODELS+=($model)
    echo "❌ $model 失敗"
  fi
done

echo ""
echo "📊 結果："
echo "可用：${WORKING_MODELS[*]}"
echo "失效：${FAILED_MODELS[*]}"

if (( ${#WORKING_MODELS[@]} > 0 )); then
  echo "建議 fallback: ${WORKING_MODELS[1]}"
  echo "設定：openclaw configure --model ${WORKING_MODELS[1]}"
else
  echo "⚠️ 全掛！檢查 API key / 額度"
fi

# Auto update cron model if possible (example for one job)
# openclaw cron update <job-id> model=${WORKING_MODELS[1]}
