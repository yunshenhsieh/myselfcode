import tkinter as tk
import xlrd,csv
def click_enter():
    try:
        save_locate='\\'.join(file_locate.get().strip().split('\\')[:-1]) + '\\'
        myWorkbook = xlrd.open_workbook(file_locate.get())
        mysheets = myWorkbook.sheets()
        i = 0
        for sheet in mysheets:
            with open(save_locate + myWorkbook.sheet_names()[i] + '.csv', 'w', newline='', encoding='utf-8')as csvWrite:
                writer = csv.writer(csvWrite)
                for nrow in range(sheet.nrows):
                    writer.writerow(sheet.row_values(nrow))
                i += 1
        msg.set('轉檔結束!!')
    except Exception as e:
        msg.set('轉檔失敗\n檔案格式或路徑不正確，請重新輸入。')

win=tk.Tk()
file_locate=tk.StringVar()
msg=tk.StringVar()
win.geometry('450x200')
win.title('xls轉csv')
label1=tk.Label(win,text='請輸入檔案位置',font=(18))
label1.pack()
key_in=tk.Entry(win,font=(14),textvariable=file_locate,width=350)
key_in.pack()
button1=tk.Button(win,text="確定",font=(14),command=click_enter)
button1.pack()
label_finishe=tk.Label(win,textvariable=msg,font=(18))
label_finishe.pack()
win.mainloop()