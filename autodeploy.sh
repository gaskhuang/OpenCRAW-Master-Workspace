#!/bin/bash
# OpenClaw 自動部署守護程序
# 當指定檔案有更新時，自動部署到 GitHub

# 設定檔路徑
CONFIG_FILE="${HOME}/.openclaw/autodeploy.conf"
PID_FILE="${HOME}/.openclaw/autodeploy.pid"
LOG_FILE="${HOME}/.openclaw/autodeploy.log"
DB_FILE="${HOME}/.openclaw/autodeploy.db"

# 確保目錄存在
mkdir -p "$(dirname "$CONFIG_FILE")"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

info() { echo -e "${BLUE}ℹ️  $1${NC}"; log "INFO: $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; log "SUCCESS: $1"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; log "WARNING: $1"; }
error() { echo -e "${RED}❌ $1${NC}"; log "ERROR: $1"; }

# 顯示幫助
show_help() {
    cat << 'EOF'
🦞 OpenClaw 自動部署系統

使用方法:
    ./autodeploy.sh [命令] [選項]

命令:
    start          啟動自動部署守護程序
    stop           停止守護程序
    status         查看狀態
    add            新增要監視的檔案
    list           列出所有監視中的檔案
    remove         移除監視檔案
    logs           查看日誌

範例:
    # 啟動自動部署
    ./autodeploy.sh start

    # 新增監視檔案
    ./autodeploy.sh add /Users/user/kanban_board.html kanban-board

    # 查看狀態
    ./autodeploy.sh status

EOF
}

# 建立預設設定檔
create_default_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        cat > "$CONFIG_FILE" << 'EOF'
# OpenClaw 自動部署設定檔
# 格式: 檔案路徑|倉庫名稱|描述
#
# 範例:
# /Users/user/kanban_board.html|kanban-board|任務看板系統
# /Users/user/service_landing_page.html|openclaw-service|服務介紹頁面

EOF
        info "已建立預設設定檔: $CONFIG_FILE"
    fi
}

# 檢查守護程序狀態
check_status() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "running:$pid"
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    echo "stopped"
    return 1
}

# 啟動守護程序
start_daemon() {
    local status=$(check_status)
    
    if [ "$status" != "stopped" ]; then
        local pid=$(echo "$status" | cut -d: -f2)
        warning "守護程序已在執行中 (PID: $pid)"
        return 1
    fi
    
    create_default_config
    
    # 在背景啟動守護程序
    (
        # 建立資料庫檔案（儲存檔案修改時間）
        touch "$DB_FILE"
        
        log "=== 自動部署守護程序啟動 ==="
        
        while true; do
            # 檢查設定檔是否存在
            if [ ! -f "$CONFIG_FILE" ]; then
                sleep 5
                continue
            fi
            
            # 讀取設定檔並檢查每個檔案
            while IFS='|' read -r file_path repo_name description; do
                # 跳過註解和空行
                [[ "$file_path" =~ ^#.*$ ]] && continue
                [[ -z "$file_path" ]] && continue
                
                # 檢查檔案是否存在
                if [ ! -f "$file_path" ]; then
                    continue
                fi
                
                # 取得目前修改時間
                local current_mtime=$(stat -f %m "$file_path" 2>/dev/null || stat -c %Y "$file_path" 2>/dev/null)
                
                # 檢查資料庫中是否有記錄
                local stored_mtime=$(grep "^$file_path|" "$DB_FILE" 2>/dev/null | cut -d'|' -f2)
                
                if [ -z "$stored_mtime" ]; then
                    # 第一次記錄，只儲存不部署
                    echo "$file_path|$current_mtime" >> "$DB_FILE"
                    log "新增監視: $file_path -> $repo_name"
                elif [ "$current_mtime" != "$stored_mtime" ]; then
                    # 檔案已更新！
                    log "檔案更新偵測: $file_path"
                    
                    # 執行部署
                    if /Users/user/deploy_to_github.sh "$file_path" "$repo_name" "$description" >> "$LOG_FILE" 2>&1; then
                        success "自動部署成功: $file_path -> $repo_name"
                        
                        # 更新資料庫
                        sed -i.bak "/^$file_path|/d" "$DB_FILE" 2>/dev/null || true
                        echo "$file_path|$current_mtime" >> "$DB_FILE"
                    else
                        error "自動部署失敗: $file_path"
                    fi
                fi
            done < "$CONFIG_FILE"
            
            # 每 3 秒檢查一次
            sleep 3
        done
    ) &
    
    local daemon_pid=$!
    echo $daemon_pid > "$PID_FILE"
    
    success "自動部署守護程序已啟動 (PID: $daemon_pid)"
    info "監視設定檔: $CONFIG_FILE"
    info "日誌檔案: $LOG_FILE"
    echo ""
    info "現在你可以："
    echo "  1. 編輯 $CONFIG_FILE 新增要監視的檔案"
    echo "  2. 或直接執行: ./autodeploy.sh add <檔案> <倉庫>"
}

# 停止守護程序
stop_daemon() {
    local status=$(check_status)
    
    if [ "$status" = "stopped" ]; then
        warning "守護程序未在執行"
        return 1
    fi
    
    local pid=$(echo "$status" | cut -d: -f2)
    
    kill "$pid" 2>/dev/null
    rm -f "$PID_FILE"
    
    success "自動部署守護程序已停止"
}

# 顯示狀態
show_status() {
    local status=$(check_status)
    
    if [ "$status" = "stopped" ]; then
        info "狀態：⭕ 已停止"
    else
        local pid=$(echo "$status" | cut -d: -f2)
        info "狀態：🟢 執行中 (PID: $pid)"
    fi
    
    # 顯示監視中的檔案
    echo ""
    info "監視中的檔案："
    
    if [ -f "$CONFIG_FILE" ]; then
        local count=0
        while IFS='|' read -r file_path repo_name description; do
            [[ "$file_path" =~ ^#.*$ ]] && continue
            [[ -z "$file_path" ]] && continue
            
            ((count++))
            local status_icon="❓"
            [ -f "$file_path" ] && status_icon="📄"
            
            echo "  $status_icon $file_path"
            echo "     ↳ https://gaskhuang.github.io/$repo_name/"
        done < "$CONFIG_FILE"
        
        if [ $count -eq 0 ]; then
            echo "  (尚無監視檔案)"
            echo ""
            info "使用以下指令新增："
            echo "  ./autodeploy.sh add <檔案路徑> <倉庫名稱>"
        fi
    else
        echo "  (設定檔不存在)"
    fi
}

# 新增監視檔案
add_watch() {
    local file_path="$1"
    local repo_name="$2"
    local description="${3:-Auto deployed file}"
    
    if [ -z "$file_path" ] || [ -z "$repo_name" ]; then
        error "使用方法: ./autodeploy.sh add <檔案路徑> <倉庫名稱> [描述]"
        return 1
    fi
    
    # 轉換為絕對路徑
    if [[ ! "$file_path" = /* ]]; then
        file_path="$(pwd)/$file_path"
    fi
    
    # 檢查檔案是否存在
    if [ ! -f "$file_path" ]; then
        warning "檔案目前不存在，但會在出現時開始監視: $file_path"
    fi
    
    create_default_config
    
    # 檢查是否已存在
    if grep -q "^$file_path|" "$CONFIG_FILE" 2>/dev/null; then
        warning "此檔案已在監視清單中"
        return 1
    fi
    
    # 新增到設定檔
    echo "$file_path|$repo_name|$description" >> "$CONFIG_FILE"
    success "已新增監視: $file_path"
    info "目標倉庫: https://github.com/gaskhuang/$repo_name"
    
    # 如果守護程序在執行，立即記錄檔案狀態
    local status=$(check_status)
    if [ "$status" != "stopped" ] && [ -f "$file_path" ]; then
        local current_mtime=$(stat -f %m "$file_path" 2>/dev/null || stat -c %Y "$file_path" 2>/dev/null)
        echo "$file_path|$current_mtime" >> "$DB_FILE"
        info "已記錄初始狀態，下次修改將自動部署"
    fi
}

# 列出監視檔案
list_watches() {
    if [ ! -f "$CONFIG_FILE" ]; then
        info "尚無監視檔案"
        return
    fi
    
    info "監視中的檔案清單："
    echo ""
    
    local count=0
    while IFS='|' read -r file_path repo_name description; do
        [[ "$file_path" =~ ^#.*$ ]] && continue
        [[ -z "$file_path" ]] && continue
        
        ((count++))
        echo "$count. $file_path"
        echo "   倉庫: $repo_name"
        echo "   描述: $description"
        
        if [ -f "$file_path" ]; then
            local mtime=$(stat -f %Sm "$file_path" 2>/dev/null || stat -c %y "$file_path" 2>/dev/null)
            echo "   修改: $mtime"
        else
            echo "   狀態: ⚠️  檔案不存在"
        fi
        echo ""
    done < "$CONFIG_FILE"
    
    if [ $count -eq 0 ]; then
        echo "  (尚無監視檔案)"
    fi
}

# 移除監視
remove_watch() {
    local file_path="$1"
    
    if [ -z "$file_path" ]; then
        # 顯示清單讓用戶選擇
        list_watches
        echo ""
        read -p "請輸入要移除的檔案路徑: " file_path
    fi
    
    if [ -z "$file_path" ]; then
        error "未指定檔案"
        return 1
    fi
    
    if [ ! -f "$CONFIG_FILE" ]; then
        error "設定檔不存在"
        return 1
    fi
    
    # 移除該行
    if grep -q "^$file_path|" "$CONFIG_FILE"; then
        sed -i.bak "/^$file_path|/d" "$CONFIG_FILE"
        success "已移除監視: $file_path"
    else
        error "找不到該檔案的監視設定"
        return 1
    fi
}

# 顯示日誌
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -n ${1:-50} "$LOG_FILE"
    else
        info "尚無日誌記錄"
    fi
}

# 主程式
main() {
    case "${1:-}" in
        start)
            start_daemon
            ;;
        stop)
            stop_daemon
            ;;
        status)
            show_status
            ;;
        add)
            add_watch "$2" "$3" "$4"
            ;;
        list)
            list_watches
            ;;
        remove)
            remove_watch "$2"
            ;;
        logs)
            show_logs "$2"
            ;;
        *)
            show_help
            ;;
    esac
}

main "$@"