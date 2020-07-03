import requests
from bs4 import BeautifulSoup
import json
''' 
這邊的難度在於發現從https://www.104.com.tw/job/695ve?jobsource=jolist_b_relevance中發現695ve是這篇的代碼，
接著去網頁「開發人員工具」-->Network-->Name裡面找到695ve，點進去看它的Headers，
General下的Request URL放入程式碼中的url，
Request Headers下的Referer就是我們的headers，但是要記得刪去某些不要的東西，詳情如下面程式碼。
這樣就看的到104裡面用javascript呈現的網頁內容了
'''

headers={'Referer':'https://www.104.com.tw/job/695ve'}
url='https://www.104.com.tw/job/ajax/content/695ve'

res = requests.get(url=url,headers=headers)
print(res)
print(type(res.text))
json_data=json.loads(res.text)
print(type(json_data))
for k in json_data['data']['condition'].items():
    print(k)
# 上面跟下面的執行結果一樣，差在items()回傳的是tuple，zip()是裡面是什麼就回傳什麼回來，可能是dict or list...
for k,v in zip(json_data['data']['condition'],json_data['data']['condition'].values()):
    # print(type(k),type(v))
    print(k,v)