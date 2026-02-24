#!/bin/bash
# ==============================================================================
# 🦞 龍蝦 AI 系統：新機自動化安裝腳本
# 版本：2026-02-24
# ==============================================================================
set -euo pipefail

RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()  { echo -e "${CYAN}[$(date +%H:%M:%S)]${RESET} $*"; }
ok()   { echo -e "${GREEN}  ✅ $*${RESET}"; }
warn() { echo -e "${YELLOW}  ⚠️  $*${RESET}"; }

OPENCLAW_SKILLS="/Users/user/openclaw/openclaw/skills"
USER_SKILLS="/Users/user/skills"

echo -e "${BOLD}🚀 龍蝦 AI 系統：新機自動化安裝腳本${RESET}"
echo "================================================================"

# ==============================================================================
# 1. 核心環境：Homebrew / NVM
# ==============================================================================
log "📦 1. 核心環境..."

if ! command -v brew &>/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
[[ -f /opt/homebrew/bin/brew ]] && eval "$(/opt/homebrew/bin/brew shellenv)"

if [[ ! -d "$HOME/.nvm" ]]; then
    curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
fi
export NVM_DIR="$HOME/.nvm"
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"

ok "核心環境就緒"

# ==============================================================================
# 2. Homebrew 套件
# ==============================================================================
log "🍺 2. Homebrew 套件..."
brew update --quiet

for pkg in node openclaw whisper-cpp tailscale rclone; do
    brew list "$pkg" &>/dev/null && ok "$pkg 已安裝" || brew install "$pkg"
done

if ! command -v rustup &>/dev/null; then
    brew install rustup && rustup-init -y --no-modify-path
fi
source "$HOME/.cargo/env" 2>/dev/null || true
ok "Homebrew 完成"

# ==============================================================================
# 3. NPM 全域套件
# ==============================================================================
log "🌐 3. NPM 套件..."
for pkg in pm2 openclaw tsx "@tobilu/qmd" agent-browser "@google/gemini-cli" web-scraper; do
    npm install -g "$pkg" || warn "$pkg 安裝失敗"
done
ok "NPM 完成"

# ==============================================================================
# 4. Python 套件
# ==============================================================================
log "🐍 4. Python 套件..."
PIP="/opt/homebrew/bin/pip3"

$PIP install --upgrade pip --quiet
$PIP install --quiet --break-system-packages \
    faster-whisper \
    python-telegram-bot \
    openai \
    tavily-python \
    firecrawl-py \
    youtube-transcript-api \
    google-generativeai \
    smooth-py \
    || warn "部分 Python 套件安裝失敗，請手動確認"

ok "Python 完成"

# ==============================================================================
# 5. OpenClaw 外掛與 MCP
# ==============================================================================
log "🦞 5. OpenClaw 外掛..."

openclaw plugins install @supermemory/openclaw-supermemory || warn "supermemory 安裝失敗"
openclaw mcp install github     2>/dev/null || warn "github MCP 請手動確認"
openclaw mcp install playwright 2>/dev/null || warn "playwright MCP 請手動確認"
openclaw browser --init         2>/dev/null || warn "browser init 失敗，可稍後執行"

ok "OpenClaw 外掛完成"

# ==============================================================================
# 6. Skills 安裝
# ==============================================================================
log "🧠 6. Skills 安裝..."

install_skill() {
    local name="$1"
    local src="$2"
    local dest="$OPENCLAW_SKILLS/$name"
    if [[ -f "$src/SKILL.md" ]]; then
        mkdir -p "$dest"
        cp "$src/SKILL.md" "$dest/SKILL.md"
        [[ -d "$src/scripts" ]] && cp -r "$src/scripts" "$dest/"
        ok "skill: $name"
    else
        warn "skill $name 找不到來源：$src"
    fi
}

# smooth-browser（從 GitHub 下載）
mkdir -p "$OPENCLAW_SKILLS/smooth-browser"
curl -fsSL "https://raw.githubusercontent.com/circlemind-ai/smooth-sdk/refs/heads/master/skills/smooth-browser/SKILL.md" \
    -o "$OPENCLAW_SKILLS/smooth-browser/SKILL.md" && ok "skill: smooth-browser" \
    || warn "smooth-browser 下載失敗"

# notebooklm（YouTube/網站→簡報/Podcast）
install_skill "notebooklm" "$OPENCLAW_SKILLS/notebooklm"

# gog（Google Workspace CLI）
install_skill "gog" "$OPENCLAW_SKILLS/gog"

# skio（安裝部署配置）
install_skill "skio" "$USER_SKILLS/skio"

if ! smooth config --show &>/dev/null 2>&1; then
    warn "smooth API Key 尚未設定，請執行：smooth config --api-key YOUR_KEY"
    warn "取得 API Key：https://app.smooth.sh"
fi

ok "Skills 完成"

# ==============================================================================
# 7. 啟動三隻龍蝦
# ==============================================================================
log "🦞🦞🦞 7. 啟動龍蝦..."

openclaw gateway install && ok "主龍蝦（port 18789）已啟動" \
    || warn "主龍蝦啟動失敗"



# ==============================================================================
# 完成
# ==============================================================================
echo ""
echo "================================================================"
echo -e "${GREEN}${BOLD}🎉 安裝完成！${RESET}"
echo ""
echo -e "${BOLD}龍蝦軍團狀態：${RESET}"
echo "  主龍蝦    → http://127.0.0.1:18789"
echo ""
echo -e "${BOLD}待完成：${RESET}"
echo "  smooth config --api-key YOUR_KEY   # 設定 Smooth API Key"
echo "================================================================"
