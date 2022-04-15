import requests, time, random
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
    dataTime, title = title.split(" ")
    dataTime = str(int(dataTime[0:3]) + 1911) + dataTime[4:6] + dataTime[7:9]
    title = dataTime + title
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
    return dataTime, headColAndStockGroupDict

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
                    print(selectType)
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

if __name__ == "__main__":
    datatime, groupCode = getStockGroupCode()
    print(groupCode)
    tmp = getTIIBuySellData(datatime, groupCode)
    with open("demo.txt", 'w', encoding="utf-8")as w:
        w.write(str(tmp))
