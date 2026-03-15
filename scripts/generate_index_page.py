#!/usr/bin/env python3
"""
生成 Use Case 索引網頁 (index.html)
"""

import os
import re
import json
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE, ".claude", "skills")
OUTPUT = os.path.join(BASE, "index.html")

# Category consolidation (merge similar categories)
CAT_MERGE = {
    "社群媒體自動化": "社群媒體",
    "商業與銷售": "商業、行銷與銷售",
    "行銷自動化": "商業、行銷與銷售",
    "企業流程": "商業、行銷與銷售",
    "人力資源": "商業、行銷與銷售",
    "產品管理": "商業、行銷與銷售",
    "學術與研究": "研究與學習",
    "AI 運維": "監控與維運",
    "IT 運維": "監控與維運",
    "DevOps": "DevOps 與工程",
    "Agent 架構": "AI 記憶與代理架構",
    "社群與通訊": "社群媒體",
    "個人生產力": "生產力工具",
}

CAT_ICONS = {
    "生產力工具": "⚡",
    "商業、行銷與銷售": "💼",
    "安全與合規": "🔒",
    "DevOps 與工程": "🛠",
    "日常生活自動化": "🏠",
    "創意與內容製作": "🎨",
    "研究與學習": "📚",
    "社群媒體": "📱",
    "監控與維運": "📡",
    "開發者工具": "💻",
    "加密貨幣與 DeFi": "🪙",
    "金融與交易": "📈",
    "健康與個人成長": "🧘",
    "AI 記憶與代理架構": "🧠",
    "其他": "📦",
}


def parse_skills():
    skills = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        if name == "usecase-index":
            continue
        skill_md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
        with open(skill_md, encoding="utf-8") as f:
            content = f.read(2000)

        # Extract ID
        m = re.search(r"#(\d{3})", content)
        num = int(m.group(1)) if m else 0

        # Extract category
        m2 = re.search(r"分類:\s*(.+?)\s*\|", content)
        cat = m2.group(1).strip() if m2 else "其他"
        cat = CAT_MERGE.get(cat, cat)

        # Extract one-liner
        desc = ""
        if "一句話描述" in content:
            after = content.split("一句話描述")[1]
            m3 = re.search(r">\s*(.+)", after)
            desc = m3.group(1).strip() if m3 else ""

        # Extract difficulty
        m4 = re.search(r"難度:\s*(\S+)", content)
        diff = m4.group(1).strip() if m4 else "中級"

        # Extract name parts
        m5 = re.match(r"(.+?)\s*\((.+?)\)", name)
        if m5:
            name_zh = m5.group(1)
            name_en = m5.group(2)
        else:
            name_zh = name
            name_en = name

        # Source label
        m6 = re.search(r"`(\w+)`:\s*`(.+?)`", content)
        source = m6.group(1) if m6 else ""

        skills.append({
            "id": num,
            "name": name,
            "name_zh": name_zh,
            "name_en": name_en,
            "category": cat,
            "icon": CAT_ICONS.get(cat, "📦"),
            "description": desc,
            "difficulty": diff,
            "source": source,
        })

    skills.sort(key=lambda s: s["id"])
    return skills


def generate_html(skills):
    cats = sorted(set(s["category"] for s in skills))
    cat_counts = Counter(s["category"] for s in skills)

    skills_json = json.dumps(skills, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenClaw Use Cases — {len(skills)} 個自動化技能</title>
<style>
:root {{
  --bg: #0d1117;
  --card-bg: #161b22;
  --border: #30363d;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --accent: #58a6ff;
  --accent2: #3fb950;
  --accent3: #d2a8ff;
  --accent4: #f78166;
  --search-bg: #0d1117;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}}
.hero {{
  text-align: center;
  padding: 60px 20px 40px;
  background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1a1e2e 100%);
  border-bottom: 1px solid var(--border);
}}
.hero h1 {{
  font-size: 2.5rem;
  margin-bottom: 12px;
  background: linear-gradient(90deg, var(--accent), var(--accent3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.hero p {{
  color: var(--text-muted);
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto;
}}
.stats {{
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 30px;
  flex-wrap: wrap;
}}
.stat {{
  text-align: center;
}}
.stat-num {{
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--accent);
}}
.stat-label {{
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}}
.container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}}
.search-bar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg);
  padding: 16px 0;
  border-bottom: 1px solid var(--border);
}}
.search-bar input {{
  width: 100%;
  padding: 14px 20px;
  font-size: 1rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--search-bg);
  color: var(--text);
  outline: none;
  transition: border-color 0.2s;
}}
.search-bar input:focus {{
  border-color: var(--accent);
}}
.search-bar input::placeholder {{
  color: var(--text-muted);
}}
.filters {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0 24px;
}}
.filter-btn {{
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}}
.filter-btn:hover {{
  border-color: var(--accent);
  color: var(--accent);
}}
.filter-btn.active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.filter-btn .count {{
  font-size: 0.75rem;
  opacity: 0.7;
  margin-left: 4px;
}}
.result-count {{
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 16px;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}}
.card {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
  cursor: default;
}}
.card:hover {{
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(88, 166, 255, 0.1);
}}
.card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}}
.card-id {{
  font-size: 0.75rem;
  color: var(--accent);
  font-weight: 600;
  background: rgba(88, 166, 255, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
}}
.card-diff {{
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 4px;
}}
.diff-初中級 {{ background: rgba(63, 185, 80, 0.15); color: var(--accent2); }}
.diff-中級 {{ background: rgba(210, 168, 255, 0.15); color: var(--accent3); }}
.diff-初級 {{ background: rgba(63, 185, 80, 0.15); color: var(--accent2); }}
.diff-進階 {{ background: rgba(247, 129, 102, 0.15); color: var(--accent4); }}
.card-title {{
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 4px;
}}
.card-title-en {{
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 10px;
}}
.card-desc {{
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}
.card-footer {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}}
.card-cat {{
  font-size: 0.78rem;
  color: var(--text-muted);
}}
.card-source {{
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 3px;
  background: rgba(139, 148, 158, 0.1);
  color: var(--text-muted);
}}
footer {{
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
  font-size: 0.85rem;
  border-top: 1px solid var(--border);
}}
footer a {{
  color: var(--accent);
  text-decoration: none;
}}
@media (max-width: 640px) {{
  .hero h1 {{ font-size: 1.8rem; }}
  .grid {{ grid-template-columns: 1fr; }}
  .stats {{ gap: 20px; }}
}}
</style>
</head>
<body>

<div class="hero">
  <h1>OpenClaw Use Cases</h1>
  <p>AI 代理自動化技能庫 — 從個人生產力到企業級工作流，一鍵啟動。</p>
  <div class="stats">
    <div class="stat">
      <div class="stat-num">{len(skills)}</div>
      <div class="stat-label">Use Cases</div>
    </div>
    <div class="stat">
      <div class="stat-num">{len(cats)}</div>
      <div class="stat-label">Categories</div>
    </div>
    <div class="stat">
      <div class="stat-num">6</div>
      <div class="stat-label">Source Repos</div>
    </div>
    <div class="stat">
      <div class="stat-num">361</div>
      <div class="stat-label">Upstream Files</div>
    </div>
  </div>
</div>

<div class="container">
  <div class="search-bar">
    <input type="text" id="search" placeholder="🔍 搜尋 use case（中文、英文、編號）..." autocomplete="off">
  </div>

  <div class="filters" id="filters">
    <button class="filter-btn active" data-cat="all">全部 <span class="count">{len(skills)}</span></button>
""" + "".join(
        f'    <button class="filter-btn" data-cat="{cat}">{CAT_ICONS.get(cat, "📦")} {cat} <span class="count">{cat_counts[cat]}</span></button>\n'
        for cat in sorted(cats, key=lambda c: -cat_counts[c])
    ) + """  </div>

  <div class="result-count" id="resultCount"></div>

  <div class="grid" id="grid"></div>
</div>

<footer>
  <p>Built with OpenClaw &middot; 自動從 6 個上游 repo 同步 &middot; 每週一 22:00 自動更新</p>
  <p style="margin-top: 8px;"><a href="https://github.com/gaskhuang/OpenCRAW-Master-Workspace/tree/claude/romantic-raman">GitHub Repo</a></p>
</footer>

<script>
const skills = """ + skills_json + """;

const grid = document.getElementById('grid');
const search = document.getElementById('search');
const resultCount = document.getElementById('resultCount');
let activeCategory = 'all';

function renderCards(filtered) {
  resultCount.textContent = `顯示 ${filtered.length} / ${skills.length} 個 use case`;
  grid.innerHTML = filtered.map(s => `
    <div class="card">
      <div class="card-header">
        <span class="card-id">#${String(s.id).padStart(3, '0')}</span>
        <span class="card-diff diff-${s.difficulty}">${s.difficulty}</span>
      </div>
      <div class="card-title">${s.name_zh}</div>
      <div class="card-title-en">${s.name_en}</div>
      <div class="card-desc">${s.description || '—'}</div>
      <div class="card-footer">
        <span class="card-cat">${s.icon} ${s.category}</span>
        ${s.source ? `<span class="card-source">${s.source}</span>` : ''}
      </div>
    </div>
  `).join('');
}

function filterSkills() {
  const q = search.value.toLowerCase();
  const filtered = skills.filter(s => {
    const matchCat = activeCategory === 'all' || s.category === activeCategory;
    const matchSearch = !q ||
      s.name_zh.toLowerCase().includes(q) ||
      s.name_en.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q) ||
      String(s.id).padStart(3, '0').includes(q) ||
      s.category.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
  renderCards(filtered);
}

search.addEventListener('input', filterSkills);

document.getElementById('filters').addEventListener('click', e => {
  const btn = e.target.closest('.filter-btn');
  if (!btn) return;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  activeCategory = btn.dataset.cat;
  filterSkills();
});

filterSkills();
</script>

</body>
</html>"""
    return html


def main():
    print("Parsing skills...")
    skills = parse_skills()
    print(f"Found {len(skills)} skills")

    print("Generating HTML...")
    html = generate_html(skills)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done! Output: {OUTPUT}")
    print(f"File size: {os.path.getsize(OUTPUT) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
