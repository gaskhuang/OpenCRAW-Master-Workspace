#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path('/Users/user')
TASK_STATE = ROOT / 'memory' / 'TASK_STATE.json'
TODAY = datetime.now().strftime('%Y-%m-%d')
OUT = ROOT / 'night-shift' / 'discussion' / f'collaboration_{TODAY}.md'

state = {}
if TASK_STATE.exists():
    try:
        state = json.loads(TASK_STATE.read_text())
    except Exception:
        state = {'_error': 'invalid TASK_STATE.json'}

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('a') as f:
    f.write('\n## 🧠 Task State Snapshot\n\n')
    f.write(f'- 時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write(f'- Current Goal：{state.get("current_goal", "(missing)")}\n')
    f.write(f'- Current Workflow：{state.get("current_workflow", "(missing)")}\n')
    f.write('- Active Tasks：\n')
    for item in state.get('active_tasks', []):
        f.write(f'  - {item}\n')
    if not state.get('active_tasks'):
        f.write('  - (none)\n')
    f.write('- Blockers：\n')
    for item in state.get('blockers', []):
        f.write(f'  - {item}\n')
    if not state.get('blockers'):
        f.write('  - (none)\n')
    f.write('- Next Actions：\n')
    for item in state.get('next_actions', []):
        f.write(f'  - {item}\n')
    if not state.get('next_actions'):
        f.write('  - (none)\n')
    f.write('\n---\n')
print(str(OUT))
