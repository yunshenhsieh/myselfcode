# Version 4.0.0
def extractReceiveNumber(contentForHeader: list[str]) -> str:
    receiveNumber = contentForHeader[3].split('：')[-1][:5].strip()
    return receiveNumber

def extractChartNumber(contentForHeader: list[str]) -> str:
    chartNumber = ''.join([n for n in contentForHeader[4][:9] if ord(n) != 32]).strip()
    return chartNumber

def extractPtName(contentForHeader: list[str]) -> str:
    ptName = contentForHeader[5][:20].strip()
    if '出' in ptName:
        ptName = ptName[:ptName.index('出')].strip()
    return ptName

def extractBirthDay(contentForHeader: list[str]) -> str:
    birthDay = ''.join([date for date in contentForHeader[5].split('年月日:')[-1][:11] if ord(date) != 32]).strip()
    return birthDay

def extractDepartment(contentForHeader: list[str]) -> str:
    department = '急診' + contentForHeader[5].strip().split('急診')[-1]
    return department

def extractDoctorName(contentForHeader: list[str]) -> str:
    doctorName = contentForHeader[5].split('醫師')[-2][-4:].strip()
    return doctorName

def sortSerialNumber(contentForDrugInfo: str) -> list:
    medisonList = [medisonData.split('\t') for medisonData in contentForDrugInfo.strip().split('\n')]
    for n, medisonData in enumerate(medisonList):
        medisonList[n][0] = int(medisonData[0])

    medisonList = sorted(medisonList, key=lambda x: x[0])

    for n, medisonData in enumerate(medisonList):
        medisonList[n][0] = str(medisonData[0])

    return medisonList

def extractMedisonInfo(contentForDrugInfo: str, drugProfileDict: dict) -> list:
    # 讓藥品按序號排列，發現藥袋列印順序也是看序號。
    medisonList = sortSerialNumber(contentForDrugInfo)

    for n, medison in enumerate(medisonList):
        drugId = medison[17].split(' ')[0].strip()
        drugCode = drugProfileDict.get(drugId, "000")[12]
        medisonList[n][2] = drugId
        medisonList[n][1] = drugCode
        # 補足最後一行list長度，不然最後一行沒有備註的話，最後一格就會是藥品編號，列印時就會印在備註。
        if len(medisonList[n]) < 20:
            medisonList[n] = medisonList[n] + ([''] * (20 - len(medisonList[n])))
    return medisonList
