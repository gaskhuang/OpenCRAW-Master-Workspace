# 🖥️ 單機多實例 HA 部署方案研究報告 (2025-2026)

> 研究日期：2026-02-26  
> 關鍵字：single machine high availability、docker compose autoheal、PM2 cluster、systemd multi-instance

---

## 📋 總覽：單機 HA 的核心概念

單機 HA 的目標是在單一伺服器（如 Mac Mini）上，透過運行應用的多個實例，來避免單一實例故障導致服務中斷。當某個實例崩潰或無回應時，自動化工具會將其重啟，或由負載均衡器將流量轉發到健康的實例上。

---

## 1️⃣ Docker Compose + Autoheal

### 🔗 熱門 GitHub 專案
- **[willfarrell/autoheal](https://github.com/willfarrell/autoheal)** - 最受歡迎的 autoheal 實作，輕量級容器監控與自動重啟

### 📝 設定範例

```yaml
version: '3.8'

services:
  # 應用程式服務
  my-app:
    build: .
    ports:
      - "8080:80"
    
    # 健康檢查設定
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s
    
    # Autoheal 標籤
    labels:
      - autoheal.start.period=30
      - autoheal.stop.timeout=10

  # Autoheal 監控服務
  autoheal:
    image: willfarrell/autoheal
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - AUTOHEAL_POLL_INTERVAL=5

  # 多實例負載均衡 (可選)
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - my-app
```

### ✅ 優缺點
| 優點 | 缺點 |
|------|------|
| 環境隔離最佳（容器級） | 輕微虛擬化性能開銷 |
| 健康檢查靈活（HTTP/TCP/腳本） | 需理解 Docker 概念 |
| 生態系成熟，易擴展 | - |
| 跨平台一致性 | - |

---

## 2️⃣ PM2 Cluster Mode

### 🔗 參考資源
- [PM2 官方文件 - Cluster Mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/)
- GitHub: [Unitech/pm2](https://github.com/Unitech/pm2)

### 📝 設定範例 (ecosystem.config.js)

```javascript
module.exports = {
  apps: [{
    name: 'my-node-app',
    script: 'app.js',

    // Cluster Mode 設定
    instances: 'max',      // 啟動與 CPU 核心數相同的實例
    exec_mode: 'cluster',  // 啟用叢集模式

    // 自動重啟設定
    autorestart: true,
    restart_delay: 5000,
    max_memory_restart: '200M',

    // 優雅重啟（零停機更新）
    kill_timeout: 5000,
    listen_timeout: 10000,

    env: {
      NODE_ENV: 'development',
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 80,
    }
  }]
};
```

### 🔧 常用命令
```bash
# 啟動應用
pm2 start ecosystem.config.js --env production

# 優雅重啟（零停機）
pm2 reload my-node-app

# 查看狀態
pm2 status
pm2 monit

# 保存設定並設為開機啟動
pm2 save
pm2 startup
```

### ✅ 優缺點
| 優點 | 缺點 |
|------|------|
| 輕量高效，資源開銷極低 | 主要針對 Node.js |
| 零停機更新（內建 reload） | 健康檢查較基礎（僅進程存活） |
| 命令列直觀易用 | - |
| 自動負載均衡 | - |

---

## 3️⃣ Systemd Multi-instance / macOS Launchd

### 🐧 Linux Systemd 設定

**檔案**: `/etc/systemd/system/my-app@.service`

```ini
[Unit]
Description=My App Instance %I
After=network.target

[Service]
ExecStart=/usr/bin/node /path/to/your/app.js --instance=%I
WorkingDirectory=/path/to/your/app
User=myuser
Group=mygroup
Environment="NODE_ENV=production"

# 自動重啟設定
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
```

**管理命令**:
```bash
# 啟動多個實例
sudo systemctl start my-app@1.service
sudo systemctl start my-app@2.service

# 開機自啟
sudo systemctl enable my-app@1.service
sudo systemctl enable my-app@2.service

# 查看狀態
sudo systemctl status my-app@1.service
```

### 🍎 macOS Launchd 設定

**檔案**: `~/Library/LaunchAgents/com.myapp.instance1.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.myapp.instance1</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/Users/user/app/app.js</string>
        <string>--instance=1</string>
        <string>--port=3001</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/user/app</string>
    
    <!-- 自動重啟設定 -->
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>Crashed</key>
        <true/>
    </dict>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/user/app/logs/instance1.out.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/user/app/logs/instance1.err.log</string>
</dict>
</plist>
```

**管理命令**:
```bash
# 載入服務
launchctl load ~/Library/LaunchAgents/com.myapp.instance1.plist

# 啟動服務
launchctl start com.myapp.instance1

# 查看狀態
launchctl list | grep com.myapp

# 卸載服務
launchctl unload ~/Library/LaunchAgents/com.myapp.instance1.plist
```

### ✅ 優缺點
| 優點 | 缺點 |
|------|------|
| 系統級整合，穩定性高 | 平台綁定（systemd/Launchd） |
| 資源開銷最低 | 設定較繁瑣 |
| - | 不支援零停機更新 |
| - | 健康檢查需額外腳本 |

---

## 4️⃣ 健康檢查實作方式

### HTTP 健康檢查
```bash
# Docker Compose 範例
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 10s
  timeout: 5s
  retries: 3
```

### TCP 連線檢查
```bash
# 自定義腳本範例
#!/bin/bash
nc -z localhost 6379 || exit 1  # 檢查 Redis
nc -z localhost 5432 || exit 1  # 檢查 PostgreSQL
exit 0
```

### 應用層深度檢查
```javascript
// Node.js /health 端點範例
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    diskSpace: checkDiskSpace(),
    memory: process.memoryUsage().rss < 500 * 1024 * 1024
  };
  
  const allHealthy = Object.values(checks).every(v => v === true);
  
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'healthy' : 'unhealthy',
    checks,
    timestamp: new Date().toISOString()
  });
});
```

---

## 5️⃣ Mac Mini 單機部署評估

### 🎯 適用性：**非常高**

Mac Mini（特別是 M1/M2/M3/M4 系列）是極佳的單機伺服器選擇：

- **性能強大**：多核心性能出色，輕鬆運行多個容器/進程
- **能效比高**：極度省電，適合 24/7 運行
- **穩定性好**：macOS 基於 UNIX，系統穩定性高

### 📊 資源配置建議

| 規格 | 建議實例數 | 建議方案 |
|------|-----------|----------|
| Mac Mini M4 (16GB) | 4-6 個實例 | Docker Compose + autoheal |
| Mac Mini M4 (24GB) | 6-10 個實例 | Docker Compose + autoheal |
| Mac Mini M4 (32GB+) | 10+ 個實例 | Docker Compose + PM2 混合 |

### 🏆 推薦方案排序

1. **首選：Docker Compose + autoheal**
   - 最現代化、功能全面
   - 跨平台一致性
   - 易於擴展

2. **Node.js 專案：PM2 Cluster Mode**
   - 極致輕量化
   - 零停機更新
   - 內建負載均衡

3. **特定需求：Launchd (macOS)**
   - 系統級整合
   - 資源開銷最低
   - 適合背景常駐服務

---

## 📊 方案比較總表

| 特性 | Docker + Autoheal | PM2 Cluster | Systemd/Launchd |
|------|-------------------|-------------|-----------------|
| **適用場景** | 所有容器化應用 | 主要 Node.js | 任何二進制/腳本 |
| **隔離性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **健康檢查** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **零停機更新** | 需額外設定 | ⭐⭐⭐⭐⭐ | ❌ |
| **跨平台** | ✅ | ✅ | ❌ |
| **資源開銷** | 中等 | 極低 | 最低 |
| **推薦度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🔗 參考連結

1. [willfarrell/autoheal - GitHub](https://github.com/willfarrell/autoheal)
2. [PM2 Cluster Mode 官方文件](https://pm2.keymetrics.io/docs/usage/cluster-mode/)
3. [systemd 模板服務文件](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
4. [Apple Launchd 官方文件](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html)

---

*報告產生時間：2026-02-26*  
*研究工具：Gemini AI Search*
