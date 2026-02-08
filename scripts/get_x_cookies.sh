#!/bin/bash
# 提取 X (Twitter) Cookie 腳本
# 適用於 macOS Chrome

echo "🔍 正在提取 X.com Cookie..."
echo ""

# 檢查是否已安裝 bird
if ! command -v bird &> /dev/null; then
    echo "⚠️ bird CLI 未安裝，正在安裝..."
    npm install -g @steipete/bird || brew install steipete/tap/bird
fi

# 嘗試從 Chrome Cookies 資料庫讀取
echo "📂 嘗試讀取 Chrome Cookies..."

COOKIES_DB="$HOME/Library/Application Support/Google/Chrome/Default/Cookies"
if [ ! -f "$COOKIES_DB" ]; then
    echo "❌ 找不到 Chrome Cookies 資料庫"
    echo "   路徑: $COOKIES_DB"
    exit 1
fi

# 使用 sqlite3 讀取 (但 cookie 值是加密的，需要解密)
# 這個方法需要 Chrome 的 Safe Storage 密鑰，比較複雜

echo ""
echo "ℹ️ 由於 macOS 安全性限制，自動提取需要額外權限"
echo ""
echo "請手動執行以下步驟："
echo ""
echo "1. 在 Chrome 中按 F12 開啟開發者工具"
echo "2. 點擊 Application (應用程式) 標籤"
echo "3. 左側展開 Cookies → https://x.com"
echo "4. 找到 auth_token 和 ct0"
echo "5. 複製這兩個值給小龍蝦"
echo ""
echo "或者使用這個 JavaScript 命令在 Console 中執行："
echo 'copy(document.cookie.split(";").find(c => c.includes("ct0")))'
echo ""

# 檢查是否可以讀取
echo "🧪 測試 bird CLI 連線..."
bird check 2>&1 | head -20
