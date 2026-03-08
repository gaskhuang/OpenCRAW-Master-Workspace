#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

paths = [
    Path('/Users/user/.zshrc'),
    Path('/Users/user/.zprofile'),
    Path('/Users/user/.agents/skills/gemini/.env'),
    Path('/Users/user/skills/nano-banana-pro/.env'),
    Path('/Users/user/Library/LaunchAgents/ai.openclaw.lobster2.plist'),
    Path('/Users/user/Library/LaunchAgents/ai.openclaw.lobster3.plist'),
]

results = {
    'shell_env': bool(os.environ.get('GEMINI_API_KEY')),
    'shell_env_length': len(os.environ.get('GEMINI_API_KEY', '')),
    'sources': []
}

for p in paths:
    item = {'path': str(p), 'exists': p.exists(), 'has_key': False, 'key_length': 0}
    if p.exists():
        txt = p.read_text(errors='ignore')
        patterns = [
            r'GEMINI_API_KEY\s*=\s*"?([^"\n<]+)"?',
            r'<key>GEMINI_API_KEY</key>\s*<string>([^<]+)</string>',
        ]
        for pat in patterns:
            m = re.search(pat, txt, re.S)
            if m:
                item['has_key'] = True
                item['key_length'] = len(m.group(1).strip())
                break
    results['sources'].append(item)

print(json.dumps(results, ensure_ascii=False, indent=2))
