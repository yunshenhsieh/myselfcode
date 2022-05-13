import ddddocr, time, random, os
from bs4 import BeautifulSoup
from datetime import datetime
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import threading, ctypes, inspect

def main(driverExe, recordItemNum):
    global pageNum, totalPage
    print("main work")
    time.sleep(10)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "divResult")))
    totalPage = int(BeautifulSoup(driverExe.page_source, "html.parser").select("span#PageControl1_lblTotalPage")[0].text.replace(",",""))
    pageNum = int(BeautifulSoup(driverExe.page_source, "html.parser").select("span#PageControl1_lblCurrentPage")[0].text.replace(",",""))
    itemCnt = recordItemNum
    failPageCnt = 0
    while totalPage > pageNum:
        time.sleep(10)
        pageNum = int(BeautifulSoup(driverExe.page_source, "html.parser").select("span#PageControl1_lblCurrentPage")[0].text.replace(",", ""))
        if failPageCnt == 0:
            js="var action=document.documentElement.scrollTop=0"
            driverExe.execute_script(js)
            print("正在第 {} 頁。".format(pageNum))
            soup = BeautifulSoup(driverExe.page_source, "html.parser")
            itemNum = str(soup.select("table#GridView1")[0]).count("GridView1_btnMore")
            failItemCnt = 0
            while itemNum > itemCnt:
                try:
                    itemName = soup.select("span#GridView1_lblSchName_{}".format(itemCnt))[0].text
                    print("Download No.{} page, No.{} item, {}。".format(pageNum, itemCnt + 1, itemName))
                    mainPageToDataPage(driverExe, itemCnt)
                    itemCnt += 1
                except Exception as e:
                    if failItemCnt < 3 :
                        failItemCnt += 1
                        driverSwitchLastWindow(driverExe)
                        time.sleep(10)
                    else:
                        errLog = "***{} | {} | 第 {} 頁 | 第 {} 項 | 原因：{}\n".format(datetime.now(), itemName, pageNum, itemCnt + 1, e)
                        if "timeout" in errLog:
                            errLog = "{}|{}\n".format(pageNum, itemCnt)
                            with open("./timeout_log.txt", "a", encoding="utf-8") as w:
                                w.write(errLog)
                        else:
                            with open("./error_log.txt", "a", encoding="utf-8")as w:
                                w.write(errLog)
                        print(e)
                        failItemCnt = 0
                        itemCnt += 1
                        driverSwitchLastWindow(driverExe)
                        pass

            driverSwitchLastWindow(driverExe)
            nextPage(driverExe)
            failPageCnt = 0
            itemCnt = 0

        else:
            time.sleep(10)
            driverSwitchLastWindow(driverExe)
            nextPage(driverExe)
            itemCnt = 0

    pass

def mainByName(nameList: list):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "referer": "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    }
    url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    seleniumOptions = selenium.webdriver.ChromeOptions()
    seleniumOptions.add_argument("user-agent={}".format(headers["user-agent"]))
    seleniumOptions.add_argument("referer={}".format(headers["referer"]))
    seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    driverExe = selenium.webdriver.Chrome(chrome_options=seleniumOptions,
                                          executable_path="../../driver/chromedriver.exe")

    driverExe.get(url)
    time.sleep(4)
    for n, name in enumerate(nameList):
        WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "txtKeyNameS")))
        driverExe.find_element(By.ID, "txtKeyNameS").clear()
        driverExe.find_element(By.ID, "txtKeyNameS").send_keys(name)
        time.sleep(5)
        driverExe.find_element(By.ID, "btnSearch").click()
        print("mainByName work")
        time.sleep(10)
        itemCnt = 0
        failPageCnt = 0
        if failPageCnt == 0:
            js = "window.scrollBy(0, 40)"
            driverExe.execute_script(js)
            print("正在處理 第{}項 {}。".format(n, name))
            soup = BeautifulSoup(driverExe.page_source, "html.parser")
            try:
                itemNum = str(soup.select("table#GridView1")[0]).count("GridView1_btnMore")
            except Exception as e:
                errLog = soup.select("span#lblMsg")[0].text
                errLog = "***{} | {} | 原因：{}\n".format(datetime.now(), name, errLog)
                with open("./other_error.txt", "a", encoding="utf-8") as w:
                    w.write(errLog)

            failItemCnt = 0
            while itemNum > itemCnt:
                try:
                    itemName = soup.select("span#GridView1_lblSchName_{}".format(itemCnt))[0].text
                    print("Download {}。".format(itemName))
                    mainPageToDataPage(driverExe, itemCnt)
                    itemCnt += 1
                except Exception as e:
                    if failItemCnt < 3:
                        failItemCnt += 1
                        driverSwitchLastWindow(driverExe)
                        time.sleep(10)
                    else:
                        errLog = "***{} | {} | 原因：{}\n".format(datetime.now(), itemName, e)
                        if "timeout" in errLog:
                            errLog = "{}\n".format(name)
                            with open("./timeout_log.txt", "a", encoding="utf-8") as w:
                                w.write(errLog)
                        else:
                            with open("./error_log.txt", "a", encoding="utf-8") as w:
                                w.write(errLog)
                        print(e)
                        failItemCnt = 0
                        itemCnt += 1
                        driverSwitchLastWindow(driverExe)
    pass

def mainPageToDataPage(driverExe, num):
    time.sleep(random.randint(6, 9))
    checkExtend = BeautifulSoup(driverExe.page_source, "html.parser").select("input#GridView1_btnMore_{}".format(num))[0]["value"]
    if not ("收合" in checkExtend):
        driverExe.find_element(By.ID, "GridView1_btnMore_{}".format(num)).click()

    time.sleep(5)
    validValue = getValidNum(driverExe, num)

    time.sleep(5)
    driverExe.find_element(By.ID, "GridView1_txtVerify_{}".format(num)).clear()
    driverExe.find_element(By.ID, "GridView1_txtVerify_{}".format(num)).send_keys(validValue)
    time.sleep(5)
    driverExe.find_element(By.ID, "GridView1_lbChgList_{}".format(num)).click()
    time.sleep(5)
    driverSwitchLastWindow(driverExe)
    getData(driverExe)
    time.sleep(5)
    driverExe.close()
    driverSwitchLastWindow(driverExe)
    pass

def getData(driverExe):
    soup = BeautifulSoup(driverExe.page_source, "html.parser")
    print(soup.select("span#lblSchName102")[0].text)
    with open("./ece_result.txt", "a", encoding="utf-8")as w:
        w.write(str(soup) + "\n")
    return

def getValidNum(driverExe, num) -> str:
    renewValidNum(driverExe, num)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "GridView1_imgValidateCode_{}".format(num))))
    time.sleep(random.randint(4, 6))
    js = "window.scrollBy(0, 40)"
    driverExe.execute_script(js)
    driverExe.find_element(By.ID, "GridView1_imgValidateCode_{}".format(num)).screenshot("demo.jpg")
    global ocr
    with open("./demo.jpg", "rb") as f:
        tmp = f.read()
        validValue = ocr.classification(tmp)
        print(validValue)
    while True:
        validValue = validValue.replace("g", "9").replace("o", "0")
        if validValue.isdigit() and len(str(validValue)) == 4:
            return validValue
        else:
            renewValidNum(driverExe, num)
            WebDriverWait(driverExe, 50).until(
                expected_conditions.presence_of_element_located((By.ID, "GridView1_imgValidateCode_{}".format(num))))
            time.sleep(random.randint(4, 6))
            driverExe.find_element(By.ID, "GridView1_imgValidateCode_{}".format(num)).screenshot("demo.jpg")
            with open("./demo.jpg", "rb") as f:
                tmp = f.read()
                validValue = ocr.classification(tmp)
                print(validValue)

def renewValidNum(driverExe, num):
    driverExe.find_element(By.ID, "GridView1_lbReGen_{}".format(num)).click()
    js = "window.scrollBy(0, 40)"
    driverExe.execute_script(js)
    time.sleep(random.randint(4, 6))
    pass

def nextPage(driverExe):
    time.sleep(random.randint(4, 6))
    driverExe.switch_to.window(driverExe.window_handles[-1])
    driverExe.find_element(By.ID, "PageControl1_lbNextPage").click()
    pass

def switchToRecordPageNum(pageNum) -> object:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "referer": "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    }
    url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    seleniumOptions = selenium.webdriver.ChromeOptions()
    seleniumOptions.add_argument("user-agent={}".format(headers["user-agent"]))
    seleniumOptions.add_argument("referer={}".format(headers["referer"]))
    seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    driverExe = selenium.webdriver.Chrome(chrome_options=seleniumOptions,
                                          executable_path="../../driver/chromedriver.exe")

    driverExe.get(url)
    time.sleep(4)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "btnSearch")))
    driverExe.find_element(By.ID, "btnSearch").click()
    time.sleep(5)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.ID, "PageControl1_txtPages")))
    driverExe.find_element(By.ID, "PageControl1_txtPages").clear()
    driverExe.find_element(By.ID, "PageControl1_txtPages").send_keys(pageNum)
    driverExe.find_element(By.ID, "PageControl1_lbPageChg").click()

    return driverExe

def driverSwitchLastWindow(driverExe):
    driverExe.switch_to.window(driverExe.window_handles[-1])
    pass

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)

def stop_thread(thread):
    """终止线程"""
    _async_raise(thread.ident, SystemExit)
    print("stop thread")

def totalPageModelStart(startPageNum, startItemNum):
    thread_1 = threading.Thread(target=main, args=(
        switchToRecordPageNum(startPageNum), startItemNum))
    thread_1.start()
    totalPage = 1
    pageNum = 0

    while totalPage > pageNum:
        print(totalPage, pageNum)
        with open("./timeout_log.txt", "r", encoding="utf-8") as f:
            checkLog = f.read().strip()
        if checkLog:
            checkLog = checkLog.split("\n")
            if checkLog.count(checkLog[-1]) >= 3:
                stop_thread(thread_1)
                pageNum, itemCnt = checkLog[-1].split("|")
                pageNum, itemCnt = int(pageNum), int(itemCnt)
                if itemCnt < 9:
                    print("第{}頁，第{}項，開始重啟。".format(pageNum, itemCnt + 1))

                    thread_1 = threading.Thread(target=main, args=(switchToRecordPageNum(pageNum), itemCnt))
                    thread_1.start()
                    with open("./timeout_log.txt", "w", encoding="utf-8") as w:
                        w.write("")
                else:
                    print("第{}頁，第{}項，開始重啟。".format(pageNum + 1, 0 + 1))

                    thread_1 = threading.Thread(target=main, args=(switchToRecordPageNum(pageNum + 1), 0))
                    thread_1.start()
                    with open("./timeout_log.txt", "w", encoding="utf-8") as w:
                        w.write("")
            else:
                stop_thread(thread_1)
                pageNum, itemCnt = checkLog[-1].split("|")
                pageNum, itemCnt = int(pageNum), int(itemCnt)
                print("第{}頁，第{}項，開始重啟。".format(pageNum, itemCnt + 1))

                thread_1 = threading.Thread(target=main, args=(switchToRecordPageNum(pageNum), itemCnt))
                thread_1.start()
        else:
            time.sleep(120)

if __name__ == "__main__":

    ocr = ddddocr.DdddOcr()
    # totalPageModelStart(430, 5)
    thread_1 = threading.Thread(target=main, args=(
        switchToRecordPageNum(689), 9))
    thread_1.start()
    totalPage = 1
    pageNum = 0

    while totalPage > pageNum:
        print(totalPage, pageNum)
        with open("./timeout_log.txt", "r", encoding="utf-8") as f:
            checkLog = f.read().strip()
        if checkLog:
            stop_thread(thread_1)
            pageNum, itemCnt = checkLog.split("|")
            pageNum, itemCnt = int(pageNum), int(itemCnt)
            print("第{}頁，第{}項，開始重啟。".format(pageNum, itemCnt + 1))

            thread_1 = threading.Thread(target=main, args=(switchToRecordPageNum(pageNum), itemCnt))
            thread_1.start()
            with open("./timeout_log.txt", "w", encoding="utf-8") as w:
                w.write("")
        else:
            time.sleep(120)
