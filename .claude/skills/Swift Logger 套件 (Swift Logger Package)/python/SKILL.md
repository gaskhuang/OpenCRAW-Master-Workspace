---
name: Swift Logger 套件 (Swift Logger Package)/python
description: "Use Case #163 Python 方案: Swift Logger 套件。使用 Python 實作 Swift Logger Package 自動化系統。"
allowed-tools: Read, Grep, Glob, Bash(pip *), Bash(python *), Bash(mkdir *), Bash(touch *)
---

# Use Case #163: Swift Logger 套件 — Python 方案

> 技術棧: Python 3.9+ / 相關 SDK / Anthropic SDK
> 難度: 中級 | 分類: 開發者工具

---

## 原始需求 (來自 Source Repos)

# Swift Logger Package

## Introduction

Custom Swift logging package built with full TDD workflow. Demonstrates autonomous package development for iOS/macOS agent integrations.

**Why it matters**: Platform-specific tools extend agent capabilities. TDD ensures reliability.

**Real-world example**: Agent designs DelamainLogger API, writes tests first, implements to make tests pass, publishes to GitHub.

## Skills You Need

| Skill | Source | Purpose |
|-------|--------|---------|
| `swift` | Built-in | Development |
| `git` | Built-in | Version control |

## How to Setup

### 1. TDD Workflow

```swift
// 1. Write test first
func testLoggerWritesToFile() {
  let logger = DelamainLogger(path: "/tmp/test.log")
  logger.info("test message")
  XCTAssertTrue(FileManager.default.fileExists("/tmp/test.log"))
}

// 2. Implement to pass test
public class DelamainLogger {
  public func info(_ message: String) {
    // Implementation
  }
}
```

### 2. Prompt Template

```markdown
## Swift Logger Package

Development workflow:
1. Define API requirements
2. Write unit tests (red)
3. Implement minimum code (green)
4. Refactor while tests pass
5. Document API
6. Tag release
7. Publish to GitHub

Quality gates:
- 100% test coverage
- SwiftLint passing
- Documentation complete
```

## Success Metrics

- [ ] All tests passing
- [ ] Published to GitHub
- [ ] Documentation complete

---

*Example: Delamain (Moltbook) - "shipped second Swift package"*


---

## Python 實作指南

### Step 1: 環境設定

```bash
mkdir -p ~/swift-logger-package
cd ~/swift-logger-package
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

建立 `main.py`，實作 Swift Logger 套件 的核心邏輯。

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def run_swift_logger_package():
    """執行 Swift Logger 套件 主流程"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": "請協助我執行 Swift Logger 套件 任務。"}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    result = run_swift_logger_package()
    print(result)
```

### Step 4: 排程執行

```bash
# 加入 crontab（每日執行）
# 0 9 * * * cd ~/swift-logger-package && python3 main.py >> output.log 2>&1
```

---

## 進階功能

- 加入錯誤重試機制
- 整合 Telegram/Slack 通知
- 持久化結果到本地 SQLite
