import extract
def templateProduce() -> str:
    template = """
    \n\n\n\n\n                                                                 {}
    \n\n         {}                          {}            {}
    \n\n\n           {}
    \n\n\n\n\n\n\n             {}
    \n\n              {}"""

    return template

def loadFile(filePath: str) -> list[str]:
    with open(filePath, "r", encoding="utf-8")as f:
        contentList = f.readlines()
    return contentList

def drugBagMaker(contentList: list[str]) -> str:
    receiveNumber = extract.extractReceiveNumber(contentList)
    ptName = extract.extractPtName(contentList)
    ptBirthDay = extract.extractBirthDay(contentList)
    dipensingDay = extract.extractDate(contentList)
    ptChartNumber = extract.extractChartNumber(contentList)

    drugNameList, usageList = extract.extractMedisonInfo(contentList)
    drugBag = [templateProduce().format(receiveNumber, ptName, ptBirthDay, dipensingDay, ptChartNumber, drugName, usage)
                for drugName, usage in zip(drugNameList, usageList)]
    return drugBag

if __name__ == "__main__":
    # Version 0.0.1
    contentList = loadFile(< filePath >)
    drugBageInfo = ""
    for data in drugBagMaker(contentList):
        drugBageInfo += data
    with open(< fileName >, "w", encoding="utf-8")as w:
        w.write(drugBageInfo)
        w.close()
    pass
