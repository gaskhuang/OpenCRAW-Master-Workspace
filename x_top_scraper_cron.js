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
    
    console.log('🌐 導航到 X.com...');
    await Page.navigate({ url: 'https://x.com/home' });
    await Page.loadEventFired();
    await sleep(8000);
    
    const extractTweets = async () => {
      const result = await Runtime.evaluate({
        expression: `
          (function() {
            const articles = document.querySelectorAll('article');
            const extracted = [];
            
            articles.forEach(article => {
              try {
                const timeEl = article.querySelector('time');
                if (!timeEl) return;
                
                // 找 tweet ID - 從時間元素開始往上找
                let href = '';
                let linkEl = timeEl.closest('a');
                if (linkEl) {
                  href = linkEl.getAttribute('href') || '';
                }
                
                // 備用方案
                if (!href.includes('/status/')) {
                  const statusLinks = article.querySelectorAll('a[href*="/status/"]');
                  for (const a of statusLinks) {
                    const h = a.getAttribute('href');
                    if (h && h.includes('/status/')) {
                      href = h;
                      break;
                    }
                  }
                }
                
                const match = href.match(/status\/(\d+)/);
                if (!match) return;
                const tweetId = match[1];
                
                // 找正文 - 多種策略
                let text = '';
                const textEl = article.querySelector('[data-testid="tweetText"]');
                if (textEl) {
                  text = textEl.innerText.trim();
                } else {
                  // 備用：從文章內所有文字節點提取
                  const textDivs = article.querySelectorAll('div[dir="auto"]');
                  for (const div of textDivs) {
                    const t = div.innerText.trim();
                    if (t.length > 10 && t.length > text.length) {
                      text = t;
                    }
                  }
                }
                
                // 找作者 handle
                let authorHandle = '';
                let authorName = '';
                const allLinks = article.querySelectorAll('a[role="link"]');
                for (const a of allLinks) {
                  const h = a.getAttribute('href') || '';
                  if (h.startsWith('/') && !h.includes('/status/') && h.length > 1 && h.split('/').length === 2) {
                    authorHandle = h.split('/')[1];
                    // 找作者名稱
                    const nameSpan = a.querySelector('div[dir="ltr"] span');
                    if (nameSpan) authorName = nameSpan.textContent.trim();
                    break;
                  }
                }
                
                const timestamp = timeEl.getAttribute('datetime');
                const timeText = timeEl.textContent.trim();
                
                // 互動數提取
                const getCount = (testid) => {
                  const el = article.querySelector('[data-testid="' + testid + '"]');
                  if (!el) return 0;
                  const txt = el.innerText;
                  const numMatch = txt.match(/([\d,.]+)([KkMm]?)\s*$/);
                  if (!numMatch) return 0;
                  const num = parseFloat(numMatch[1].replace(/,/g, ''));
                  const suffix = numMatch[2].toUpperCase();
                  if (suffix === 'K') return Math.round(num * 1000);
                  if (suffix === 'M') return Math.round(num * 1000000);
                  return Math.round(num);
                };
                
                extracted.push({
                  tweetId,
                  authorName: authorName || authorHandle,
                  authorHandle: authorHandle ? '@' + authorHandle : '',
                  text,
                  timestamp,
                  timeText,
                  likes: getCount('like'),
                  retweets: getCount('retweet'),
                  replies: getCount('reply'),
                  url: 'https://x.com' + href.split('?')[0]
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
    console.log('  初始: ' + allTweets.length + ' 條推文');
    
    // 滾動 80 次
    console.log('📜 開始滾動 80 次...');
    for (let i = 0; i < 80; i++) {
      await Runtime.evaluate({
        expression: 'window.scrollTo(0, document.body.scrollHeight);',
        returnByValue: true
      });
      await sleep(1000 + Math.random() * 600);
      
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
        console.log('  滾動 ' + (i+1) + '/80 - 新增 ' + added + ' 條，總計 ' + allTweets.length);
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
    
    console.log('\n✅ 完成! 共抓取 ' + allTweets.length + ' 條推文');
    
    // 保存結果
    const outputDir = '/Users/user/data';
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputFile = path.join(outputDir, 'x_top_raw_' + timestamp + '.json');
    fs.writeFileSync(outputFile, JSON.stringify(allTweets, null, 2));
    
    console.log('💾 已保存: ' + outputFile);
    console.log('\nOUTPUT_FILE:' + outputFile);
    console.log('TOTAL_TWEETS:' + allTweets.length);
    
    // 顯示前5條
    console.log('\n🔥 熱門推文 TOP 5:');
    allTweets.slice(0, 5).forEach((t, i) => {
      console.log((i+1) + '. [' + t.engagement + '] ' + t.authorName + ': ' + t.text.substring(0, 50) + '...');
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
