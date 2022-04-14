import requests, time, os, datetime, random
from bs4 import BeautifulSoup
from collections import deque

headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
twseUrl = "https://www.twse.com.tw"

nowTime = datetime.datetime.now()
prevDayTime = nowTime + datetime.timedelta(days = -1)
prevDayFormatTime = prevDayTime.strftime("%Y%m%d")

def getStockGroupCode() -> dict:
    headColAndStockGroupDict = {}
    headerColumnList = "/fund/T86?response=html"
    respones = requests.get(url=twseUrl + headerColumnList, headers=headers)
    soup = BeautifulSoup(respones.text, "html.parser")
    headTrList = soup.select("thead")[0].select("tr")
    title = headTrList[0].select("div")[0].text
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
    return headColAndStockGroupDict

# Three Institutional Investors Buy/Sell
def getTIIBuySellData(headColAndStockGroupDict) -> dict:
    selectTypeDeque = deque(headColAndStockGroupDict.keys())
    roundCount = 0
    while selectTypeDeque and roundCount < 3:
        selectType = selectTypeDeque.popleft()
        typeCode = selectType.split("|")[0]
        try:
            if len(typeCode) == 2:
                BuySellUrl = "/fund/T86?response=html&date={}&selectType={}".format(prevDayFormatTime, typeCode)
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
            selectTypeDeque.append(selectType)
            roundCount += 1

    return headColAndStockGroupDict

if __name__ == "__main__":
    tmp = getTIIBuySellData(getStockGroupCode())
    with open("demo_json.txt", 'w', encoding="utf-8")as w:
        w.write(str(tmp))
