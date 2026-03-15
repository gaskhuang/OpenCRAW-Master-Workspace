---
name: 奧運每日簡報 (Olympics Daily Briefing)/python
description: "Use Case #138 Python 方案: 奧運每日簡報。使用 Python 實作 Olympics Daily Briefing 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #138: 奧運每日簡報 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# Olympics Daily Briefing

## Introduction

Automated sports event tracking that delivers a comprehensive morning briefing covering Italian athletes competing that day, medal results from the previous day, and controversy or crisis stories. Formatted for Telegram topic threads.

**Why it matters**: Sports journalists and fans need curated, timely information without manually checking multiple sources.

**Real-world example**: Italy at 24 medals (9 gold) - the briefing caught Arianna Fontana becoming Italy's most decorated Olympian, a hockey player injured after 25 seconds, and Jutta Leerdam private jet drama before newspapers.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| [`web_search`](https://clawhub.ai/skills/searching-assistant) | ClawHub | Search athlete schedules |
| `web_fetch` | Built-in | Scrape results |
| `telegram` | Built-in | Deliver briefing |
| `cron` | Built-in | Daily automation |

## How to Setup

### 1. Configure Data Sources

```
Identify:
- Official Olympics results API
- Italian athlete roster
- Sports news RSS feeds
- Social media monitoring for controversies
```

### 2. Create Briefing Template

```markdown
## 🏅 Olympics Briefing - {{date}}

### Today's Italian Competitors
{{#athletes}}
- {{name}} - {{event}} at {{time}}
{{/athletes}}

### Yesterday's Medals
{{#medals}}
- {{type}}: {{event}} - {{athlete}}
{{/medals}}
Total: {{gold}}🥇 {{silver}}🥈 {{bronze}}🥉

### 🔥 Hot Stories
{{#stories}}
- {{headline}}: {{summary}}
{{/stories}}

### Historic Moments
{{#records}}
- {{description}}
{{/records}}
```

### 3. Prompt Template

Add to your `SKILL.md`:

```markdown
## Olympics Daily Briefing

Every day at 07:00 Rome time:
1. Search for Italian athletes competing today
2. Fetch yesterday's medal results
3. Scan news for controversy/crisis stories
4. Check for historic records broken
5. Format into Telegram message
6. Send to topic thread #olympics-briefing

Editorial judgment: Flag stories with 🔥 if they have >1000 social mentions.
```

### 4. Cron Configuration

```json
{
  "schedule": "0 7 * * *",
  "timezone": "Europe/Rome",
  "task": "olympics_briefing",
  "steps": [
    "fetch_competitors",
    "fetch_medals", 
    "scan_controversies",
    "format_telegram",
    "send_notification"
  ]
}
```

### 5. Telegram Integration

```javascript
// Send to specific topic
await telegram.sendMessage({
  chat_id: human.telegram_chat,
  message_thread_id: 12345, // Olympics topic
  text: briefing,
  parse_mode: "Markdown"
});
```

## Success Metrics

- [ ] Delivered by 07:00 Rome time daily
- [ ] All Italian competitors listed
- [ ] Medal count accurate within 1 hour of events
- [ ] Controversy stories flagged before mainstream media

## Variations

| Use Case | Modification |
|----------|--------------|
| World Cup | Change search to FIFA API |
| Local sports | Filter by regional teams |
| Specific athlete | Track only named athletes |

---

*Example: OttoIlRobotto (Moltbook) - "The Olympic briefing pipeline"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/olympics-daily-briefing
cd ~/olympics-daily-briefing
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

建立 `main.py`，實作 奧運每日簡報 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_olympics_daily_briefing():
    """執行 奧運每日簡報 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 奧運每日簡報 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_olympics_daily_briefing()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/olympics-daily-briefing && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
