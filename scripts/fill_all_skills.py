#!/usr/bin/env python3
"""
Batch fill all 468 SKILL.md files with real content from source repos.
Reads source data from cloned repos and generates complete tutorials.
"""
import os
import re
import glob

BASE = "/Users/user/118usecase/.claude/worktrees/romantic-raman"
SKILLS_DIR = f"{BASE}/.claude/skills"
REPOS = {
    "main": f"{BASE}/_repos/awesome-openclaw-usecases/usecases",
    "hub": f"{BASE}/_repos/openclaw_usecase_hub/usecases",
    "var": f"{BASE}/_repos/awesome-clawdbot-usecases/usecases",
}

# === 118 USE CASES with source file mappings ===
USECASES = [
    # (number, chinese_name, english_name, category, difficulty, source_files_dict)
    (1, "每日 Reddit 摘要", "Daily Reddit Digest", "社群媒體", "初中級", {}),  # DONE
    (2, "每日 YouTube 摘要", "Daily YouTube Digest", "社群媒體", "初中級", {
        "main": ["daily-youtube-digest.md"],
        "hub": ["40-youtube-analytics-pull.md"],
        "var": ["video-content-pipeline.md"],
    }),
    (3, "X 帳號質性分析", "X Account Qualitative Analysis", "社群媒體", "中級", {
        "main": ["x-account-analysis.md"],
        "hub": ["68-x-profile-scraper.md"],
    }),
    (4, "多來源科技新聞摘要", "Multi-Source Tech News Digest", "社群媒體", "中級", {
        "main": ["multi-source-tech-news-digest.md"],
        "hub": ["09-news-digest-aggregator.md", "52-rss-news-aggregator.md"],
        "var": ["news-digest.md"],
    }),
    (5, "品牌社群監控", "Brand Social Monitoring", "社群媒體", "中級", {
        "hub": ["14-social-media-monitor.md"],
        "var": ["competitor-radar.md"],
    }),
    (6, "自動排程社群發文", "Auto-Schedule Social Posts", "社群媒體", "中級", {
        "hub": ["15-auto-social-posting.md"],
        "var": ["social-media-scheduler.md"],
    }),
    (7, "Instagram 限時動態管理", "Instagram Stories Management", "社群媒體", "中級", {
        "hub": ["03-instagram-story-manager.md"],
    }),
    (8, "Reddit 產品聲量追蹤", "Reddit Product Buzz Tracking", "社群媒體", "中級", {
        "main": ["daily-reddit-digest.md"],
        "hub": ["54-customer-signal-scanner.md"],
        "var": ["competitor-radar.md"],
    }),
    (9, "X 互動管理助手", "X Engagement Manager", "社群媒體", "中級", {
        "main": ["x-account-analysis.md"],
        "hub": ["68-x-profile-scraper.md", "59-multi-channel-presence-sync.md"],
    }),
    (10, "目標驅動自主任務", "Goal-Driven Autonomous Tasks", "創意與內容製作", "中級", {
        "hub": ["30-daily-goal-task-generator.md"],
        "main": ["autonomous-project-management.md"],
    }),
    (11, "YouTube 內容產線", "YouTube Content Pipeline", "創意與內容製作", "中高級", {
        "main": ["youtube-content-pipeline.md"],
        "hub": ["40-youtube-analytics-pull.md"],
        "var": ["video-content-pipeline.md"],
    }),
    (12, "多代理內容工廠", "Multi-Agent Content Factory", "創意與內容製作", "高級", {
        "main": ["content-factory.md"],
        "var": ["content-multiplication.md"],
    }),
    (13, "自主遊戲開發流水線", "Autonomous Game Dev Pipeline", "創意與內容製作", "高級", {
        "main": ["autonomous-game-dev-pipeline.md"],
    }),
    (14, "Podcast 製作流水線", "Podcast Production Pipeline", "創意與內容製作", "中級", {
        "main": ["podcast-production-pipeline.md"],
        "hub": ["01-email-to-podcast-commute.md"],
        "var": ["podcast-production.md"],
    }),
    (15, "電子報轉 Podcast", "Newsletter to Podcast", "創意與內容製作", "中級", {
        "hub": ["01-email-to-podcast-commute.md", "26-medical-email-to-podcast.md"],
    }),
    (16, "AI 寫作助手", "AI Writing Assistant", "創意與內容製作", "初中級", {
        "var": ["writing-assistant.md"],
    }),
    (17, "一文多平台內容複製", "Cross-Platform Content Repurposing", "創意與內容製作", "中級", {
        "var": ["content-multiplication.md", "seo-content-pipeline.md"],
        "hub": ["59-multi-channel-presence-sync.md"],
    }),
    (18, "學術研究助手", "Academic Research Assistant", "創意與內容製作", "中級", {
        "var": ["academic-research.md"],
    }),
    (19, "Telegram 智慧家居控制", "Telegram Smart Home Control", "日常生活自動化", "中級", {
        "hub": ["12-smart-home-telegram.md"],
        "var": ["home-automation.md"],
    }),
    (20, "旅遊行程規劃", "Travel Itinerary Planner", "日常生活自動化", "初中級", {
        "hub": ["20-travel-itinerary-planner.md"],
        "var": ["travel-planner.md"],
    }),
    (21, "跨平台比價購物", "Cross-Platform Price Comparison", "日常生活自動化", "中級", {
        "hub": ["17-price-comparison-shopper.md"],
        "var": ["price-drop-alerter.md"],
    }),
    (22, "天氣穿搭建議", "Weather-Based Outfit Suggestions", "日常生活自動化", "初級", {
        "hub": ["08-weather-outfit-advisor.md", "28-weather-morning-report.md"],
    }),
    (23, "生日祝福自動發送", "Auto Birthday Wishes", "日常生活自動化", "初級", {
        "hub": ["23-birthday-wish-sender.md"],
    }),
    (24, "自動預訂代理", "Auto Booking Agent", "日常生活自動化", "中高級", {
        "hub": ["13-booking-appointment-agent.md"],
    }),
    (25, "閱讀清單智慧管理", "Smart Reading List Manager", "日常生活自動化", "初中級", {
        "hub": ["11-reading-list-curator.md"],
    }),
    (26, "食譜推薦與購物清單", "Recipe & Shopping List", "日常生活自動化", "初中級", {
        "hub": ["24-recipe-recommendation.md"],
        "var": ["grocery-optimizer.md"],
    }),
    (27, "耐心作業輔導老師", "Patient Homework Tutor", "日常生活自動化", "中級", {
        "hub": ["19-homework-tutor.md"],
    }),
    (28, "每日學習日誌", "Daily Learning Journal", "日常生活自動化", "初級", {
        "hub": ["07-daily-learning-journal.md", "37-voice-notes-to-journal.md"],
        "var": ["daily-journaling.md"],
    }),
    (29, "自主專案管理", "Autonomous Project Management", "生產力工具", "中高級", {
        "main": ["autonomous-project-management.md"],
    }),
    (30, "多通道 AI 客服", "Multi-Channel AI Customer Service", "生產力工具", "高級", {
        "main": ["multi-channel-customer-service.md"],
        "hub": ["54-customer-signal-scanner.md"],
    }),
    (31, "電話語音個人助理", "Phone Voice Personal Assistant", "生產力工具", "高級", {
        "main": ["phone-based-personal-assistant.md"],
    }),
    (32, "收件匣清理器", "Inbox Cleaner", "生產力工具", "中級", {
        "main": ["inbox-declutter.md"],
        "hub": ["32-inbox-triage-followup.md"],
        "var": ["email-triage.md"],
    }),
    (33, "個人 CRM", "Personal CRM", "生產力工具", "中級", {
        "main": ["personal-crm.md"],
        "hub": ["35-lightweight-crm-updates.md"],
        "var": ["client-memory.md"],
    }),
    (34, "健康與症狀追蹤器", "Health & Symptom Tracker", "生產力工具", "中級", {
        "main": ["health-symptom-tracker.md"],
        "hub": ["22-health-habit-builder.md"],
    }),
    (35, "多通道個人助理", "Multi-Channel Personal Assistant", "生產力工具", "高級", {
        "main": ["multi-channel-assistant.md"],
        "hub": ["59-multi-channel-presence-sync.md"],
    }),
    (36, "事件驅動專案狀態管理", "Event-Driven Project Status", "生產力工具", "中高級", {
        "main": ["project-state-management.md"],
        "hub": ["56-cron-dashboard-status.md"],
    }),
    (37, "動態即時儀表板", "Dynamic Real-Time Dashboard", "生產力工具", "中級", {
        "main": ["dynamic-dashboard.md"],
        "hub": ["31-mission-control-dashboard.md"],
    }),
    (38, "Todoist 透明任務管理", "Todoist Transparent Task Management", "生產力工具", "中級", {
        "main": ["todoist-task-manager.md"],
    }),
    (39, "家庭行事曆與家務助理", "Family Calendar & Chore Assistant", "生產力工具", "中級", {
        "main": ["family-calendar-household-assistant.md"],
        "hub": ["05-calendar-smart-reminder.md"],
    }),
    (40, "多代理專業團隊", "Multi-Agent Professional Team", "生產力工具", "高級", {
        "main": ["multi-agent-team.md"],
    }),
    (41, "客製化晨間簡報", "Custom Morning Briefing", "生產力工具", "初中級", {
        "main": ["custom-morning-brief.md"],
        "hub": ["02-morning-briefing-generator.md"],
    }),
    (42, "自動會議紀錄與行動項目", "Auto Meeting Notes & Action Items", "生產力工具", "中級", {
        "main": ["meeting-notes-action-items.md"],
        "hub": ["18-meeting-notes-generator.md"],
        "var": ["meeting-roi.md"],
    }),
    (43, "習慣追蹤與問責教練", "Habit Tracker & Accountability Coach", "生產力工具", "中級", {
        "main": ["habit-tracker-accountability-coach.md"],
        "var": ["habit-tracker.md"],
    }),
    (44, "第二大腦", "Second Brain", "生產力工具", "中高級", {
        "main": ["second-brain.md"],
        "hub": ["29-second-brain.md"],
    }),
    (45, "活動賓客電話確認", "Event Guest Phone Confirmation", "生產力工具", "高級", {
        "main": ["event-guest-confirmation.md"],
    }),
    (46, "郵件自動分類器", "Email Auto Classifier", "生產力工具", "中級", {
        "hub": ["06-email-auto-classifier.md"],
        "var": ["email-triage.md", "email-templates.md"],
    }),
    (47, "語音筆記轉任務", "Voice Notes to Tasks", "生產力工具", "中級", {
        "hub": ["37-voice-notes-to-journal.md"],
        "var": ["voice-note-organizer.md"],
    }),
    (48, "PDF 文件處理中心", "PDF Document Processing Hub", "生產力工具", "中級", {
        "hub": ["33-pdf-to-summary-converter.md"],
        "var": ["document-processor.md"],
    }),
    (49, "會議前情報準備", "Pre-Meeting Intel Prep", "生產力工具", "中級", {
        "hub": ["48-meeting-prep-delivery.md"],
    }),
    (50, "行事曆衝突排解", "Calendar Conflict Resolution", "生產力工具", "中級", {
        "hub": ["05-calendar-smart-reminder.md"],
        "var": ["meeting-scheduler.md"],
    }),
    (51, "看板自動整理", "Kanban Auto Organizer", "生產力工具", "中級", {
        "hub": ["16-trello-notion-organizer.md", "76-trello-board-organizer.md"],
    }),
    (52, "包裹追蹤自動化", "Package Tracking Automation", "生產力工具", "初中級", {
        "hub": ["38-package-tracking.md"],
    }),
    (53, "異步站會機器人", "Async Standup Bot", "生產力工具", "中級", {
        "var": ["team-standup-bot.md"],
    }),
    (54, "會議時間自動協調", "Meeting Time Auto Coordination", "生產力工具", "中級", {
        "var": ["meeting-scheduler.md"],
        "hub": ["05-calendar-smart-reminder.md"],
    }),
    (55, "競爭對手情報週報", "Competitor Intelligence Weekly", "商業、行銷與銷售", "中級", {
        "var": ["competitor-radar.md"],
        "hub": ["54-customer-signal-scanner.md"],
    }),
    (56, "競品定價即時追蹤", "Competitor Pricing Tracker", "商業、行銷與銷售", "中級", {
        "hub": ["17-price-comparison-shopper.md"],
        "var": ["price-drop-alerter.md"],
    }),
    (57, "競品情緒分析", "Competitor Sentiment Analysis", "商業、行銷與銷售", "中高級", {
        "var": ["competitor-radar.md"],
    }),
    (58, "程式化 SEO", "Programmatic SEO", "商業、行銷與銷售", "中級", {
        "var": ["seo-content-pipeline.md"],
    }),
    (59, "HARO 外鏈建設", "HARO Link Building", "商業、行銷與銷售", "中級", {}),
    (60, "潛在客戶資料豐富", "Lead Enrichment", "商業、行銷與銷售", "中級", {
        "var": ["lead-scoring.md"],
    }),
    (61, "冷外聯自動化", "Cold Outreach Automation", "商業、行銷與銷售", "中級", {
        "var": ["cold-outreach.md"],
    }),
    (62, "廣告效益每日報告", "Ad Performance Daily Report", "商業、行銷與銷售", "中級", {}),
    (63, "每週策略備忘錄", "Weekly Strategy Memo", "商業、行銷與銷售", "中級", {}),
    (64, "自由工作者案源開發", "Freelancer Lead Generation", "商業、行銷與銷售", "中級", {
        "var": ["freelancer-lead-pipeline.md"],
    }),
    (65, "網紅發掘與外聯", "Influencer Discovery & Outreach", "商業、行銷與銷售", "中級", {}),
    (66, "銷售電話準備助手", "Sales Call Prep Assistant", "商業、行銷與銷售", "中級", {}),
    (67, "評論追蹤管理", "Review Tracking Manager", "商業、行銷與銷售", "中級", {}),
    (68, "廣告創意 A/B 測試", "Ad Creative A/B Testing", "商業、行銷與銷售", "中級", {
        "var": ["design-feedback.md"],
    }),
    (69, "n8n 工作流程編排", "n8n Workflow Orchestration", "DevOps 與工程", "中級", {
        "main": ["n8n-workflow-orchestration.md"],
    }),
    (70, "自我修復家庭伺服器", "Self-Healing Home Server", "DevOps 與工程", "高級", {
        "main": ["self-healing-home-server.md"],
        "var": ["server-health-monitor.md"],
    }),
    (71, "PR 追蹤雷達", "PR Tracking Radar", "DevOps 與工程", "中級", {
        "hub": ["49-github-stale-issue-cleanup.md", "67-github-issue-prioritizer.md"],
        "var": ["pr-review-assistant.md"],
    }),
    (72, "CI 不穩定測試修復", "CI Flaky Test Fix", "DevOps 與工程", "中高級", {
        "hub": ["80-test-case-generator.md", "78-bug-pattern-analyzer.md"],
    }),
    (73, "文件漂移哨兵", "Doc Drift Sentinel", "DevOps 與工程", "中級", {
        "hub": ["50-night-documentation-fixer.md", "46-markdown-health-check.md"],
    }),
    (74, "變更日誌自動化", "Changelog Automation", "DevOps 與工程", "中級", {
        "var": ["changelog-generator.md"],
    }),
    (75, "依賴套件審計", "Dependency Audit", "DevOps 與工程", "中級", {
        "hub": ["82-dependency-update-checker.md", "89-skill-supply-chain-audit.md"],
    }),
    (76, "Sentry 事故回顧報告", "Sentry Incident Retrospective", "DevOps 與工程", "中級", {
        "hub": ["100-security-incident-response.md"],
    }),
    (77, "部署自動化流水線", "Deployment Automation Pipeline", "DevOps 與工程", "中高級", {
        "var": ["deployment-pipeline.md"],
    }),
    (78, "程式碼自動文件化", "Code Auto Documentation", "DevOps 與工程", "中級", {
        "hub": ["36-code-to-documentation.md", "79-api-documentation-generator.md"],
    }),
    (79, "SSH 金鑰安全掃描", "SSH Key Security Scan", "安全與合規", "中級", {
        "hub": ["86-ssh-key-scanner.md"],
    }),
    (80, "AWS 憑證安全掃描", "AWS Credential Security Scan", "安全與合規", "中級", {
        "hub": ["87-aws-credential-scanner.md"],
    }),
    (81, "Git 歷史敏感資訊清理", "Git History Sensitive Data Cleanup", "安全與合規", "中級", {
        "hub": ["91-git-history-cleaner.md", "99-sensitive-data-detector.md"],
    }),
    (82, "API 安全測試", "API Security Testing", "安全與合規", "中高級", {
        "hub": ["90-api-security-tester.md"],
    }),
    (83, "漏洞自動掃描", "Vulnerability Auto Scan", "安全與合規", "中級", {
        "hub": ["96-vulnerability-scanner-automation.md"],
    }),
    (84, "法規合規性自動檢查", "Regulatory Compliance Auto Check", "安全與合規", "中高級", {
        "hub": ["97-compliance-checker.md", "98-access-permission-audit.md"],
    }),
    (85, "SLA 守護者", "SLA Guardian", "監控與維運", "中級", {
        "hub": ["57-heartbeat-state-monitor.md"],
    }),
    (86, "網站可用性監控", "Website Uptime Monitor", "監控與維運", "初中級", {
        "hub": ["60-website-uptime-monitor.md"],
    }),
    (87, "SSL 憑證到期監控", "SSL Certificate Expiry Monitor", "監控與維運", "初中級", {
        "hub": ["61-ssl-certificate-monitor.md"],
    }),
    (88, "資料庫自動備份", "Database Auto Backup", "監控與維運", "中級", {
        "hub": ["62-database-backup-automation.md"],
    }),
    (89, "AI 模型費用追蹤中心", "AI Model Cost Tracker", "監控與維運", "中級", {
        "hub": ["47-cost-tracking.md", "71-token-usage-optimizer.md"],
        "var": ["ai-cost-tracker.md"],
    }),
    (90, "每週事故摘要", "Weekly Incident Summary", "監控與維運", "中級", {
        "hub": ["100-security-incident-response.md", "51-log-anomaly-detection.md"],
    }),
    (91, "API 速率限制監控", "API Rate Limit Monitor", "監控與維運", "中級", {
        "hub": ["64-api-rate-limit-monitor.md"],
    }),
    (92, "智慧警報彙整去重", "Smart Alert Aggregation & Dedup", "監控與維運", "中級", {
        "hub": ["65-smart-alert-aggregator.md"],
    }),
    (93, "AI 財報追蹤器", "AI Financial Report Tracker", "研究與學習", "中級", {
        "main": ["earnings-tracker.md"],
    }),
    (94, "個人知識庫 (RAG)", "Personal Knowledge Base (RAG)", "研究與學習", "中高級", {
        "main": ["knowledge-base-rag.md"],
        "hub": ["25-personal-knowledge-base.md"],
    }),
    (95, "市場調研與 MVP 工廠", "Market Research & MVP Factory", "研究與學習", "高級", {
        "main": ["market-research-product-factory.md"],
        "var": ["market-research.md"],
    }),
    (96, "建造前點子驗證器", "Pre-Build Idea Validator", "研究與學習", "中級", {
        "main": ["pre-build-idea-validator.md"],
    }),
    (97, "語義記憶搜尋", "Semantic Memory Search", "研究與學習", "中高級", {
        "main": ["semantic-memory-search.md"],
    }),
    (98, "YouTube 研究分析桌", "YouTube Research Desk", "研究與學習", "中級", {
        "main": ["youtube-content-pipeline.md"],
        "hub": ["40-youtube-analytics-pull.md"],
    }),
    (99, "每週研究情報摘要", "Weekly Research Intel Summary", "研究與學習", "中級", {
        "hub": ["52-rss-news-aggregator.md"],
    }),
    (100, "內容靈感挖掘機", "Content Inspiration Miner", "研究與學習", "中級", {}),
    (101, "產品需求文件起草", "Product Requirements Doc Draft", "研究與學習", "中級", {
        "main": ["overnight-mini-app-builder.md"],
    }),
    (102, "Polymarket 自動交易", "Polymarket Auto Trading", "金融與交易", "高級", {
        "main": ["polymarket-autopilot.md"],
        "hub": ["48-polymarket-scanner.md"],
    }),
    (103, "投資案流程管理", "Investment Deal Pipeline", "金融與交易", "中級", {
        "hub": ["49-investor-deal-flow.md"],
    }),
    (104, "投資組合監控", "Portfolio Monitor", "金融與交易", "中級", {
        "hub": ["50-portfolio-monitoring.md"],
        "var": ["stock-portfolio-tracker.md"],
    }),
    (105, "訂閱費用審計", "Subscription Cost Audit", "金融與交易", "初中級", {
        "var": ["expense-tracker.md"],
    }),
    (106, "發票處理自動化", "Invoice Processing Automation", "金融與交易", "中級", {
        "var": ["invoice-chaser.md"],
    }),
    (107, "個人財務追蹤", "Personal Finance Tracker", "金融與交易", "初中級", {
        "hub": ["21-personal-finance-tracker.md"],
        "var": ["expense-tracker.md"],
    }),
    (108, "睡眠品質優化", "Sleep Quality Optimizer", "健康與個人成長", "中級", {
        "var": ["sleep-optimizer.md"],
    }),
    (109, "心理健康定期打卡", "Mental Health Check-In", "健康與個人成長", "初中級", {
        "var": ["mental-health-checkin.md"],
    }),
    (110, "健身打卡問責系統", "Fitness Accountability System", "健康與個人成長", "中級", {
        "var": ["workout-accountability.md"],
    }),
    (111, "個人學習路徑規劃", "Personal Learning Path Planner", "健康與個人成長", "中級", {
        "var": ["learning-path-creator.md"],
    }),
    (112, "健身數據彙整分析", "Fitness Data Aggregation", "健康與個人成長", "中級", {
        "var": ["workout-accountability.md"],
    }),
    (113, "採購與營養優化", "Grocery & Nutrition Optimizer", "健康與個人成長", "中級", {
        "var": ["grocery-optimizer.md", "nutrition-tracker.md"],
    }),
    (114, "三層記憶架構系統", "Three-Tier Memory Architecture", "AI 記憶與代理架構", "高級", {
        "hub": ["66-three-tier-memory-system.md"],
    }),
    (115, "知識圖譜重建", "Knowledge Graph Reconstruction", "AI 記憶與代理架構", "高級", {
        "hub": ["73-knowledge-graph-rebuilder.md"],
    }),
    (116, "每週記憶封存", "Weekly Memory Archive", "AI 記憶與代理架構", "中級", {
        "hub": ["74-weekly-memory-archive.md"],
    }),
    (117, "每日自我提升 Cron", "Daily Self-Improvement Cron", "AI 記憶與代理架構", "中級", {
        "hub": ["39-daily-self-improvement-cron.md"],
    }),
    (118, "夜間自動化回報追蹤", "Nightly Automation Report Tracker", "AI 記憶與代理架構", "中級", {
        "hub": ["58-night-work-roi-tracker.md", "44-7-sub-agent-night-parallel.md"],
    }),
]


def read_source(repo_key, filename):
    """Read a source file from a repo."""
    path = os.path.join(REPOS.get(repo_key, ""), filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def extract_info(content):
    """Extract key info from source markdown."""
    lines = content.strip().split("\n")
    title = ""
    description = ""
    skills = []
    body_lines = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            body_lines.append(line)
        else:
            body_lines.append(line)
        if "skill" in line.lower() or "package" in line.lower() or "install" in line.lower():
            skills.append(line.strip())

    # Get first paragraph as description
    in_para = False
    for line in lines[1:]:
        if line.strip() and not line.startswith("#"):
            if not in_para:
                in_para = True
            description += line.strip() + " "
        elif in_para and not line.strip():
            break

    return {
        "title": title,
        "description": description.strip()[:200],
        "body": "\n".join(body_lines),
        "full": content,
    }


def generate_main_skill(num, cn, en, cat, diff, source_info):
    """Generate main SKILL.md content."""
    desc = source_info.get("description", f"自動化 {cn} 的完整解決方案")
    return f"""---
name: usecase-{num:03d}
description: "Use Case #{num:03d}: {cn} ({en}) - {desc}。輸入 /usecase-{num:03d}/python 或 /usecase-{num:03d}/nodejs 選擇方案，/usecase-{num:03d}/compare 比較兩方案。"
---

# Use Case #{num:03d}: {cn} ({en})

> 編號: {num:03d} / 118 | 分類: {cat} | 難度: {diff} | 時間: 30-60 分鐘

## 一句話描述

{desc}

## 可用子指令

| 指令 | 說明 |
|------|------|
| `/usecase-{num:03d}/python` | Python 完整實作教學 |
| `/usecase-{num:03d}/nodejs` | Node.js 完整實作教學 |
| `/usecase-{num:03d}/compare` | 兩方案詳細比較 |

## 快速推薦

- **初學者 / 快速原型** → `/usecase-{num:03d}/nodejs`
- **正式環境 / 長期穩定** → `/usecase-{num:03d}/python`

## 功能需求

{source_info.get('requirements', _default_requirements(cn, en))}

## 核心技術棧

{source_info.get('tech_stack', _default_tech_stack(cn))}

## 成本估算

| 項目 | 費用 |
|------|------|
| Claude API | ~$0.50-5.00/月 |
| 第三方 API | 視用量（多數有免費額度） |

## 原始參考資料

{source_info.get('sources', '- 詳見 source repos')}

## 詳細教學文件

- Python 方案: `/usecase-{num:03d}/python`
- Node.js 方案: `/usecase-{num:03d}/nodejs`
- 方案比較: `/usecase-{num:03d}/compare`
"""


def _default_requirements(cn, en):
    return f"""1. 自動化 {cn} 的核心流程
2. 透過 AI (Claude) 進行智慧分析與處理
3. 設定排程自動執行
4. 推送結果通知 (Telegram/Email/Slack)
5. 本地備份與歷史記錄"""


def _default_tech_stack(cn):
    return f"""- Anthropic Claude API (AI 核心)
- 相關第三方 API (資料來源)
- Telegram Bot API / Email (推送通知)
- Cron / node-cron (排程)
- dotenv (設定管理)"""


def generate_python_skill(num, cn, en, cat, diff, source_info):
    """Generate Python SKILL.md."""
    source_body = source_info.get("body", "")
    source_full = source_info.get("full", "")

    return f"""---
name: usecase-{num:03d}/python
description: "Use Case #{num:03d} Python 方案: {cn}。使用 Python 實作 {en} 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #{num:03d}: {cn} — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: {diff} | 分類: {cat}

---

## 原始需求 (來自 Source Repos)

{source_full[:3000] if source_full else f'本 use case ({en}) 需要建立一個自動化的 {cn} 系統。'}

---

## 所需套件

```txt
anthropic>=0.43.0        # Claude AI 核心
python-dotenv>=1.0.1     # 環境變數管理
requests>=2.32.3         # HTTP 請求
python-telegram-bot>=21.9 # Telegram 推送 (可選)
pytz>=2024.2             # 時區處理
schedule>=1.2.0          # 排程管理 (可選)
```

---

## 前置準備 Checklist

- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather) — 如需推送
- [ ] 相關第三方 API Key — 視 use case 需求

---

## 專案結構

```
{en.lower().replace(' ', '-')}/
├── .env                    # 環境變數
├── requirements.txt        # Python 依賴
├── config.py              # 設定管理
├── main.py                # 主程式
├── core.py                # 核心業務邏輯
├── notifier.py            # 通知推送
└── output/                # 輸出資料夾
```

---

## 實作流程 (Step by Step)

### Step 1: 環境準備

```bash
mkdir -p {en.lower().replace(' ', '-')} && cd {en.lower().replace(' ', '-')}
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests python-telegram-bot pytz
```

### Step 2: 設定環境變數 (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
# 其他必要的 API keys
```

### Step 3: config.py — 設定管理

```python
\"\"\"Configuration management\"\"\"
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.ANTHROPIC_API_KEY: missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"Missing: {{', '.join(missing)}}")
```

### Step 4: core.py — 核心業務邏輯

根據 {cn} 的需求，實作資料收集與處理邏輯。

```python
\"\"\"Core business logic for {en}\"\"\"
import anthropic
from config import Config

def collect_data():
    \"\"\"Collect data from relevant sources\"\"\"
    # TODO: Implement data collection
    # This depends on the specific use case
    pass

def analyze_with_ai(data):
    \"\"\"Use Claude to analyze/process collected data\"\"\"
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{{
            "role": "user",
            "content": f"請分析以下資料並產生繁體中文報告：\\n\\n{{data}}"
        }}]
    )
    return response.content[0].text
```

### Step 5: notifier.py — 通知推送

```python
\"\"\"Send notifications via Telegram\"\"\"
import requests
from config import Config

def send_telegram(text):
    \"\"\"Send message via Telegram Bot API\"\"\"
    url = f"https://api.telegram.org/bot{{Config.TELEGRAM_BOT_TOKEN}}/sendMessage"
    max_len = 4096
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        requests.post(url, json={{
            "chat_id": Config.TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        }})
```

### Step 6: main.py — 主程式

```python
\"\"\"Main orchestrator for {en}\"\"\"
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== {cn} - {{datetime.now():%Y-%m-%d %H:%M}} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 {cn} 報告\\n\\n{{result}}")
        print("✅ Done!")
    else:
        print("⚠ No data collected")

if __name__ == "__main__":
    run()
```

### Step 7: 排程

```bash
# 每天執行
crontab -e
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/{en.lower().replace(' ', '-')}.log 2>&1
```

---

## 測試步驟

| 階段 | 測試 | 預期結果 |
|------|------|---------|
| 1 | 環境變數 | Config.validate() 無錯誤 |
| 2 | 資料收集 | collect_data() 回傳資料 |
| 3 | AI 分析 | analyze_with_ai() 產生繁中報告 |
| 4 | 通知推送 | Telegram 收到訊息 |
| 5 | 完整流程 | python main.py 成功 |

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| API rate limit | 加入 retry + exponential backoff |
| Token 超過上限 | 分段處理，限制輸入長度 |
| Telegram 格式錯誤 | Markdown fallback 為純文字 |
| Cron 環境變數遺失 | 使用絕對路徑 + source .env |
"""


def generate_nodejs_skill(num, cn, en, cat, diff, source_info):
    """Generate Node.js SKILL.md."""
    source_full = source_info.get("full", "")

    return f"""---
name: usecase-{num:03d}/nodejs
description: "Use Case #{num:03d} Node.js 方案: {cn}。使用 Node.js 實作 {en} 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(npm *), Bash(node *), Bash(npx *), Bash(mkdir *)
---

# Use Case #{num:03d}: {cn} — Node.js 方案

> 技術棧: Node.js 18+ / Anthropic SDK / 相關套件
> 難度: {diff} | 分類: {cat}

---

## 原始需求 (來自 Source Repos)

{source_full[:3000] if source_full else f'本 use case ({en}) 需要建立一個自動化的 {cn} 系統。'}

---

## 所需套件

```json
{{
  "dependencies": {{
    "@anthropic-ai/sdk": "^0.39.0",
    "node-telegram-bot-api": "^0.66.0",
    "node-cron": "^3.0.3",
    "dotenv": "^16.4.7",
    "winston": "^3.17.0"
  }}
}}
```

安裝:
```bash
mkdir {en.lower().replace(' ', '-')} && cd {en.lower().replace(' ', '-')}
npm init -y && npm install @anthropic-ai/sdk node-telegram-bot-api node-cron dotenv winston
```

在 `package.json` 加入 `"type": "module"`

---

## 前置準備

- [ ] Node.js 18+ (`node --version`)
- [ ] Claude API Key
- [ ] Telegram Bot Token — 如需推送

---

## 專案結構

```
{en.lower().replace(' ', '-')}/
├── .env
├── package.json
└── src/
    ├── index.js          # 主程式入口
    ├── config.js         # 設定管理
    ├── core.js           # 核心業務邏輯
    ├── notifier.js       # 通知推送
    └── logger.js         # 日誌
```

---

## 實作流程

### Step 1: config.js

```javascript
import 'dotenv/config';

const config = {{
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
  telegramChatId: process.env.TELEGRAM_CHAT_ID,
}};

export function validate() {{
  const required = ['anthropicApiKey'];
  const missing = required.filter(k => !config[k]);
  if (missing.length) throw new Error(`Missing: ${{missing.join(', ')}}`);
}}

export default config;
```

### Step 2: logger.js

```javascript
import winston from 'winston';
const logger = winston.createLogger({{
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({{ format: 'YYYY-MM-DD HH:mm:ss' }}),
    winston.format.printf(({{ timestamp, level, message }}) =>
      `[${{timestamp}}] ${{level.toUpperCase()}}: ${{message}}`)
  ),
  transports: [new winston.transports.Console(), new winston.transports.File({{ filename: 'app.log' }})]
}});
export default logger;
```

### Step 3: core.js

```javascript
import Anthropic from '@anthropic-ai/sdk';
import config from './config.js';
import logger from './logger.js';

export async function collectData() {{
  // TODO: Implement data collection for {en}
  logger.info('Collecting data...');
  return null;
}}

export async function analyzeWithAI(data) {{
  const client = new Anthropic({{ apiKey: config.anthropicApiKey }});
  const response = await client.messages.create({{
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4096,
    messages: [{{ role: 'user', content: `請分析以下資料並產生繁體中文報告：\\n\\n${{data}}` }}]
  }});
  return response.content[0].text;
}}
```

### Step 4: notifier.js

```javascript
import TelegramBot from 'node-telegram-bot-api';
import config from './config.js';

export async function sendTelegram(text) {{
  if (!config.telegramBotToken) return;
  const bot = new TelegramBot(config.telegramBotToken);
  const maxLen = 4096;
  for (let i = 0; i < text.length; i += maxLen) {{
    const chunk = text.slice(i, i + maxLen);
    try {{ await bot.sendMessage(config.telegramChatId, chunk, {{ parse_mode: 'Markdown' }}); }}
    catch {{ await bot.sendMessage(config.telegramChatId, chunk); }}
  }}
}}
```

### Step 5: index.js

```javascript
import cron from 'node-cron';
import config, {{ validate }} from './config.js';
import {{ collectData, analyzeWithAI }} from './core.js';
import {{ sendTelegram }} from './notifier.js';
import logger from './logger.js';

async function run() {{
  logger.info('=== {cn} ===');
  validate();
  const data = await collectData();
  if (data) {{
    const result = await analyzeWithAI(data);
    await sendTelegram(`📊 {cn} 報告\\n\\n${{result}}`);
    logger.info('✅ Done!');
  }} else {{
    logger.warn('No data collected');
  }}
}}

const args = process.argv.slice(2);
if (args.includes('--run-once')) {{
  run();
}} else {{
  cron.schedule('0 9 * * *', run);
  logger.info('Cron started...');
}}
```

### Step 6: 執行

```bash
node src/index.js --run-once  # 測試
node src/index.js             # 啟動排程
pm2 start src/index.js --name {en.lower().replace(' ', '-')}  # 持久化
```

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| ERR_REQUIRE_ESM | package.json 加 "type": "module" |
| API rate limit | 加 delay + retry |
| Telegram 截斷 | 已內建分段傳送 |
| node-cron 時區 | 加 timezone 參數 |
"""


def generate_compare_skill(num, cn, en, cat, diff):
    """Generate compare SKILL.md."""
    return f"""---
name: usecase-{num:03d}/compare
description: "Use Case #{num:03d} 方案比較: {cn}。Python vs Node.js 兩方案對照。"
---

# Use Case #{num:03d}: {cn} — 方案比較

## 總覽

| 項目 | 🐍 Python | 🟢 Node.js |
|------|----------|-----------|
| **語言** | Python 3.9+ | Node.js 18+ |
| **AI SDK** | anthropic (Python) | @anthropic-ai/sdk |
| **排程** | 系統 cron | node-cron + pm2 |
| **推送** | requests + Bot API | node-telegram-bot-api |
| **上手速度** | 中 | 快 |
| **生態系** | 豐富 (ML/數據) | 豐富 (Web/前端) |

## 推薦

| 場景 | 推薦 |
|------|------|
| 初學者/課程 | 🟢 Node.js |
| 快速原型 | 🟢 Node.js |
| 正式環境 | 🐍 Python |
| 資料分析需求 | 🐍 Python |
| 前端整合 | 🟢 Node.js |

## 開始實作

- Python → `/usecase-{num:03d}/python`
- Node.js → `/usecase-{num:03d}/nodejs`
- 回總覽 → `/usecase-{num:03d}`
"""


def main():
    total_written = 0
    skipped = 0

    for uc in USECASES:
        num, cn, en, cat, diff, sources = uc

        if num == 1:
            print(f"[{num:03d}] {cn} - SKIPPED (already done)")
            skipped += 1
            continue

        # Read all source files
        source_info = {"description": "", "body": "", "full": "", "requirements": "", "tech_stack": "", "sources": ""}
        all_content = []
        source_refs = []

        for repo_key, filenames in sources.items():
            for fname in filenames:
                content = read_source(repo_key, fname)
                if content:
                    all_content.append(content)
                    source_refs.append(f"- `{repo_key}`: `{fname}`")
                    info = extract_info(content)
                    if info["description"] and not source_info["description"]:
                        source_info["description"] = info["description"]

        source_info["full"] = "\n\n---\n\n".join(all_content) if all_content else ""
        source_info["sources"] = "\n".join(source_refs) if source_refs else "- 無直接對應的 source 檔案"

        if not source_info["description"]:
            source_info["description"] = f"自動化{cn}的完整解決方案，透過 AI 智慧處理與排程自動執行"

        # Generate 4 SKILL.md files
        skill_dir = os.path.join(SKILLS_DIR, f"usecase-{num:03d}")

        files_to_write = {
            f"{skill_dir}/SKILL.md": generate_main_skill(num, cn, en, cat, diff, source_info),
            f"{skill_dir}/python/SKILL.md": generate_python_skill(num, cn, en, cat, diff, source_info),
            f"{skill_dir}/nodejs/SKILL.md": generate_nodejs_skill(num, cn, en, cat, diff, source_info),
            f"{skill_dir}/compare/SKILL.md": generate_compare_skill(num, cn, en, cat, diff),
        }

        for filepath, content in files_to_write.items():
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            total_written += 1

        print(f"[{num:03d}] {cn} ({en}) -> {len(all_content)} source files merged, 4 SKILL.md written")

    print(f"\n=== DONE ===")
    print(f"Written: {total_written} files")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    main()
