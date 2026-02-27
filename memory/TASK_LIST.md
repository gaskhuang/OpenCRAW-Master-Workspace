# 今晚待辦清單 (2026-02-23)
## P0 高優先 (今晚衝)
1. 手機截圖自動抓取 + 內容辨識重命名 + 分類資料夾
2. FB/IG/X/Reddit/Threads 多平台爬蟲流程
3. 修語音輸入可用 + 免持喚醒
4. Landing Page 修正 + 銷售頁重寫

## P1 中優先
5. 網站補圖/視覺優化
6. 完成 AI SEO 網站版本

## P2 文章發佈 (明天)
7. 為什麼用 Mac mini
8. 省 API 成本
9. models.json / openclaw.json 教學

## 執行紀錄 (2026-02-27)
- [x] Threads OpenClaw 監控（記者版）：已執行，因 Browser Control timeout 阻塞；已輸出阻塞報告並推送 GitHub（commit: 8c8471e）。

## 執行紀錄 (2026-02-28)
- [x] Reddit OpenClaw 監控（cron:398ccdaf）：Pushshift API 回傳 403，已自動切換 Reddit JSON API 採集；完成採集→分析→歸檔→GitHub 上傳。
  - 報告：`reports/openclaw-monitoring/reddit_openclaw_report_2026-02-28_01-02.md`
  - 資料：`reports/openclaw-monitoring/reddit_openclaw_data_2026-02-28_01-02.json`
  - GitHub commit：`9af8959`- [x] OpenClaw X 平台智能分析（cron:4fcc1bcf，每3小時）：輸出格式切換為網站版（對齊 x.deepsrt.com 互動邏輯），並確保資料受阻時仍輸出同版型且附阻擋原因，避免虛構 tweet_id。
  - HTML：`reports/web/x_monitor_20260228_0113.html`
  - MD：`reports/x_monitor_20260228_0113.md`
