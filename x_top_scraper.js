const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

// 延遲函數
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 隨機延遲（防反爬蟲）
const randomDelay = async (min, max) => {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await sleep(delay);
};

// 提取推文數據
async function extractTweets(client) {
  const { Runtime } = client;
  
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const articles = document.querySelectorAll('article[data-testid="tweet"]');
        const tweets = [];
        
        articles.forEach((article, index) => {
          try {
            // 獲取 tweet_id 和連結
            const linkElement = article.querySelector('a[href*="/status/"]');
            let tweetId = '';
            let tweetUrl = '';
            if (linkElement) {
              const href = linkElement.getAttribute('href');
              const match = href.match(/\/status\/(\d+)/);
              if (match) {
                tweetId = match[1];
                tweetUrl = 'https://x.com' + href.split('?')[0];
              }
            }
            
            // 獲取作者
            const authorElement = article.querySelector('[data-testid="User-Name"] a');
            const author = authorElement ? authorElement.textContent.trim() : '';
            const authorHandle = authorElement ? authorElement.getAttribute('href')?.replace('/', '@') : '';
            
            // 獲取時間
            const timeElement = article.querySelector('time');
            const timestamp = timeElement ? timeElement.getAttribute('datetime') : '';
            const timeText = timeElement ? timeElement.textContent.trim() : '';
            
            // 獲取正文
            const textElement = article.querySelector('[data-testid="tweetText"]');
            const text = textElement ? textElement.textContent.trim() : '';
            
            // 獲取互動數
            const getCount = (testid) => {
              const el = article.querySelector('[data-testid="' + testid + '"]');
              if (!el) return 0;
              const text = el.textContent.trim();
              if (!text) return 0;
              // 處理 K/M 單位
              if (text.includes('K')) return parseFloat(text.replace('K', '')) * 1000;
              if (text.includes('M')) return parseFloat(text.replace('M', '')) * 1000000;
              return parseInt(text.replace(/[^0-9]/g, '')) || 0;
            };
            
            const likes = getCount('like');
            const retweets = getCount('retweet');
            const replies = getCount('reply');
            const bookmarks = getCount('bookmark');
            
            if (tweetId && text) {
              tweets.push({
                tweetId,
                author,
                authorHandle,
                timestamp,
                timeText,
                text,
                likes,
                retweets,
                replies,
                bookmarks,
                tweetUrl,
                engagement: likes + retweets + replies
              });
            }
          } catch (e) {}
        });
        
        return tweets;
      })()
    `,
    returnByValue: true
  });
  
  return result.result.value || [];
}

// 滾動頁面
async function scrollPage(client) {
  const { Runtime } = client;
  await Runtime.evaluate({
    expression: `window.scrollTo(0, document.body.scrollHeight);`,
    returnByValue: true
  });
}

// 主函數
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
    
    // 打開 X Top
    console.log('🌐 打開 X Top...');
    await Page.navigate({ url: 'https://x.com/explore/tabs/top' });
    await Page.loadEventFired();
    await sleep(5000);
    
    // 等待頁面加載
    console.log('⏳ 等待頁面加載...');
    await sleep(3000);
    
    // 滾動 80 次
    console.log('📜 開始滾動...');
    for (let i = 0; i < 80; i++) {
      await scrollPage(client);
      await randomDelay(800, 1500);
      
      // 每 5 次提取一次數據
      if ((i + 1) % 5 === 0) {
        const tweets = await extractTweets(client);
        let newCount = 0;
        tweets.forEach(tweet => {
          if (!seenIds.has(tweet.tweetId)) {
            seenIds.add(tweet.tweetId);
            allTweets.push(tweet);
            newCount++;
          }
        });
        console.log(`  滾動 ${i + 1}/80 - 新增 ${newCount} 條推文，總計 ${allTweets.length}`);
      }
      
      if ((i + 1) % 10 === 0) {
        console.log(`  已滾動 ${i + 1}/80 次...`);
      }
    }
    
    // 最後一次提取
    const finalTweets = await extractTweets(client);
    finalTweets.forEach(tweet => {
      if (!seenIds.has(tweet.tweetId)) {
        seenIds.add(tweet.tweetId);
        allTweets.push(tweet);
      }
    });
    
    console.log(`✅ 抓取完成，共 ${allTweets.length} 條推文`);
    
    // 保存結果
    const outputDir = '/Users/user/data';
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputFile = path.join(outputDir, `x_top_raw_${timestamp}.json`);
    fs.writeFileSync(outputFile, JSON.stringify(allTweets, null, 2));
    console.log(`💾 原始數據已保存: ${outputFile}`);
    
    // 輸出摘要到 stdout
    console.log('\n📊 抓取摘要:');
    console.log(JSON.stringify({
      total: allTweets.length,
      sample: allTweets.slice(0, 3).map(t => ({
        id: t.tweetId,
        author: t.author,
        engagement: t.engagement,
        text: t.text.substring(0, 50) + '...'
      }))
    }, null, 2));
    
    // 輸出結果檔案路徑
    console.log(`\nOUTPUT_FILE:${outputFile}`);
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
    process.exit(1);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

main();
