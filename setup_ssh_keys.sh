#!/bin/bash
# SSH 金鑰設定助手
# 幫你快速設定免密登入到客戶機器

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

echo "🦞 OpenClaw SSH 金鑰設定助手"
echo "=============================="
echo ""

# 檢查 SSH 金鑰
if [ ! -f ~/.ssh/id_rsa.pub ] && [ ! -f ~/.ssh/id_ed25519.pub ]; then
    info "尚未建立 SSH 金鑰，正在建立..."
    
    read -p "請輸入您的 Email: " email
    
    # 建立 ED25519 金鑰（更安全）
    ssh-keygen -t ed25519 -C "$email" -f ~/.ssh/id_ed25519 -N ""
    
    success "SSH 金鑰已建立！"
    echo ""
fi

# 選擇金鑰
KEY_FILE=""
if [ -f ~/.ssh/id_ed25519.pub ]; then
    KEY_FILE="~/.ssh/id_ed25519.pub"
    info "使用 ED25519 金鑰"
elif [ -f ~/.ssh/id_rsa.pub ]; then
    KEY_FILE="~/.ssh/id_rsa.pub"
    info "使用 RSA 金鑰"
fi

# 顯示公鑰內容
echo ""
echo "📋 您的 SSH 公鑰內容（請複製這個）："
echo "==================================="
cat "$KEY_FILE"
echo "==================================="
echo ""

# 選擇設定方式
echo "請選擇設定方式："
echo "1) 自動複製到單台機器（需要密碼）"
echo "2) 顯示公鑰，手動貼上到多台機器"
echo "3) 批次設定（從 hosts 檔案）"
read -p "請選擇 (1/2/3): " choice

case $choice in
    1)
        read -p "請輸入客戶機器位址 (user@hostname): " remote_host
        info "正在複製金鑰到 $remote_host..."
        
        if ssh-copy-id "$remote_host"; then
            success "金鑰複製成功！"
            info "測試連線中..."
            if ssh "$remote_host" "echo '✅ SSH 免密登入成功！'"; then
                success "設定完成！"
            else
                error "連線測試失敗"
            fi
        else
            error "金鑰複製失敗"
        fi
        ;;
    
    2)
        echo ""
        echo "📖 手動設定步驟："
        echo "1. 登入到客戶的機器"
        echo "2. 編輯 ~/.ssh/authorized_keys"
        echo "3. 貼上上面的公鑰內容"
        echo "4. 儲存並退出"
        echo ""
        echo "或請客戶執行："
        echo "mkdir -p ~/.ssh && echo '$(cat "$KEY_FILE")' >> ~/.ssh/authorized_keys"
        ;;
    
    3)
        if [ ! -f "openclaw_hosts.txt" ]; then
            error "找不到 openclaw_hosts.txt"
            exit 1
        fi
        
        info "批次設定 SSH 金鑰..."
        
        while IFS= read -r host || [[ -n "$host" ]]; do
            [[ "$host" =~ ^#.*$ ]] && continue
            [[ -z "$host" ]] && continue
            
            echo ""
            info "設定 $host..."
            
            if ssh-copy-id "$host" 2>/dev/null; then
                success "$host 設定成功"
            else
                warning "$host 設定失敗（可能需要手動設定）"
            fi
        done < "openclaw_hosts.txt"
        
        success "批次設定完成！"
        ;;
    
    *)
        error "無效選項"
        exit 1
        ;;
esc

echo ""
echo "🎉 SSH 設定完成！"
echo ""
echo "現在可以執行："
echo "  ./update_openclaw_models.sh -r openclaw_hosts.txt"
echo ""
echo "來批量更新所有客戶的 OpenClaw 了！"