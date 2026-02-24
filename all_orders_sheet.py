#!/usr/bin/env python3
"""
統一訂單 Google Sheet 創建腳本
同時處理百佳和百食C兩張訂單
"""

import gspread
from google.oauth2 import service_account
import os
import sys
import csv

# ============== 設定 ==============
SHEET_TITLE = "統用企業訂單彙總_2025-02-24"

# 認證檔案路徑
CREDENTIALS_FILE = os.path.expanduser("~/credentials.json")

# CSV 檔案路徑
BAIJIA_CSV = "baijia_order_605754.csv"
BAISHI_CSV = "訂單_百食C_2-23.csv"

# ============== 欄位寬度設定 ==============
COLUMN_WIDTHS = {
    'A': 12,  # 代號/產品代號
    'B': 35,  # 品名/產品名稱
    'C': 10,  # 數量
    'D': 10,  # 單價
    'E': 15,  # 備註
}


def read_csv_file(filepath):
    """讀取 CSV 檔案並回傳資料列表"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"❌ 讀取 {filepath} 失敗：{e}")
        return None


def setup_credentials():
    """設置 Google API 認證"""
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ 錯誤：找不到認證檔案 {CREDENTIALS_FILE}")
        print("\n請按照 GOOGLE_SHEETS_SETUP.md 的步驟設置認證")
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


def format_worksheet(ws, row_count):
    """格式化工作表"""
    # 格式化表頭
    ws.format('A1:E1', {
        'textFormat': {'bold': True},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
        'horizontalAlignment': 'CENTER'
    })
    
    # 設定欄位寬度和對齊
    for col, width in COLUMN_WIDTHS.items():
        ws.format(f'{col}:{col}', {
            'horizontalAlignment': 'CENTER'
        })
    
    # 設定資料列對齊
    if row_count > 1:
        ws.format(f'A2:E{row_count}', {
            'horizontalAlignment': 'CENTER'
        })


def create_combined_sheet():
    """創建統一訂單 Google Sheet"""
    credentials = setup_credentials()
    if not credentials:
        return None
    
    # 讀取兩個 CSV 檔案
    print("📂 讀取訂單資料...")
    
    baijia_data = read_csv_file(BAIJIA_CSV)
    if not baijia_data:
        return None
    
    baishi_data = read_csv_file(BAISHI_CSV)
    if not baishi_data:
        return None
    
    print(f"  ✓ 百佳訂單：{len(baijia_data)} 行")
    print(f"  ✓ 百食C訂單：{len(baishi_data)} 行")
    
    try:
        print("\n🔗 連接到 Google Sheets...")
        gc = gspread.authorize(credentials)
        
        # 創建新 Spreadsheet
        print(f"📄 創建 '{SHEET_TITLE}'...")
        spreadsheet = gc.create(SHEET_TITLE)
        
        # ========== 第一個分頁：百佳訂單 ==========
        ws1 = spreadsheet.sheet1
        ws1.update_title("百佳_605754")
        
        print("📝 寫入百佳訂單...")
        ws1.update(baijia_data)
        format_worksheet(ws1, len(baijia_data))
        
        # ========== 第二個分頁：百食C訂單 ==========
        ws2 = spreadsheet.add_worksheet(title="百食C_2-23", rows="100", cols="10")
        
        print("📝 寫入百食C訂單...")
        ws2.update(baishi_data)
        format_worksheet(ws2, len(baishi_data))
        
        # 取得網址
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        
        print("\n" + "="*60)
        print("✅ Google Sheet 創建成功！")
        print("="*60)
        print(f"\n📋 標題：{SHEET_TITLE}")
        print(f"📑 分頁：")
        print(f"   • 百佳_605754 ({len(baijia_data)-1} 項產品)")
        print(f"   • 百食C_2-23 ({len(baishi_data)-1} 項產品)")
        print(f"\n🔗 網址：{sheet_url}")
        print("\n💡 提示：")
        print("   - 請登入 Google 帳號後開啟連結")
        print("   - 點擊右上角「分享」可設定權限")
        print("="*60)
        
        return sheet_url
        
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        return None


def main():
    """主程式"""
    print("="*60)
    print("統用企業訂單 Google Sheet 統一創建工具")
    print("="*60)
    print()
    
    url = create_combined_sheet()
    
    if url:
        return 0
    else:
        print("\n❌ 創建失敗，請檢查上述錯誤訊息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
