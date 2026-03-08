# Nano Banana 2 / 阿蓋二號 狀態確認

日期：2026-03-09

## 結論
- Nano Banana 2 已實測成功。
- `GEMINI_API_KEY` 並非真正缺失，而是部分舊 session / 舊檢查入口沒有讀到最新環境。
- 後續檢查請以統一 preflight 腳本為準，不要只憑單一 shell 回報「沒 key」。

## 實測結果
- 指令：
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "一隻穿西裝的龍蝦，正面站姿，乾淨背景，插畫風" --filename "nano-banana2-lobster-test.png" --model nano2 --resolution 1K`
- 輸出檔案：
  - `/Users/user/nano-banana2-lobster-test.png`

## 已補上的 key 來源
- `~/.zshrc`
- `~/.zprofile`
- `/Users/user/.agents/skills/gemini/.env`
- `/Users/user/skills/nano-banana-pro/.env`
- `/Users/user/Library/LaunchAgents/ai.openclaw.lobster2.plist`
- `/Users/user/Library/LaunchAgents/ai.openclaw.lobster3.plist`

## 後續統一檢查方式
- 檢查腳本：`/Users/user/scripts/check_gemini_env.py`
- 用法：
  - `zsh -lc '/Users/user/scripts/check_gemini_env.py'`

## 流程修正
- 若之後遇到「Gemini API Key 未設定」訊息：
  1. 先跑 `check_gemini_env.py`
  2. 若 key 來源都有值，視為舊 session / 舊 shell 誤判
  3. 直接做實跑測試，不再只停在口頭判定
