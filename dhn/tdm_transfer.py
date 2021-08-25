import xlwt
from bs4 import BeautifulSoup
def clear_vital_sign_data():
    with open('D:\暫存\長庚臨床作業\data.txt','r',encoding='big5')as f:
        tmp = f.read()
    ans = []
    tmp = tmp.split('\n')
    region = len(tmp[0].split(' ')) - 2
    for i, c in enumerate(tmp):
        tmp_table = []
        if '生化組' not in c:
            c = c.split(' ')
            start_n = len(c) - region
            tmp_table.append(c[:start_n])
            tmp_table.append(c[start_n:-1])
            ans.append(tmp_table)
        else:
            tmp_table.append([c,'===='])
            ans.append(tmp_table)
    return ans

def wt_values(worksheet,row,val_list):
    for col_n, val in enumerate(val_list[1]):
        worksheet.write(row, col_n + 2, label=val)

def wt_header(worksheet,row,header):
    if len(header[0]) > 2:
        worksheet.write(row, 0, label=''.join(header[0][:-1]))
        worksheet.write(row, 1, label=header[0][-1])
    else:
        worksheet.write(row, 0, label=header[0][0])
        worksheet.write(row, 1, label=header[0][1])

def tdm_data_to_excel():
    """
            # 建立一個workbook 設定編碼
            workbook = xlwt.Workbook(encoding = 'utf-8')
            # 建立一個worksheet
            worksheet = workbook.add_sheet('result')

            # 寫入excel
            # 引數對應 row, col, 值
            worksheet.write(2,1, label = 'this is test')
            # 儲存
            workbook.save('vital_sign.xls')
            """
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('vital_sign')

    tmp = clear_vital_sign_data()
    for i in tmp:
        print(i)
    for row, content in enumerate(tmp[:-1]):
        if '生化組' in content[0][0]:
            wt_header(worksheet, row, content)
        else:
            wt_header(worksheet, row, content)
            wt_values(worksheet, row, content)
    workbook.save('vital_sign.xls')

    
if __name__ == "__main__":
    tdm_data_to_excel()

