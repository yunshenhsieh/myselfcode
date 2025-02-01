import datetime
import os
import extract
import docx, qrcode
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Cm
import win32api, win32print
import tkinter as tk

def loadDrugProfile(filePath: str) -> dict:
    with open(filePath, 'r', encoding='big5-hkscs') as f:
        dataList = f.readlines()
    drugProfileDict = {}
    for data in dataList:
        data = data.split(';')
        if len(data) >= 120:
            drugProfileDict[data[0]] = data

    return drugProfileDict

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

def qrcodeMaker(qrcodeData: str, tmpStoragePath: str, qrSize: int = 25):
    qr = qrcode.QRCode(
        border=2,
    )
    qr.add_data(qrcodeData)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img = img.resize((qrSize, qrSize))
    img.save(tmpStoragePath + '{}.png'.format(qrcodeData))
    qrcodePath = tmpStoragePath + '{}.png'.format(qrcodeData)
    return qrcodePath

def drugBagMaker(contentList: list[str], useageWayDict: dict, frequencyDict: dict, beforeOrAfterDict: dict, envSettingDict: dict, drugProfileDict: dict):
    msDoc = msWordFormat(float(envSettingDict['pageWd']), float(envSettingDict['pageHt']),
                         float(envSettingDict['marginL']), float(envSettingDict['marginR']),
                         float(envSettingDict['marginT']), float(envSettingDict['marginB']))
    pharmacistName = envSettingDict['調劑藥師']

    contentForHeader: list = contentList[0].strip().split('\n')
    receiveNumber: str = extract.extractReceiveNumber(contentForHeader)
    ptName: str = extract.extractPtName(contentForHeader)
    ptBirthDay: str = extract.extractBirthDay(contentForHeader)
    dipensingDay: datetime.strftime = datetime.datetime.now().strftime('%Y/%m/%d')
    ptChartNumber: str = extract.extractChartNumber(contentForHeader)
    department = extract.extractDepartment(contentForHeader)
    doctorName = extract.extractDoctorName(contentForHeader)

    contentForDrugInfo: str = contentList[1]
    drugList = extract.extractMedisonInfo(contentForDrugInfo, drugProfileDict)

    paragraph_format = msDoc.styles['Normal'].paragraph_format
    paragraph_format.space_after = 1

    tmpStoragePath = './history/{}_{}/'.format(receiveNumber, dipensingDay.replace('/', ''))
    if not os.path.isdir(tmpStoragePath):
        os.makedirs(tmpStoragePath)


    drugCount = len(drugList)

    for index in range(drugCount):
        headerTable = msDoc.add_table(rows=5, cols=4)
        msDoc.add_paragraph()
        headerTable.alignment = WD_TABLE_ALIGNMENT.RIGHT
        contentTable = msDoc.add_table(rows=7, cols=3)
        contentTable.cell(0, 1).width = Cm(8)

        headerTable.rows[1].cells[3].text = receiveNumber + ' 林口'
        headerTable.rows[1].cells[3].paragraphs[0].runs[0].font.bold = True
        headerTable.rows[2].cells[0].text = ptName
        headerTable.rows[2].cells[2].text = ptBirthDay
        headerTable.rows[3].cells[0].text = ptChartNumber
        headerTable.rows[3].cells[3].text = dipensingDay
        headerTable.rows[4].cells[0].text = department
        headerTable.rows[4].cells[1].text = doctorName
        headerTable.rows[4].cells[3].text = pharmacistName

        headerTable.rows[1].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[2].cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        headerTable.rows[3].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[3].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        headerTable.rows[4].cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        headerTable.rows[4].cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        drugProfile = drugProfileDict.get(drugList[index][2], '無資料')

        drugCode = drugProfile[12]
        totalCnt = '000' + drugList[index][5]
        qrcodeData = drugCode + totalCnt[-3:] + '    ' + ptChartNumber
        qrCodePath = qrcodeMaker(qrcodeData, tmpStoragePath)

        headerTable.rows[0].cells[0].paragraphs[0].add_run().add_picture(qrCodePath)
        headerTable.rows[0].cells[0].add_paragraph()
        headerTable.rows[0].cells[0].paragraphs[1].text = '離線列印'
        headerTable.rows[0].cells[0].paragraphs[1].runs[0].font.bold = True


        contentTable.rows[0].cells[0].text = chr(12304) + '藥名' + chr(12305)
        contentTable.rows[0].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.DISTRIBUTE
        contentTable.rows[0].cells[1].text = '{}   {}'.format(drugProfile[12], drugProfile[1])
        contentTable.rows[0].cells[1].paragraphs[0].runs[0].font.bold = True
        contentTable.rows[0].cells[2].text = '{} PC'.format(drugList[index][5])

        contentTable.rows[1].cells[0].text = chr(12304) + '商品名' + chr(12305)
        contentTable.rows[1].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.DISTRIBUTE
        contentTable.rows[1].cells[1].text = drugProfile[2]

        contentTable.rows[2].cells[0].text = chr(12304) + '使用方法' + chr(12305)
        contentTable.rows[2].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.DISTRIBUTE
        contentTable.rows[2].cells[1].text = '{}'.format(useageWayDict.get(drugList[index][12], 'None'))
        contentTable.rows[2].cells[2].text = '{} - {}'.format(index + 1, drugCount)

        if 'H' in drugList[index][10]:
            contentTable.rows[3].cells[1].text = '{}，每次{}'.format(
                                        frequencyDict.get(drugList[index][10], "None"),
                                        drugList[index][8] + drugList[index][9])
        else:
            contentTable.rows[3].cells[1].text = '{}，{}，每次{}'.format(
                frequencyDict.get(drugList[index][10], 'None'),
                beforeOrAfterDict.get(drugList[index][11], ''),
                drugList[index][8] + drugList[index][9])


        contentTable.rows[3].cells[1].paragraphs[0].runs[0].font.bold = True
        contentTable.rows[4].cells[0].text = chr(12304) + '備註' + chr(12305)
        contentTable.rows[4].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.DISTRIBUTE
        contentTable.rows[4].cells[1].text = drugList[index][-1]

        serialNumberData = '{}     {}'.format(ptChartNumber, drugList[index][0])
        serialNumberQrCodePath = qrcodeMaker(serialNumberData, tmpStoragePath)

        contentTable.rows[6].cells[0].paragraphs[0].add_run().add_picture(serialNumberQrCodePath)
        contentTable.rows[6].cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        contentTable.rows[6].cells[0].add_paragraph()
        contentTable.rows[6].cells[0].paragraphs[1].text = serialNumberData
        contentTable.rows[6].cells[0].paragraphs[1].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        for row in contentTable.rows:
            row.cells[-1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        if index != drugCount - 1:
            msDoc.add_page_break()

    msDoc.save('./history/{}_{}/{}_{}.docx'.format(receiveNumber, dipensingDay.replace('/', ''), receiveNumber, dipensingDay.replace('/', '')))
    print('領藥號：{}，病人：{}，已完成。'.format(receiveNumber, ptName))

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
    root.title('急診離線藥袋列印')
    root.geometry('{}x{}'.format(envSettingDict["視窗寬度"], envSettingDict["視窗高度"]))

    text = tk.Text(root)  # 放入多行輸入框
    text.pack()
    resultInfoTxt_1 = tk.StringVar()
    resultInfoTxt_2 = tk.StringVar()
    resultInfoLabel_1 = tk.Label(root, textvariable=resultInfoTxt_1, font=('Arial', 20))
    resultInfoLabel_2 = tk.Label(root, textvariable=resultInfoTxt_2, font=('Arial', 20))
    resultInfoLabel_1.pack()
    resultInfoLabel_2.pack()

    def save():
        contentList = text.get(1.0, 'end-1c').split("===")
        # 使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )
        info = drugBagMaker(contentList, useageWayDict, frequencyDict, beforeOrAfterDict, envSettingDict, drugProfileDict)
        resultInfoTxt_1.set("領藥號：{}，病人：{}".format(info[0], info[2]))
        resultInfoTxt_2.set("已存檔至history資料夾")
        clear()
        pass

    def saveAndPrint():
        contentList = text.get(1.0, 'end-1c').split("===")
        # 使用 end-1c 表示取得倒數第二個字元 ( 因為最後一個字元是換行符 )
        info = drugBagMaker(contentList, useageWayDict, frequencyDict, beforeOrAfterDict, envSettingDict, drugProfileDict)
        printerName = envSettingDict["印表機名稱"]

        loadPrint('./history/{}_{}/{}_{}.docx'.format(info[0], info[1].replace("/", ""), info[0], info[1].replace("/", "")), printerName,
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

    verInfo = tk.Label(root, text='Ver：4.0.1\n作者：謝昀燊Vincent')
    verInfo.pack()

    root.mainloop()
    pass

if __name__ == "__main__":
    drugProfileDict = loadDrugProfile('./Adgn.txt')
    useageWayDict = loadUseageWay('./使用方式.txt')
    frequencyDict = loadUseageWay('./頻次.txt')
    envSettingDict = envSet('./env')
    beforeOrAfterDict = {'P': '飯後', 'A': '飯前'}
    print('版本：4.0.1')
    print('作者：謝昀燊Vincent')
    tkinterSet()
    pass
