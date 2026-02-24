#!/usr/bin/env python3
"""
統用企業訂單 Google Sheet 創建腳本
使用前請先設置 Google Sheets API 認證
"""

import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
import os
import sys

# ============== 設定 ==============
# Google Sheet 標題
SHEET_TITLE = "統用企業訂單彙總"

# 第一個分頁名稱
SHEET_NAME = "百食C_2-23"

# 認證檔案路徑 (請修改為你的認證檔案路徑)
CREDENTIALS_FILE = os.path.expanduser("~/credentials.json")

# ============== 訂單資料 ==============
ORDER_DATA = [
    # 表頭
    ["產品代號", "產品名稱", "數量", "備註"],
    # 麥香系列
    ["C0078", "300麥香紅茶", "80", ""],
    ["C0077", "300麥香奶茶", "82/162", ""],
    ["C7402", "300麥香綠茶", "30", ""],
    # 茶裏王系列
    ["C2480", "600茶裏王日式", "50", ""],
    # 贈品區
    ["C7409", "600茶裏王台式", "贈", ""],
]

# ============== 設定欄位寬度 ==============
COLUMN_WIDTHS = {
    'A': 12,  # 產品代號
    'B': 20,  # 產品名稱
    'C': 10,  # 數量
    'D': 15,  # 備註
}


def setup_credentials():
    """設置 Google API 認證"""
    # 檢查認證檔案是否存在
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ 錯誤：找不到認證檔案 {CREDENTIALS_FILE}")
        print("\n請按照以下步驟設置 Google Sheets API 認證：")
        print("1. 前往 https://console.cloud.google.com/")
        print("2. 創建新專案或選擇現有專案")
        print("3. 啟用 Google Sheets API 和 Google Drive API")
        print("4. 建立服務帳號 (Service Account)")
        print("5. 下載 JSON 格式的認證金鑰")
        print(f"6. 將認證檔案放在 {CREDENTIALS_FILE}")
        print("\n詳細教學：https://docs.gspread.org/en/latest/oauth2.html")
        return None
    
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=scopes
        )
        return credentials
    except Exception as e:
        print(f"❌ 認證失敗：{e}")
        return None


def create_sheet():
    """創建 Google Sheet"""
    credentials = setup_credentials()
    if not credentials:
        return None
    
    try:
        # 連接到 Google Sheets
        print("🔗 連接到 Google Sheets...")
        gc = gspread.authorize(credentials)
        
        # 創建新 Spreadsheet
        print(f"📄 創建 '{SHEET_TITLE}'...")
        spreadsheet = gc.create(SHEET_TITLE)
        
        # 取得第一個工作表並重新命名
        worksheet = spreadsheet.sheet1
        worksheet.update_title(SHEET_NAME)
        
        # 寫入資料
        print(f"📝 寫入訂單資料到 '{SHEET_NAME}'...")
        worksheet.update(ORDER_DATA)
        
        # 格式化表頭（加粗、背景色）
        print("🎨 格式化表頭...")
        worksheet.format('A1:D1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
            'horizontalAlignment': 'CENTER'
        })
        
        # 設定欄位寬度
        print("📐 調整欄位寬度...")
        for col, width in COLUMN_WIDTHS.items():
            worksheet.format(f'{col}:{col}', {
                'horizontalAlignment': 'CENTER'
            })
        
        # 設定儲存格對齊
        worksheet.format('A2:D6', {
            'horizontalAlignment': 'CENTER'
        })
        
        # 設定分享權限（可選：設為任何人都可以查看）
        # spreadsheet.share('', perm_type='anyone', role='reader')
        
        # 取得網址
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        
        print("\n" + "="*50)
        print("✅ Google Sheet 創建成功！")
        print("="*50)
        print(f"\n📋 標題：{SHEET_TITLE}")
        print(f"📑 分頁：{SHEET_NAME}")
        print(f"\n🔗 網址：{sheet_url}")
        print("\n💡 提示：")
        print("   - 請登入 Google 帳號後開啟連結")
        print("   - 點擊右上角「分享」可設定權限")
        print("="*50)
        
        return sheet_url
        
    except gspread.exceptions.APIError as e:
        print(f"❌ Google API 錯誤：{e}")
        return None
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        return None


def main():
    """主程式"""
    print("="*50)
    print("統用企業訂單 Google Sheet 創建工具")
    print("="*50)
    print()
    
    url = create_sheet()
    
    if url:
        return 0
    else:
        print("\n❌ 創建失敗，請檢查上述錯誤訊息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
