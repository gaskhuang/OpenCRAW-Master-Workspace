#!/usr/bin/env python3
"""
每週自動同步上游 repo，偵測新增 use case，產生報告。

Usage:
  python3 scripts/weekly_repo_sync.py

功能：
1. git pull 所有 5 個上游 repo
2. 掃描所有 use case markdown 檔案
3. 比對現有 skills 資料夾，找出新增的
4. 產生差異報告 (reports/weekly-sync-YYYY-MM-DD.md)
5. 自動 commit 到本 repo

可搭配 cron 每週執行：
  0 9 * * 1 cd /path/to/repo && python3 scripts/weekly_repo_sync.py
"""

import os
import subprocess
import json
import re
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================
BASE = "/Users/user/118usecase/.claude/worktrees/romantic-raman"
REPOS_DIR = f"{BASE}/_repos"
SKILLS_DIR = f"{BASE}/.claude/skills"
REPORTS_DIR = f"{BASE}/reports"
SYNC_LOG = f"{BASE}/scripts/sync_history.json"

REPOS = {
    "awesome-openclaw-usecases": {
        "url": "https://github.com/hesamsheikh/awesome-openclaw-usecases.git",
        "usecases_dir": "usecases",
        "label": "MAIN",
    },
    "openclaw_usecase_hub": {
        "url": "https://github.com/zhulin025/openclaw_usecase_hub.git",
        "usecases_dir": "usecases",
        "label": "HUB",
    },
    "awesome-clawdbot-usecases": {
        "url": "https://github.com/webvijayi/awesome-clawdbot-usecases.git",
        "usecases_dir": "",  # root level .md files
        "label": "VAR",
    },
    "awesome-openclaw-examples": {
        "url": "https://github.com/OthmaneBlial/awesome-openclaw-examples.git",
        "usecases_dir": "",
        "label": "EXAMPLES",
    },
    "ronakkadhi": {
        "url": "https://github.com/Ronakkadhi/awesome-openclaw-usecases.git",
        "usecases_dir": "",
        "label": "RONAK",
    },
    "awesome-openclaw-usecases-moltbook": {
        "url": "https://github.com/EvoLinkAI/awesome-openclaw-usecases-moltbook.git",
        "usecases_dir": "usecases",
        "label": "MOLTBOOK",
    },
}


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=120
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def load_sync_history():
    if os.path.exists(SYNC_LOG):
        with open(SYNC_LOG, "r") as f:
            return json.load(f)
    return {"runs": [], "known_files": {}}


def save_sync_history(history):
    with open(SYNC_LOG, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def pull_repo(name, info):
    """Git pull a repo. Clone if doesn't exist."""
    repo_path = os.path.join(REPOS_DIR, name)

    if not os.path.exists(repo_path):
        print(f"  Cloning {name}...")
        out, err, code = run_cmd(f"git clone {info['url']} {repo_path}")
        if code != 0:
            print(f"  ❌ Clone failed: {err}")
            return None, "clone_failed"
        return "cloned", "new"

    # Get current commit before pull
    old_hash, _, _ = run_cmd("git rev-parse HEAD", cwd=repo_path)

    # Pull latest
    out, err, code = run_cmd("git pull --ff-only origin main 2>/dev/null || git pull --ff-only origin master 2>/dev/null || git pull --ff-only", cwd=repo_path)

    # Get new commit
    new_hash, _, _ = run_cmd("git rev-parse HEAD", cwd=repo_path)

    if old_hash == new_hash:
        return old_hash[:7], "no_changes"
    else:
        # Get diff summary
        diff_out, _, _ = run_cmd(f"git diff --stat {old_hash}..{new_hash}", cwd=repo_path)
        return new_hash[:7], f"updated ({diff_out.split(chr(10))[-1].strip() if diff_out else 'unknown changes'})"


def scan_md_files(repo_name, info):
    """Scan a repo for all markdown use case files."""
    repo_path = os.path.join(REPOS_DIR, repo_name)
    usecases_subdir = info.get("usecases_dir", "")
    scan_path = os.path.join(repo_path, usecases_subdir) if usecases_subdir else repo_path

    if not os.path.exists(scan_path):
        return []

    files = []
    for f in Path(scan_path).rglob("*.md"):
        # Skip READMEs, LICENSE, CONTRIBUTING, etc.
        fname = f.name.lower()
        if fname in ("readme.md", "license.md", "contributing.md", "changelog.md", "code_of_conduct.md"):
            continue
        # Skip hidden and template files
        if fname.startswith(".") or fname.startswith("_"):
            continue

        rel_path = str(f.relative_to(repo_path))
        # Read first 500 chars to get title
        try:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read(500)
            title = ""
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
        except:
            title = ""

        files.append({
            "path": rel_path,
            "filename": f.name,
            "title": title,
            "full_path": str(f),
            "size": f.stat().st_size,
        })

    return files


def get_existing_skills():
    """Get list of existing skill folder names."""
    if not os.path.exists(SKILLS_DIR):
        return set()
    return set(os.listdir(SKILLS_DIR))


def generate_report(pull_results, all_files, new_files, existing_skills):
    """Generate a markdown sync report."""
    now = datetime.now()
    report = f"""# 🔄 每週 Repo 同步報告

> 執行時間: {now:%Y-%m-%d %H:%M}
> 監控 repos: {len(REPOS)}
> 現有 skills: {len(existing_skills)}

---

## 📡 Repo Pull 狀態

| Repo | Label | 狀態 |
|------|-------|------|
"""
    for name, (commit, status) in pull_results.items():
        emoji = "✅" if "no_changes" not in status else "⏸️"
        if "failed" in status:
            emoji = "❌"
        elif "updated" in status or "new" in status:
            emoji = "🆕"
        report += f"| {name} | {REPOS[name]['label']} | {emoji} {status} (commit: {commit}) |\n"

    report += f"""
---

## 📊 檔案統計

| Repo | 檔案數 | 代表檔案 |
|------|--------|----------|
"""
    for name, files in all_files.items():
        sample = files[0]["filename"] if files else "-"
        report += f"| {name} | {len(files)} | {sample} |\n"

    total_files = sum(len(f) for f in all_files.values())
    report += f"\n**總計: {total_files} 個 use case 檔案**\n"

    # New files section
    report += f"""
---

## 🆕 新增檔案 ({len(new_files)} 個)

"""
    if new_files:
        for f in new_files:
            report += f"- **[{f['repo']}]** `{f['path']}` — {f['title'] or '(無標題)'}\n"
        report += """
### 🎯 建議動作

以上新增檔案尚未對應到現有 skill。建議：
1. 檢視新增檔案內容
2. 判斷是否為全新 use case 或現有 case 的補充
3. 如為新 case，執行 `python3 scripts/regenerate_skills_v2.py` 生成對應 skill
"""
    else:
        report += "沒有發現新增檔案。所有上游 use case 都已對應到現有 skill。\n"

    # Existing coverage
    report += f"""
---

## ✅ 現有 Skill 覆蓋率

- 現有 skill 資料夾: {len(existing_skills)} 個
- 上游 use case 檔案: {total_files} 個

---

*此報告由 `scripts/weekly_repo_sync.py` 自動產生*
"""
    return report


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    history = load_sync_history()

    print("=" * 60)
    print(f"🔄 Weekly Repo Sync — {datetime.now():%Y-%m-%d %H:%M}")
    print("=" * 60)

    # Phase 1: Pull all repos
    print("\n📡 Phase 1: Pulling repos...")
    pull_results = {}
    for name, info in REPOS.items():
        print(f"\n  [{name}]")
        commit, status = pull_repo(name, info)
        pull_results[name] = (commit or "???", status)
        print(f"    → {status}")

    # Phase 2: Scan all files
    print("\n📊 Phase 2: Scanning files...")
    all_files = {}
    all_file_paths = set()
    for name, info in REPOS.items():
        files = scan_md_files(name, info)
        all_files[name] = files
        for f in files:
            all_file_paths.add(f"{name}/{f['path']}")
        print(f"  {name}: {len(files)} files")

    # Phase 3: Compare with existing skills
    print("\n🔍 Phase 3: Comparing with existing skills...")
    existing_skills = get_existing_skills()
    known_files = set(history.get("known_files", {}).keys())

    new_files = []
    for name, files in all_files.items():
        for f in files:
            file_key = f"{name}/{f['path']}"
            if file_key not in known_files:
                new_files.append({**f, "repo": name})

    print(f"  Existing skills: {len(existing_skills)}")
    print(f"  Previously known files: {len(known_files)}")
    print(f"  New files found: {len(new_files)}")

    # Phase 4: Generate report
    print("\n📝 Phase 4: Generating report...")
    report = generate_report(pull_results, all_files, new_files, existing_skills)
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(REPORTS_DIR, f"weekly-sync-{report_date}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report saved: {report_path}")

    # Phase 5: Update history
    history["known_files"] = {
        f"{name}/{f['path']}": {
            "title": f["title"],
            "size": f["size"],
            "first_seen": history.get("known_files", {}).get(
                f"{name}/{f['path']}", {}
            ).get("first_seen", datetime.now().isoformat()),
        }
        for name, files in all_files.items()
        for f in files
    }
    history["runs"].append({
        "date": datetime.now().isoformat(),
        "new_files": len(new_files),
        "total_files": sum(len(f) for f in all_files.values()),
        "pull_results": {k: v[1] for k, v in pull_results.items()},
    })
    save_sync_history(history)

    # Phase 6: Git commit (if there are changes)
    print("\n📦 Phase 6: Committing changes...")
    # Add report and updated repos
    run_cmd(f"git add {report_path}", cwd=BASE)
    run_cmd(f"git add scripts/sync_history.json", cwd=BASE)

    # Check if there are staged changes
    status_out, _, _ = run_cmd("git diff --cached --name-only", cwd=BASE)
    if status_out.strip():
        commit_msg = f"sync: weekly repo sync {report_date} — {len(new_files)} new files found"
        run_cmd(f'git commit -m "{commit_msg}"', cwd=BASE)
        print(f"  ✅ Committed: {commit_msg}")

        # Push
        push_out, push_err, push_code = run_cmd("git push", cwd=BASE)
        if push_code == 0:
            print("  ✅ Pushed to remote")
        else:
            print(f"  ⚠️ Push failed: {push_err}")
    else:
        print("  No changes to commit")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if new_files:
        print(f"  🆕 {len(new_files)} new files found:")
        for f in new_files[:10]:
            print(f"     - [{f['repo']}] {f['path']} — {f['title']}")
        if len(new_files) > 10:
            print(f"     ... and {len(new_files) - 10} more")
    else:
        print("  ✅ No new files — all repos up to date")
    print(f"  📝 Report: {report_path}")


if __name__ == "__main__":
    main()
