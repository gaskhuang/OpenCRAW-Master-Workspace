#!/usr/bin/env python3
"""
Rename all skill folders from usecase-NNN to descriptive Chinese+English names.
Also updates all internal references in SKILL.md files.
"""
import os
import re
import shutil

BASE = "/Users/user/118usecase/.claude/worktrees/romantic-raman"
SKILLS_DIR = f"{BASE}/.claude/skills"

# All 118 use cases: (number, chinese_name, english_name)
USECASES = [
    (1, "每日 Reddit 摘要", "Daily Reddit Digest"),
    (2, "每日 YouTube 摘要", "Daily YouTube Digest"),
    (3, "X 帳號質性分析", "X Account Qualitative Analysis"),
    (4, "多來源科技新聞摘要", "Multi-Source Tech News Digest"),
    (5, "品牌社群監控", "Brand Social Monitoring"),
    (6, "自動排程社群發文", "Auto-Schedule Social Posts"),
    (7, "Instagram 限時動態管理", "Instagram Stories Management"),
    (8, "Reddit 產品聲量追蹤", "Reddit Product Buzz Tracking"),
    (9, "X 互動管理助手", "X Engagement Manager"),
    (10, "目標驅動自主任務", "Goal-Driven Autonomous Tasks"),
    (11, "YouTube 內容產線", "YouTube Content Pipeline"),
    (12, "多代理內容工廠", "Multi-Agent Content Factory"),
    (13, "自主遊戲開發流水線", "Autonomous Game Dev Pipeline"),
    (14, "Podcast 製作流水線", "Podcast Production Pipeline"),
    (15, "電子報轉 Podcast", "Newsletter to Podcast"),
    (16, "AI 寫作助手", "AI Writing Assistant"),
    (17, "一文多平台內容複製", "Cross-Platform Content Repurposing"),
    (18, "學術研究助手", "Academic Research Assistant"),
    (19, "Telegram 智慧家居控制", "Telegram Smart Home Control"),
    (20, "旅遊行程規劃", "Travel Itinerary Planner"),
    (21, "跨平台比價購物", "Cross-Platform Price Comparison"),
    (22, "天氣穿搭建議", "Weather-Based Outfit Suggestions"),
    (23, "生日祝福自動發送", "Auto Birthday Wishes"),
    (24, "自動預訂代理", "Auto Booking Agent"),
    (25, "閱讀清單智慧管理", "Smart Reading List Manager"),
    (26, "食譜推薦與購物清單", "Recipe & Shopping List"),
    (27, "耐心作業輔導老師", "Patient Homework Tutor"),
    (28, "每日學習日誌", "Daily Learning Journal"),
    (29, "自主專案管理", "Autonomous Project Management"),
    (30, "多通道 AI 客服", "Multi-Channel AI Customer Service"),
    (31, "電話語音個人助理", "Phone Voice Personal Assistant"),
    (32, "收件匣清理器", "Inbox Cleaner"),
    (33, "個人 CRM", "Personal CRM"),
    (34, "健康與症狀追蹤器", "Health & Symptom Tracker"),
    (35, "多通道個人助理", "Multi-Channel Personal Assistant"),
    (36, "事件驅動專案狀態管理", "Event-Driven Project Status"),
    (37, "動態即時儀表板", "Dynamic Real-Time Dashboard"),
    (38, "Todoist 透明任務管理", "Todoist Transparent Task Management"),
    (39, "家庭行事曆與家務助理", "Family Calendar & Chore Assistant"),
    (40, "多代理專業團隊", "Multi-Agent Professional Team"),
    (41, "客製化晨間簡報", "Custom Morning Briefing"),
    (42, "自動會議紀錄與行動項目", "Auto Meeting Notes & Action Items"),
    (43, "習慣追蹤與問責教練", "Habit Tracker & Accountability Coach"),
    (44, "第二大腦", "Second Brain"),
    (45, "活動賓客電話確認", "Event Guest Phone Confirmation"),
    (46, "郵件自動分類器", "Email Auto Classifier"),
    (47, "語音筆記轉任務", "Voice Notes to Tasks"),
    (48, "PDF 文件處理中心", "PDF Document Processing Hub"),
    (49, "會議前情報準備", "Pre-Meeting Intel Prep"),
    (50, "行事曆衝突排解", "Calendar Conflict Resolution"),
    (51, "看板自動整理", "Kanban Auto Organizer"),
    (52, "包裹追蹤自動化", "Package Tracking Automation"),
    (53, "異步站會機器人", "Async Standup Bot"),
    (54, "會議時間自動協調", "Meeting Time Auto Coordination"),
    (55, "競爭對手情報週報", "Competitor Intelligence Weekly"),
    (56, "競品定價即時追蹤", "Competitor Pricing Tracker"),
    (57, "競品情緒分析", "Competitor Sentiment Analysis"),
    (58, "程式化 SEO", "Programmatic SEO"),
    (59, "HARO 外鏈建設", "HARO Link Building"),
    (60, "潛在客戶資料豐富", "Lead Enrichment"),
    (61, "冷外聯自動化", "Cold Outreach Automation"),
    (62, "廣告效益每日報告", "Ad Performance Daily Report"),
    (63, "每週策略備忘錄", "Weekly Strategy Memo"),
    (64, "自由工作者案源開發", "Freelancer Lead Generation"),
    (65, "網紅發掘與外聯", "Influencer Discovery & Outreach"),
    (66, "銷售電話準備助手", "Sales Call Prep Assistant"),
    (67, "評論追蹤管理", "Review Tracking Manager"),
    (68, "廣告創意 A/B 測試", "Ad Creative A-B Testing"),
    (69, "n8n 工作流程編排", "n8n Workflow Orchestration"),
    (70, "自我修復家庭伺服器", "Self-Healing Home Server"),
    (71, "PR 追蹤雷達", "PR Tracking Radar"),
    (72, "CI 不穩定測試修復", "CI Flaky Test Fix"),
    (73, "文件漂移哨兵", "Doc Drift Sentinel"),
    (74, "變更日誌自動化", "Changelog Automation"),
    (75, "依賴套件審計", "Dependency Audit"),
    (76, "Sentry 事故回顧報告", "Sentry Incident Retrospective"),
    (77, "部署自動化流水線", "Deployment Automation Pipeline"),
    (78, "程式碼自動文件化", "Code Auto Documentation"),
    (79, "SSH 金鑰安全掃描", "SSH Key Security Scan"),
    (80, "AWS 憑證安全掃描", "AWS Credential Security Scan"),
    (81, "Git 歷史敏感資訊清理", "Git History Sensitive Data Cleanup"),
    (82, "API 安全測試", "API Security Testing"),
    (83, "漏洞自動掃描", "Vulnerability Auto Scan"),
    (84, "法規合規性自動檢查", "Regulatory Compliance Auto Check"),
    (85, "SLA 守護者", "SLA Guardian"),
    (86, "網站可用性監控", "Website Uptime Monitor"),
    (87, "SSL 憑證到期監控", "SSL Certificate Expiry Monitor"),
    (88, "資料庫自動備份", "Database Auto Backup"),
    (89, "AI 模型費用追蹤中心", "AI Model Cost Tracker"),
    (90, "每週事故摘要", "Weekly Incident Summary"),
    (91, "API 速率限制監控", "API Rate Limit Monitor"),
    (92, "智慧警報彙整去重", "Smart Alert Aggregation & Dedup"),
    (93, "AI 財報追蹤器", "AI Financial Report Tracker"),
    (94, "個人知識庫 (RAG)", "Personal Knowledge Base RAG"),
    (95, "市場調研與 MVP 工廠", "Market Research & MVP Factory"),
    (96, "建造前點子驗證器", "Pre-Build Idea Validator"),
    (97, "語義記憶搜尋", "Semantic Memory Search"),
    (98, "YouTube 研究分析桌", "YouTube Research Desk"),
    (99, "每週研究情報摘要", "Weekly Research Intel Summary"),
    (100, "內容靈感挖掘機", "Content Inspiration Miner"),
    (101, "產品需求文件起草", "Product Requirements Doc Draft"),
    (102, "Polymarket 自動交易", "Polymarket Auto Trading"),
    (103, "投資案流程管理", "Investment Deal Pipeline"),
    (104, "投資組合監控", "Portfolio Monitor"),
    (105, "訂閱費用審計", "Subscription Cost Audit"),
    (106, "發票處理自動化", "Invoice Processing Automation"),
    (107, "個人財務追蹤", "Personal Finance Tracker"),
    (108, "睡眠品質優化", "Sleep Quality Optimizer"),
    (109, "心理健康定期打卡", "Mental Health Check-In"),
    (110, "健身打卡問責系統", "Fitness Accountability System"),
    (111, "個人學習路徑規劃", "Personal Learning Path Planner"),
    (112, "健身數據彙整分析", "Fitness Data Aggregation"),
    (113, "採購與營養優化", "Grocery & Nutrition Optimizer"),
    (114, "三層記憶架構系統", "Three-Tier Memory Architecture"),
    (115, "知識圖譜重建", "Knowledge Graph Reconstruction"),
    (116, "每週記憶封存", "Weekly Memory Archive"),
    (117, "每日自我提升 Cron", "Daily Self-Improvement Cron"),
    (118, "夜間自動化回報追蹤", "Nightly Automation Report Tracker"),
]


def make_folder_name(num, cn, en):
    """Create folder name like: 每日 Reddit 摘要 (Daily Reddit Digest)"""
    return f"{cn} ({en})"


def update_skill_md(filepath, old_name, new_name, num, cn, en):
    """Update a SKILL.md file: frontmatter name, descriptions, internal links."""
    if not os.path.exists(filepath):
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    old_folder = f"usecase-{num:03d}"
    new_folder = make_folder_name(num, cn, en)

    # Update name in frontmatter
    content = content.replace(f"name: usecase-{num:03d}/", f"name: {new_folder}/")
    content = content.replace(f"name: usecase-{num:03d}\n", f"name: {new_folder}\n")
    content = content.replace(f'name: "usecase-{num:03d}/', f'name: "{new_folder}/')
    content = content.replace(f'name: "usecase-{num:03d}"', f'name: "{new_folder}"')

    # Update all /usecase-NNN references (slash commands)
    content = content.replace(f"/usecase-{num:03d}/python", f"/{new_folder}/python")
    content = content.replace(f"/usecase-{num:03d}/nodejs", f"/{new_folder}/nodejs")
    content = content.replace(f"/usecase-{num:03d}/compare", f"/{new_folder}/compare")
    content = content.replace(f"/usecase-{num:03d}`", f"/{new_folder}`")

    # Update description references
    content = content.replace(f"Use Case #{num:03d}", f"Use Case #{num:03d}")  # keep as-is

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def update_index(index_path):
    """Update the usecase-index/SKILL.md with new folder names."""
    if not os.path.exists(index_path):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    for num, cn, en in USECASES:
        old_ref = f"usecase-{num:03d}"
        new_ref = make_folder_name(num, cn, en)
        content = content.replace(f"/usecase-{num:03d}/", f"/{new_ref}/")
        content = content.replace(f"/usecase-{num:03d}`", f"/{new_ref}`")
        content = content.replace(f"/usecase-{num:03d} ", f"/{new_ref} ")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    renamed = 0
    updated_files = 0
    errors = []

    # Phase 1: Rename all directories
    print("=" * 60)
    print("Phase 1: Renaming directories")
    print("=" * 60)

    for num, cn, en in USECASES:
        old_dir = os.path.join(SKILLS_DIR, f"usecase-{num:03d}")
        new_folder = make_folder_name(num, cn, en)
        new_dir = os.path.join(SKILLS_DIR, new_folder)

        if not os.path.exists(old_dir):
            print(f"  SKIP: {old_dir} does not exist")
            continue

        if os.path.exists(new_dir):
            print(f"  SKIP: {new_dir} already exists")
            continue

        try:
            os.rename(old_dir, new_dir)
            renamed += 1
            print(f"  ✓ usecase-{num:03d} → {new_folder}")
        except Exception as e:
            errors.append(f"usecase-{num:03d}: {e}")
            print(f"  ✗ usecase-{num:03d}: {e}")

    # Phase 2: Update all SKILL.md files inside renamed directories
    print("\n" + "=" * 60)
    print("Phase 2: Updating SKILL.md internal references")
    print("=" * 60)

    for num, cn, en in USECASES:
        new_folder = make_folder_name(num, cn, en)
        skill_dir = os.path.join(SKILLS_DIR, new_folder)

        if not os.path.exists(skill_dir):
            continue

        # Update main SKILL.md
        main_skill = os.path.join(skill_dir, "SKILL.md")
        if update_skill_md(main_skill, f"usecase-{num:03d}", new_folder, num, cn, en):
            updated_files += 1

        # Update sub-skills
        for sub in ["python", "nodejs", "compare"]:
            sub_skill = os.path.join(skill_dir, sub, "SKILL.md")
            if update_skill_md(sub_skill, f"usecase-{num:03d}", new_folder, num, cn, en):
                updated_files += 1

    # Phase 3: Update index
    print("\n" + "=" * 60)
    print("Phase 3: Updating usecase-index")
    print("=" * 60)

    index_path = os.path.join(SKILLS_DIR, "usecase-index", "SKILL.md")
    if os.path.exists(index_path):
        update_index(index_path)
        print("  ✓ Updated usecase-index/SKILL.md")
    else:
        print("  SKIP: usecase-index/SKILL.md not found")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Directories renamed: {renamed}")
    print(f"  SKILL.md files updated: {updated_files}")
    print(f"  Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"    - {e}")


if __name__ == "__main__":
    main()
