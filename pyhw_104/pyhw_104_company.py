import requests
from bs4 import BeautifulSoup


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
url='https://www.104.com.tw/jobs/search/?keyword=python&order=1&jobsource=2018indexpoc&ro=0'

res = requests.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')
company_list=soup.select('a[title]')
# print(company_list)
for i in company_list:
    try:
        company=i
        print(company.text,file=open('./test4.txt','a',encoding='utf-8'))
    except:
        print('=========')
        print(company)
        print('=========')