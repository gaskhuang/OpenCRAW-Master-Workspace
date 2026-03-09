# Context Flush Reports

這裡存放 compact 前的 context flush checklist。

## 用法

```bash
python3 /Users/user/scripts/prepare_context_flush.py
```

或由：

```bash
/Users/user/scripts/lobster_memory_guard.sh
```

自動先跑 flush，再檢查主 session 使用率，必要時提醒執行 `/compact`。
