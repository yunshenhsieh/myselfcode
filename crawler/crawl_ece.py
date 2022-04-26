import ddddocr, time, random
from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "referer": "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
        }
    url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    seleniumOptions = selenium.webdriver.ChromeOptions()
    seleniumOptions.add_argument("user-agent={}".format(headers["user-agent"]))
    seleniumOptions.add_argument("referer={}".format(headers["referer"]))
    seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    driverExe = selenium.webdriver.Chrome(chrome_options=seleniumOptions, executable_path="../../driver/chromedriver.exe")

    driverExe.get(url)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "btnSearch")))
    driverExe.find_element(By.ID, "btnSearch").click()
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "divResult")))
    totalPage = int(BeautifulSoup(driverExe.page_source, "html.parser").select("span#lblRowCnt")[0].text.replace(",",""))

    for pageNum in range(totalPage):
        print("正在第 {} 頁。".format(pageNum + 1))
        itemNum = str(BeautifulSoup(driverExe.page_source, "html.parser").select("table#GridView1")[0]).count("GridView1_btnMore")
        for num in range(itemNum):
            print("Download No.{} item。".format(num + 1))
            mainPageToDataPage(driverExe, num)
        nextPage(driverExe)
    pass

def mainPageToDataPage(driverExe, num):
    time.sleep(random.randint(4, 6))
    driverExe.find_element(By.ID, "GridView1_btnMore_{}".format(num)).click()

    time.sleep(5)
    validValue = getValidNum(driverExe, num)

    time.sleep(5)
    driverExe.find_element(By.ID, "GridView1_txtVerify_{}".format(num)).send_keys(validValue)
    time.sleep(5)
    try:
        driverExe.find_element(By.ID, "GridView1_lbChgList_{}".format(num)).click()
        time.sleep(5)
        driverSwitchLastWindow(driverExe)
        getData(driverExe)
        time.sleep(5)
        driverExe.close()
        driverSwitchLastWindow(driverExe)
    except:
        print("第 {} 項 失敗。".format(num))
    pass

def getData(driverExe):
    soup = BeautifulSoup(driverExe.page_source, "html.parser")
    print(soup.select("span#lblSchName102")[0].text)
    return

def getValidNum(driverExe, num) -> str:
    renewValidNum(driverExe, num)
    time.sleep(random.randint(4, 6))
    driverExe.find_element(By.ID, "GridView1_imgValidateCode_{}".format(num)).screenshot("demo.jpg")
    global ocr
    with open("./demo.jpg", "rb") as f:
        tmp = f.read()
        validValue = ocr.classification(tmp)
        print(validValue)
    while True:
        validValue = validValue.replace("g", "9").replace("o", "0")
        if validValue.isdigit():
            return validValue
        else:
            renewValidNum(driverExe, num)
            driverExe.find_element(By.ID, "GridView1_imgValidateCode_{}".format(num)).screenshot("demo.jpg")
            with open("./demo.jpg", "rb") as f:
                tmp = f.read()
                validValue = ocr.classification(tmp)
                print(validValue)

def renewValidNum(driverExe, num):
    driverExe.find_element(By.ID, "GridView1_lbReGen_{}".format(num)).click()
    time.sleep(random.randint(4, 6))
    pass

def nextPage(driverExe):
    driverExe.find_element(By.ID, "PageControl1_lbNextPage").click()
    time.sleep(random.randint(4, 6))
    pass

def driverSwitchLastWindow(driverExe):
    driverExe.switch_to.window(driverExe.window_handles[-1])
    pass

if __name__ == "__main__":
    input("enter鍵開始")
    ocr = ddddocr.DdddOcr()
    main()
