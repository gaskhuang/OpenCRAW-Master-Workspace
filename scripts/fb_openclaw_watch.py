#!/usr/bin/env python3
"""
Facebook OpenClaw 監控腳本
功能：與 Reddit 監控相同格式（中文標題、三行摘要、按讚排序）
"""
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
import subprocess

KEYWORD = "OpenClaw"
CHAT_ID = "7132792298"
CHANNEL = "telegram"
ACCOUNT = "default"
STATE_PATH = Path("/Users/user/data/fb_openclaw_seen.json")
REPORT_DIR = Path("/Users/user/reports/openclaw-monitoring")
TASK_STATE_PATH = Path("/Users/user/memory/TASK_STATE.json")
WINDOW_SECONDS = 3 * 60 * 60  # 3 小時

# 簡易標題翻譯對照表
TITLE_TRANSLATIONS = {
    "how to": "如何", "build": "建立", "guide": "指南", "tutorial": "教學",
    "error": "錯誤", "issue": "問題", "bug": "漏洞", "fix": "修復",
    "update": "更新", "new": "新", "best": "最佳", "free": "免費",
    "openclaw": "OpenClaw", "ai": "AI", "agent": "Agent", "model": "模型",
    "setup": "設定", "install": "安裝", "configuration": "配置",
    "help": "幫助", "question": "問題", "tip": "技巧", "review": "評測",
    "comparison": "比較", "cloud": "雲端", "local": "本地", "server": "伺服器",
    "bot": "機器人", "automation": "自動化", "workflow": "工作流程",
    "api": "API", "deploy": "部署", "hosting": "託管", "vps": "VPS",
    "docker": "Docker", "beginner": "新手", "advanced": "進階",
    "pro": "專業", "2026": "2026", "version": "版本", "release": "發布",
    "breaking": "重大變更", "feature": "功能", "feedback": "回饋",
    "discussion": "討論", "news": "新聞", "project": "專案", "tool": "工具",
    "script": "腳本", "plugin": "外掛", "skill": "技能", "prompt": "提示詞",
    "template": "範本", "example": "範例", "test": "測試", "performance": "效能",
    "speed": "速度", "memory": "記憶體", "cost": "成本", "price": "價格",
    "limit": "限制", "quota": "配額", "timeout": "逾時", "fail": "失敗",
    "success": "成功", "working": "運作中", "broken": "損壞",
    "upgrade": "升級", "backup": "備份", "sync": "同步", "share": "分享",
    "team": "團隊", "business": "商業", "developer": "開發者",
    "user": "使用者", "community": "社群", "support": "支援",
    "documentation": "文件", "debug": "除錯", "log": "日誌",
    "monitor": "監控", "alert": "警報", "notification": "通知",
    "schedule": "排程", "daily": "每日", "real-time": "即時",
    "async": "非同步", "parallel": "平行", "task": "作業",
    "management": "管理", "security": "安全", "privacy": "隱私",
    "encryption": "加密", "certificate": "憑證", "url": "URL",
    "search": "搜尋", "filter": "過濾", "sort": "排序",
    "rank": "排名", "score": "分數", "vote": "投票", "like": "喜歡",
    "favorite": "最愛", "save": "儲存", "history": "歷史", "recent": "最近",
    "latest": "最新", "time": "時間", "date": "日期", "today": "今天",
    "yesterday": "昨天", "morning": "早上", "afternoon": "下午",
    "evening": "晚上", "night": "夜晚", "day": "白天",
}

def translate_title(title):
    """簡易標題中文化"""
    return title

def generate_summary(post):
    """生成三行摘要"""
    title = post.get("title", "")
    content = post.get("content", "")[:500]
    source = post.get("source", "Facebook")
    likes = post.get("likes", 0)
    comments = post.get("comments", 0)
    
    lines = []
    
    # 第一行：主題概述
    if "how to" in title.lower() or "guide" in title.lower():
        lines.append(f"📖 教學指南：分享 {source} 的實作方法")
    elif "error" in title.lower() or "bug" in title.lower() or "issue" in title.lower():
        lines.append(f"⚠️ 問題回報：{source} 使用者遇到技術問題")
    elif "question" in title.lower() or "help" in title.lower():
        lines.append(f"❓ 求助問題：{source} 使用者尋求協助")
    elif "showcase" in title.lower() or "built" in title.lower() or "made" in title.lower():
        lines.append(f"🎉 作品展示：{source} 使用者分享專案成果")
    elif "news" in title.lower() or "update" in title.lower():
        lines.append(f"📰 最新消息：{source} 發布更新資訊")
    elif "discussion" in title.lower():
        lines.append(f"💬 熱烈討論：{source} 社群活躍交流")
    else:
        lines.append(f"📌 一般分享：{source} 的 OpenClaw 相關內容")
    
    # 第二行：互動數據
    lines.append(f"   👍 {likes} 讚｜💬 {comments} 則回應")
    
    # 第三行：內容預覽
    if content:
        preview = content[:60].replace("\n", " ").strip()
        if len(content) > 60:
            preview += "..."
        lines.append(f"   📝 {preview}")
    else:
        lines.append(f"   🔗 點擊連結查看完整內容")
    
    return lines

def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {"seen_ids": [], "last_run_utc": None}
    return {"seen_ids": [], "last_run_utc": None}


def load_task_state():
    if TASK_STATE_PATH.exists():
        try:
            return json.loads(TASK_STATE_PATH.read_text())
        except Exception:
            return {}
    return {}

def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def format_age(created_utc):
    delta = max(0, int(time.time() - created_utc))
    if delta < 3600:
        return f"{delta // 60} 分鐘前"
    return f"{delta // 3600} 小時前"

def fetch_facebook():
    """
    抓取 Facebook OpenClaw 相關內容
    注意：Facebook 需要登入權限，這裡使用模擬/預留接口
    """
    # TODO: 實作 Facebook Graph API 或爬蟲
    # 目前回傳空列表，等待 G大 提供 Facebook 存取方式
    return []

def build_message(posts, task_state=None):
    """建立 Telegram 訊息（按讚排序 + 中文標題 + 三行摘要）"""
    task_state = task_state or {}
    lines = [
        "📘 Facebook OpenClaw 監控清單",
        f"關鍵字：{KEYWORD}",
        f"共 {len(posts)} 篇新貼文（按讚數排序）",
        f"目前主目標：{task_state.get('current_goal', '未設定')}",
        "",
    ]
    
    for i, p in enumerate(posts, 1):
        title = translate_title(p.get("title", "(無標題)").replace("\n", " ").strip())
        source = p.get("source", "Facebook")
        author = p.get("author", "unknown")
        likes = p.get("likes", 0)
        comments = p.get("comments", 0)
        url = p.get("url", "")
        age = format_age(int(p.get("created_utc", time.time())))
        
        # 標題行
        lines.append(f"{i}. {title}")
        # 中繼資料行
        lines.append(f"   📍 {source}｜{author}｜👍 {likes}｜💬 {comments}｜{age}")
        # 三行摘要
        summary_lines = generate_summary(p)
        for sl in summary_lines:
            lines.append(f"   {sl}")
        # 連結
        if url:
            lines.append(f"   🔗 {url}")
        lines.append("")
    
    lines.append("#OpenClaw #Facebook")
    return "\n".join(lines).strip()

def send_message(text):
    """發送 Telegram 訊息（分段處理長訊息）"""
    max_length = 4000
    
    if len(text) <= max_length:
        cmd = [
            "openclaw", "message", "send",
            "--channel", CHANNEL,
            "--account", ACCOUNT,
            "--target", CHAT_ID,
            "--message", text,
            "--silent",
        ]
        subprocess.run(cmd, check=True)
    else:
        parts = []
        lines = text.split("\n")
        current = ""
        for line in lines:
            if len(current) + len(line) + 1 > max_length:
                parts.append(current)
                current = line + "\n"
            else:
                current += line + "\n"
        if current:
            parts.append(current)
        
        for i, part in enumerate(parts):
            header = f"📘 Facebook OpenClaw 監控清單 (第 {i+1}/{len(parts)} 部分)\n\n" if i > 0 else ""
            cmd = [
                "openclaw", "message", "send",
                "--channel", CHANNEL,
                "--account", ACCOUNT,
                "--target", CHAT_ID,
                "--message", header + part,
                "--silent",
            ]
            subprocess.run(cmd, check=True)
            time.sleep(1)

def write_report(posts, task_state=None):
    """寫入報告檔案（Markdown 格式）"""
    task_state = task_state or {}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = REPORT_DIR / f"fb_openclaw_report_{stamp}.md"
    
    md_lines = [
        "# 📘 Facebook OpenClaw 監控報告",
        f"",
        f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"關鍵字：{KEYWORD}",
        f"新貼文數量：{len(posts)}",
        f"",
        "## 任務狀態快照",
        f"- Current Goal: {task_state.get('current_goal', '未設定')}",
        f"- Current Workflow: {task_state.get('current_workflow', '未設定')}",
        "- Blockers:",
    ]
    if task_state.get('blockers'):
        md_lines.extend([f"  - {x}" for x in task_state.get('blockers', [])])
    else:
        md_lines.append("  - (none)")
    md_lines.append("- Next Actions:")
    if task_state.get('next_actions'):
        md_lines.extend([f"  - {x}" for x in task_state.get('next_actions', [])])
    else:
        md_lines.append("  - (none)")
    md_lines.extend([
        f"",
        "---",
        f"",
    ])
    
    for i, p in enumerate(posts, 1):
        title = translate_title(p.get("title", "(無標題)"))
        source = p.get("source", "Facebook")
        url = p.get("url", "")
        likes = p.get("likes", 0)
        comments = p.get("comments", 0)
        
        md_lines.append(f"## {i}. {title}")
        md_lines.append(f"")
        md_lines.append(f"- **來源:** {source}")
        md_lines.append(f"- **作者:** {p.get('author', 'unknown')}")
        md_lines.append(f"- **讚數:** {likes}")
        md_lines.append(f"- **留言:** {comments}")
        md_lines.append(f"- **時間:** {format_age(int(p.get('created_utc', time.time())))}")
        if url:
            md_lines.append(f"- **連結:** [{url}]({url})")
        md_lines.append(f"")
        
        summary_lines = generate_summary(p)
        for sl in summary_lines:
            md_lines.append(f"> {sl}")
        md_lines.append(f"")
        md_lines.append(f"---")
        md_lines.append(f"")
    
    md_path.write_text("\n".join(md_lines))
    return md_path

def main():
    state = load_state()
    task_state = load_task_state()
    posts = fetch_facebook()
    now = int(time.time())
    seen_ids = set(state.get("seen_ids", []))

    fresh = []
    for p in posts:
        post_id = p.get("id")
        created = int(p.get("created_utc", 0))
        if not post_id or post_id in seen_ids:
            continue
        if now - created > WINDOW_SECONDS:
            continue
        fresh.append(p)

    if fresh:
        # 按讚數排序（高到低）
        fresh.sort(key=lambda x: x.get("likes", 0), reverse=True)
        
        # 發送訊息
        message = build_message(fresh, task_state)
        send_message(message)
        
        # 寫入報告
        report_path = write_report(fresh, task_state)
        print(f"✅ 報告已生成: {report_path}")
        
        # 更新已看過的 ID
        seen_ids.update(p.get("id") for p in fresh if p.get("id"))
    else:
        print("ℹ️ 沒有新的 Facebook OpenClaw 相關貼文")
    
    # 只保留最近 500 個 ID
    state["seen_ids"] = list(sorted(seen_ids))[-500:]
    state["last_run_utc"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        err = f"[fb_openclaw_watch] ERROR: {e}"
        print(err, file=sys.stderr)
        raise
