#!/usr/bin/env python3
"""
OpenClaw X 平台智能分析 - Cron 入口
統一改為網站版輸出（對齊 x.deepsrt.com 風格），避免使用任何虛構 tweet_id。
"""

from generate_x_monitor_web_report import main as web_main


if __name__ == "__main__":
    web_main()
