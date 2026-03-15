---
name: 多頻道狀態同步 (Multi-Channel Presence Sync)/python
description: "Use Case #171 Python 方案: 多頻道狀態同步。使用 Python 實作 Multi-Channel Presence Sync 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #171: 多頻道狀態同步 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 社群與通訊

---

## 原始需求 (來自 Source Repos)

# Multi-Channel Presence Sync

## Introduction

Synchronizes agent presence across multiple platforms: Moltbook, Telegram, Discord. Maintains consistent identity and activity tracking everywhere.

**Why it matters**: Fragmented presence dilutes identity. Unified presence builds stronger reputation and community connection.

**Real-world example**: Agent posts on Moltbook, cross-shares to Discord, replies to Telegram DMs, tracks all engagement centrally.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `telegram` | Built-in | Messaging |
| `discord` | Built-in | Community |
| `moltbook` | Built-in | Agent social |

## How to Setup

### 1. Sync Configuration

```javascript
const channels = {
  moltbook: { auto_post: true },
  discord: { mirror: 'moltbook', channel: '#agent-updates' },
  telegram: { notify: 'high_engagement_only' }
};
```

### 2. Prompt Template

```markdown
## Multi-Channel Presence Sync

For each post:
1. Publish to primary (Moltbook)
2. Mirror to Discord if engagement >threshold
3. Summarize for Telegram daily
4. Track responses across channels
5. Consolidate engagement metrics

Consistency rules:
- Same identity everywhere
- Cross-reference when relevant
- Respect channel norms
```

## Success Metrics

- [ ] 100% posts on primary
- [ ] Cross-posting automated
- [ ] Engagement tracked centrally

---

*Example: multi-platform agent presence patterns*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/multi-channel-presence-sync
cd ~/multi-channel-presence-sync
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests
```

### Step 2: 設定環境變數

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
EOF
```

### Step 3: 主程式

建立 `main.py`，實作 多頻道狀態同步 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_multi_channel_presence_sync():
    """執行 多頻道狀態同步 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 多頻道狀態同步 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_multi_channel_presence_sync()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/multi-channel-presence-sync && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
