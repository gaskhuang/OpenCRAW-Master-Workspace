---
name: 天氣穿搭建議 (Weather-Based Outfit Suggestions)/python
description: "Use Case #022 Python 方案: 天氣穿搭建議。使用 Python 實作 Weather-Based Outfit Suggestions 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #022: 天氣穿搭建議 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 初級 | 分類: 日常生活自動化

---

## 原始需求 (來自 Source Repos)

# 天气穿搭顾问

## 简介

每天早上的"今天穿什么"问题？这个使用案例根据天气预报、你的日程安排和个人风格偏好，为你推荐每日穿搭。

**为什么重要**：节省时间，确保穿着得体，避免天气带来的尴尬。

**真实例子**：一位商务人士使用此代理后，不再因为天气突变而穿着不当，代理会根据他的会议安排推荐合适的着装。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `calendar` | [ClawdHub](https://clawhub.com/skills/calendar) | 查看日程 |
| `wardrobe` | [ClawdHub](https://clawhub.com/skills/wardrobe) | 管理衣橱 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送建议 |

---

## 设置步骤

### 1. 前置条件

- 天气 API 密钥
- 衣橱清单（可选）
- 个人风格偏好

### 2. 提示词模板

```markdown
## 天气穿搭顾问

你是我的时尚顾问。每天早上 7 点为我推荐穿搭：

### 输入数据
1. 今日天气预报（温度、降水、风力）
2. 日程安排（会议、活动类型）
3. 个人风格偏好
4. 衣橱可用选项

### 推荐逻辑
**温度 < 10°C**
- 保暖外套 + 毛衣 + 长裤
- 围巾、手套建议

**温度 10-20°C**
- 轻薄外套 + 长袖
- 可脱卸层次

**温度 > 20°C**
- 短袖/衬衫 + 轻薄下装
- 防晒建议

**雨天**
- 防水外套
- 雨鞋建议
- 带伞提醒

**正式场合**
- 西装/正装建议
- 配饰搭配

### 输出格式
```
🌤️ 今日天气：晴，15-22°C

👔 推荐穿搭：
- 上装：浅蓝色衬衫 + 灰色开衫
- 下装：深色西裤
- 鞋子：棕色皮鞋
- 配饰：简约手表

💡 特别提醒：
- 晚上有雨，带把伞
- 下午有客户会议，保持正式
```

### 学习偏好
- 记录我喜欢的搭配
- 记住我常穿的衣服
- 根据反馈调整推荐
```

### 3. 配置

```
Schedule: 0 7 * * *
Action: 获取天气 → 分析日程 → 生成建议 → 发送
```

---

## 成功指标

- [ ] 每天早上收到穿搭建议
- [ ] 建议符合天气和场合
- [ ] 节省选择穿搭的时间
- [ ] 穿着满意度提升

---

## 变体与扩展

### 变体 1：旅行打包助手
根据目的地天气和行程推荐打包清单。

### 变体 2：购物建议
根据衣橱缺口推荐需要购买的单品。

---

## 故障排除

### 问题：建议不符合个人风格
**解决方案**：提供更多风格偏好示例给代理学习。

### 问题：天气数据不准确
**解决方案**：检查天气 API 配置，考虑使用多个数据源。

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 天气早间报告

## 简介

每天早上了解天气情况对日程安排很重要。这个使用案例生成语音天气报告，包含今日天气、穿衣建议和出行提醒，通过 Telegram 或邮件发送。

**为什么重要**：及时了解天气变化，合理安排日程，避免天气带来的不便。

**真实例子**：一位通勤者使用此代理每天早上收到语音天气报告，根据建议调整出行方式和穿着，不再因为天气突变而措手不及。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `weather` | [ClawdHub](https://clawhub.com/skills/weather) | 获取天气 |
| `tts` | [ClawdHub](https://clawhub.com/skills/tts) | 文本转语音 |
| `telegram` | [ClawdHub](https://clawhub.com/skills/telegram) | 发送报告 |

---

## 设置步骤

### 1. 前置条件

- 天气 API 密钥
- TTS 服务
- Telegram Bot

### 2. 提示词模板

```markdown
## 天气早间报告

你是我的天气助手。每天早上生成天气报告：

### 报告内容

**当前天气**
- 温度
- 天气状况
- 湿度
- 风速

**今日预报**
- 最高/最低温度
- 降水概率
- 紫外线指数
- 空气质量

**穿衣建议**
- 上装建议
- 下装建议
- 配饰建议（伞、帽、墨镜）

**出行提醒**
- 交通影响
- 路况提醒
- 出行时间建议

### 语音报告格式

```
"早上好！今天是 [日期]。

当前温度 [X] 度，[天气状况]。
今天最高 [X] 度，最低 [X] 度，
降水概率 [X]%。

建议穿着：[穿衣建议]。
[出行提醒]。

祝您有美好的一天！"
```

### 文本报告格式

```
🌤️ 早间天气报告

📍 [城市]
🌡️ 当前：XX°C [状况]
📈 今日：XX°C / XX°C
💧 降水：XX%
💨 风速：XX km/h

👔 穿衣建议
- [建议 1]
- [建议 2]

🚗 出行提醒
- [提醒 1]

💡 今日提示
- [提示]
```

### 个性化
- 根据用户反馈调整建议
- 学习用户偏好
- 特殊天气提前提醒
```

### 3. 配置

```
Schedule: 0 7 * * *
Action: 获取天气 → 生成报告 → TTS → 发送
```

---

## 成功指标

- [ ] 每天早上准时收到报告
- [ ] 建议准确有用
- [ ] 出行准备充分
- [ ] 用户满意度高

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

## 所需套件

```txt
anthropic>=0.43.0        # Claude AI 核心
python-dotenv>=1.0.1     # 環境變數管理
requests>=2.32.3         # HTTP 請求
python-telegram-bot>=21.9 # Telegram 推送 (可選)
pytz>=2024.2             # 時區處理
schedule>=1.2.0          # 排程管理 (可選)
```

---

## 前置準備 Checklist

- [ ] Python 3.9+ 已安裝
- [ ] Claude API Key (console.anthropic.com)
- [ ] Telegram Bot Token (@BotFather) — 如需推送
- [ ] 相關第三方 API Key — 視 use case 需求

---

## 專案結構

```
weather-based-outfit-suggestions/
├── .env                    # 環境變數
├── requirements.txt        # Python 依賴
├── config.py              # 設定管理
├── main.py                # 主程式
├── core.py                # 核心業務邏輯
├── notifier.py            # 通知推送
└── output/                # 輸出資料夾
```

---

## 實作流程 (Step by Step)

### Step 1: 環境準備

```bash
mkdir -p weather-based-outfit-suggestions && cd weather-based-outfit-suggestions
python3 -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv requests python-telegram-bot pytz
```

### Step 2: 設定環境變數 (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
# 其他必要的 API keys
```

### Step 3: config.py — 設定管理

```python
"""Configuration management"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.ANTHROPIC_API_KEY: missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"Missing: {', '.join(missing)}")
```

### Step 4: core.py — 核心業務邏輯

根據 天氣穿搭建議 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Weather-Based Outfit Suggestions"""
import anthropic
from config import Config

def collect_data():
    """Collect data from relevant sources"""
    # TODO: Implement data collection
    # This depends on the specific use case
    pass

def analyze_with_ai(data):
    """Use Claude to analyze/process collected data"""
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"請分析以下資料並產生繁體中文報告：\n\n{data}"
        }]
    )
    return response.content[0].text
```

### Step 5: notifier.py — 通知推送

```python
"""Send notifications via Telegram"""
import requests
from config import Config

def send_telegram(text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    max_len = 4096
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        requests.post(url, json={
            "chat_id": Config.TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        })
```

### Step 6: main.py — 主程式

```python
"""Main orchestrator for Weather-Based Outfit Suggestions"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 天氣穿搭建議 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 天氣穿搭建議 報告\n\n{result}")
        print("✅ Done!")
    else:
        print("⚠ No data collected")

if __name__ == "__main__":
    run()
```

### Step 7: 排程

```bash
# 每天執行
crontab -e
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/weather-based-outfit-suggestions.log 2>&1
```

---

## 測試步驟

| 階段 | 測試 | 預期結果 |
|------|------|---------|
| 1 | 環境變數 | Config.validate() 無錯誤 |
| 2 | 資料收集 | collect_data() 回傳資料 |
| 3 | AI 分析 | analyze_with_ai() 產生繁中報告 |
| 4 | 通知推送 | Telegram 收到訊息 |
| 5 | 完整流程 | python main.py 成功 |

---

## 常見陷阱

| 問題 | 解法 |
|------|------|
| API rate limit | 加入 retry + exponential backoff |
| Token 超過上限 | 分段處理，限制輸入長度 |
| Telegram 格式錯誤 | Markdown fallback 為純文字 |
| Cron 環境變數遺失 | 使用絕對路徑 + source .env |
