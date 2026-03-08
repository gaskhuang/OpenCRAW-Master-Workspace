#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CHANNEL = "telegram"
ACCOUNT = "default"
CHAT_ID = "7132792298"
REPORT_DIR = Path("/Users/user/reports/fb-openclaw-scan")
LOG_PATH = Path("/Users/user/fb_openclaw_watch.log")
TARGETS = [
    {
        "name": "OpenClaw(Clawdbot.Moltbot)龍蝦助理中文社團",
        "url": "https://www.facebook.com/share/g/1BppXGio9Q/?mibextid=wwXIfr",
    },
    {
        "name": "OpenClaw 中文社群",
        "url": "https://www.facebook.com/share/g/17Eo8Kwybn/?mibextid=wwXIfr",
    },
]


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{proc.stderr.strip()}")
    return proc.stdout


def log(msg: str):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(msg.rstrip() + "\n")


def send_message(text: str):
    subprocess.run([
        "openclaw", "message", "send",
        "--channel", CHANNEL,
        "--account", ACCOUNT,
        "--target", CHAT_ID,
        "--message", text,
        "--silent",
    ], check=False)


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = REPORT_DIR / f"fb_openclaw_watch_{stamp}.md"
    raw_dir = REPORT_DIR / f"raw_{stamp}"
    raw_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Facebook OpenClaw 監控報告\n",
        f"- 產生時間：{datetime.now().isoformat(timespec='seconds')}\n",
        f"- 頻率：每 3 小時\n",
        f"- 說明：目前先保存 agent-browser 原始 snapshot，供後續摘要流程使用。\n",
        "",
    ]

    for idx, target in enumerate(TARGETS, 1):
        name = target["name"]
        url = target["url"]
        log(f"[fb_openclaw_watch] scanning {name} {url}")
        try:
            run(["agent-browser", "--session", "facebook", "open", url])
            run(["agent-browser", "--session", "facebook", "wait", "2500"])
            snapshot = run(["agent-browser", "--session", "facebook", "snapshot", "-i", "-c"])
            raw_path = raw_dir / f"target_{idx}.txt"
            raw_path.write_text(snapshot, encoding="utf-8")
            lines.extend([
                f"## {idx}. {name}",
                f"- URL: {url}",
                f"- 原始快照: {raw_path.name}",
                "",
                "```text",
                snapshot[:8000],
                "```",
                "",
            ])
        except Exception as e:
            lines.extend([
                f"## {idx}. {name}",
                f"- URL: {url}",
                f"- 狀態: 失敗",
                f"- 錯誤: {e}",
                "",
            ])
            log(f"[fb_openclaw_watch] ERROR {name}: {e}")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    send_message(
        "🦞 FB OpenClaw 監控已執行\n"
        "- 頻率：每 3 小時\n"
        f"- 報告：{md_path}\n"
        "- 目前先保存 raw snapshot，後續再補摘要優化"
    )
    log(f"[fb_openclaw_watch] wrote {md_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"[fb_openclaw_watch] FATAL: {e}")
        print(e, file=sys.stderr)
        sys.exit(1)
