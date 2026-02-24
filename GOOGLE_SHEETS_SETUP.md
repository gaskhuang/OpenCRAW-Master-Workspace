# Google Sheets API 設定教學

這份教學將協助你設置 Google Sheets API 認證，以便運行 `create_order_sheet.py` 創建訂單表。

## 快速步驟

### 1. 前往 Google Cloud Console
開啟 https://console.cloud.google.com/

### 2. 創建新專案
- 點擊頂部專案選擇器
- 點擊「新增專案」
- 輸入專案名稱（例如：「統用企業訂單系統」）
- 點擊「建立」

### 3. 啟用 API
- 在搜尋欄搜尋 "Google Sheets API"
- 點擊「啟用」
- 同樣方式搜尋並啟用 "Google Drive API"

### 4. 建立服務帳號
- 前往「API 和服務」→「憑證」
- 點擊「建立憑證」→「服務帳號」
- 輸入服務帳號名稱（例如：「order-sheet-service」）
- 點擊「建立並繼續」
- 角色選擇「編輯者」或「擁有者」
- 點擊「完成」

### 5. 下載認證金鑰
- 在服務帳號列表中，點擊剛建立的服務帳號
- 前往「金鑰」標籤
- 點擊「新增金鑰」→「建立新的金鑰」
- 選擇「JSON」格式
- 點擊「建立」，檔案會自動下載

### 6. 放置認證檔案
將下載的 JSON 檔案重新命名為 `credentials.json`，並放在家目錄：
```bash
mv ~/Downloads/你的檔案名稱.json ~/credentials.json
```

### 7. 安裝必要套件
```bash
pip3 install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

### 8. 執行腳本
```bash
cd ~
python3 create_order_sheet.py
```

## 預期結果

執行成功後，你會看到類似以下的輸出：

```
==================================================
統用企業訂單 Google Sheet 創建工具
==================================================

🔗 連接到 Google Sheets...
📄 創建 '統用企業訂單彙總'...
📝 寫入訂單資料到 '百食C_2-23'...
🎨 格式化表頭...
📐 調整欄位寬度...

==================================================
✅ Google Sheet 創建成功！
==================================================

📋 標題：統用企業訂單彙總
📑 分頁：百食C_2-23

🔗 網址：https://docs.google.com/spreadsheets/d/xxxxx...

💡 提示：
   - 請登入 Google 帳號後開啟連結
   - 點擊右上角「分享」可設定權限
==================================================
```

## 訂單資料預覽

創建後的 Google Sheet 將包含以下內容：

| 產品代號 | 產品名稱 | 數量 | 備註 |
|---------|---------|------|------|
| C0078 | 300麥香紅茶 | 80 | |
| C0077 | 300麥香奶茶 | 82/162 | |
| C7402 | 300麥香綠茶 | 30 | |
| C2480 | 600茶裏王日式 | 50 | |
| C7409 | 600茶裏王台式 | 贈 | |

## 常見問題

### Q: 出現 "FileNotFoundError: credentials.json"
A: 認證檔案路徑不正確。請確認檔案放在 `~/credentials.json`

### Q: 出現 "API has not been used" 錯誤
A: 請確認已啟用 Google Sheets API 和 Google Drive API

### Q: 出現權限錯誤
A: 服務帳號需要至少「編輯者」權限

### Q: 如何分享給其他人？
A: 開啟 Sheet 後，點擊右上角「分享」，輸入對方 Gmail 即可

## 參考資源

- [gspread 官方文件](https://docs.gspread.org/)
- [Google Sheets API 文件](https://developers.google.com/sheets/api)
