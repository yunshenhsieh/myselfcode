# Version 1.0.0
def extractReceiveNumber(contentList: list[str]) -> str:
    receiveNumber = contentList[3].split("：")[-1][:5].strip()
    return receiveNumber

def extractChartNumber(contentList: list[str]) -> str:
    chartNumber = "".join([n for n in contentList[4][:9] if ord(n) != 32]).strip()
    return chartNumber

def extractPtName(contentList: list[str]) -> str:
    ptName = contentList[5][:20].strip()
    if "出" in ptName:
        ptName = ptName[:ptName.index("出")].strip()
    return ptName

def extractBirthDay(contentList: list[str]) -> str:
    birthDay = "".join([date for date in contentList[5].split("年月日:")[-1][:11] if ord(date) != 32]).strip()
    return birthDay

def extractDepartment(contentList: list[str]) -> str:
    department = contentList[5][-10:-6].strip()
    return department

def extractDoctorName(contentList: list[str]) -> str:
    doctorName = contentList[5].split("醫師")[-2][-4:].strip()
    return doctorName

def checkBeginAndEnd(contentList: list[str]) -> int:
    numBegin , numEnd= 0, 0
    for listNum ,content in enumerate(contentList):
        if ("藥品" and "劑量" and "首日") in content:
            numBegin = listNum
        elif "Total Item" in content:
            numEnd = listNum
    return numBegin, numEnd

def extractUsageInfo(content: str) -> list:
    usageInfo = content.split("-")[-1].split(" ")
    usageInfo = [info.strip() for info in usageInfo if info != ""]
    return usageInfo

def extractMedisonInfo(contentList: list[str]) -> list:
    numBegin , numEnd= checkBeginAndEnd(contentList)
    drugNameList ,usageList, brandNameAndNoticeList = [], [], []
    nextPageNum = numBegin
    for content in contentList[numBegin:numEnd]:
        nextPageNum = nextPageNum + 1
        if " ." in content and "---" in content:
            drugName = content.split("---")[0][6:].strip()
            drugNameList.append(drugName)

            usageInfo = extractUsageInfo(content)
            usageList.append(usageInfo)

        elif " ." in content and len(content) < 90:
            drugName = content.split("---")[0][6:].strip()
            drugName = drugName + contentList[nextPageNum + 1].split("---")[0].strip()
            drugNameList.append(drugName)

        elif "---" in content:
            usageInfo = extractUsageInfo(content)
            usageList.append(usageInfo)

        if "商品:" in content:
            brandName = content.split("商品:")[-1].strip()
            notice = ""
            if "備註:" in contentList[nextPageNum]:
                notice = contentList[nextPageNum].split("備註:")[-1].strip()
            brandNameAndNoticeList.append((brandName, notice))

    return drugNameList, usageList, brandNameAndNoticeList
