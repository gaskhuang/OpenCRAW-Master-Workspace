#!/bin/bash
# 🍎 OpenClaw Mac 一键安装脚本（Apple Silicon/Intel 通用）
# 专为 macOS 优化

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🦞 OpenClaw for Mac - 一键安装器                  ║"
echo "║         专为 Apple Silicon & Intel 优化                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检测 Mac 类型
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    MAC_TYPE="Apple Silicon (M1/M2/M3)"
else
    MAC_TYPE="Intel Mac"
fi

echo "检测到: $MAC_TYPE"
echo ""

# 检查 macOS 版本
MACOS_VERSION=$(sw_vers -productVersion)
echo "macOS 版本: $MACOS_VERSION"
echo ""

# 检查并安装 Homebrew
install_homebrew() {
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}🔧 正在安装 Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # 配置环境变量
        if [ "$ARCH" = "arm64" ]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.bash_profile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        echo -e "${GREEN}✅ Homebrew 安装完成${NC}"
    else
        echo -e "${GREEN}✅ Homebrew 已安装${NC}"
    fi
}

# 安装依赖
install_dependencies() {
    echo ""
    echo -e "${YELLOW}📦 正在安装依赖...${NC}"
    
    # 核心依赖
    brew install node python git curl jq
    
    # 可选但推荐的工具
    brew install --cask visual-studio-code
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
}

# 安装 OpenClaw
install_openclaw() {
    echo ""
    echo -e "${YELLOW}🦞 正在安装 OpenClaw...${NC}"
    
    npm install -g openclaw
    
    echo -e "${GREEN}✅ OpenClaw 安装完成${NC}"
}

# 配置快捷指令
setup_shortcuts() {
    echo ""
    echo -e "${YELLOW}⚡ 正在配置快捷指令...${NC}"
    
    # 添加到 .zshrc 或 .bash_profile
    SHELL_RC="$HOME/.zshrc"
    if [ ! -f "$SHELL_RC" ]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
    
    cat >> "$SHELL_RC" << 'EOF'

# OpenClaw 快捷指令
alias oc='openclaw'
alias ocg='openclaw gateway'
alias ocstart='openclaw gateway start'
alias ocstop='openclaw gateway stop'
alias ocstatus='openclaw status'
alias ocmodels='openclaw models'
alias ocmenu='openclaw menu'

EOF
    
    echo -e "${GREEN}✅ 快捷指令已配置${NC}"
    echo ""
    echo "可用的快捷指令:"
    echo "  oc      - OpenClaw 主命令"
    echo "  ocg     - Gateway 相关"
    echo "  ocstart - 启动服务"
    echo "  ocstop  - 停止服务"
    echo "  ocmenu  - 打开菜单"
}

# 安装 Mac 特定优化
mac_optimizations() {
    echo ""
    echo -e "${YELLOW}🍎 Mac 特定优化...${NC}"
    
    # 创建 LaunchAgent（开机自动启动）
    LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.openclaw.guide.plist"
    
    cat > "$LAUNCH_AGENT" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.guide</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which openclaw)</string>
        <string>gateway</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF
    
    echo -e "${GREEN}✅ 已创建开机启动配置${NC}"
    echo "   位置: $LAUNCH_AGENT"
    echo "   （如需开机启动，请运行: launchctl load $LAUNCH_AGENT）"
}

# 主安装流程
main() {
    echo "开始安装流程..."
    echo ""
    
    install_homebrew
    install_dependencies
    install_openclaw
    setup_shortcuts
    mac_optimizations
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                   🎉 安装完成！                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "📋 下一步:"
    echo ""
    echo "1️⃣  重启终端或运行:"
    echo "   source ~/.zshrc"
    echo ""
    echo "2️⃣  配置 API Keys:"
    echo "   openclaw configure"
    echo ""
    echo "3️⃣  启动服务:"
    echo "   ocstart"
    echo "   或"
    echo "   openclaw gateway start"
    echo ""
    echo "4️⃣  打开控制台:"
    echo "   open http://localhost:18789"
    echo ""
    echo -e "${YELLOW}💡 提示:${NC}"
    echo "• 使用 'ocmenu' 快速打开模型切换菜单"
    echo "• 配置文件位置: ~/.openclaw/openclaw.json"
    echo "• 日志位置: ~/.openclaw/logs/"
    echo ""
    echo -e "${BLUE}需要帮助? 联系 Telegram: @gskgino${NC}"
    echo ""
}

# 询问是否开始
read -p "是否开始安装? (y/N): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    main
else
    echo "安装已取消"
    exit 0
fi