const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  let client;
  const allTweets = [];
  const seenIds = new Set();
  
  try {
    console.log('🔗 連接到 CDP...');
    client = await CDP({ host: CDP_HOST, port: CDP_PORT });
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    // 打開 X 首頁
    console.log('🌐 打開 X.com...');
    await Page.navigate({ url: 'https://x.com/home' });
    await Page.loadEventFired();
    await sleep(5000);
    
    // 提取推文函數
    const extractTweets = async () => {
      const result = await Runtime.evaluate({
        expression: `
          (function() {
            const articles = document.querySelectorAll('article');
            const extracted = [];
            
            articles.forEach(article => {
              try {
                // 找到時間元素
                const timeEl = article.querySelector('time');
                if (!timeEl) return;
                
                // 從時間元素獲取連結
                let linkEl = timeEl.closest('a');
                if (!linkEl) {
                  linkEl = article.querySelector('a[href*="/status/"]');
                }
                if (!linkEl) return;
                
                const href = linkEl.getAttribute('href');
                const match = href.match(/status\/(\d+)/);
                if (!match) return;
                
                const tweetId = match[1];
                
                // 正文
                const textEl = article.querySelector('[data-testid="tweetText"]');
                const text = textEl ? textEl.innerText.trim() : '';
                
                // 作者
                const authorEl = article.querySelector('a[role="link"] div[dir="ltr"] span');
                const authorName = authorEl ? authorEl.textContent.trim() : '';
                
                const handleEl = article.querySelector('a[role="link"][href^="/"]');
                const authorHandle = handleEl ? handleEl.getAttribute('href').split('/')[1] : '';
                
                // 時間
                const timestamp = timeEl.getAttribute('datetime');
                const timeText = timeEl.textContent.trim();
                
                // 互動數
                const getCount = (testid) => {
                  const el = article.querySelector('[data-testid="' + testid + '"]');
                  if (!el) return 0;
                  const spans = el.querySelectorAll('span');
                  for (const span of spans) {
                    const txt = span.textContent.trim();
                    if (txt && !isNaN(parseFloat(txt.replace(/[KM,]/g, '')))) {
                      if (txt.includes('K')) return Math.round(parseFloat(txt.replace('K', '')) * 1000);
                      if (txt.includes('M')) return Math.round(parseFloat(txt.replace('M', '')) * 1000000);
                      return parseInt(txt.replace(/[^0-9]/g, '')) || 0;
                    }
                  }
                  return 0;
                };
                
                extracted.push({
                  tweetId,
                  authorName,
                  authorHandle: '@' + authorHandle,
                  text,
                  timestamp,
                  timeText,
                  likes: getCount('like'),
                  retweets: getCount('retweet'),
                  replies: getCount('reply'),
                  bookmarks: getCount('bookmark'),
                  url: 'https://x.com' + href.split('?')[0],
                  engagement: 0
                });
              } catch (e) {}
            });
            
            return extracted;
          })()
        `,
        returnByValue: true
      });
      return result.result.value || [];
    };
    
    // 初始提取
    console.log('📥 初始提取...');
    let tweets = await extractTweets();
    tweets.forEach(t => {
      t.engagement = t.likes + t.retweets + t.replies;
      if (!seenIds.has(t.tweetId)) {
        seenIds.add(t.tweetId);
        allTweets.push(t);
      }
    });
    console.log(`  初始: ${allTweets.length} 條推文`);
    
    // 滾動 80 次
    console.log('📜 開始滾動 80 次...');
    for (let i = 0; i < 80; i++) {
      await Runtime.evaluate({
        expression: 'window.scrollTo(0, document.body.scrollHeight);',
        returnByValue: true
      });
      await sleep(1000 + Math.random() * 800);
      
      if ((i + 1) % 5 === 0) {
        tweets = await extractTweets();
        let added = 0;
        tweets.forEach(t => {
          t.engagement = t.likes + t.retweets + t.replies;
          if (!seenIds.has(t.tweetId)) {
            seenIds.add(t.tweetId);
            allTweets.push(t);
            added++;
          }
        });
        console.log(`  滾動 ${i+1}/80 - 新增 ${added} 條，總計 ${allTweets.length}`);
      }
    }
    
    // 最終提取
    tweets = await extractTweets();
    tweets.forEach(t => {
      t.engagement = t.likes + t.retweets + t.replies;
      if (!seenIds.has(t.tweetId)) {
        seenIds.add(t.tweetId);
        allTweets.push(t);
      }
    });
    
    // 排序：按互動數
    allTweets.sort((a, b) => b.engagement - a.engagement);
    
    console.log(`\n✅ 完成! 共抓取 ${allTweets.length} 條推文`);
    
    // 保存結果
    const outputDir = '/Users/user/data';
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputFile = path.join(outputDir, `x_top_raw_${timestamp}.json`);
    fs.writeFileSync(outputFile, JSON.stringify(allTweets, null, 2));
    
    console.log(`💾 已保存: ${outputFile}`);
    console.log(`\nOUTPUT_FILE:${outputFile}`);
    console.log(`TOTAL_TWEETS:${allTweets.length}`);
    
    // 顯示前3條
    console.log('\n熱門推文預覽:');
    allTweets.slice(0, 3).forEach((t, i) => {
      console.log(`${i+1}. ${t.authorName} (${t.engagement} 互動): ${t.text.substring(0, 60)}...`);
    });
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    console.error(err.stack);
  } finally {
    if (client) await client.close();
  }
}

main();
