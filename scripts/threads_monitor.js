const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const KEYWORDS = ['OpenClaw', '龍蝦', 'openclaw', '#OpenClaw', '#龍蝦'];
const OUT_DIR = '/Users/user/data/threads_monitor';

function numFromToken(t) {
  if (!t) return null;
  const s = String(t).trim().replace(/,/g, '');
  if (/^\d+(\.\d+)?萬$/.test(s)) return Math.round(parseFloat(s) * 10000);
  if (/^\d+(\.\d+)?千$/.test(s)) return Math.round(parseFloat(s) * 1000);
  const n = Number(s.replace(/[^\d.]/g, ''));
  return Number.isFinite(n) ? Math.round(n) : null;
}

function extractComments(fullText, max = 5) {
  const out = [];
  const re = /\n([a-zA-Z0-9._]{2,30})\n(?:\d+天|\d+小時|\d+分|\d+分鐘|\d+週|\d+月|\d+年).*?\n([\s\S]*?)(?=\n[a-zA-Z0-9._]{2,30}\n(?:\d+天|\d+小時|\d+分|\d+分鐘|\d+週|\d+月|\d+年)|\n登入即可查看更多回覆。|$)/g;
  let m;
  while ((m = re.exec(fullText)) && out.length < max) {
    const username = m[1].trim();
    const content = m[2].split('\n').map(x => x.trim()).filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
    if (content && !/^翻譯$/.test(content)) out.push({ username, content });
  }
  return out;
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const ts = new Date();
  const runId = ts.toISOString().replace(/[:.]/g, '-');

  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox']
  });

  const page = await browser.newPage();
  const postMap = new Map();
  const keywordHits = {};

  for (const kw of KEYWORDS) {
    const url = `https://www.threads.net/search?q=${encodeURIComponent(kw)}`;
    await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(3000);
    const links = await page.$$eval('a[href*="/post/"]', as => Array.from(new Set(as.map(a => a.href))).slice(0, 12));
    const filtered = links.filter(u => !u.endsWith('/media'));
    keywordHits[kw] = filtered;
    for (const u of filtered) {
      if (!postMap.has(u)) postMap.set(u, { url: u, keywords: new Set([kw]) });
      else postMap.get(u).keywords.add(kw);
    }
  }

  const detailPage = await browser.newPage();
  const posts = [];
  for (const [url, meta] of postMap.entries()) {
    try {
      await detailPage.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
      await detailPage.waitForTimeout(2500);
      const title = await detailPage.title();
      const bodyText = await detailPage.locator('body').innerText();
      const lines = bodyText.split('\n').map(x => x.trim()).filter(Boolean);

      let postText = null;
      const ogDesc = await detailPage.getAttribute('meta[property="og:description"]', 'content');
      if (ogDesc) postText = ogDesc.trim();

      const viewMatch = bodyText.match(/([\d.,萬千]+)\s*次瀏覽/);
      const views = viewMatch ? numFromToken(viewMatch[1]) : null;

      let commentsCount = null;
      let likesCount = null;
      const idx = lines.indexOf('翻譯');
      if (idx >= 0) {
        const nums = [];
        for (let i = idx + 1; i < Math.min(lines.length, idx + 10); i++) {
          if (/^[\d.,萬千]+$/.test(lines[i])) nums.push(lines[i]);
          if (nums.length >= 4) break;
        }
        if (nums.length >= 1) commentsCount = numFromToken(nums[0]);
        if (nums.length >= 4) likesCount = numFromToken(nums[3]);
      }

      const m = url.match(/threads\.com\/@([^/]+)\/post\/([^/?#]+)/);
      const author = m ? m[1] : null;
      const postId = m ? m[2] : null;

      const comments = extractComments('\n' + bodyText, 5);

      posts.push({
        postId,
        url,
        author,
        title,
        text: postText,
        views,
        commentsCount,
        likesCount,
        keywords: Array.from(meta.keywords),
        topComments: comments
      });
    } catch (e) {
      posts.push({ url, keywords: Array.from(meta.keywords), error: String(e) });
    }
  }

  await browser.close();

  const okPosts = posts.filter(p => !p.error);
  okPosts.sort((a, b) => (b.likesCount || 0) - (a.likesCount || 0));

  const payload = {
    runAt: ts.toISOString(),
    timezone: 'Asia/Taipei',
    keywords: KEYWORDS,
    keywordHits,
    totals: {
      uniquePosts: okPosts.length,
      totalLikes: okPosts.reduce((s, p) => s + (p.likesCount || 0), 0),
      totalComments: okPosts.reduce((s, p) => s + (p.commentsCount || 0), 0),
      withViews: okPosts.filter(p => p.views != null).length
    },
    posts: okPosts,
    errors: posts.filter(p => p.error)
  };

  const jsonPath = path.join(OUT_DIR, `threads_openclaw_monitor_${runId}.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(payload, null, 2));
  console.log(jsonPath);
})();