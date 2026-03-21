# OpenClaw Auto Update 報告

- 日期：2026-03-22
- 執行時間：2026-03-22 00:00:03 CST
- Node：v25.7.0
- npm：11.10.1
- OpenClaw（更新前）：OpenClaw 2026.3.13-beta.1 (94a2926)

## 1. OpenClaw 更新
- 更新指令：`openclaw update`
- 更新前：
  - `OpenClaw 2026.3.13-beta.1 (94a2926)`
- 更新後：
  - `OpenClaw 2026.3.13-beta.1 (94a2926)`

```text
[plugins] [lcm] Compaction summarization model: anthropic/claude-sonnet-4-6 (default)
[plugins] memory-lancedb-pro@1.0.32: plugin registered (db: /Users/user/.openclaw/memory/lancedb-pro, model: jina-embeddings-v5-text-small)
[plugins] memory-lancedb-pro: loaded without install/load-path provenance; treat as untracked local code and pin trust via plugins.allow or install records (/Users/user/.openclaw/extensions/memory-lancedb-pro/index.ts)
Updating OpenClaw...


Update Result: OK
  Root: /Users/user/openclaw/openclaw
  Before: 2026.3.13-beta.1
  After: 2026.3.13-beta.1

Steps:
  ✓ clean check (54ms)
  ✓ git fetch (2.25s)
  ✓ git checkout v2026.3.13-beta.1 (34ms)
  ✓ deps install (2.17s)
  ✓ build (24.78s)
  ✓ ui:build (2.21s)
  ✓ openclaw doctor (10.64s)
  ✓ git rev-parse HEAD (after) (20ms)

Total time: 42.22s

Updating plugins...
Downloading @art_style666/hi-light…
Extracting /var/folders/z9/_tvj15zd1blf1c4hn076flpc0000gn/T/openclaw-npm-pack-99bUdM/art_style666-hi-light-2.0.4.tgz…
Installing to /Users/user/.openclaw/extensions/hi-light…
Installing plugin dependencies…
Downloading @martian-engineering/lossless-claw…
Extracting /var/folders/z9/_tvj15zd1blf1c4hn076flpc0000gn/T/openclaw-npm-pack-jevnpo/martian-engineering-lossless-claw-0.4.0.tgz…
Plugin "lossless-claw" has 1 suspicious code pattern(s). Run "openclaw security audit --deep" for details.
Installing to /Users/user/.openclaw/extensions/lossless-claw…
Installing plugin dependencies…
Config overwrite: /Users/user/.openclaw/openclaw.json (sha256 ac701bd7eba8e3bea8bd916650f12a62674dfa7ccded4bf4eed0ab9481d1b222 -> 5de6e4285f57e0b2b1bfd989c2914956f9c653c78c29aecf95fcf1567898941a, backup=/Users/user/.openclaw/openclaw.json.bak)
npm plugins: 0 updated, 2 unchanged.

Restarting service...
Daemon restart completed.

I've evolved. Try to keep up.
```

## 2. ~/skills 更新
### opennews-mcp
- branch: main
- commit: ce08698 -> ce08698
```text
From https://github.com/6551Team/opennews-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### gstack
- branch: main
- commit: 1f4b6fd -> 1f4b6fd
```text
From https://github.com/garrytan/gstack
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### chrome-cdp-skill
- branch: main
- commit: 1fd55c7 -> 1fd55c7
```text
From https://github.com/pasky/chrome-cdp-skill
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### opentwitter-mcp
- branch: main
- commit: b2949fa -> b2949fa
```text
From https://github.com/6551Team/opentwitter-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

## 3. /Users/user/openclaw repo 更新
- 未偵測到 git repo，略過。

## 4. 健康檢查
```text
[plugins] [lcm] Plugin loaded (enabled=true, db=/Users/user/.openclaw/lcm.db, threshold=0.75)
[plugins] [lcm] Compaction summarization model: anthropic/claude-sonnet-4-6 (default)
[plugins] memory-lancedb-pro@1.0.32: plugin registered (db: /Users/user/.openclaw/memory/lancedb-pro, model: jina-embeddings-v5-text-small)
[plugins] memory-lancedb-pro: loaded without install/load-path provenance; treat as untracked local code and pin trust via plugins.allow or install records (/Users/user/.openclaw/extensions/memory-lancedb-pro/index.ts)
[plugins] memory-lancedb-pro@1.0.32: plugin registered (db: /Users/user/.openclaw/memory/lancedb-pro, model: jina-embeddings-v5-text-small)
[plugins] memory-lancedb-pro: loaded without install/load-path provenance; treat as untracked local code and pin trust via plugins.allow or install records (/Users/user/.openclaw/extensions/memory-lancedb-pro/index.ts)
OpenClaw status

Overview
┌─────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Item            │ Value                                                                                              │
├─────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Dashboard       │ http://127.0.0.1:18789/                                                                            │
│ OS              │ macos 26.3 (arm64) · node 25.7.0                                                                   │
│ Tailscale       │ off                                                                                                │
│ Channel         │ beta (config)                                                                                      │
│ Git             │ detached · tag v2026.3.13-beta.1 · @ 94a29268                                                      │
│ Update          │ available · git HEAD · npm update 2026.3.13 · deps ok                                              │
│ Gateway         │ local · ws://127.0.0.1:18789 (local loopback) · unreachable (missing scope: operator.read)         │
│ Gateway service │ LaunchAgent installed · loaded · running (pid 96998, state active)                                 │
│ Node service    │ LaunchAgent not installed                                                                          │
│ Agents          │ 1 · no bootstrap files · sessions 5 · default hq active 34m ago                                    │
│ Memory          │ enabled (plugin memory-lancedb-pro)                                                                │
│ Probes          │ skipped (use --deep)                                                                               │
│ Events          │ none                                                                                               │
│ Heartbeat       │ 1h (hq)                                                                                            │
│ Sessions        │ 5 active · default claude-sonnet-4-6 (200k ctx) · ~/.openclaw/agents/hq/sessions/sessions.json     │
└─────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘

Security audit
Summary: 3 critical · 4 warn · 2 info
  CRITICAL Open groupPolicy with elevated tools enabled
    Found groupPolicy="open" at: - channels.telegram.groupPolicy With tools.elevated enabled, a prompt injection in those rooms can become a high-impact incident.
    Fix: Set groupPolicy="allowlist" and keep elevated allowlists extremely tight.
  CRITICAL Open groupPolicy with runtime/filesystem tools exposed
    Found groupPolicy="open" at: - channels.telegram.groupPolicy Risky tool exposure contexts: - agents.defaults (sandbox=off; runtime=[exec, process]; fs=[read, w…
    Fix: For open groups, prefer tools.profile="messaging" (or deny group:runtime/group:fs), set tools.fs.workspaceOnly=true, and use agents.defaults.sandbox.mode="all" for exposed agents.
  CRITICAL Telegram security warning
    Telegram groups: groupPolicy="open" with no channels.telegram.groups allowlist; any group can add + ping (mention-gated). Set channels.telegram.groupPolicy="al…
  WARN Reverse proxy headers are not trusted
    gateway.bind is loopback and gateway.trustedProxies is empty. If you expose the Control UI through a reverse proxy, configure trusted proxies so local-client c…
    Fix: Set gateway.trustedProxies to your proxy IPs or keep the Control UI local-only.
  WARN Potential multi-user setup detected (personal-assistant model warning)
    Heuristic signals indicate this gateway may be reachable by multiple users: - channels.telegram.groupPolicy="open" Runtime/process tools are exposed without fu…
    Fix: If users may be mutually untrusted, split trust boundaries (separate gateways + credentials, ideally separate OS users/hosts). If you intentionally run shared-user access, set agents.defaults.sandbox.mode="all", keep tools.fs.workspaceOnly=true, deny runtime/fs/web tools unless required, and keep personal/private identities + credentials off that runtime.
  WARN Extension plugin tools may be reachable under permissive tool policy
    Enabled extension plugins: hi-light, lossless-claw, memory-lancedb-pro. Permissive tool policy contexts: - default - agents.list.hq
    Fix: Use restrictive profiles (`minimal`/`coding`) or explicit tool allowlists that exclude plugin tools for agents handling untrusted input.
… +1 more
Full report: openclaw security audit
Deep probe: openclaw security audit --deep

Channels
┌──────────┬─────────┬────────┬────────────────────────────────────────────────────────────────────────────────────────┐
│ Channel  │ Enabled │ State  │ Detail                                                                                 │
├──────────┼─────────┼────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ Telegram │ ON      │ OK     │ token config (8322…t_kM · len 46) · accounts 1/1                                       │
│ HiLight  │ ON      │ SETUP  │ wsUrl is not set in channels.hi-light config                                           │
└──────────┴─────────┴────────┴────────────────────────────────────────────────────────────────────────────────────────┘

Sessions
┌───────────────────────────────────────────┬────────┬─────────┬───────────────────┬───────────────────────────────────┐
│ Key                                       │ Kind   │ Age     │ Model             │ Tokens                            │
├───────────────────────────────────────────┼────────┼─────────┼───────────────────┼───────────────────────────────────┤
│ agent:hq:main                             │ direct │ 34m ago │ claude-sonnet-4-6 │ 43k/200k (22%) · 🗄️ 90% cached    │
│ agent:hq:cron:b43d1459-9db8-466…          │ direct │ 1h ago  │ claude-sonnet-4-6 │ 34k/200k (17%) · 🗄️ 722% cached   │
│ agent:hq:cron:b43d1459-9db8-466…          │ direct │ 1h ago  │ claude-sonnet-4-6 │ 34k/200k (17%) · 🗄️ 722% cached   │
│ agent:hq:telegram:direct:713279…          │ direct │ 1h ago  │ claude-sonnet-4-6 │ 317k/200k (158%) · 🗄️ 100% cached │
│ agent:hq:telegram:slash:7132792…          │ direct │ 16d ago │ claude-sonnet-4-6 │ unknown/200k (?%)                 │
└───────────────────────────────────────────┴────────┴─────────┴───────────────────┴───────────────────────────────────┘

FAQ: https://docs.openclaw.ai/faq
Troubleshooting: https://docs.openclaw.ai/troubleshooting

Update available (npm 2026.3.13). Run: openclaw update

Next steps:
  Need to share?      openclaw status --all
  Need to debug live? openclaw logs --follow
  Fix reachability first: openclaw gateway probe
```

## 5. 總結
- 已更新 OpenClaw 與技能庫
- skills repo 檢查數量：4
- 本報告由 OpenClaw 版 auto-updater 自動生成
