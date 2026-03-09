# OpenClaw Auto Update 報告

- 日期：2026-03-10
- 執行時間：2026-03-10 00:09:11 CST
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
│
◇  Doctor warnings ────────────────────────────────────────────────────────╮
│                                                                          │
│  - channels.telegram.groupPolicy is "allowlist" but groupAllowFrom (and  │
│    allowFrom) is empty — all group messages will be silently dropped.    │
│    Add sender IDs to channels.telegram.groupAllowFrom or                 │
│    channels.telegram.allowFrom, or set groupPolicy to "open".            │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────╯
Updating OpenClaw...


Update Result: SKIPPED
  Root: /Users/user/openclaw/openclaw
  Reason: dirty
  Before: 2026.3.7

Steps:
  ✓ clean check (161ms)

Total time: 290ms
Skipped: working directory has uncommitted changes. Commit or stash them first.
```

## 2. ~/skills 更新
### opennews-mcp
- branch: main
- commit: 1b7b806 -> 1b7b806
```text
From https://github.com/6551Team/opennews-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

### clawdhub
- branch: main
- commit: c617ef1 -> e07198a
```text
 package.json                                  |   3 +-
 scripts/verify-convex-contract.ts             |  85 +++++++++++++++++
 src/components/DeploymentDriftBanner.test.tsx |  83 +++++++++++++++++
 src/components/DeploymentDriftBanner.tsx      | 101 ++++++++++++++++++++
 src/lib/deploymentDrift.test.ts               |  43 +++++++++
 src/lib/deploymentDrift.ts                    |  23 +++++
 src/routes/__root.tsx                         |   2 +
 20 files changed, 786 insertions(+), 3 deletions(-)
 create mode 100644 .github/workflows/deploy.yml
 create mode 100644 convex/appMeta.ts
 create mode 100644 e2e/catalog-workflows.pw.test.ts
 create mode 100644 e2e/helpers/runtimeErrors.ts
 create mode 100644 e2e/home-workflows.pw.test.ts
 create mode 100644 e2e/publish-entry-workflows.pw.test.ts
 create mode 100644 e2e/upload-auth-smoke.pw.test.ts
 create mode 100644 scripts/verify-convex-contract.ts
 create mode 100644 src/components/DeploymentDriftBanner.test.tsx
 create mode 100644 src/components/DeploymentDriftBanner.tsx
 create mode 100644 src/lib/deploymentDrift.test.ts
 create mode 100644 src/lib/deploymentDrift.ts
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
- commit: d3dd331 -> d3dd331
```text
From https://github.com/6551Team/opentwitter-mcp
 * branch            main       -> FETCH_HEAD
Already up to date.
```

## 3. /Users/user/openclaw repo 更新
- 未偵測到 git repo，略過。

## 4. 健康檢查
```text
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
│ Update          │ available · git HEAD · dirty · npm update 2026.3.8 · deps ok                                      │
│ Gateway         │ local · ws://127.0.0.1:18789 (local loopback) · reachable 53ms · auth token · userdeMacBook-Pro.  │
│                 │ local (192.168.1.110) app 2026.3.7 macos 26.3                                                     │
│ Gateway service │ LaunchAgent installed · loaded · running (pid 89175, state active)                                │
│ Node service    │ LaunchAgent not installed                                                                         │
│ Agents          │ 1 · no bootstrap files · sessions 3 · default hq active 14m ago                                   │
│ Memory          │ 55 files · 99 chunks · sources memory · plugin memory-core · vector ready · fts ready · cache on  │
│                 │ (318)                                                                                             │
│ Probes          │ skipped (use --deep)                                                                              │
│ Events          │ none                                                                                              │
│ Heartbeat       │ 1h (hq)                                                                                           │
│ Sessions        │ 3 active · default claude-sonnet-4-6 (200k ctx) · ~/.openclaw/agents/hq/sessions/sessions.json    │
└─────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────┘

Security audit
Summary: 1 critical · 2 warn · 2 info
  CRITICAL Extensions exist but plugins.allow is not set
    Found 1 extension(s) under /Users/user/.openclaw/extensions. Without plugins.allow, any discovered plugin id may load (depending on config and plugin behavior)…
    Fix: Set plugins.allow to an explicit list of plugin ids you trust.
  WARN Reverse proxy headers are not trusted
    gateway.bind is loopback and gateway.trustedProxies is empty. If you expose the Control UI through a reverse proxy, configure trusted proxies so local-client c…
    Fix: Set gateway.trustedProxies to your proxy IPs or keep the Control UI local-only.
  WARN Extension plugin tools may be reachable under permissive tool policy
    Enabled extension plugins: .openclaw-install-backups. Permissive tool policy contexts: - default - agents.list.hq
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
┌────────────────────────────────────────────┬────────┬─────────┬───────────────────┬─────────────────────────────────┐
│ Key                                        │ Kind   │ Age     │ Model             │ Tokens                          │
├────────────────────────────────────────────┼────────┼─────────┼───────────────────┼─────────────────────────────────┤
│ agent:hq:telegram:direct:713279…           │ direct │ 14m ago │ gpt-5.4           │ 171k/200k (86%) · 🗄️ 98% cached │
│ agent:hq:main                              │ direct │ 24h ago │ claude-opus-4-6   │ 55k/131k (42%)                  │
│ agent:hq:telegram:slash:7132792…           │ direct │ 4d ago  │ claude-sonnet-4-6 │ unknown/200k (?%)               │
└────────────────────────────────────────────┴────────┴─────────┴───────────────────┴─────────────────────────────────┘

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
