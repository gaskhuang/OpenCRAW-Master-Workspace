#!/bin/bash

# 🦞 OpenCRAW 雙龍蝦 HA 一鍵啟動腳本 (Lobster Swarm Script)
# 版本: 2026.02.08

echo "🚀 正在啟動 OpenCRAW 雙龍蝦軍團..."

# 1. 啟動龍蝦 A (主控助理 - Port 18789)
echo "🦞 龍蝦 A (助理模式) 正在就位... (Port: 18789)"
openclaw gateway start --port 18789

# 2. 啟動龍蝦 B (特種爬蟲 - Port 18790)
# 使用獨立的 profile 確保記憶與 Token 隔離
echo "🦞 龍蝦 B (特種模式) 正在進入房間... (Port: 18790)"
openclaw --profile bot2 gateway start --port 18790

echo "✅ 雙龍蝦架構部署完成！"
echo "助理 A: http://localhost:18789"
echo "助理 B: http://localhost:18790"
echo "------------------------------------------------"
echo "提示：您可以使用 'openclaw status' 與 'openclaw --profile bot2 status' 分別檢查狀態。"
