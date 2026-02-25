#!/bin/bash
# ==========================================
# X Top Crawler Chrome Launcher
# 啟動 Chrome 並開啟 CDP 端口 19222
# ==========================================

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
USER_DATA_DIR="/Users/user/.openclaw/chrome-crawler-profile"
PROFILE_DIR="CrawlerKing"
CDP_PORT=19222

# 檢查 Chrome 是否存在
if [ ! -f "$CHROME_PATH" ]; then
    echo "❌ Chrome not found at: $CHROME_PATH"
    exit 1
fi

# 創建用戶資料目錄
mkdir -p "$USER_DATA_DIR"

# 檢查是否已有 Chrome 進程使用該端口
EXISTING_PID=$(lsof -ti:$CDP_PORT 2>/dev/null)
if [ -n "$EXISTING_PID" ]; then
    echo "⚠️ Chrome CDP already running on port $CDP_PORT (PID: $EXISTING_PID)"
    # 測試 CDP 是否可用
    if curl -s http://127.0.0.1:$CDP_PORT/json/version > /dev/null 2>&1; then
        echo "✅ CDP port $CDP_PORT is responsive"
        exit 0
    else
        echo "⚠️ CDP not responsive, killing existing process..."
        kill -9 $EXISTING_PID 2>/dev/null
        sleep 2
    fi
fi

echo "🚀 Starting Chrome with CDP on port $CDP_PORT..."

# 啟動 Chrome
"$CHROME_PATH" \
    --remote-debugging-port=$CDP_PORT \
    --user-data-dir="$USER_DATA_DIR" \
    --profile-directory="$PROFILE_DIR" \
    --no-first-run \
    --no-default-browser-check \
    --enable-automation \
    --disable-blink-features=AutomationControlled \
    --disable-web-security \
    --disable-features=IsolateOrigins,site-per-process \
    --window-size=1920,1080 \
    "https://x.com" \
    > /dev/null 2>&1 &

CHROME_PID=$!
echo "🔄 Chrome started with PID: $CHROME_PID"

# 等待 CDP 端口可用
echo "⏳ Waiting for CDP port $CDP_PORT to be ready..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:$CDP_PORT/json/version > /dev/null 2>&1; then
        echo "✅ CDP is ready on port $CDP_PORT"
        exit 0
    fi
    sleep 1
done

echo "❌ CDP port $CDP_PORT did not become ready within 30 seconds"
exit 1
