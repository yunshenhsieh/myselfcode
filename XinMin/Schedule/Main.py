import tkinter as tk
def loadStaffSchedule(staffSet: set, staffScheduleFileName: str) -> dict:
    staffScheduleDict = {staffName: [] for staffName in staffSet}

    with open(staffScheduleFileName, 'r', encoding='utf-8') as f:
        staffSchedule = f.readlines()

    for data in staffSchedule:
        data = data.split(',')
        staffScheduleDict[data[1]].append((data[0].strip(), data[-2].strip(), data[-1].strip()))
    return staffScheduleDict

def loadLabSchedule(labSet: set, labScheduleFileName: str) -> dict:
    labScheduleDict = {labName: [] for labName in labSet}

    with open(labScheduleFileName, 'r', encoding='utf-8') as f:
        labSchedule = f.readlines()

    for data in labSchedule:
        data = data.split(',')
        labScheduleDict[data[1]].append((data[0].strip(), data[-2].strip(), data[-1].strip()))
    return labScheduleDict

def loadStaffList(staffListFileName: str) -> set:
    staffSet = set()
    with open(staffListFileName, 'r', encoding='utf-8') as f:
        for line in f:
            staffSet.add(line.strip())
    return staffSet

def loadLabList(labListFileName: str) -> set:
    labSet = set()
    with open(labListFileName, 'r', encoding='utf-8') as f:
        for line in f:
            labSet.add(line.strip())
    return labSet

def checkStaffOverlap(date: str, inputStaffName: str, inputStart: str, inputEnd: str, errorLabel: tk):
    staffScheduleDict = loadStaffSchedule(staffSet, 'staff_schedul.txt')
    compareDict = dict()
    for k, v in staffScheduleDict.items():
        for timeData in v:
            if date == timeData[0]:
                compareDict.setdefault(k, []).append(timeData)
    for _, satffScheduleStart, staffScheduleEnd in compareDict.get(inputStaffName, []):
        if inputStart < staffScheduleEnd and inputEnd > satffScheduleStart:
            print('{}：{}/{}-{}跟現有{}-{}重疊'.format(inputStaffName, date, inputStart, inputEnd, satffScheduleStart, staffScheduleEnd))
            errorLabel.config(text='{}\n{}\n{}-{}\n跟現有{}-{}重疊'.format(inputStaffName, date, inputStart, inputEnd, satffScheduleStart, staffScheduleEnd))
            return False

    return True


def checkLabOverlap(date: str, inputLabName: str, inputStart: str, inputEnd: str, errorLabel: tk):
    labScheduleDict = loadLabSchedule(labSet, 'lab_schedul.txt')
    compareDict = dict()
    for k, v in labScheduleDict.items():
        for timeData in v:
            if date == timeData[0]:
                compareDict.setdefault(k, []).append(timeData)
    for _, labScheduleStart, labScheduleEnd in compareDict.get(inputLabName, []):
        if inputStart < labScheduleEnd and inputEnd > labScheduleStart:
            print('{}：{}//{}-{}跟現有{}-{}重疊'.format(inputLabName, date, inputStart, inputEnd, labScheduleStart, labScheduleEnd))
            errorLabel.config(text='{}\n{}\n{}-{}\n跟現有{}-{}重疊'.format(inputLabName, date, inputStart, inputEnd, labScheduleStart, labScheduleEnd))
            return False

    return True


def mainGUI(staffSet: set, labSet: set):
    root = tk.Tk()
    root.title('排程系統')
    root.geometry('600x700')

    tk.Label(root, text='請使用24小時制', font=('微軟正黑體', 16)).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(root, text='日期：8位數', font=('微軟正黑體', 16)).grid(row=1, column=0, padx=5, pady=5)
    dateInput = tk.Entry(root, font=('微軟正黑體', 16))
    dateInput.grid(row=1, column=1)

    tk.Label(root, text='開始時間：4位數', font=('微軟正黑體', 16)).grid(row=2, column=0, padx=5, pady=5)
    startTimeInput = tk.Entry(root, font=('微軟正黑體', 16))
    startTimeInput.grid(row=2, column=1)

    tk.Label(root, text='結束時間：4位數', font=('微軟正黑體', 16)).grid(row=3, column=0, padx=5, pady=5)
    endTimeInput = tk.Entry(root, font=('微軟正黑體', 16))
    endTimeInput.grid(row=3, column=1)

    tk.Label(root, text='批號', font=('微軟正黑體', 16)).grid(row=4, column=0, padx=5, pady=5)
    batchNumberInput = tk.Entry(root, font=('微軟正黑體', 16))
    batchNumberInput.grid(row=4, column=1)

    # 員工下拉選單
    tk.Label(root, text='人員：', font=('微軟正黑體', 16)).grid(row=5, column=0, padx=5, pady=5)
    staffOptions = sorted(list(staffSet))
    staffSelected = tk.StringVar(value=staffOptions[0])
    staffMenu = tk.OptionMenu(root, staffSelected, *staffOptions)
    staffMenu.config(font=('微軟正黑體', 16))
    staffMenu['menu'].config(font=('微軟正黑體', 16))
    staffMenu.grid(row=5, column=1)

    # 地點下拉選單
    tk.Label(root, text='地點：', font=('微軟正黑體', 16)).grid(row=6, column=0, padx=5, pady=5)
    labOptions = sorted(list(labSet))
    labSelected = tk.StringVar(value=labOptions[0])
    labMenu = tk.OptionMenu(root, labSelected, *labOptions)
    labMenu.config(font=('微軟正黑體', 16))
    labMenu['menu'].config(font=('微軟正黑體', 16))
    labMenu.grid(row=6, column=1)

    errorLabel = tk.Label(
        root,
        text='',
        font=('微軟正黑體', 16),
        fg='red'
    )
    errorLabel.grid(row=7, column=1, padx=5, pady=5)

    def checkVal(date, startTime, endTime):
        if len(date) != 8 or len(startTime) != 4 or len(endTime) != 4:
            return False
        else:
            return date, startTime, endTime

    def click():
        date, startTime, endTime, batchNumber = dateInput.get(), startTimeInput.get(), endTimeInput.get(), batchNumberInput.get()
        if checkVal(date, startTime, endTime):
            staff = staffSelected.get()
            lab = labSelected.get()

            if checkStaffOverlap(date, staff, startTime, endTime, errorLabel) and checkLabOverlap(date, lab, startTime, endTime, errorLabel):
                with open('staff_schedul.txt', 'a', encoding='utf-8')as w:
                    w.write('{},{},{},{},{}\n'.format(date, staff, batchNumber, startTime, endTime))
                with open('lab_schedul.txt', 'a', encoding='utf-8')as w:
                    w.write('{},{},{},{},{}\n'.format(date, lab, batchNumber, startTime, endTime))
                with open('total_schedul.txt', 'a', encoding='utf-8')as w:
                    w.write('{},{},{},{},{},{}\n'.format(date, lab, staff, batchNumber, startTime, endTime))
                clean()
        else:
            errorLabel.config(text='格式輸入錯誤')
        return

    def clean():
        errorLabel.config(text='')
        dateInput.delete(0, tk.END)
        startTimeInput.delete(0, tk.END)
        endTimeInput.delete(0, tk.END)
        batchNumberInput.delete(0, tk.END)
        dateInput.focus_set()
        return

    def allReSet():
        errorLabel.config(text='')
        dateInput.delete(0, tk.END)
        startTimeInput.delete(0, tk.END)
        endTimeInput.delete(0, tk.END)
        batchNumberInput.delete(0, tk.END)
        staffSelected.set(staffOptions[0])
        labSelected.set(labOptions[0])
        dateInput.focus_set()
        return

    button = tk.Button(root, text='送出', font=('微軟正黑體', 16), command=click)
    button.grid(row=8, column=1, padx=5, pady=30)
    button = tk.Button(root, text='清除', font=('微軟正黑體', 16), command=clean)
    button.grid(row=8, column=2, padx=5, pady=30)
    button = tk.Button(root, text='全輸入框回復', font=('微軟正黑體', 16), command=allReSet)
    button.grid(row=9, column=1, padx=5, pady=30)

    tk.Label(root, text='Version 1.0.1', font=('微軟正黑體', 16)).grid(row=10, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    # Version 1.0.1
    staffSet = loadStaffList('staff.txt')
    labSet = loadLabList('lab.txt')

    mainGUI(staffSet, labSet)
    pass
