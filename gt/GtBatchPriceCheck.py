from bs4 import BeautifulSoup
from datetime import datetime
import requests, time, random

def gtBatchCheck(headers, prodData, index, fileWriter):
    productNum, price = prodData.split("_")
    price = int(price)
    url = "https://shop.greattree.com.tw/product?SaleID={}".format(productNum)
    req = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(req.text, "html.parser")
    soup = soup.select('div[class="pdcnt_info"]')

    tmp_list = ["", "", "", ""]
    titleGroup = soup[0].select('div[class="js-productName js-group"]')
    priceGroup = soup[0].select('div[class="js-productPrice js-group"]')

    tmp_list[0], _, tmp_list[1], tmp_list[2] = titleGroup[0].select("h1")[0].text.strip().split("\n")
    tmp_list = [data.strip() for data in tmp_list]

    tmp_list[3] = int(priceGroup[0].select("span.price-sale")[0].text.replace("$", "").replace(",", ""))

    if tmp_list[3] == price:
        print("{}、{}，價格 {} 正確。".format(index, tmp_list[1], price))
    else:
        warningMSG = "{}、{}，{} 與網頁價格 {} 不同，請核對。".format(index, tmp_list[1], price, tmp_list[3])

        fileWriter.write(warningMSG + "\n")
        fileWriter.flush()

        print("{}、{}，{} 與網頁價格 {} 不同，請核對。".format(index, tmp_list[1], price, tmp_list[3]))
    pass

if __name__ == "__main__":
    print("版本：1.0.0\n發佈日期：2022/9/14\n作者：Vincent 燊。\n啟動執行中…")
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
    with open("./batch/gt_prod_num.txt", "r", encoding="utf-8")as f:
        tmp = f.readlines()

    fileWriter = open("./result/{}.txt".format(datetime.now().strftime("%Y%m%d_%H_%M_%S")), "a", encoding="utf-8")

    for index, prodData in enumerate(tmp[1:]):
        gtBatchCheck(headers, prodData, index + 1, fileWriter)
        time.sleep(random.randint(3, 7))
        print("")

    input("按enter結束程式。")
