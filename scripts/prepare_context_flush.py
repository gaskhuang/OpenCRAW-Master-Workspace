#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

TZ = 'Asia/Taipei'
ROOT = Path('/Users/user')
TASK_STATE = ROOT / 'memory' / 'TASK_STATE.json'
TODAY = datetime.now().strftime('%Y-%m-%d')
DAILY = ROOT / 'memory' / f'{TODAY}.md'
OUT = ROOT / 'reports' / 'context-flush'
OUT.mkdir(parents=True, exist_ok=True)
REPORT = OUT / f'context-flush-{TODAY}.md'


def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {'_error': 'invalid json'}


def main():
    state = load_json(TASK_STATE)
    daily_exists = DAILY.exists()
    report = []
    report.append('# Context Flush Checklist')
    report.append('')
    report.append(f'- date: {TODAY}')
    report.append(f'- task_state: `{TASK_STATE}`')
    report.append(f'- daily_note: `{DAILY}`')
    report.append('')
    report.append('## Current Goal')
    report.append(state.get('current_goal', '(missing)'))
    report.append('')
    report.append('## Current Workflow')
    report.append(state.get('current_workflow', '(missing)'))
    report.append('')
    report.append('## Active Tasks')
    for item in state.get('active_tasks', []):
        report.append(f'- {item}')
    if not state.get('active_tasks'):
        report.append('- (none)')
    report.append('')
    report.append('## Blockers')
    for item in state.get('blockers', []):
        report.append(f'- {item}')
    if not state.get('blockers'):
        report.append('- (none)')
    report.append('')
    report.append('## Next Actions')
    for item in state.get('next_actions', []):
        report.append(f'- {item}')
    if not state.get('next_actions'):
        report.append('- (none)')
    report.append('')
    report.append('## Pre-Compact Check')
    report.append('- [ ] 新偏好是否已寫入 daily note')
    report.append('- [ ] 新規則 / 新 SOP 是否已寫入 daily note / MEMORY')
    report.append('- [ ] 任務狀態變更是否已寫回 TASK_STATE')
    report.append('- [ ] blocker 與 next action 是否明確')
    report.append(f'- [ ] daily note exists: {daily_exists}')
    report.append('')
    REPORT.write_text('\n'.join(report) + '\n')
    print(str(REPORT))


if __name__ == '__main__':
    main()
