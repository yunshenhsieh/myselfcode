import tkinter as tk
import xlrd
def click_enter():
    try:
        myWorkbook = xlrd.open_workbook(file_locate.get())
        mysheets = myWorkbook.sheets()
        i= 0;col=[]
        for sheet in mysheets:
            for row in sheet.get_rows():
                col.append(row)
        with open(path_locate.get().strip() + '\cust_insert.csv','w',encoding='utf-8')as csvWrite:
            for row in col[1:]:
                n = 0
                for cell in row:
                    if type(cell.value) == float:
                        tmp = int(cell.value)
                        row[n] = str(tmp)
                        n += 1
                    else:
                        row[n] = cell.value
                        n += 1
                csvWrite.write(','.join(row) + '\n')
            i += 1
        msg.set('轉檔結束!!')
    except Exception as e:
        msg.set('轉檔失敗\n檔案格式或路徑不正確，請重新輸入。')

win=tk.Tk()
file_locate=tk.StringVar()
path_locate=tk.StringVar()
msg=tk.StringVar()
win.geometry('450x200')
win.title('xls轉csv')
label1=tk.Label(win,text='請輸入檔案位置',font=(18))
label1.pack()
key_in=tk.Entry(win,font=(14),textvariable=file_locate,width=350)
key_in.pack()

path_label=tk.Label(win,text='請輸入存入檔案路徑',font=(18))
path_label.pack()
path_way=tk.Entry(win,font=(14),textvariable=path_locate,width=350)
path_way.pack()

button1=tk.Button(win,text="確定",font=(14),command=click_enter)
button1.pack()
label_finishe=tk.Label(win,textvariable=msg,font=(18))
label_finishe.pack()
win.mainloop()