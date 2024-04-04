# Version 3.0.0
import datetime
import os
import extract
import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Cm
import win32api, win32print
import tkinter as tk

def loadUseageWay(filePath: str) -> dict:
    useageWayDict = {}
    with open(filePath, "r", encoding="utf-8")as f:
        for data in f.readlines():
            data = data.split("=")
            useageWayDict[data[0].strip()] = data[1].strip()
    return useageWayDict

def loadPrint(filePath: str, printerName: str, receiveNumber: str, ptName: str):
    filePath = os.getcwd() + filePath
    win32api.ShellExecute(
        0,
        "print",
        filePath,
        "/d:{}".format(win32print.OpenPrinter(printerName)),
        ".",
        0
    )
    print("領藥號：{}，病人：{}，列印完成。".format(receiveNumber, ptName))
    pass

def msWordFormat(pageWd: float, pageHt: float, marginL: float, marginR: float, marginT: float, marginB: float) -> docx.Document():
    msDoc = docx.Document()
    section = msDoc.sections[0]
    section.page_width = Cm(pageWd)

    section.page_height = Cm(pageHt)

    section.left_margin = Cm(marginL)

    section.right_margin = Cm(marginR)

    section.top_margin = Cm(marginT)

    section.bottom_margin = Cm(marginB)

    return msDoc

def drugBagMaker(contentList: list[str], useageWayDict: dict, frequencyDict: dict, beforeOrAfterDict: dict, envSettingDict: dict):
    msDoc = msWordFormat(float(envSettingDict["pageWd"]), float(envSettingDict["pageHt"]),
                         float(envSettingDict["marginL"]), float(envSettingDict["marginR"]),
                         float(envSettingDict["marginT"]), float(envSettingDict["marginB"]))
    pharmacistName = envSettingDict["調劑藥師"]

    receiveNumber: str = extract.extractReceiveNumber(contentList)
    ptName: str = extract.extractPtName(contentList)
    ptBirthDay: str = extract.extractBirthDay(contentList)
    dipensingDay: datetime.strftime = datetime.datetime.now().strftime("%Y/%m/%d")
    ptChartNumber: str = extract.extractChartNumber(contentList)
    department = extract.extractDepartment(contentList)
    doctorName = extract.extractDoctorName(contentList)

    drugNameList, usageList, brandNameAndNoticeList = extract.extractMedisonInfo(contentList)

    paragraph_format = msDoc.styles['Normal'].paragraph_format
    paragraph_format.space_after = 1

    drugCount = len(drugNameList)

    for index in range(drugCount):
        headerTable = msDoc.add_table(rows=4, cols=4)
        msDoc.add_paragraph()
        headerTable.alignment = WD_TABLE_ALIGNMENT.RIGHT
        contentTable = msDoc.add_table(rows=5, cols=3)
        contentTable.cell(0, 1).width = Cm(8)


        headerTable.rows[0].cells[3].text = receiveNumber + " 林口"
        headerTable.rows[0].cells[3].paragraphs[0].runs[0].font.bold = True
        headerTable.rows[1].cells[0].text = ptName
        headerTable.rows[1].cells[2].text = ptBirthDay
        headerTable.rows[2].cells[0].text = ptChartNumber
        headerTable.rows[2].cells[3].text = dipensingDay
        headerTable.rows[3].cells[0].text = department
        headerTable.rows[3].cells[1].text = doctorName
        headerTable.rows[3].cells[3].text = pharmacistName

        headerTable.rows[0].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[1].cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        headerTable.rows[2].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[2].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        headerTable.rows[3].cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[3].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT


        contentTable.rows[0].cells[0].text = chr(12304) + "藥名" + chr(12305)
        contentTable.rows[0].cells[1].text = drugNameList[index]
        contentTable.rows[0].cells[2].text = "{} PC".format(usageList[index][-2].replace("PC", ""))
        contentTable.rows[1].cells[0].text = chr(12304) + "商品名" + chr(12305)
        contentTable.rows[1].cells[1].text = brandNameAndNoticeList[index][0]
        contentTable.rows[2].cells[0].text = chr(12304) + "使用方法" + chr(12305)
        contentTable.rows[2].cells[1].text = "{}".format(useageWayDict.get(usageList[index][2], "None"))
        contentTable.rows[2].cells[2].text = "{} - {}".format(index + 1, drugCount)
        contentTable.rows[3].cells[1].text = "每次{}，{}，{}".format(
                                    usageList[index][0],
                                    frequencyDict.get(usageList[index][1], "None"),
                                    beforeOrAfterDict.get(usageList[index][3], ""))
        contentTable.rows[4].cells[0].text = chr(12304) + "備註" + chr(12305)
        contentTable.rows[4].cells[1].text = brandNameAndNoticeList[index][1]

        for row in contentTable.rows:
            row.cells[-1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        if index != drugCount - 1:
            msDoc.add_page_break()

    msDoc.save("./history/{}_{}.docx".format(receiveNumber, dipensingDay.replace("/", "")))
    print("領藥號：{}，病人：{}，已完成。".format(receiveNumber, ptName))

    return [receiveNumber, dipensingDay, ptName]

def envSet(filePath: str) -> dict:
    with open(filePath, "r", encoding="utf-8")as f:
        envSettingDict = {}
        for setting in f.readlines():
            setting = setting.split("=")
            envSettingDict[setting[0].strip()] = setting[1].strip()

    return envSettingDict

def tkinterSet():
    root = tk.Tk()
    root.title('離線藥袋列印')
    root.geometry('600x700')

    text = tk.Text(root)  # 放入多行輸入框
    text.pack()
    resultInfoTxt_1 = tk.StringVar()
    resultInfoTxt_2 = tk.StringVar()
    resultInfoLabel_1 = tk.Label(root, textvariable=resultInfoTxt_1, font=('Arial', 20))
    resultInfoLabel_2 = tk.Label(root, textvariable=resultInfoTxt_2, font=('Arial', 20))
    resultInfoLabel_1.pack()
    resultInfoLabel_2.pack()

    def save():
        contentList = text.get(1.0, 'end-1c').split("\n")
        # 使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )
        info = drugBagMaker(contentList, useageWayDict, frequencyDict, beforeOrAfterDict, envSettingDict)
        resultInfoTxt_1.set("領藥號：{}，病人：{}".format(info[0], info[2]))
        resultInfoTxt_2.set("已存檔至history資料夾")
        clear()
        pass

    def saveAndPrint():
        contentList = text.get(1.0, 'end-1c').split("\n")
        # 使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )
        info = drugBagMaker(contentList, useageWayDict, frequencyDict, beforeOrAfterDict, envSettingDict)
        printerName = envSettingDict["印表機名稱"]

        loadPrint("/history/{}_{}.docx".format(info[0], info[1].replace("/", "")), printerName,
                  receiveNumber=info[0], ptName=info[2])
        resultInfoTxt_1.set("領藥號：{}，病人：{}".format(info[0], info[2]))
        resultInfoTxt_2.set("已存檔至history資料夾並列印")
        clear()
        pass

    def clear():
        text.delete(1.0, 'end')
        # 執行 clear 函式時，清空內容
        pass

    btnSaveAndPrint = tk.Button(root, text='列印並存成word', font=('Arial', 30, 'bold'), command=saveAndPrint)  # 放入顯示按鈕
    btnSaveAndPrint.pack()

    btnSave = tk.Button(root, text='存成word', font=('Arial', 30, 'bold'), command=save)  # 放入清空按鈕
    btnSave.pack()

    btnClear = tk.Button(root, text='clear', font=('Arial', 30, 'bold'), command=clear)  # 放入清空按鈕
    btnClear.pack()

    verInfo = tk.Label(root, text='Ver：3.0.0\n作者：謝昀燊Vincent')
    verInfo.pack()

    root.mainloop()
    pass

if __name__ == "__main__":
    useageWayDict = loadUseageWay("./使用方式.txt")
    frequencyDict = loadUseageWay("./頻次.txt")
    envSettingDict = envSet("./env")
    beforeOrAfterDict = {"PC": "飯後", "AC": "飯前"}
    print("作者：謝昀燊Vincent")
    print("Version：3.0.0")
    tkinterSet()
    pass
