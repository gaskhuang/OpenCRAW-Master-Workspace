const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 19222;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  let client;
  
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
    
    // 檢查頁面內容
    console.log('🔍 檢查頁面狀態...');
    const pageInfo = await Runtime.evaluate({
      expression: `
        (function() {
          const title = document.title;
          const url = window.location.href;
          const articles = document.querySelectorAll('article').length;
          const bodyText = document.body.innerText.substring(0, 500);
          return { title, url, articles, bodyText };
        })()
      `,
      returnByValue: true
    });
    
    console.log('頁面資訊:', JSON.stringify(pageInfo.result.value, null, 2));
    
    // 嘗試多種選擇器提取推文
    const tweets = await Runtime.evaluate({
      expression: `
        (function() {
          const results = [];
          
          // 方法1: 標準 article[data-testid="tweet"]
          let articles = document.querySelectorAll('article[data-testid="tweet"]');
          results.push({ method: 'data-testid tweet', count: articles.length });
          
          // 方法2: 所有 article
          articles = document.querySelectorAll('article');
          results.push({ method: 'all articles', count: articles.length });
          
          // 方法3: 嘗試其他常見選擇器
          const selectors = [
            '[data-testid="cellInnerDiv"]',
            '[data-testid="tweetText"]',
            'div[role="article"]'
          ];
          
          selectors.forEach(sel => {
            const els = document.querySelectorAll(sel);
            if (els.length > 0) {
              results.push({ method: sel, count: els.length });
            }
          });
          
          // 提取實際推文數據
          const allArticles = document.querySelectorAll('article');
          const extracted = [];
          
          allArticles.forEach((article, idx) => {
            try {
              // 嘗試找到時間元素
              const timeEl = article.querySelector('time');
              if (!timeEl) return;
              
              const linkEl = timeEl.closest('a') || article.querySelector('a[href*="/status/"]');
              if (!linkEl) return;
              
              const href = linkEl.getAttribute('href');
              const match = href.match(/status\/(\d+)/);
              if (!match) return;
              
              const tweetId = match[1];
              
              // 作者
              const authorEl = article.querySelector('a[role="link"]');
              const author = authorEl ? authorEl.textContent.trim() : '';
              
              // 正文
              const textEl = article.querySelector('[data-testid="tweetText"]');
              const text = textEl ? textEl.textContent.trim() : '';
              
              // 時間
              const time = timeEl.getAttribute('datetime');
              
              // 互動數
              const getCount = (testid) => {
                const el = article.querySelector('[data-testid="' + testid + '"]');
                if (!el) return 0;
                const span = el.querySelector('span');
                if (!span) return 0;
                const txt = span.textContent.trim();
                if (!txt) return 0;
                if (txt.includes('K')) return parseFloat(txt.replace('K', '')) * 1000;
                if (txt.includes('M')) return parseFloat(txt.replace('M', '')) * 1000000;
                return parseInt(txt.replace(/[^0-9]/g, '')) || 0;
              };
              
              extracted.push({
                tweetId,
                author: author.substring(0, 50),
                text: text.substring(0, 200),
                time,
                likes: getCount('like'),
                retweets: getCount('retweet'),
                replies: getCount('reply'),
                url: 'https://x.com' + href
              });
            } catch (e) {}
          });
          
          return { diagnostics: results, tweets: extracted.slice(0, 5) };
        })()
      `,
      returnByValue: true
    });
    
    console.log('診斷結果:', JSON.stringify(tweets.result.value, null, 2));
    
    // 如果成功提取，繼續滾動
    if (tweets.result.value.tweets.length > 0) {
      console.log('✅ 找到推文，開始滾動收集...');
      
      const allTweets = [...tweets.result.value.tweets];
      const seenIds = new Set(allTweets.map(t => t.tweetId));
      
      for (let i = 0; i < 80; i++) {
        await Runtime.evaluate({
          expression: 'window.scrollTo(0, document.body.scrollHeight);',
          returnByValue: true
        });
        await sleep(1000 + Math.random() * 500);
        
        if ((i + 1) % 5 === 0) {
          const newTweets = await Runtime.evaluate({
            expression: `
              (function() {
                const articles = document.querySelectorAll('article');
                const extracted = [];
                articles.forEach(article => {
                  try {
                    const timeEl = article.querySelector('time');
                    if (!timeEl) return;
                    const linkEl = timeEl.closest('a');
                    if (!linkEl) return;
                    const href = linkEl.getAttribute('href');
                    const match = href.match(/status\/(\d+)/);
                    if (!match) return;
                    
                    const tweetId = match[1];
                    const textEl = article.querySelector('[data-testid="tweetText"]');
                    const text = textEl ? textEl.textContent.trim() : '';
                    
                    const getCount = (testid) => {
                      const el = article.querySelector('[data-testid="' + testid + '"]');
                      if (!el) return 0;
                      const span = el.querySelector('span');
                      if (!span) return 0;
                      const txt = span.textContent.trim();
                      if (!txt) return 0;
                      if (txt.includes('K')) return parseFloat(txt.replace('K', '')) * 1000;
                      if (txt.includes('M')) return parseFloat(txt.replace('M', '')) * 1000000;
                      return parseInt(txt.replace(/[^0-9]/g, '')) || 0;
                    };
                    
                    extracted.push({
                      tweetId,
                      author: '',
                      text: text.substring(0, 200),
                      time: timeEl.getAttribute('datetime'),
                      likes: getCount('like'),
                      retweets: getCount('retweet'),
                      replies: getCount('reply'),
                      url: 'https://x.com' + href
                    });
                  } catch (e) {}
                });
                return extracted;
              })()
            `,
            returnByValue: true
          });
          
          let added = 0;
          newTweets.result.value.forEach(t => {
            if (!seenIds.has(t.tweetId)) {
              seenIds.add(t.tweetId);
              allTweets.push(t);
              added++;
            }
          });
          console.log(`  滾動 ${i+1}/80 - 新增 ${added} 條，總計 ${allTweets.length}`);
        }
      }
      
      // 保存結果
      const outputDir = '/Users/user/data';
      if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
      
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const outputFile = path.join(outputDir, `x_top_raw_${timestamp}.json`);
      fs.writeFileSync(outputFile, JSON.stringify(allTweets, null, 2));
      
      console.log(`\n✅ 完成! 共抓取 ${allTweets.length} 條推文`);
      console.log(`OUTPUT_FILE:${outputFile}`);
      
    } else {
      console.log('❌ 未找到推文，可能需要登入');
    }
    
  } catch (err) {
    console.error('❌ 錯誤:', err.message);
  } finally {
    if (client) await client.close();
  }
}

main();
