#!/bin/bash
# Threads 抓取腳本 - 使用 browser-use

set -e

echo "🚀 Threads Top News Reporter 啟動..."
echo "時間: $(date '+%Y/%m/%d %H:%M')"

# 創建數據目錄
mkdir -p /Users/user/data

# 初始化數據文件
DATA_FILE="/Users/user/data/threads_raw_$(date '+%Y%m%d_%H%M').json"
echo "[]" > "$DATA_FILE"

# 打開 Threads
echo "🌐 打開 Threads..."
browser-use --browser real open https://www.threads.net
sleep 10

# 檢查頁面
echo "🔍 檢查頁面狀態..."
STATE=$(browser-use state 2>&1)
if echo "$STATE" | grep -q "Forbidden\|login\|登入"; then
    echo "❌ Threads 需要登入或被阻擋"
    exit 1
fi

echo "✅ 頁面已載入"

# 提取數據的 JavaScript 函數
extract_posts() {
    browser-use eval '
    (function() {
        const posts = [];
        const seenIds = new Set();
        
        const allDivs = document.querySelectorAll("div[data-pressable-container=\"true\"]");
        
        allDivs.forEach(container => {
            try {
                let text = "";
                const spans = container.querySelectorAll("span[dir=\"auto\"]");
                for (const span of spans) {
                    const txt = span.innerText.trim();
                    if (txt.length > 20 && !txt.match(/^(Like|Reply|Repost|Share|・)$/)) {
                        text = txt;
                        break;
                    }
                }
                
                if (!text || text.length < 20) return;
                
                let author = "";
                let authorHandle = "";
                const links = container.querySelectorAll("a");
                for (const link of links) {
                    const href = link.getAttribute("href") || "";
                    if (href.startsWith("/@")) {
                        const parts = href.split("/");
                        if (parts[1]) {
                            authorHandle = parts[1].replace("@", "");
                            author = link.innerText.trim() || authorHandle;
                            break;
                        }
                    }
                }
                
                let postUrl = "";
                let postId = "";
                for (const link of links) {
                    const href = link.getAttribute("href") || "";
                    if (href.includes("/post/")) {
                        const match = href.match(/\\/post\\/([^/?]+)/);
                        if (match && !seenIds.has(match[1])) {
                            postId = match[1];
                            seenIds.add(postId);
                            postUrl = href.startsWith("http") ? href.split("?")[0] : "https://www.threads.net" + href.split("?")[0];
                            break;
                        }
                    }
                }
                
                if (!postId) return;
                
                let timeText = "";
                const timeEl = container.querySelector("time");
                if (timeEl) {
                    timeText = timeEl.innerText.trim() || timeEl.getAttribute("datetime") || "";
                }
                
                const fullText = container.innerText;
                let likes = 0;
                let comments = 0;
                
                const likeMatch = fullText.match(/(\\d+(?:,\\d+)*)\\s*(?:like|likes|個讚|讚)/i);
                if (likeMatch) likes = parseInt(likeMatch[1].replace(/,/g, ""));
                
                const replyMatch = fullText.match(/(\\d+(?:,\\d+)*)\\s*(?:reply|replies|則回覆|回覆)/i);
                if (replyMatch) comments = parseInt(replyMatch[1].replace(/,/g, ""));
                
                posts.push({
                    postId,
                    author: author || authorHandle || "unknown",
                    authorHandle: authorHandle || "",
                    text: text.substring(0, 500),
                    timeText,
                    likes,
                    comments,
                    url: postUrl,
                    engagement: likes + comments
                });
            } catch (e) {}
        });
        
        return JSON.stringify(posts);
    })()
    '
}

# 初始提取
echo "📥 初始提取..."
INITIAL_DATA=$(extract_posts 2>&1 | grep -o '\[.*\]' || echo "[]")
echo "$INITIAL_DATA" > "$DATA_FILE"
INITIAL_COUNT=$(echo "$INITIAL_DATA" | grep -o '"postId"' | wc -l)
echo "  初始: $INITIAL_COUNT 條貼文"

# 滾動 80 次
echo "📜 開始滾動 80 次..."
for i in $(seq 1 80); do
    browser-use scroll down --amount 800 > /dev/null 2>&1
    sleep 0.8
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "  滾動 $i/80..."
    fi
done

# 最終提取
echo "📥 最終提取..."
FINAL_DATA=$(extract_posts 2>&1 | grep -o '\[.*\]' || echo "[]")
echo "$FINAL_DATA" > "$DATA_FILE"
FINAL_COUNT=$(echo "$FINAL_DATA" | grep -o '"postId"' | wc -l)
echo "✅ 完成! 共抓取 $FINAL_COUNT 條貼文"

echo "💾 數據保存至: $DATA_FILE"
echo "OUTPUT_FILE: $DATA_FILE"

# 關閉瀏覽器
browser-use close 2>/dev/null || true
