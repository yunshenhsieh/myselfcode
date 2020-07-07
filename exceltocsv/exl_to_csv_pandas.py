import pandas as pd
data=pd.read_excel('C:\\Users\\user\\Desktop\\test.xls')
b=data.to_csv(encoding='utf-8',index=0)
b=b.split('\r\n')
b='\n'.join(b[1:])
with open('./test.csv','w',encoding='utf-8')as f:
    f.write(b)