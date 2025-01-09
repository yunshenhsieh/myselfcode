import tkinter as tk

def resetEntry():
    entry.delete(0, 'end')
    pass

def setCheckVal():
    global checkVal
    checkVal = entry.get().strip()
    checkValSet.set('正在比對的項目：{}'.format(checkVal))
    resetEntry()
    pass

def matchWindowSetting():
    global envSet
    root = tk.Tk()
    root.title('內容相符')
    root.geometry('{}x{}'.format(envSet['checkMatchWindowWidth'], envSet['checkMatchWindowHeight']))
    root.configure(bg=envSet['checkMatchWindowBackgroundColor'])
    label = tk.Label(root, text='比對內容相符',
                     font=(envSet['checkMatchWindowLabelFont'], int(envSet['checkMatchWindowLabelFontSize']), 'bold'),
                     fg=envSet['checkMatchWindowLabelFontColor'],
                     bg=envSet['checkMatchWindowLabelBackgroundColor'])
    label.pack()
    root.mainloop()
    pass

def checkMatch(event):
    global envSet
    tmp = entry.get().strip()
    if envSet['searchMod'] == "0":
        if (checkVal == tmp):
            resetEntry()
            matchWindowSetting()
        else:
            resetEntry()
    else:
        if (checkVal in tmp):
            resetEntry()
            matchWindowSetting()
        else:
            resetEntry()
    pass

if "__main__" == __name__:
    envSet = {}
    with open('./check_val.env', 'r', encoding="utf-8")as f:
        tmp = [x.strip().split('=') for x in f.readlines() if x.strip() != ""]
        envSet = {status[0] : status[1] for status in tmp}
    checkVal = ""
    root = tk.Tk()
    root.title('檢查用程式')
    root.geometry('{}x{}'.format(envSet['width'], envSet['height']))

    checkValSet = tk.StringVar()  # 建立文字變數
    checkValSet.set('正在比對的項目：')

    label = tk.Label(root, textvariable=checkValSet, font=(envSet['font'], int(envSet['labelFontSize']), 'bold'))
    label.pack()

    entry = tk.Entry(root, font=(envSet['font'], int(envSet['inputFontSize'])))  # 放入單行輸入框
    entry.pack()

    btn = tk.Button(root, text='submit', font=(envSet['submitFont'], int(envSet['submitFontSize'])), command=setCheckVal)  # 執行鈕
    btn.pack()

    label = tk.Label(root, text="Version：1.0.2\n作者：謝昀燊 Vincent Xie", font=(envSet['font'], 10, 'bold'))
    label.pack()

    entry.bind('<Return>', checkMatch)
    root.mainloop()
