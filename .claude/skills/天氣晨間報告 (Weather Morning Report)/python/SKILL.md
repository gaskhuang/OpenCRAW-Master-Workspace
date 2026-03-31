---
name: 天氣晨間報告 (Weather Morning Report)/python
description: "Use Case #139 Python 方案: 天氣晨間報告。使用 Python 實作 Weather Morning Report 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #139: 天氣晨間報告 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 個人生產力

---

## 原始需求 (來自 Source Repos)

# Weather Morning Report

## Introduction

Automated weather briefing delivered via Telegram every morning at 9:00 AM local time. Fetches forecast by coordinates, parses 4 time periods (morning/day/evening/night), translates weather condition codes to local language, and sends formatted message with temperature, feels-like, humidity, and wind speed.

**Why it matters**: Eliminates the need to check weather apps; proactive information delivery before the day starts.

**Real-world example**: Saratov, Russia - daily forecast at 51.53, 46.03 coordinates with Russian language output.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `weather` | Built-in | Fetch forecast data |
| `telegram` | Built-in | Deliver report |
| `cron` | Built-in | Daily automation |

## How to Setup

### 1. Get API Key

```
1. Visit https://yandex.ru/pogoda/b2b/smarthome
2. Register for free API key (50 requests/day)
3. Save key to environment: YANDEX_WEATHER_API_KEY
```

### 2. Configure Location

```javascript
const CONFIG = {
  lat: 51.53,      // Your latitude
  lon: 46.03,      // Your longitude
  lang: "ru_RU",   // Output language
  timezone: "Europe/Moscow"
};
```

### 3. Create Weather Parser

```javascript
const conditionMap = {
  "clear": "ясно",
  "overcast": "пасмурно",
  "cloudy": "облачно",
  "rain": "дождь",
  "snow": "снег",
  "partly-cloudy": "переменная облачность"
};

function formatWeather(data) {
  const parts = data.forecasts[0].parts;
  return `
🌤️ Погода на сегодня:

🌅 Утро: ${parts.morning.temp_avg}°C (${conditionMap[parts.morning.condition]})
🌞 День: ${parts.day.temp_avg}°C (ощущается ${parts.day.feels_like}°C)
🌆 Вечер: ${parts.evening.temp_avg}°C
🌙 Ночь: ${parts.night.temp_avg}°C

💧 Влажность: ${parts.day.humidity}%
💨 Ветер: ${parts.day.wind_speed} м/с
  `.trim();
}
```

### 4. Prompt Template

Add to your `SKILL.md`:

```markdown
## Weather Morning Report

Every morning at 09:00 local time:
1. Fetch weather from Yandex API using configured coordinates
2. Parse 4 time periods: morning, day, evening, night
3. Translate condition codes to Russian
4. Format message with emojis
5. Send via Telegram
6. Log temperature to memory/weather-log.md for trends

Alert if:
- Temperature drops below -15°C
- Wind speed > 15 m/s
- Precipitation expected during commute hours
```

### 5. Cron Configuration

```json
{
  "schedule": "0 9 * * *",
  "timezone": "Europe/Moscow",
  "task": "weather_report",
  "action": "fetch_and_send_weather"
}
```

### 6. Telegram Message Format

```markdown
🌤️ Погода на {{date}}

🌅 Утро: {{morning_temp}}°C ({{morning_condition}})
🌞 День: {{day_temp}}°C (ощущается {{feels_like}}°C)
🌆 Вечер: {{evening_temp}}°C
🌙 Ночь: {{night_temp}}°C

💧 Влажность: {{humidity}}%
💨 Ветер: {{wind_speed}} м/с

{{#alert}}
⚠️ {{alert_message}}
{{/alert}}
```

## Success Metrics

- [ ] Delivered at 09:00 ± 2 minutes
- [ ] All 4 time periods included
- [ ] Alerts sent for extreme weather
- [ ] 30-day temperature trend available

## API Limits

| Tier | Requests/Day | Cost |
|------|--------------|------|
| Free | 50 | $0 |
| Standard | 1000 | $10/month |
| Business | Unlimited | $50/month |

---

*Example: MyxAI (Moltbook) - "Yandex Weather API automation"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/weather-morning-report
cd ~/weather-morning-report
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

建立 `main.py`，實作 天氣晨間報告 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_weather_morning_report():
    """執行 天氣晨間報告 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 天氣晨間報告 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_weather_morning_report()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/weather-morning-report && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
