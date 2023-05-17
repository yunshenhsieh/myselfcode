import json, openpyxl, os
def fileLoad(filePath: str) -> dict:
    with open(filePath, "r", encoding="utf-8")as f:
        tmp = f.read()
        rawDataDict = json.loads(tmp)

    return rawDataDict

def dataClean(fileLoad: dict) -> list:
    # 把資料轉成，[{"name": 名字}, {"data": {<attribute>: <值>}}]
    attrDict = {}
    rawDataDict = fileLoad
    for attr in rawDataDict["attributes"]:
        attrDict[attr["trait_type"]] = attr["value"]

    singalDataList = [{"name": rawDataDict["name"]}, {"data": attrDict}]
    return singalDataList

def setDefaultColumn(columnList: list, singalDataList: list):
    attrList = list(singalDataList[1]["data"].keys())
    for colVal in attrList:
        if colVal not in columnList:
            columnList.append(colVal)
    pass

def setColumnCustomer(filePath: str):
    with open(filePath, "r", encoding="utf-8") as f:
        tmp = f.readlines()
        columnList = [col.strip() for col in tmp]
    return columnList

def exportExcel(columnList: list, allDataList: list):
    wb = openpyxl.Workbook()
    sheetData = wb.create_sheet("data")
    sheetData.append(columnList)
    for singalData in allDataList:
        singalList = [singalData[0]["name"]]
        for attrKey in columnList[1:]:
            singalList.append(singalData[1]["data"].get(attrKey, ""))
        sheetData.append(singalList)

    wb.remove(wb["Sheet"])
    wb.save("result.xlsx")
    pass

def defaultMain(fileNameList: list):
    columnList = ["名字"]
    allDataList = []
    for n in range(len(fileNameList)):
        data = dataClean(fileLoad("./res/{}".format(fileNameList[n])))
        allDataList.append(data)
        setDefaultColumn(columnList, data)
    exportExcel(columnList, allDataList)
    pass

def customerMain(fileNameList: list):
    try:
        columnList = setColumnCustomer("./column_data/column.txt")
    except Exception:
        print("請確認column_data資料夾內，是否有column.txt的欄位檔。")

    allDataList = []
    for n in range(len(fileNameList)):
        data = dataClean(fileLoad("./res/{}".format(fileNameList[n])))
        allDataList.append(data)

    exportExcel(columnList, allDataList)
    pass

if __name__ == "__main__":
    try:
        fileNameList = os.listdir("./res")
        fileNameList.sort(key=lambda x: int(x.split(".")[0]))
    except Exception:
        print("請確認res資料夾內，是否有需要轉檔的檔案，以及檔名是否正確。")

    print("Version 1.0.1")
    print("不需要自訂欄位及順序，請輸入0。")
    print("自訂欄位及順序，請按enter直接執行。")
    exeCode = input("請輸入：").strip()

    if exeCode == "0":
        defaultMain(fileNameList)
        print("不自訂欄位及順序，轉檔已完成。")
    else:
        customerMain(fileNameList)
        print("自訂欄位及順序，轉檔已完成。")

    input("請按enter鍵，結束程式。")
