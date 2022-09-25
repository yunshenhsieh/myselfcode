from bs4 import BeautifulSoup
from datetime import datetime
import time, random
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def setSeleniumOptionsAndDriverExe() -> object:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }
    seleniumOptions = selenium.webdriver.ChromeOptions()
    seleniumOptions.add_argument("user-agent={}".format(headers["user-agent"]))
    seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    seleniumOptions.add_argument('--headless')
    driverExe = selenium.webdriver.Chrome(chrome_options=seleniumOptions,
                                          executable_path="./driver/chromedriver.exe")
    return driverExe

def gtStorageCheck(driverExe, prodNumList, fileWriter0, fileWriter1):
    urlList = \
        ["https://shop.greattree.com.tw/product?SaleID={}".format(prodNum) for prodNum in prodNumList]

    for n, url in enumerate(urlList):
        driverExe.get(url)
        WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "pdcnt_info_number")))
        time.sleep(5)
        soup = BeautifulSoup(driverExe.page_source, "html.parser")
        soup = soup.select("div.pdcnt_info_number")
        prodNum = soup[0].select("option")[-1].text
        if int(prodNum) == 0:
            fileWriter0.write(prodNumList[n].strip() + "\n")
            fileWriter0.flush()
            print("商品編：{}，無庫存。".format(prodNumList[n].strip(), prodNum))
        else:
            fileWriter1.write("{}_{}\n".format(prodNumList[n].strip(), prodNum))
            fileWriter1.flush()
            print("商品編：{}，庫存為{}。".format(prodNumList[n].strip(), prodNum))
        time.sleep(random.randint(5, 7))

    pass

if __name__ == "__main__":
    print("版本：1.0.1\n發佈日期：2022/9/25\n作者：Vincent 燊。\n啟動執行中…")
    try:
        driverExe = setSeleniumOptionsAndDriverExe()
    except selenium.common.exceptions.SessionNotCreatedException as e:
        print("啟動失敗!!!")
        print("驅動器與當前chrome瀏覽器版本不同。")
        print("請確認瀏覽器版本後，至https://chromedriver.chromium.org/downloads下載對應版本。")
        print("解壓縮後，將檔名「chromedriver.exe」放入「driver」資料夾，刪除原先的chromedriver.exe即可正常運作。")
        input("按enter結束程式。")
    except selenium.common.exceptions.WebDriverException as e:
        print("啟動失敗!!!")
        print("請檢查「driver」資料夾內是否有「chromedriver.exe」檔案。")
        print("沒有請確認瀏覽器版本後，至https://chromedriver.chromium.org/downloads下載對應版本。")
        print("解壓縮後，將檔名「chromedriver.exe」放入「driver」資料夾，即可正常運作。")
        input("按enter結束程式。")

    with open("./batch/gt_prod_num_storage.txt", "r", encoding="utf-8")as f:
        prodNumList = f.readlines()

    fileWriter0 = open("./result/zero{}.txt".format(datetime.now().strftime("%Y%m%d_%H_%M_%S")), "a", encoding="utf-8")
    fileWriter1 = open("./result/{}.txt".format(datetime.now().strftime("%Y%m%d_%H_%M_%S")), "a", encoding="utf-8")

    gtStorageCheck(driverExe=driverExe, prodNumList=prodNumList[1:], fileWriter0=fileWriter0, fileWriter1=fileWriter1)

    input("按enter結束程式。")
