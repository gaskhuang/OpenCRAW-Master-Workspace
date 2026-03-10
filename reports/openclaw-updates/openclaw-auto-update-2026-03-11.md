# OpenClaw Auto Update 報告

- 日期：2026-03-11
- 執行時間：2026-03-11 00:00:03 CST
- Node：v25.7.0
- npm：11.10.1
- OpenClaw（更新前）：2026.3.7

## 1. OpenClaw 更新
- 更新指令：`openclaw update`
- 更新前：
  - `2026.3.7`
- 更新後：
  - `2026.3.7`

```text
Updating OpenClaw...


Update Result: SKIPPED
  Root: /Users/user/openclaw/openclaw
  Reason: dirty
  Before: 2026.3.7

Steps:
  ✓ clean check (73ms)

Total time: 170ms
Skipped: working directory has uncommitted changes. Commit or stash them first.
```

## 2. ~/skills 更新
### opennews-mcp
- branch: main
- commit: d608baa -> d608baa
```text
From https://github.com/6551Team/opennews-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### clawdhub
- branch: main
- commit: e07198a -> e07198a
```text
From https://github.com/steipete/clawdhub
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### proactive-agent
- branch: main
- commit: 058ed00 -> 058ed00
```text
From https://github.com/halthelobster/proactive-agent
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### opentwitter-mcp
- branch: main
- commit: d8121b8 -> d8121b8
```text
From https://github.com/6551Team/opentwitter-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

## 3. /Users/user/openclaw repo 更新
- 未偵測到 git repo，略過。

## 4. 健康檢查
```text
[plugins] memory-lancedb-pro@1.0.32: plugin registered (db: /Users/user/.openclaw/memory/lancedb-pro, model: jina-embeddings-v5-text-small)
[plugins] memory-lancedb-pro: loaded without install/load-path provenance; treat as untracked local code and pin trust via plugins.allow or install records (/Users/user/.openclaw/extensions/memory-lancedb-pro/index.ts)
OpenClaw status

Overview
┌─────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Item            │ Value                                                                                             │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Dashboard       │ http://127.0.0.1:18789/                                                                           │
│ OS              │ macos 26.3 (arm64) · node 25.7.0                                                                  │
│ Tailscale       │ off                                                                                               │
│ Channel         │ beta (config)                                                                                     │
│ Git             │ detached · tag v2026.3.7 · @ 42a1394c                                                             │
│ Update          │ available · git HEAD · dirty · fetch failed · npm update 2026.3.8 · deps ok                       │
│ Gateway         │ local · ws://127.0.0.1:18789 (local loopback) · reachable 107ms · auth token · userdeMacBook-Pro. │
│                 │ local (192.168.1.110) app 2026.3.7 macos 26.3                                                     │
│ Gateway service │ LaunchAgent installed · loaded · running (pid 48980, state active)                                │
│ Node service    │ LaunchAgent not installed                                                                         │
│ Agents          │ 1 · no bootstrap files · sessions 3 · default hq active 3h ago                                    │
│ Memory          │ enabled (plugin memory-lancedb-pro)                                                               │
│ Probes          │ skipped (use --deep)                                                                              │
│ Events          │ none                                                                                              │
│ Heartbeat       │ 1h (hq)                                                                                           │
│ Sessions        │ 3 active · default claude-sonnet-4-6 (200k ctx) · ~/.openclaw/agents/hq/sessions/sessions.json    │
└─────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────┘

Security audit
Summary: 3 critical · 3 warn · 2 info
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
    Enabled extension plugins: memory-lancedb-pro. Permissive tool policy contexts: - default - agents.list.hq
    Fix: Use restrictive profiles (`minimal`/`coding`) or explicit tool allowlists that exclude plugin tools for agents handling untrusted input.
Full report: openclaw security audit
Deep probe: openclaw security audit --deep

Channels
┌──────────┬─────────┬────────┬───────────────────────────────────────────────────────────────────────────────────────┐
│ Channel  │ Enabled │ State  │ Detail                                                                                │
├──────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────┤
│ Telegram │ ON      │ OK     │ token config (8322…t_kM · len 46) · accounts 1/1                                      │
└──────────┴─────────┴────────┴───────────────────────────────────────────────────────────────────────────────────────┘

Sessions
┌───────────────────────────────────────────┬────────┬─────────┬───────────────────┬──────────────────────────────────┐
│ Key                                       │ Kind   │ Age     │ Model             │ Tokens                           │
├───────────────────────────────────────────┼────────┼─────────┼───────────────────┼──────────────────────────────────┤
│ agent:hq:telegram:direct:713279…          │ direct │ 3h ago  │ gpt-5.4           │ 139k/200k (70%) · 🗄️ 100% cached │
│ agent:hq:main                             │ direct │ 8h ago  │ gpt-5.4           │ 56k/200k (28%) · 🗄️ 90% cached   │
│ agent:hq:telegram:slash:7132792…          │ direct │ 5d ago  │ claude-sonnet-4-6 │ unknown/200k (?%)                │
└───────────────────────────────────────────┴────────┴─────────┴───────────────────┴──────────────────────────────────┘

FAQ: https://docs.openclaw.ai/faq
Troubleshooting: https://docs.openclaw.ai/troubleshooting

Update available (npm 2026.3.8). Run: openclaw update

Next steps:
  Need to share?      openclaw status --all
  Need to debug live? openclaw logs --follow
  Need to test channels? openclaw status --deep
```

## 5. 總結
- 已更新 OpenClaw 與技能庫
- skills repo 檢查數量：4
- 本報告由 OpenClaw 版 auto-updater 自動生成
