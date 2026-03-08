---
name: openclaw-auto-updater
description: OpenClaw 版自動更新器。每天固定檢查並更新 OpenClaw、~/skills、workspace 內指定 repo，產出 Markdown 報告，並同步 GitHub。
---

# OpenClaw Auto Updater

這是針對 **OpenClaw + launchd + GitHub 同步** 環境設計的自動更新 skill，不使用 Clawdbot / clawdhub cron。

## 功能

每天固定執行：

1. 檢查並更新 OpenClaw
2. 更新 `~/skills/` 內 git repo
3. 視需要更新 `/Users/user/openclaw/` repo
4. 產出更新報告（Markdown）
5. 將報告與相關設定同步到 GitHub
6. 回報 Telegram

## 執行腳本

```bash
/Users/user/scripts/openclaw_auto_update.sh
```

## 報告位置

```bash
/Users/user/reports/openclaw-updates/
```

## 排程

launchd:

```bash
/Users/user/Library/LaunchAgents/com.agaikid.openclaw-auto-update.plist
```

預設每天 00:00 執行。

## 手動執行

```bash
bash /Users/user/scripts/openclaw_auto_update.sh
```

## GitHub 同步規則

- 所有新產生或修改的 `.md` / config 檔，一律同步到目前 workspace git repo
- 若含敏感資訊，需先去敏感再同步
