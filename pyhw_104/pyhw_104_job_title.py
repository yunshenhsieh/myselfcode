import requests
from bs4 import BeautifulSoup

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers = {'User-Agent':useragent}
url = 'https://www.104.com.tw/jobs/search/?keyword=python&order=1&jobsource=2018indexpoc&ro=0'

res = requests.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')
title_list = soup.select('article[class]')
for i in range(len(title_list)):
    try:
        title=title_list[i].select('a')
        print(title[0].text)
        print(title_list[i].select('a')[0]['href'])
    except:
        print('==========')
        print(title)
        print('==========')