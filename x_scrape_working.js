const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  let client;
  const allTweets = [];
  const seenIds = new Set();
  
  try {
    console.log('🔗 連接到 CDP...');
    client = await CDP({ host: '127.0.0.1', port: 19222 });
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    console.log('🌐 導航到 X...');
    await Page.navigate({ url: 'https://x.com/home' });
    await Page.loadEventFired();
    await sleep(8000);
    
    // 提取函數
    const extract = async () => {
      const r = await Runtime.evaluate({
        expression: `
          (function() {
            const results = [];
            document.querySelectorAll('article').forEach(art => {
              const timeEl = art.querySelector('time');
              if (!timeEl) return;
              
              const linkEl = timeEl.closest('a');
              if (!linkEl) return;
              
              const href = linkEl.getAttribute('href');
              const match = href.match(/status\/(\d+)/);
              if (!match) return;
              
              const tweetId = match[1];
              const textEl = art.querySelector('[data-testid="tweetText"]');
              const text = textEl ? textEl.innerText.trim() : '';
              
              // 提取作者
              let author = '';
              let handle = '';
              const userLinks = art.querySelectorAll('a[role="link"]');
              for (const link of userLinks) {
                const h = link.getAttribute('href') || '';
                if (h.startsWith('/') && !h.includes('status') && h.split('/').length === 2) {
                  handle = h.replace('/', '');
                  const nameEl = link.querySelector('span');
                  author = nameEl ? nameEl.textContent.trim() : handle;
                  break;
                }
              }
              
              // 互動數
              const getNum = (sel) => {
                const el = art.querySelector('[data-testid="' + sel + '"]');
                if (!el) return 0;
                const txt = el.innerText;
                const m = txt.match(/([\d.]+)([KM]?)/i);
                if (!m) return 0;
                let n = parseFloat(m[1]);
                if (m[2].toUpperCase() === 'K') n *= 1000;
                if (m[2].toUpperCase() === 'M') n *= 1000000;
                return Math.round(n);
              };
              
              results.push({
                tweetId,
                author,
                handle: '@' + handle,
                text,
                time: timeEl.getAttribute('datetime'),
                likes: getNum('like'),
                retweets: getNum('retweet'),
                replies: getNum('reply'),
                url: 'https://x.com' + href.split('?')[0]
              });
            });
            return results;
          })()
        `,
        returnByValue: true
      });
      return r.result.value || [];
    };
    
    // 初始提取
    let tweets = await extract();
    tweets.forEach(t => {
      t.engagement = t.likes + t.retweets + t.replies;
      if (!seenIds.has(t.tweetId)) {
        seenIds.add(t.tweetId);
        allTweets.push(t);
      }
    });
    console.log(`📥 初始: ${allTweets.length} 條`);
    
    // 滾動 80 次
    console.log('📜 滾動中...');
    for (let i = 0; i < 80; i++) {
      await Runtime.evaluate({ expression: 'window.scrollTo(0, document.body.scrollHeight);' });
      await sleep(800 + Math.random() * 400);
      
      if ((i + 1) % 5 === 0) {
        tweets = await extract();
        let added = 0;
        tweets.forEach(t => {
          t.engagement = t.likes + t.retweets + t.replies;
          if (!seenIds.has(t.tweetId)) {
            seenIds.add(t.tweetId);
            allTweets.push(t);
            added++;
          }
        });
        console.log(`  ${i+1}/80: +${added} = ${allTweets.length} 條`);
      }
    }
    
    // 排序
    allTweets.sort((a, b) => b.engagement - a.engagement);
    
    // 保存
    const dir = '/Users/user/data';
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const file = path.join(dir, `x_top_raw_${ts}.json`);
    fs.writeFileSync(file, JSON.stringify(allTweets, null, 2));
    
    console.log(`\n✅ 完成! ${allTweets.length} 條推文`);
    console.log(`💾 ${file}`);
    
    // 顯示 TOP 3
    console.log('\n🔥 TOP 3:');
    allTweets.slice(0, 3).forEach((t, i) => {
      console.log(`${i+1}. [${t.engagement}] ${t.author}: ${t.text.substring(0, 40)}...`);
    });
    
    console.log(`\nOUTPUT_FILE:${file}`);
    console.log(`TOTAL:${allTweets.length}`);
    
  } catch (err) {
    console.error('❌', err.message);
    process.exit(1);
  } finally {
    if (client) await client.close();
  }
}

main();
