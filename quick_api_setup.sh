#!/bin/bash
# 🔑 OpenClaw API Key 快速配置工具

echo "🦞 OpenClaw API Key 配置助手"
echo ""

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 未找到配置文件，请先安装 OpenClaw"
    exit 1
fi

# 备份原配置
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d)"

echo "请输入你的 API Keys（按 Enter 跳过）:"
echo ""

# Google Gemini（免费）
echo "🌐 Google Gemini API Key"
echo "   获取方式: https://ai.google.dev/"
read -p "   输入: " google_key

# Moonshot（可选）
echo ""
echo "🌙 Moonshot (Kimi) API Key"
echo "   获取方式: https://platform.moonshot.cn/"
read -p "   输入: " moonshot_key

# OpenAI（可选）
echo ""
echo "🤖 OpenAI API Key"
echo "   获取方式: https://platform.openai.com/"
read -p "   输入: " openai_key

# 使用 Python 更新配置（更可靠）
python3 << EOF
import json

config_file = "$CONFIG_FILE"

with open(config_file, 'r') as f:
    config = json.load(f)

# 更新 Google
if "$google_key":
    if 'models' not in config:
        config['models'] = {}
    if 'providers' not in config['models']:
        config['models']['providers'] = {}
    if 'google' not in config['models']['providers']:
        config['models']['providers']['google'] = {}
    config['models']['providers']['google']['apiKey'] = "$google_key"
    print("✅ Google API Key 已配置")

# 更新 Moonshot
if "$moonshot_key":
    if 'moonshot' not in config['models']['providers']:
        config['models']['providers']['moonshot'] = {}
    config['models']['providers']['moonshot']['apiKey'] = "$moonshot_key"
    print("✅ Moonshot API Key 已配置")

# 更新 OpenAI
if "$openai_key":
    if 'openai' not in config['models']['providers']:
        config['models']['providers']['openai'] = {}
    config['models']['providers']['openai']['apiKey'] = "$openai_key"
    print("✅ OpenAI API Key 已配置")

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("")
print("🎉 配置完成！")
EOF

echo ""
echo "配置文件已备份到: $CONFIG_FILE.backup.$(date +%Y%m%d)"
echo ""
echo "现在可以启动服务: openclaw gateway start"