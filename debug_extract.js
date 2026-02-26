const CDP = require('chrome-remote-interface');

async function debug() {
  const client = await CDP({ host: '127.0.0.1', port: 19222 });
  const { Runtime } = client;
  await Runtime.enable();
  
  // 直接測試提取函數
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const articles = document.querySelectorAll('article');
        const extracted = [];
        
        articles.forEach((article, idx) => {
          try {
            const timeEl = article.querySelector('time');
            if (!timeEl) {
              extracted.push({ idx, error: 'no time element' });
              return;
            }
            
            let linkEl = timeEl.closest('a');
            if (!linkEl) {
              linkEl = article.querySelector('a[href*="/status/"]');
            }
            if (!linkEl) {
              extracted.push({ idx, error: 'no link element' });
              return;
            }
            
            const href = linkEl.getAttribute('href');
            const match = href.match(/status\\/(\\d+)/);
            if (!match) {
              extracted.push({ idx, error: 'no tweet id match', href });
              return;
            }
            
            extracted.push({ idx, success: true, tweetId: match[1], href });
          } catch (e) {
            extracted.push({ idx, error: e.message });
          }
        });
        
        return extracted;
      })()
    `,
    returnByValue: true
  });
  
  console.log('提取結果:', JSON.stringify(result.result.value, null, 2));
  
  await client.close();
}

debug().catch(console.error);
