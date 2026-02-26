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
          const url = window.location.href;
          const title = document.title;
          const articles = document.querySelectorAll('article');
          const times = document.querySelectorAll('time');
          const loginBtn = document.querySelector('[data-testid="loginButton"]');
          
          return {
            url,
            title,
            articleCount: articles.length,
            timeCount: times.length,
            hasLoginButton: !!loginBtn,
            firstArticleHTML: articles[0] ? articles[0].outerHTML.substring(0, 800) : null
          };
        })()
      `,
      returnByValue: true
    });
    
    console.log('頁面狀態:', JSON.stringify(result.result.value, null, 2));
    
  } catch (err) {
    console.error('錯誤:', err);
  } finally {
    if (client) await client.close();
  }
}

main();
