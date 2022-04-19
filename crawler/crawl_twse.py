import requests, time, random, datetime, json, openpyxl
from bs4 import BeautifulSoup
from collections import deque

headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
twseUrl = "https://www.twse.com.tw"

def getStockGroupCode() -> dict:
    headColAndStockGroupDict = {}
    headerColumnList = "/fund/T86?response=html"
    respones = requests.get(url=twseUrl + headerColumnList, headers=headers)
    soup = BeautifulSoup(respones.text, "html.parser")
    headTrList = soup.select("thead")[0].select("tr")
    title = headTrList[0].select("div")[0].text
    dataTimeNow, title = title.split(" ")
    dataTimeNow = str(int(dataTimeNow[0:3]) + 1911) + dataTimeNow[4:6] + dataTimeNow[7:9]
    headColumnList = headTrList[1].select("td")
    headColAndStockGroupDict[title] = []
    for col in headColumnList:
        headColAndStockGroupDict[title].append(col.text)

    TIIUrl = "/zh/page/trading/fund/T86.html"
    respones = requests.get(url=twseUrl + TIIUrl, headers=headers)

    soup = BeautifulSoup(respones.text, "html.parser")
    stock_group_list = soup.select("select[name='selectType']")[0].select("option")
    for code in stock_group_list:
        tmp = code["value"]
        if len(tmp) == 2 and tmp.isdigit():
            headColAndStockGroupDict[tmp + "|" + code.text] = None
    return dataTimeNow, headColAndStockGroupDict

# Three Institutional Investors Buy/Sell
def getTIIBuySellData(dataTime, headColAndStockGroupDict) -> dict:
    selectTypeDeque = deque(headColAndStockGroupDict.keys())

    for round in range(3):
        catchLoseDeque = deque()
        while selectTypeDeque:
            selectType = selectTypeDeque.popleft()
            typeCode = selectType.split("|")[0]
            try:
                if len(typeCode) == 2:
                    BuySellUrl = "/fund/T86?response=html&date={}&selectType={}".format(dataTime, typeCode)
                    respones = requests.get(url=twseUrl + BuySellUrl, headers=headers)
                    time.sleep(random.randint(2, 5))
                    soup = BeautifulSoup(respones.text, "html.parser")
                    print(dataTime, selectType)
                    stockDataList = soup.select("tbody")[0].select("tr")
                    result = []
                    for stockData in stockDataList:
                        tmp = []
                        for data in stockData.select("td"):
                            tmp.append(data.text.strip())
                        result.append(tmp)
                    headColAndStockGroupDict[selectType] = result
            except Exception as e:
                print(selectType, e)
                print(soup.text)
                catchLoseDeque.append(selectType)
        selectTypeDeque = catchLoseDeque
        print("===========", round + 1, "==============")
    return headColAndStockGroupDict


def getMultiDayData(frequency, dataTimeNowStr, headColAndStockGroupDict) -> dict:
    result = {}
    for day in range(frequency):
        nowTime = datetime.datetime.strptime(dataTimeNowStr, "%Y%m%d")
        getDataDayTime = nowTime + datetime.timedelta(days = -day)
        getDataDayTime = getDataDayTime.strftime("%Y%m%d")
        result[getDataDayTime] = getTIIBuySellData(getDataDayTime, headColAndStockGroupDict)
    return result

def outputToExcel(jsonData):
    wb = openpyxl.Workbook()
    for item in jsonData.items():
        day = item[0]
        wDaySheet = wb.create_sheet(day)
        title, Headers = ["三大法人買賣超日報"], item[1]["三大法人買賣超日報"]
        wDaySheet.append(title)
        wDaySheet.append(Headers)
        for data in list(item[1].items())[1:]:
            print(data[0])
            wDaySheet.append([data[0].split("|")[1]])
            if data[1]:
                [wDaySheet.append(stockData) for stockData in data[1]]
            else:
                wDaySheet.append(["無資料。"])
    fileName = list(jsonData.keys())
    wb.remove(wb["Sheet"])
    wb.save("{}_{}.xlsx".format(fileName[0], fileName[-1]))
    pass

if __name__ == "__main__":
    dataTime, groupCode = getStockGroupCode()
    jsonData = getMultiDayData(2, dataTime, groupCode)
    outputToExcel(jsonData)
