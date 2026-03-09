#!/usr/bin/env python3
import json, os, re, subprocess
from pathlib import Path

ROOTS = [Path('/Users/user/skills'), Path('/Users/user/.agents/skills')]
OUT = Path('/Users/user/reports/skill-healthcheck')
OUT.mkdir(parents=True, exist_ok=True)
REPORT = OUT / 'skill-healthcheck-2026-03-10.md'

HELP_TESTS = {
    'whisper': ['whisper', '--help'],
    'gog': ['gog', '--help'],
    'gh': ['gh', '--help'],
    'tmux': ['tmux', '-V'],
    'gemini': ['gemini', '--help'],
    'mcporter': ['mcporter', '--help'],
    'rg': ['rg', '--version'],
    'blogwatcher': ['blogwatcher', '--help'],
    'memo': ['memo', '--help'],
    'remindctl': ['remindctl', '--help'],
    'grizzly': ['grizzly', '--help'],
    'blu': ['blu', '--help'],
    'camsnap': ['camsnap', '--help'],
    'eightctl': ['eightctl', '--help'],
    'gifgrep': ['gifgrep', '--help'],
    'imsg': ['imsg', '--help'],
    'nano-pdf': ['nano-pdf', '--help'],
    'obsidian-cli': ['obsidian-cli', '--help'],
    'openhue': ['openhue', '--help'],
    'oracle': ['oracle', '--help'],
    'ordercli': ['ordercli', '--help'],
    'peekaboo': ['peekaboo', '--help'],
    'sag': ['sag', '--help'],
    'songsee': ['songsee', '--help'],
    'sonos': ['sonos', '--help'],
    'spogo': ['spogo', '--help'],
    'spotify_player': ['spotify_player', '--help'],
    'things': ['things', '--help'],
    'wacli': ['wacli', '--help'],
    'xurl': ['xurl', '--help'],
    'codexbar': ['codexbar', '--help'],
    'op': ['op', '--help'],
}

def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return p.returncode == 0, (p.stdout or p.stderr).strip().splitlines()[:3]
    except Exception as e:
        return False, [str(e)]

def parse_skill(path):
    txt = path.read_text(errors='ignore')
    name = re.search(r'^name:\s*(.+)$', txt, re.M)
    desc = re.search(r'^description:\s*(.+)$', txt, re.M)
    bins = re.findall(r'bins": \[(.*?)\]', txt)
    envs = re.findall(r'env": \[(.*?)\]', txt)
    anybins = re.findall(r'anyBins": \[(.*?)\]', txt)
    def split_items(matches):
        items=[]
        for m in matches:
            items += [x.strip().strip('"\'') for x in m.split(',') if x.strip()]
        return items
    return {
        'name': name.group(1).strip().strip('"\'') if name else path.parent.name,
        'path': str(path),
        'description': desc.group(1).strip() if desc else '',
        'bins': split_items(bins),
        'anyBins': split_items(anybins),
        'env': split_items(envs),
    }

skills=[]
for root in ROOTS:
    if root.exists():
        for p in sorted(root.iterdir()):
            if p.is_dir() and (p/'SKILL.md').exists():
                skills.append(parse_skill(p/'SKILL.md'))

ok, out = run(['openclaw', 'skills', 'check'])
check_text = '\n'.join(out)
full_ok, full_lines = run(['openclaw','skills','check'])
# rerun for full capture without truncation helper
p = subprocess.run(['openclaw','skills','check'], capture_output=True, text=True, timeout=60)
full_check = (p.stdout or '') + (p.stderr or '')

lines=[]
lines.append('# Skill Healthcheck Report')
lines.append('')
lines.append(f'- total skill folders scanned: {len(skills)}')
lines.append('')

for s in skills:
    name=s['name']
    read_by_openclaw = (name in full_check)
    lines.append(f'## {name}')
    lines.append(f'- path: `{s["path"]}`')
    lines.append(f'- OpenClaw read: {"YES" if read_by_openclaw else "NO/UNKNOWN"}')
    deps=[]
    if s['bins']: deps.append('bins=' + ', '.join(s['bins']))
    if s['anyBins']: deps.append('anyBins=' + ', '.join(s['anyBins']))
    if s['env']: deps.append('env=' + ', '.join(s['env']))
    lines.append(f'- dependencies: {"; ".join(deps) if deps else "none declared"}')

    tested=False
    passed=False
    detail=[]
    candidates=[]
    if s['bins']:
        candidates.extend(s['bins'])
    elif s['anyBins']:
        candidates.extend(s['anyBins'])
    for b in candidates:
        if b in HELP_TESTS:
            tested=True
            passed, detail = run(HELP_TESTS[b])
            if passed:
                break
    if not tested and s['env']:
        tested=True
        missing=[e for e in s['env'] if not os.environ.get(e)]
        passed = len(missing)==0
        detail = ['missing env: ' + ', '.join(missing)] if missing else ['env present']
    if not tested:
        detail = ['No deterministic CLI/env declared; MVP test = SKILL present + OpenClaw skills check visibility']
        passed = read_by_openclaw
    lines.append(f'- MVP test: {"PASS" if passed else "FAIL"}')
    for d in detail:
        lines.append(f'  - {d}')
    lines.append('')

REPORT.write_text('\n'.join(lines)+'\n')
print(REPORT)
