import requests
from pyquery import PyQuery as pq
url='https://www.zhihu.com/explore'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
	}
html=requests.get(url,headers=headers).text
doc=pq(html)
items=doc('.explore-tab .explore-feed.feed-item').items()
file=open('explore.txt','w',encoding='utf-8')
for item in items:
	question=item.find('h2').text()
	author=item.find('.author-link-line').text()
	answer=pq(item.find('.content').html()).text()
	file.write('\n\n'.join([question,author,answer]))
	file.write('\n'+"="*50+'\n')
file.close()
