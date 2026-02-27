import json
import re
from bs4 import BeautifulSoup

# Get page HTML
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Find all articles/posts
articles = soup.find_all('article') or soup.find_all('div', {'data-pressable-container': 'true'})

posts = []
for article in articles[:20]:  # Limit to first 20
    post = {
        'text': '',
        'author': '',
        'likes': 0,
        'reposts': 0,
        'replies': 0,
        'url': ''
    }
    
    # Extract text
    text_elem = article.find('span', {'dir': 'auto'})
    if text_elem:
        post['text'] = text_elem.get_text(strip=True)
    
    # Extract author
    author_elem = article.find('a', href=lambda x: x and '/@' in x)
    if author_elem:
        post['author'] = author_elem.get_text(strip=True)
    
    # Extract engagement numbers from text content
    text_content = article.get_text()
    
    # Likes
    like_match = re.search(r'(\d+(?:,\d+)*)\s*(?:likes?|讚)', text_content, re.IGNORECASE)
    if like_match:
        post['likes'] = int(like_match.group(1).replace(',', ''))
    
    # Reposts
    repost_match = re.search(r'(\d+(?:,\d+)*)\s*(?:reposts?|轉貼|轉發)', text_content, re.IGNORECASE)
    if repost_match:
        post['reposts'] = int(repost_match.group(1).replace(',', ''))
    
    # Replies
    reply_match = re.search(r'(\d+(?:,\d+)*)\s*(?:replies?|留言|回覆)', text_content, re.IGNORECASE)
    if reply_match:
        post['replies'] = int(reply_match.group(1).replace(',', ''))
    
    # Extract URL
    link_elem = article.find('a', href=lambda x: x and '/post/' in x)
    if link_elem:
        href = link_elem.get('href', '')
        if href.startswith('/'):
            post['url'] = 'https://www.threads.net' + href.split('?')[0]
        else:
            post['url'] = href.split('?')[0]
    
    if post['text'] and len(post['text']) > 10:
        posts.append(post)

# Filter for TSMC-related posts
tsmc_keywords = ['台積電', 'TSMC', 'tsmc', '台積', '晶圓', '半導體', '2330']
tsmc_posts = [p for p in posts if any(kw in p['text'] for kw in tsmc_keywords)]

# Filter by engagement (500+ likes, 100+ reposts)
hot_posts = [p for p in tsmc_posts if p['likes'] >= 500 and p['reposts'] >= 100]

print(json.dumps(hot_posts, ensure_ascii=False, indent=2))
print(f"\nTotal posts found: {len(posts)}")
print(f"TSMC-related posts: {len(tsmc_posts)}")
print(f"Hot posts (500+ likes, 100+ reposts): {len(hot_posts)}")
