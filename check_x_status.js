const CDP = require('chrome-remote-interface');

async function check() {
  const client = await CDP({ host: '127.0.0.1', port: 19222 });
  const { Page, Runtime } = client;
  await Page.enable();
  await Runtime.enable();
  
  // 獲取頁面標題和 URL
  const title = await Runtime.evaluate({
    expression: 'document.title',
    returnByValue: true
  });
  
  const url = await Runtime.evaluate({
    expression: 'window.location.href',
    returnByValue: true
  });
  
  // 檢查是否有登錄提示
  const loginCheck = await Runtime.evaluate({
    expression: `
      document.body.innerText.includes('登入') || 
      document.body.innerText.includes('Sign in') ||
      document.body.innerText.includes('Log in') ||
      document.querySelector('input[name="text"]') !== null
    `,
    returnByValue: true
  });
  
  // 檢查文章數量
  const articleCount = await Runtime.evaluate({
    expression: 'document.querySelectorAll("article").length',
    returnByValue: true
  });
  
  console.log('標題:', title.result.value);
  console.log('URL:', url.result.value);
  console.log('需要登錄:', loginCheck.result.value);
  console.log('文章數量:', articleCount.result.value);
  
  await client.close();
}

check().catch(console.error);
