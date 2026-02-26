const CDP = require('chrome-remote-interface');

async function main() {
  let client;
  try {
    client = await CDP({ host: '127.0.0.1', port: 19222 });
    const { Page, Runtime } = client;
    
    await Page.enable();
    await Runtime.enable();
    
    console.log('🌐 導航到 X.com...');
    await Page.navigate({ url: 'https://x.com/home' });
    await Page.loadEventFired();
    await new Promise(r => setTimeout(r, 10000));
    
    const result = await Runtime.evaluate({
      expression: `
        (function() {
          const articles = document.querySelectorAll('article');
          const tweets = [];
          
          articles.forEach((article, i) => {
            try {
              const timeEl = article.querySelector('time');
              if (!timeEl) return;
              
              // 找 tweet ID - 從時間元素找父連結
              let linkEl = timeEl.closest('a');
              let href = linkEl ? linkEl.getAttribute('href') : '';
              
              // 如果沒找到，嘗試其他方式
              if (!href) {
                const allLinks = article.querySelectorAll('a[href*="/status/"]');
                for (const a of allLinks) {
                  const h = a.getAttribute('href');
                  if (h && h.includes('/status/')) {
                    href = h;
                    break;
                  }
                }
              }
              
              // 找正文
              const textEl = article.querySelector('[data-testid="tweetText"]');
              const text = textEl ? textEl.innerText : '';
              
              // 找作者
              const allLinks2 = article.querySelectorAll('a[role="link"]');
              let authorHandle = '';
              for (const a of allLinks2) {
                const h = a.getAttribute('href');
                if (h && h.startsWith('/') && !h.includes('/status/') && h.length > 1) {
                  authorHandle = h.split('/')[1];
                  break;
                }
              }
              
              tweets.push({
                index: i,
                href,
                text: text.substring(0, 100),
                authorHandle,
                timeText: timeEl.textContent
              });
            } catch (e) {}
          });
          
          return tweets;
        })()
      `,
      returnByValue: true
    });
    
    console.log('提取結果:', JSON.stringify(result.result.value, null, 2));
    
  } catch (err) {
    console.error('錯誤:', err);
  } finally {
    if (client) await client.close();
  }
}

main();
