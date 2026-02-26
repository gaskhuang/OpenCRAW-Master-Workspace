const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  let client;
  const allPosts = [];
  const seenIds = new Set();
  
  try {
    console.log('🔌 連接到 CDP...');
    client = await CDP({ host: CDP_HOST, port: CDP_PORT });
    const { Page, Runtime, DOM } = client;
    
    await Page.enable();
    await Runtime.enable();
    await DOM.enable();
    
    // 導航到 Threads
    console.log('🌐 導航到 Threads.net...');
    await Page.navigate({ url: 'https://www.threads.net' });
    await Page.loadEventFired();
    console.log('⏳ 等待頁面加載...');
    await sleep(15000); // 等待 JavaScript 渲染
    
    // 檢查頁面內容
    const checkPage = await Runtime.evaluate({
      expression: `
        (function() {
          return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
            hasArticles: document.querySelectorAll('article').length,
            hasDivContent: document.querySelectorAll('div[data-pressable-container="true"]').length
          };
        })()
      `,
      returnByValue: true
    });
    console.log('📄 頁面狀態:', JSON.stringify(checkPage.result.value, null, 2));
    
    // 提取貼文函數 - 更積極的策略
    const extractPosts = async () => {
      const result = await Runtime.evaluate({
        expression: `
          (function() {
            const posts = [];
            
            // 策略 1: 尋找所有包含貼文內容的 div
            const allDivs = document.querySelectorAll('div');
            const postContainers = [];
            
            for (const div of allDivs) {
              // 尋找有 data-pressable-container 的 div
              if (div.getAttribute('data-pressable-container') === 'true') {
                postContainers.push(div);
              }
            }
            
            // 策略 2: 也嘗試 article 標籤
            document.querySelectorAll('article').forEach(a => postContainers.push(a));
            
            for (const container of postContainers) {
              try {
                // 提取文字
                let text = '';
                const spans = container.querySelectorAll('span[dir="auto"]');
                for (const span of spans) {
                  const txt = span.innerText.trim();
                  if (txt.length > 20 && !txt.match(/^(Like|Reply|Repost|Share|·)$/)) {
                    text = txt;
                    break;
                  }
                }
                
                if (!text || text.length < 20) continue;
                
                // 提取作者
                let author = '';
                let authorHandle = '';
                const links = container.querySelectorAll('a');
                for (const link of links) {
                  const href = link.getAttribute('href') || '';
                  if (href.startsWith('/@')) {
                    const parts = href.split('/');
                    if (parts[1]) {
                      authorHandle = parts[1].replace('@', '');
                      author = link.innerText.trim() || authorHandle;
                      break;
                    }
                  }
                }
                
                // 提取 URL 和 ID
                let postUrl = '';
                let postId = '';
                for (const link of links) {
                  const href = link.getAttribute('href') || '';
                  if (href.includes('/post/')) {
                    const match = href.match(/\/post\/([^/?]+)/);
                    if (match) {
                      postId = match[1];
                      postUrl = href.startsWith('http') ? href.split('?')[0] : 'https://www.threads.net' + href.split('?')[0];
                      break;
                    }
                  }
                }
                
                // 如果沒有找到 post ID，創建一個基於內容的 ID
                if (!postId && text) {
                  postId = 'text_' + text.substring(0, 30).replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '');
                  postUrl = authorHandle ? 'https://www.threads.net/@' + authorHandle : '';
                }
                
                // 提取時間
                let timeText = '';
                const timeEl = container.querySelector('time');
                if (timeEl) {
                  timeText = timeEl.innerText.trim() || timeEl.getAttribute('datetime') || '';
                }
                
                // 提取互動數
                const fullText = container.innerText;
                let likes = 0;
                let comments = 0;
                let reposts = 0;
                
                // 尋找數字模式
                const likePatterns = fullText.match(/(\d+(?:,\d+)*)\s*(?:like|讚|likes)/i);
                if (likePatterns) likes = parseInt(likePatterns[1].replace(/,/g, ''));
                
                const replyPatterns = fullText.match(/(\d+(?:,\d+)*)\s*(?:reply|replies|留言)/i);
                if (replyPatterns) comments = parseInt(replyPatterns[1].replace(/,/g, ''));
                
                const repostPatterns = fullText.match(/(\d+(?:,\d+)*)\s*(?:repost|reposts|轉發)/i);
                if (repostPatterns) reposts = parseInt(repostPatterns[1].replace(/,/g, ''));
                
                posts.push({
                  postId,
                  author: author || authorHandle || 'unknown',
                  authorHandle: authorHandle || '',
                  text: text.substring(0, 800),
                  timeText,
                  likes,
                  comments,
                  reposts,
                  url: postUrl,
                  engagement: likes + comments + reposts
                });
              } catch (e) {}
            }
            
            return posts;
          })()
        `,
        returnByValue: true
      });
      return result.result.value || [];
    };
    
    // 多次提取 + 滾動
    console.log('📥 開始提取...');
    
    for (let round = 0; round < 16; round++) {
      // 提取當前內容
      const posts = await extractPosts();
      let added = 0;
      posts.forEach(p => {
        if (!seenIds.has(p.postId)) {
          seenIds.add(p.postId);
          allPosts.push(p);
          added++;
        }
      });
      
      console.log(`  輪次 ${round + 1}/16 - 新增 ${added} 條，總計 ${allPosts.length}`);
      
      // 滾動
      await Runtime.evaluate({
        expression: `
          window.scrollTo(0, document.body.scrollHeight);
          document.body.scrollHeight;
        `,
        returnByValue: true
      });
      await sleep(2500 + Math.random() * 1000);
    }
    
    // 最終提取
    const finalPosts = await extractPosts();
    finalPosts.forEach(p => {
      if (!seenIds.has(p.postId)) {
        seenIds.add(p.postId);
        allPosts.push(p);
      }
    });
    
    // 排序：按互動數
    allPosts.sort((a, b) => b.engagement - a.engagement);
    
    console.log(`\n✅ 完成! 共抓取 ${allPosts.length} 條貼文`);
    
    if (allPosts.length > 0) {
      // 保存結果
      const outputDir = '/Users/user/data';
      if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
      
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const outputFile = path.join(outputDir, `threads_top_raw_${timestamp}.json`);
      fs.writeFileSync(outputFile, JSON.stringify(allPosts, null, 2));
      
      console.log(`💾 已保存: ${outputFile}`);
      console.log(`\nOUTPUT_FILE:${outputFile}`);
      console.log(`TOTAL_POSTS:${allPosts.length}`);
      
      // 顯示前5條
      console.log('\n🔥 熱門貼文 TOP 5:');
      allPosts.slice(0, 5).forEach((p, i) => {
        console.log(`${i+1}. [${p.engagement}] @${p.author}: ${p.text.substring(0, 50)}...`);
      });
      
      return outputFile;
    } else {
      console.log('⚠️ 未提取到任何貼文，可能 Threads 需要登入或有反爬機制');
      return null;
    }
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    console.error(err.stack);
    return null;
  } finally {
    if (client) await client.close();
  }
}

main().then(file => {
  process.exit(file ? 0 : 1);
});
