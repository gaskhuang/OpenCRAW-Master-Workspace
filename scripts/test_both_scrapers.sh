#!/bin/bash
# 雙平台爬蟲測試腳本
# 同時測試 X/Twitter 和 Threads 爬蟲

echo "=========================================="
echo "🚀 雙平台爬蟲測試開始"
echo "=========================================="
echo ""

# 安裝依賴（如果需要）
echo "📦 檢查依賴..."
pip3 install playwright asyncio 2>/dev/null || pip install playwright asyncio 2>/dev/null

# 檢查 Playwright 瀏覽器
echo "🔧 檢查 Playwright..."
python3 -c "from playwright.sync_api import sync_playwright; print('✅ Playwright OK')" 2>/dev/null || echo "⚠️ 可能需要執行: playwright install"

echo ""
echo "🧵 啟動 Threads 爬蟲..."
python3 ~/scripts/threads_scraper_complete.py &
THREADS_PID=$!

echo ""
echo "🐦 啟動 X/Twitter 爬蟲..."
python3 ~/scripts/x_scraper_complete.py &
X_PID=$!

# 等待兩個進程完成
echo ""
echo "⏳ 等待爬蟲完成（可能需要幾分鐘）..."
wait $THREADS_PID
wait $X_PID

echo ""
echo "=========================================="
echo "✅ 測試完成！"
echo "=========================================="
echo ""
echo "📁 報告位置:"
echo "   ~/memory/daily-reports/"
echo ""
ls -lh ~/memory/daily-reports/*.html 2>/dev/null || echo "   暫無報告生成"
