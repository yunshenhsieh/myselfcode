import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
# 下載「https://www.nhi.gov.tw/QueryN/Query1.aspx」查詢結果的excel，轉存成SQLite資料庫。
with open(r'C:\Users\user\Downloads\a.html','r',encoding='utf-8')as f:
    html_a = f.read()

with open(r'C:\Users\user\Downloads\b.html','r',encoding='utf-8')as f:
    html_b = f.read()

with open(r'C:\Users\user\Downloads\n.html','r',encoding='utf-8')as f:
    html_n = f.read()

def convert_drug_html_to_pandas(string_data):
    soup = BeautifulSoup(string_data,'html.parser')
    soup = soup.select('tr')

    soup_th = soup[0].select('th')
    tmp_th = []
    for i in soup_th:
        i = str(i).replace('"',"*").replace('|','$').replace('<hr/>','|')
        i = BeautifulSoup(i,'html.parser')
        tmp_th.append(i.text.strip())

    tmp_td = []
    for soup_td in soup[1:]:
        tmp_content = []
        for i in soup_td.select('td'):
            i = str(i).replace('"',"*").replace('|','$').replace('<hr/>','|')
            i = BeautifulSoup(i,'html.parser')
            tmp_content.append(i.text.strip().lower())
        tmp_td.append(tmp_content)

    df = pd.DataFrame(data=tmp_td,columns=tmp_th)
    return df

df_a = convert_drug_html_to_pandas(html_a)
df_b = convert_drug_html_to_pandas(html_b)
df_n = convert_drug_html_to_pandas(html_n)


df = df_a.append(df_b)
# print(df)
df = df_a.append(df_b).append(df_n)
# print(df)
df = df.drop_duplicates('藥品代碼')
# print(df)

conn = sqlite3.connect('nhi_drug_data.db')
df.to_sql('nhi_drug_data',conn,index=0)