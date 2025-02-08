# Version 4.0.6
def extractReceiveNumber(contentHeaderList: list[str]) -> str:
    receiveNumber = contentHeaderList[3].split('：')[-1][:5].strip()
    return receiveNumber

def extractChartNumber(contentHeaderList: list[str]) -> str:
    chartNumber = ''.join([n for n in contentHeaderList[4][:9] if ord(n) != 32]).strip()
    return chartNumber

def extractPtName(contentHeaderList: list[str]) -> str:
    ptName = contentHeaderList[5][:20].strip()
    if '出' in ptName:
        ptName = ptName[:ptName.index('出')].strip()
    return ptName

def extractBirthDay(contentHeaderList: list[str]) -> str:
    birthDay = ''.join([date for date in contentHeaderList[5].split('年月日:')[-1][:11] if ord(date) != 32]).strip()
    return birthDay

def extractDepartment(contentHeaderList: list[str]) -> str:
    department = '急診' + contentHeaderList[5].strip().split('急診')[-1]
    return department

def extractDoctorName(contentHeaderList: list[str]) -> str:
    doctorName = contentHeaderList[5].split('醫師')[-2][-4:].strip()
    return doctorName

def sortSerialNumber(contentMedicineList: list) -> list:
    medicineList = [medicineData.strip().split('\t') for medicineData in contentMedicineList]

    for n, medicineData in enumerate(medicineList):
        medicineList[n][0] = int(medicineData[0])

    medicineList = sorted(medicineList, key=lambda x: x[0])

    for n, medicineData in enumerate(medicineList):
        medicineList[n][0] = str(medicineData[0])

    return medicineList

def extractMedicineInfo(contentMedicineList: list, drugProfileDict: dict) -> list:
    # 讓藥品按序號排列，發現藥袋列印順序也是看序號。
    medicineList = sortSerialNumber(contentMedicineList)

    for n, medicine in enumerate(medicineList):
        drugId = medicine[17].split(' ')[0].strip()
        # 藥品編號查無資料時，給13個空值的串列，這樣就不會因為串列長度不足而跳錯。
        drugCode = drugProfileDict.get(drugId, ['' for n in range(13)])[12]
        medicineList[n][2] = drugId
        medicineList[n][1] = drugCode
        # 補足最後一行list長度，不然最後一行沒有備註的話，最後一格就會是藥品編號，列印時就會印在備註。
        if len(medicineList[n]) < 20:
            medicineList[n] = medicineList[n] + ([''] * (20 - len(medicineList[n])))
    return medicineList

def seperateHeaderAndMedicineInfo(contentList: list) -> list:
    contentHeaderList = []
    contentMedicineList = []
    for content in contentList:
        if '\t' in content:
            contentMedicineList.append(content)
        else:
            contentHeaderList.append(content)
    return contentHeaderList, contentMedicineList
