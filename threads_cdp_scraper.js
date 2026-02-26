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
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    // 打開 Threads 首頁
    console.log('🌐 打開 Threads.net...');
    await Page.navigate({ url: 'https://www.threads.net' });
    await Page.loadEventFired();
    await sleep(10000);
    
    // 提取貼文函數
    const extractPosts = async () => {
      const result = await Runtime.evaluate({
        expression: `
          (function() {
            const posts = [];
            const articles = document.querySelectorAll('article, [role="article"]');
            
            articles.forEach(article => {
              try {
                // 提取文字內容
                let text = '';
                const textElements = article.querySelectorAll('span[dir="auto"]');
                for (const el of textElements) {
                  const txt = el.innerText.trim();
                  if (txt.length > 15 && !txt.includes('Like') && !txt.includes('Reply')) {
                    text = txt;
                    break;
                  }
                }
                
                if (!text) return;
                
                // 提取作者
                let author = '';
                let authorHandle = '';
                const authorLinks = article.querySelectorAll('a[href^="/@"]');
                for (const link of authorLinks) {
                  const href = link.getAttribute('href');
                  if (href && href.startsWith('/@')) {
                    authorHandle = href.replace('/@', '').split('/')[0];
                    author = link.innerText.trim() || authorHandle;
                    break;
                  }
                }
                
                // 提取貼文 URL 和 ID
                let postUrl = '';
                let postId = '';
                const postLinks = article.querySelectorAll('a[href*="/post/"]');
                for (const link of postLinks) {
                  const href = link.getAttribute('href');
                  if (href && href.includes('/post/')) {
                    const match = href.match(/\/post\/([^/?]+)/);
                    if (match) {
                      postId = match[1];
                      postUrl = 'https://www.threads.net' + href.split('?')[0];
                      break;
                    }
                  }
                }
                
                // 提取時間
                let timeText = '';
                const timeEl = article.querySelector('time');
                if (timeEl) {
                  timeText = timeEl.innerText.trim() || timeEl.getAttribute('datetime') || '';
                }
                
                // 提取互動數
                let likes = 0;
                let comments = 0;
                let reposts = 0;
                
                const allText = article.innerText;
                
                // Like patterns
                const likeMatch = allText.match(/(\d+(?:,\d+)*)\s*(?:likes?|讚)/i);
                if (likeMatch) likes = parseInt(likeMatch[1].replace(',', ''));
                
                // Comment patterns  
                const commentMatch = allText.match(/(\d+(?:,\d+)*)\s*(?:replies?|留言)/i);
                if (commentMatch) comments = parseInt(commentMatch[1].replace(',', ''));
                
                // Repost patterns
                const repostMatch = allText.match(/(\d+(?:,\d+)*)\s*(?:reposts?|轉發)/i);
                if (repostMatch) reposts = parseInt(repostMatch[1].replace(',', ''));
                
                if (postId && text) {
                  posts.push({
                    postId,
                    author: author || authorHandle,
                    authorHandle,
                    text: text.substring(0, 500),
                    timeText,
                    likes,
                    comments,
                    reposts,
                    url: postUrl,
                    engagement: likes + comments + reposts
                  });
                }
              } catch (e) {}
            });
            
            return posts;
          })()
        `,
        returnByValue: true
      });
      return result.result.value || [];
    };
    
    // 初始提取
    console.log('📥 初始提取...');
    let posts = await extractPosts();
    posts.forEach(p => {
      if (!seenIds.has(p.postId)) {
        seenIds.add(p.postId);
        allPosts.push(p);
      }
    });
    console.log(`  初始: ${allPosts.length} 條貼文`);
    
    // 滾動 80 次
    console.log('📜 開始滾動 80 次...');
    for (let i = 0; i < 80; i++) {
      await Runtime.evaluate({
        expression: 'window.scrollTo(0, document.body.scrollHeight);',
        returnByValue: true
      });
      await sleep(1000 + Math.random() * 500);
      
      if ((i + 1) % 5 === 0) {
        posts = await extractPosts();
        let added = 0;
        posts.forEach(p => {
          if (!seenIds.has(p.postId)) {
            seenIds.add(p.postId);
            allPosts.push(p);
            added++;
          }
        });
        console.log(`  滾動 ${i+1}/80 - 新增 ${added} 條，總計 ${allPosts.length}`);
      }
    }
    
    // 最終提取
    posts = await extractPosts();
    posts.forEach(p => {
      if (!seenIds.has(p.postId)) {
        seenIds.add(p.postId);
        allPosts.push(p);
      }
    });
    
    // 排序：按互動數
    allPosts.sort((a, b) => b.engagement - a.engagement);
    
    console.log(`\n✅ 完成! 共抓取 ${allPosts.length} 條貼文`);
    
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
      console.log(`${i+1}. [${p.engagement}] ${p.author}: ${p.text.substring(0, 50)}...`);
    });
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    console.error(err.stack);
    process.exit(1);
  } finally {
    if (client) await client.close();
  }
}

main();
