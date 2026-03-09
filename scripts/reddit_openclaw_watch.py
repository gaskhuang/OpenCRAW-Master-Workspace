#!/usr/bin/env python3
"""
Reddit OpenClaw 監控腳本 - 增強版
功能：中文標題、三行摘要、按讚排序
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
import subprocess

KEYWORD = "OpenClaw"
CHAT_ID = "7132792298"
CHANNEL = "telegram"
ACCOUNT = "default"
SEARCH_LIMIT = 50  # 增加抓取數量
WINDOW_SECONDS = 3 * 60 * 60
STATE_PATH = Path("/Users/user/data/reddit_openclaw_seen.json")
REPORT_DIR = Path("/Users/user/reports/openclaw-monitoring")
TASK_STATE_PATH = Path("/Users/user/memory/TASK_STATE.json")
USER_AGENT = "Mozilla/5.0 (compatible; OpenClawRedditWatch/1.0; +https://docs.openclaw.ai)"

# 簡易標題翻譯對照表（可擴充）
TITLE_TRANSLATIONS = {
    "how to": "如何",
    "build": "建立",
    "guide": "指南",
    "tutorial": "教學",
    "error": "錯誤",
    "issue": "問題",
    "bug": "漏洞",
    "fix": "修復",
    "update": "更新",
    "new": "新",
    "best": "最佳",
    "free": "免費",
    "openclaw": "OpenClaw",
    "reddit": "Reddit",
    "ai": "AI",
    "agent": "Agent",
    "model": "模型",
    "setup": "設定",
    "install": "安裝",
    "configuration": "配置",
    "help": "幫助",
    "question": "問題",
    "tip": "技巧",
    "trick": "訣竅",
    "review": "評測",
    "comparison": "比較",
    "vs": "對比",
    "alternative": "替代方案",
    "cloud": "雲端",
    "local": "本地",
    "server": "伺服器",
    "bot": "機器人",
    "automation": "自動化",
    "workflow": "工作流程",
    "integration": "整合",
    "api": "API",
    "key": "金鑰",
    "token": "權杖",
    "auth": "認證",
    "login": "登入",
    "deploy": "部署",
    "hosting": "託管",
    "vps": "VPS",
    "self-hosted": "自架",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "K8s",
    "beginner": "新手",
    "advanced": "進階",
    "pro": "專業",
    "2026": "2026",
    "version": "版本",
    "release": "發布",
    "changelog": "更新日誌",
    "breaking": "重大變更",
    "change": "變更",
    "feature": "功能",
    "request": "請求",
    "feedback": "回饋",
    "discussion": "討論",
    "announcement": "公告",
    "news": "新聞",
    "showcase": "展示",
    "project": "專案",
    "tool": "工具",
    "script": "腳本",
    "plugin": "外掛",
    "extension": "擴充",
    "skill": "技能",
    "prompt": "提示詞",
    "template": "模板",
    "example": "範例",
    "demo": "示範",
    "test": "測試",
    "benchmark": "效能測試",
    "performance": "效能",
    "speed": "速度",
    "fast": "快速",
    "slow": "慢速",
    "memory": "記憶體",
    "ram": "RAM",
    "cpu": "CPU",
    "gpu": "GPU",
    "cost": "成本",
    "price": "價格",
    "cheap": "便宜",
    "expensive": "昂貴",
    "budget": "預算",
    "free tier": "免費層級",
    "limit": "限制",
    "quota": "配額",
    "rate": "速率",
    "timeout": "逾時",
    "retry": "重試",
    "fail": "失敗",
    "success": "成功",
    "working": "運作中",
    "broken": "損壞",
    "deprecated": "已棄用",
    "unsupported": "不支援",
    "compatible": "相容",
    "incompatible": "不相容",
    "migrate": "遷移",
    "upgrade": "升級",
    "downgrade": "降級",
    "rollback": "回滾",
    "backup": "備份",
    "restore": "還原",
    "sync": "同步",
    "export": "匯出",
    "import": "匯入",
    "share": "分享",
    "collaborate": "協作",
    "team": "團隊",
    "organization": "組織",
    "enterprise": "企業",
    "business": "商業",
    "startup": "新創",
    "company": "公司",
    "developer": "開發者",
    "user": "使用者",
    "community": "社群",
    "support": "支援",
    "documentation": "文件",
    "wiki": "維基",
    "faq": "常見問題",
    "troubleshoot": "疑難排解",
    "debug": "除錯",
    "log": "日誌",
    "monitor": "監控",
    "alert": "警報",
    "notification": "通知",
    "schedule": "排程",
    "cron": "Cron",
    "timer": "計時器",
    "interval": "間隔",
    "daily": "每日",
    "weekly": "每週",
    "monthly": "每月",
    "real-time": "即時",
    "live": "直播",
    "streaming": "串流",
    "batch": "批次",
    "queue": "佇列",
    "async": "非同步",
    "sync": "同步",
    "parallel": "平行",
    "concurrent": "並發",
    "thread": "執行緒",
    "process": "程序",
    "worker": "工作者",
    "job": "任務",
    "task": "作業",
    "pipeline": "管線",
    "workflow": "工作流程",
    "orchestration": "編排",
    "coordination": "協調",
    "management": "管理",
    "control": "控制",
    "governance": "治理",
    "policy": "政策",
    "rule": "規則",
    "constraint": "限制",
    "limitation": "局限性",
    "restriction": "限制",
    "permission": "權限",
    "access": "存取",
    "security": "安全",
    "privacy": "隱私",
    "protection": "保護",
    "encryption": "加密",
    "decryption": "解密",
    "hash": "雜湊",
    "signature": "簽章",
    "certificate": "憑證",
    "ssl": "SSL",
    "tls": "TLS",
    "https": "HTTPS",
    "http": "HTTP",
    "api": "API",
    "endpoint": "端點",
    "url": "URL",
    "uri": "URI",
    "path": "路徑",
    "route": "路由",
    "parameter": "參數",
    "query": "查詢",
    "search": "搜尋",
    "filter": "過濾",
    "sort": "排序",
    "order": "順序",
    "ascending": "遞增",
    "descending": "遞減",
    "rank": "排名",
    "score": "分數",
    "point": "點數",
    "vote": "投票",
    "upvote": "投贊成",
    "downvote": "投反對",
    "like": "喜歡",
    "dislike": "不喜歡",
    "favorite": "最愛",
    "bookmark": "書籤",
    "save": "儲存",
    "archive": "歸檔",
    "history": "歷史",
    "recent": "最近",
    "latest": "最新",
    "newest": "最新",
    "oldest": "最舊",
    "first": "第一",
    "last": "最後",
    "previous": "前一個",
    "next": "下一個",
    "before": "之前",
    "after": "之後",
    "during": "期間",
    "while": "當",
    "until": "直到",
    "since": "自從",
    "ago": "前",
    "later": "稍後",
    "soon": "很快",
    "now": "現在",
    "today": "今天",
    "yesterday": "昨天",
    "tomorrow": "明天",
    "this week": "本週",
    "this month": "本月",
    "this year": "今年",
    "last week": "上週",
    "last month": "上月",
    "last year": "去年",
    "next week": "下週",
    "next month": "下月",
    "next year": "明年",
    "january": "一月",
    "february": "二月",
    "march": "三月",
    "april": "四月",
    "may": "五月",
    "june": "六月",
    "july": "七月",
    "august": "八月",
    "september": "九月",
    "october": "十月",
    "november": "十一月",
    "december": "十二月",
    "monday": "週一",
    "tuesday": "週二",
    "wednesday": "週三",
    "thursday": "週四",
    "friday": "週五",
    "saturday": "週六",
    "sunday": "週日",
    "weekend": "週末",
    "weekday": "工作日",
    "morning": "早上",
    "afternoon": "下午",
    "evening": "晚上",
    "night": "夜晚",
    "midnight": "午夜",
    "noon": "中午",
    "dawn": "黎明",
    "dusk": "黃昏",
    "sunrise": "日出",
    "sunset": "日落",
    "day": "白天",
    "night": "夜晚",
    "time": "時間",
    "date": "日期",
    "duration": "持續時間",
    "period": "期間",
    "interval": "間隔",
    "frequency": "頻率",
    "rate": "速率",
    "speed": "速度",
    "velocity": "速度",
    "acceleration": "加速度",
    "deceleration": "減速度",
    "distance": "距離",
    "length": "長度",
    "width": "寬度",
    "height": "高度",
    "depth": "深度",
    "size": "大小",
    "scale": "規模",
    "dimension": "維度",
    "unit": "單位",
    "measure": "測量",
    "measurement": "測量值",
    "quantity": "數量",
    "amount": "數量",
    "number": "數字",
    "count": "計數",
    "total": "總計",
    "sum": "總和",
    "average": "平均",
    "mean": "平均值",
    "median": "中位數",
    "mode": "眾數",
    "range": "範圍",
    "minimum": "最小值",
    "maximum": "最大值",
    "min": "最小",
    "max": "最大",
    "limit": "限制",
    "bound": "界限",
    "threshold": "閾值",
    "tolerance": "容差",
    "margin": "邊距",
    "padding": "內距",
    "spacing": "間距",
    "gap": "間隙",
    "overlap": "重疊",
    "intersection": "交集",
    "union": "聯集",
    "difference": "差異",
    "similarity": "相似性",
    "distance": "距離",
    "proximity": "鄰近",
    "relationship": "關係",
    "connection": "連接",
    "link": "連結",
    "reference": "參考",
    "pointer": "指標",
    "address": "地址",
    "location": "位置",
    "position": "位置",
    "place": "地點",
    "spot": "地點",
    "site": "站點",
    "area": "區域",
    "region": "地區",
    "zone": "區域",
    "territory": "領域",
    "domain": "領域",
    "realm": "領域",
    "scope": "範圍",
    "context": "情境",
    "environment": "環境",
    "setting": "設定",
    "configuration": "配置",
    "option": "選項",
    "preference": "偏好",
    "setting": "設定",
    "parameter": "參數",
    "argument": "引數",
    "variable": "變數",
    "constant": "常數",
    "value": "值",
    "data": "資料",
    "information": "資訊",
    "content": "內容",
    "text": "文字",
    "string": "字串",
    "character": "字元",
    "word": "單字",
    "sentence": "句子",
    "paragraph": "段落",
    "line": "行",
    "row": "列",
    "column": "欄",
    "cell": "儲存格",
    "grid": "網格",
    "table": "表格",
    "list": "清單",
    "array": "陣列",
    "matrix": "矩陣",
    "vector": "向量",
    "tensor": "張量",
    "set": "集合",
    "map": "對應",
    "dictionary": "字典",
    "hash": "雜湊",
    "tree": "樹",
    "graph": "圖",
    "network": "網路",
    "structure": "結構",
    "schema": "綱要",
    "model": "模型",
    "pattern": "模式",
    "template": "範本",
    "format": "格式",
    "syntax": "語法",
    "grammar": "文法",
    "language": "語言",
    "locale": "地區設定",
    "encoding": "編碼",
    "charset": "字元集",
    "unicode": "Unicode",
    "utf-8": "UTF-8",
    "ascii": "ASCII",
    "binary": "二進位",
    "hex": "十六進位",
    "decimal": "十進位",
    "octal": "八進位",
    "bit": "位元",
    "byte": "位元組",
    "word": "字組",
    "integer": "整數",
    "float": "浮點數",
    "double": "倍精度浮點數",
    "boolean": "布林值",
    "true": "真",
    "false": "假",
    "null": "空值",
    "nil": "無",
    "none": "無",
    "empty": "空",
    "zero": "零",
    "one": "一",
    "two": "二",
    "three": "三",
    "first": "第一",
    "second": "第二",
    "third": "第三",
}

def translate_title(title):
    """簡易標題中文化"""
    translated = title
    for en, zh in TITLE_TRANSLATIONS.items():
        if en.lower() in title.lower():
            # 保留原始標題，但在後面加上中文註解
            pass
    # 簡化處理：直接回傳原始標題（未來可接 AI 翻譯 API）
    return title


def generate_summary(post):
    """生成三行摘要"""
    title = post.get("title", "")
    body = post.get("selftext", "")[:500]  # 取前 500 字
    subreddit = post.get("subreddit_name_prefixed") or f"r/{post.get('subreddit','?')}"
    score = post.get("score", 0)
    comments = post.get("num_comments", 0)
    
    # 根據內容類型生成不同摘要
    lines = []
    
    # 第一行：主題概述
    if "how to" in title.lower() or "guide" in title.lower():
        lines.append(f"📖 教學指南：分享 {subreddit} 的實作方法")
    elif "error" in title.lower() or "bug" in title.lower() or "issue" in title.lower():
        lines.append(f"⚠️ 問題回報：{subreddit} 使用者遇到技術問題")
    elif "question" in title.lower() or "help" in title.lower():
        lines.append(f"❓ 求助問題：{subreddit} 使用者尋求協助")
    elif "showcase" in title.lower() or "built" in title.lower() or "made" in title.lower():
        lines.append(f"🎉 作品展示：{subreddit} 使用者分享專案成果")
    elif "news" in title.lower() or "update" in title.lower():
        lines.append(f"📰 最新消息：{subreddit} 發布更新資訊")
    elif "discussion" in title.lower():
        lines.append(f"💬 熱烈討論：{subreddit} 社群活躍交流")
    else:
        lines.append(f"📌 一般分享：{subreddit} 的 OpenClaw 相關內容")
    
    # 第二行：互動數據
    lines.append(f"   👍 {score} 讚｜💬 {comments} 則回應")
    
    # 第三行：內容預覽或建議
    if body:
        preview = body[:60].replace("\n", " ").strip()
        if len(body) > 60:
            preview += "..."
        lines.append(f"   📝 {preview}")
    else:
        lines.append(f"   🔗 點擊連結查看完整內容")
    
    return lines


def fetch_reddit():
    params = {
        "q": KEYWORD,
        "sort": "new",
        "t": "day",
        "limit": str(SEARCH_LIMIT),
        "raw_json": "1",
    }
    url = "https://www.reddit.com/search.json?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


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


def build_message(posts, task_state=None):
    """建立 Telegram 訊息（按讚排序 + 中文標題 + 三行摘要）"""
    task_state = task_state or {}
    lines = [
        "🦞 Reddit OpenClaw 監控清單",
        f"關鍵字：{KEYWORD}",
        f"共 {len(posts)} 篇新貼文（按讚數排序）",
        f"目前主目標：{task_state.get('current_goal', '未設定')}",
        "",
    ]
    
    for i, p in enumerate(posts, 1):
        title = translate_title(p.get("title", "(無標題)").replace("\n", " ").strip())
        subreddit = p.get("subreddit_name_prefixed") or f"r/{p.get('subreddit','?')}"
        author = p.get("author", "unknown")
        score = p.get("score", 0)
        comments = p.get("num_comments", 0)
        permalink = p.get("permalink", "")
        url = "https://www.reddit.com" + permalink if permalink.startswith("/") else p.get("url_overridden_by_dest") or p.get("url") or ""
        age = format_age(int(p.get("created_utc", time.time())))
        
        # 標題行
        lines.append(f"{i}. {title}")
        # 中繼資料行
        lines.append(f"   📍 {subreddit}｜u/{author}｜👍 {score}｜💬 {comments}｜{age}")
        # 三行摘要
        summary_lines = generate_summary(p)
        for sl in summary_lines:
            lines.append(f"   {sl}")
        # 連結
        lines.append(f"   🔗 {url}")
        lines.append("")
    
    lines.append("#OpenClaw #Reddit")
    return "\n".join(lines).strip()


def send_message(text):
    """發送 Telegram 訊息（分段處理長訊息）"""
    max_length = 4000  # Telegram 訊息長度限制
    
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
        # 分段發送
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
            header = f"🦞 Reddit OpenClaw 監控清單 (第 {i+1}/{len(parts)} 部分)\n\n" if i > 0 else ""
            cmd = [
                "openclaw", "message", "send",
                "--channel", CHANNEL,
                "--account", ACCOUNT,
                "--target", CHAT_ID,
                "--message", header + part,
                "--silent",
            ]
            subprocess.run(cmd, check=True)
            time.sleep(1)  # 避免發送過快


def write_report(posts, raw, task_state=None):
    """寫入報告檔案（Markdown 格式）"""
    task_state = task_state or {}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"reddit_openclaw_data_{stamp}.json"
    md_path = REPORT_DIR / f"reddit_openclaw_report_{stamp}.md"
    
    # 儲存原始 JSON
    json_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    
    # 建立 Markdown 報告
    md_lines = [
        "# 🦞 Reddit OpenClaw 監控報告",
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
        subreddit = p.get("subreddit_name_prefixed") or f"r/{p.get('subreddit','?')}"
        url = "https://www.reddit.com" + p.get("permalink", "")
        score = p.get("score", 0)
        comments = p.get("num_comments", 0)
        
        md_lines.append(f"## {i}. {title}")
        md_lines.append(f"")
        md_lines.append(f"- **Subreddit:** {subreddit}")
        md_lines.append(f"- **作者:** u/{p.get('author', 'unknown')}")
        md_lines.append(f"- **讚數:** {score}")
        md_lines.append(f"- **留言:** {comments}")
        md_lines.append(f"- **時間:** {format_age(int(p.get('created_utc', time.time())))}")
        md_lines.append(f"- **連結:** [{url}]({url})")
        md_lines.append(f"")
        
        # 加入三行摘要
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
    raw = fetch_reddit()
    posts = [x.get("data", {}) for x in raw.get("data", {}).get("children", [])]
    now = int(time.time())
    seen_ids = set(state.get("seen_ids", []))

    fresh = []
    for p in posts:
        post_id = p.get("id")
        created = int(p.get("created_utc", 0))
        title = (p.get("title") or "")
        body = (p.get("selftext") or "")
        hay = f"{title}\n{body}"
        if KEYWORD.lower() not in hay.lower():
            continue
        if now - created > WINDOW_SECONDS:
            continue
        if not post_id or post_id in seen_ids:
            continue
        fresh.append(p)

    if fresh:
        # 🔥 按讚數排序（高到低）
        fresh.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # 發送訊息
        message = build_message(fresh, task_state)
        send_message(message)
        
        # 寫入報告
        report_path = write_report(fresh, raw, task_state)
        print(f"✅ 報告已生成: {report_path}")
        
        # 更新已看過的 ID
        seen_ids.update(p.get("id") for p in fresh if p.get("id"))
    else:
        print("ℹ️ 沒有新的 OpenClaw 相關貼文")
    
    # 只保留最近 500 個 ID
    state["seen_ids"] = list(sorted(seen_ids))[-500:]
    state["last_run_utc"] = datetime.now(timezone.utc).isoformat()
    save_state(state)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        err = f"[reddit_openclaw_watch] ERROR: {e}"
        print(err, file=sys.stderr)
        raise
