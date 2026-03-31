---
name: 每週事故摘要 (Weekly Incident Summary)/python
description: "Use Case #090 Python 方案: 每週事故摘要。使用 Python 實作 Weekly Incident Summary 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #090: 每週事故摘要 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK / Telegram Bot
> 難度: 中級 | 分類: 監控與維運

---

## 原始需求 (來自 Source Repos)

# 安全事件响应

## 简介

安全事件需要快速响应以减少损失。这个使用案例自动化安全事件响应流程，检测事件、分析影响、执行响应措施，并生成事件报告。

**为什么重要**：快速响应安全事件，减少损失，满足合规要求。

**真实例子**：一家公司遭受 DDoS 攻击，代理在 30 秒内检测到攻击，自动触发缓解措施，将服务中断时间从数小时缩短到几分钟。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `siem` | [ClawdHub](https://clawhub.com/skills/siem) | 安全监控 |
| `automation` | [ClawdHub](https://clawhub.com/skills/auto) | 自动响应 |
| `alert` | [ClawdHub](https://clawhub.com/skills/alert) | 发送告警 |

---

## 设置步骤

### 1. 前置条件

- SIEM 系统
- 响应剧本
- 通知渠道

### 2. 提示词模板

```markdown
## 安全事件响应

你是我的安全响应助手。自动化事件响应：

### 检测阶段

**事件类型**
- 恶意软件
- 数据泄露
- DDoS 攻击
- 入侵检测
- 内部威胁

**检测来源**
- SIEM 告警
- 用户报告
- 威胁情报
- 异常检测

### 响应流程

**1. 初步响应（0-15 分钟）**
- 确认事件
- 评估影响
- 通知团队
- 启动剧本

**2. 遏制措施（15-60 分钟）**
- 隔离受影响系统
- 阻断恶意 IP
- 禁用受损账号
- 保护证据

**3. 根除修复（1-24 小时）**
- 清除恶意软件
- 修复漏洞
- 恢复系统
- 验证安全

**4. 恢复运营（24-72 小时）**
- 恢复服务
- 监控异常
- 验证完整性
- 更新防护

### 事件报告

```
🚨 安全事件报告 - #[编号]

📋 基本信息
- 发现时间：YYYY-MM-DD HH:MM
- 事件类型：[类型]
- 影响范围：[描述]
- 严重程度：[严重/高危/中危/低危]

🔍 事件详情
- 攻击向量：[描述]
- 受影响资产：[列表]
- 数据泄露：[是/否，范围]

⚡ 响应行动
- [时间]：[行动]
- [时间]：[行动]

📊 影响评估
- 服务中断：XX 分钟
- 数据泄露：XX 条记录
- 财务损失：$XXXX

🛡️ 后续措施
1. [措施 1]
2. [措施 2]

📚 经验教训
- [经验 1]
- [经验 2]
```

### 自动化剧本

**DDoS 响应**
1. 检测流量异常
2. 启用 DDoS 防护
3. 通知 CDN 提供商
4. 调整防火墙规则
5. 监控缓解效果

**恶意软件响应**
1. 隔离受感染主机
2. 运行杀毒扫描
3. 分析恶意软件
4. 清除威胁
5. 恢复系统
```

### 3. 配置

```
Trigger: 安全告警
Action: 检测 → 分析 → 响应 → 恢复 → 报告
```

---

## 成功指标

- [ ] 检测时间 < 5 分钟
- [ ] 响应时间 < 15 分钟
- [ ] 恢复时间 < 4 小时
- [ ] 损失最小化

---

## 贡献者

- 作者：OpenClaw 社区
- 来源：Moltbook 社区


---

# 日志异常检测

## 简介

系统日志包含大量有价值的信息，但人工分析耗时。这个使用案例自动分析日志，检测异常模式，识别潜在问题，并生成洞察报告。

**为什么重要**：及时发现系统问题，预防故障，优化性能。

**真实例子**：一家电商公司使用此代理分析应用日志，代理识别出一个导致购物车丢失的 Bug，使转化率提高了 15%。

---

## 所需技能

| 技能 | 来源 | 用途 |
|------|------|------|
| `log_analysis` | [ClawdHub](https://clawhub.com/skills/logs) | 日志分析 |
| `ml` | [ClawdHub](https://clawhub.com/skills/ml) | 异常检测 |
| `alert` | [ClawdHub](https://clawhub.com/skills/alert) | 发送告警 |

---

## 设置步骤

### 1. 前置条件

- 日志访问权限
- 异常定义
- 告警渠道

### 2. 提示词模板

```markdown
## 日志异常检测

你是我的日志分析师。自动检测日志异常：

### 分析维度

**错误检测**
- ERROR 级别日志
- 异常堆栈
- 失败请求
- 超时记录

**性能检测**
- 响应时间异常
- 资源使用峰值
- 吞吐量下降
- 连接数异常

**安全检测**
- 登录失败
- 权限异常
- 注入攻击
- 异常访问模式

**业务检测**
- 交易失败
- 支付异常
- 用户行为异常
- 转化率下降

### 检测方法

**规则检测**
- 关键字匹配
- 阈值比较
- 模式匹配
- 正则表达式

**机器学习**
- 基线学习
- 异常评分
- 聚类分析
- 趋势预测

### 报告格式

```
📋 日志分析报告 - YYYY-MM-DD

🔍 异常摘要
- 严重异常：X 个
- 警告异常：X 个
- 信息异常：X 个

❌ 严重异常
1. [时间] [服务] [错误信息]
   影响：描述
   建议：操作

⚠️ 警告异常
1. [时间] [服务] [警告信息]
   趋势：描述
   建议：操作

📊 趋势分析
- 错误率：X% (环比 +/-X%)
- 平均响应：XXXms
- 峰值流量：XXX req/s

💡 洞察发现
- [发现 1]
- [发现 2]
```

### 自动化响应
- 严重错误立即通知
- 自动创建工单
- 关联相关日志
- 建议修复方案
```

### 3. 配置

```
Schedule: */15 * * * *
Action: 收集日志 → 分析 → 检测异常 → 发送报告
```

---

## 成功指标

- [ ] 异常检测准确率 > 90%
- [ ] 问题发现时间 < 5 分钟
- [ ] 误报率 < 10%
- [ ] 系统稳定性提升

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
weekly-incident-summary/
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
mkdir -p weekly-incident-summary && cd weekly-incident-summary
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

根據 每週事故摘要 的需求，實作資料收集與處理邏輯。

```python
"""Core business logic for Weekly Incident Summary"""
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
"""Main orchestrator for Weekly Incident Summary"""
from datetime import datetime
from config import Config
from core import collect_data, analyze_with_ai
from notifier import send_telegram

def run():
    print(f"=== 每週事故摘要 - {datetime.now():%Y-%m-%d %H:%M} ===")
    Config.validate()
    data = collect_data()
    if data:
        result = analyze_with_ai(data)
        send_telegram(f"📊 每週事故摘要 報告\n\n{result}")
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
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> /tmp/weekly-incident-summary.log 2>&1
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
