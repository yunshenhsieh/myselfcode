# Version 0.0.1
def extractDate(contentList: list[str]) -> str:
    visitDate = contentList[1][5:13]
    return visitDate

def extractReceiveNumber(contentList: list[str]) -> str:
    receiveNumber = contentList[3].split("：")[-1][:5]
    return receiveNumber

def extractChartNumber(contentList: list[str]) -> str:
    chartNumber = "".join([n for n in contentList[4][:9] if ord(n) != 32])
    return chartNumber

def extractPtName(contentList: list[str]) -> str:
    ptName = "".join([n for n in contentList[5][:9] if ord(n) != 32])
    return ptName

def extractBirthDay(contentList: list[str]) -> str:
    birthDay = "".join([date for date in contentList[5].split("年月日:")[-1][:11] if ord(date) != 32])
    return birthDay

def checkBeginAndEnd(contentList: list[str]) -> int:
    numBegin , numEnd= 0, 0
    for listNum ,content in enumerate(contentList):
        if ("藥品" and "劑量" and "首日") in content:
            numBegin = listNum
        elif "Total Item" in content:
            numEnd = listNum
    return numBegin, numEnd

def extractMedisonInfo(contentList: list[str]) -> str:
    numBegin , numEnd= checkBeginAndEnd(contentList)
    drugNameList ,usageList = [], []
    for content in contentList[numBegin:numEnd]:
        if " ." in content:
            drugName = content.split("---")[0]
            drugNameList.append(drugName)
        if "---" in content:
            usageInfo = content.split("-")[-1]
            usageList.append(usageInfo)
    return drugNameList, usageList
