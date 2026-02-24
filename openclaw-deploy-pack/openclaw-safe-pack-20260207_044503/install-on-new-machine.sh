#!/bin/bash
# === 新機器安裝腳本 ===
# 使用方式：在新機器上解壓後執行此腳本

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 開始部署 OpenClaw 設定..."

# 確認 OpenClaw 已安裝
if ! command -v openclaw &> /dev/null; then
    echo "❌ 請先安裝 OpenClaw："
    echo "   npm install -g openclaw"
    exit 1
fi

# 確認 Node.js 版本
NODE_VER=$(node --version | cut -d'.' -f1 | tr -d 'v')
if [ "$NODE_VER" -lt 22 ]; then
    echo "⚠️  建議 Node.js v22+，當前版本：$(node --version)"
fi

# 複製 Skills
if [ -d "${SCRIPT_DIR}/skills" ]; then
    mkdir -p "$HOME/.openclaw/workspace/skills"
    cp -r "${SCRIPT_DIR}/skills/"* "$HOME/.openclaw/workspace/skills/" 2>/dev/null
    echo "  ✅ Skills 已安裝"
fi

# 複製 Prompts
if [ -d "${SCRIPT_DIR}/prompts" ]; then
    mkdir -p "$HOME/.openclaw/workspace/prompts"
    cp -r "${SCRIPT_DIR}/prompts/"* "$HOME/.openclaw/workspace/prompts/" 2>/dev/null
    echo "  ✅ Prompts 已安裝"
fi

# 複製 IDENTITY.md
if [ -f "${SCRIPT_DIR}/IDENTITY.md" ]; then
    mkdir -p "$HOME/.openclaw/workspace"
    cp "${SCRIPT_DIR}/IDENTITY.md" "$HOME/.openclaw/workspace/IDENTITY.md"
    echo "  ✅ IDENTITY.md 已安裝"
fi

# 套用 Gateway 設定模板
if [ -f "${SCRIPT_DIR}/openclaw-template.json" ]; then
    echo ""
    echo "⚠️  Gateway 設定模板已準備好，但你需要手動："
    echo "   1. 執行 openclaw setup 完成初始設定"
    echo "   2. 或手動將模板合併到 ~/.openclaw/openclaw.json"
    echo "   3. 記得設定你自己的 API Key（不要用別人的）"
    echo ""
fi

echo ""
echo "🎉 設定檔部署完成！"
echo ""
echo "接下來你需要："
echo "  1. 執行 openclaw setup 進行初始化（設定你的 API Key）"
echo "  2. 或 openclaw configure 調整進階設定"
echo "  3. 執行 openclaw doctor 確認一切正常"
