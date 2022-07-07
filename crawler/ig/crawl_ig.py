import os
from bs4 import BeautifulSoup
import selenium.webdriver, time, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# js往下滑會自動讀出舊貼文。
# 先一直往下滑，儲存所有文章網址，用放入set跟判斷len是否改變來決定是否到最後頁了。

# 每則貼文網址：<div class="_aabd _aa8k _aanf"><a class..... href="....."><div>
# 主文方塊：<li class="_a9zj _a9zl _a9z5"></li>
# 每則回文方塊：<ul class="_a9ym"></ul>
# 發文者：<span class="_aap6 _aap7 _aap8"></span>
# 內文：<span class="_aacl _aaco _aacu _aacx _aad7 _aade"></span>
# 查看回覆：<ul class="_a9yo"><button class="_acan _acao _acas"></button></ul>
# 載入更多留言：<div class="_ab8w _ab94 _ab99 _ab9h _ab9m _ab9p _abcj"></div>

def waitTime(down: int=8, top: int=13):
    time.sleep(random.randint(down, top))
    pass

def login(IGLoginUrl: str, username: str, password: str) -> selenium:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "referer": "https://www.instagram.com/"
    }
    seleniumOptions = selenium.webdriver.ChromeOptions()
    seleniumOptions.add_argument("user-agent={}".format(headers["user-agent"]))
    seleniumOptions.add_argument("referer={}".format(headers["referer"]))
    # 下三行為不要彈出是否儲存帳密。
    prefs = {"": ""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    seleniumOptions.add_experimental_option("prefs", prefs)

    seleniumOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    driverExe = selenium.webdriver.Chrome(chrome_options=seleniumOptions,
                                          executable_path="../../driver/chromedriver.exe")

    driverExe.get(IGLoginUrl)
    WebDriverWait(driverExe, 50).until(expected_conditions.presence_of_element_located((By.NAME, "username")))
    waitTime()
    driverExe.find_element(By.NAME, "username").send_keys(username)
    driverExe.find_element(By.NAME, "password").send_keys(password)
    waitTime()
    driverExe.find_element(By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']").click()
    # waitTime()
    # WebDriverWait(driverExe, 50).until(
    #     expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "button[class='sqdOP yWX7d    y3zKF     ']")))
    # driverExe.find_element(By.CSS_SELECTOR, "button[class='sqdOP yWX7d    y3zKF     ']").click()
    waitTime()
    return driverExe

def getPostArticleSite(driverExe: selenium, personalUrl: str) -> set:
    personalName = personalUrl.split("/")[-2]
    path = "./data/{}/".format(personalName)
    if not os.path.isdir(path):
        os.makedirs("./data/{}/".format(personalName))

    driverExe.get(personalUrl)
    waitTime()

    soup = BeautifulSoup(driverExe.page_source, "html.parser")
    tmp = soup.select("div[class='_aabd _aa8k _aanf'] a")
    articleSiteSet = set([articleSite["href"] for articleSite in tmp])

    cntArticleSite = len(articleSiteSet)
    cntRetry = 0
    flag = True

    while flag:
        js = "window.scrollBy(0, document.body.scrollHeight)"
        driverExe.execute_script(js)
        waitTime()
        soup = BeautifulSoup(driverExe.page_source, "html.parser")
        tmp = soup.select("div[class='_aabd _aa8k _aanf'] a")
        [articleSiteSet.add(articleSite["href"]) for articleSite in tmp]

        newCnt = len(articleSiteSet)

        if newCnt > cntArticleSite:
            cntArticleSite = newCnt
            print(cntArticleSite)
            cntRetry = 0
        else:
            if cntRetry == 3:
                print("The getPostArticleSite function retry number is over.")
                print("End the function go to the next step.")
                flag = False
            else:
                cntRetry += 1

    with open("./data/{}/websites.txt".format(personalName) ,"w", encoding="utf-8")as w:
        articleSite = "\n".join(list(articleSiteSet))
        w.write(articleSite)
    print("Total article websites get.")

    return articleSiteSet, personalName

def getMainPostBlock(driverExe: selenium, articleUrl: str) -> tuple:
    driverExe.get(articleUrl)
    print("Get main post block")
    waitTime()
    soup = BeautifulSoup(driverExe.page_source, "html.parser")
    mainPostBlock = soup.select("li[class='_a9zj _a9zl _a9z5']")[0]
    mainPostAndContentText = getText(mainPostBlock)

    return mainPostAndContentText

def getReplyPost(soup: BeautifulSoup) -> list:
    replyList = []
    replyPostList = soup.select("ul[class='_a9ym']")
    for replyPost in replyPostList:
        replyList.append(getText(replyPost))

    return replyList

def getPoster(soup: BeautifulSoup) -> str:
    poster = soup.select("span[class='_aap6 _aap7 _aap8']")[0].text
    return poster

def getText(soup: BeautifulSoup) -> tuple:
    contentText = soup.select("span[class='_aacl _aaco _aacu _aacx _aad7 _aade']")
    if len(contentText) != 0:
        poster = getPoster(soup)
        return (poster, contentText[0].text)

def loadMoreReplyPost(driverExe: selenium, articleUrl: str) -> BeautifulSoup:
    driverExe.get(articleUrl)
    waitTime()
    flag = True
    cntRetry = 0
    while flag:
        if "載入更多留言" in str(BeautifulSoup(driverExe.page_source, "html.parser")):
            btnList = driverExe.find_elements(By.CLASS_NAME, "_abl-")
            btnList[-3].click()
            cntRetry = 0
            waitTime()
        else:
            if cntRetry == 4:
                flag = False
            else:
                cntRetry += 1

    return BeautifulSoup(driverExe.page_source, "html.parser")

def appMain(driverExe: selenium, personalUrl: str):
    articleSiteSet, personalName = getPostArticleSite(driverExe, personalUrl)
    for num in range(len(articleSiteSet)):
        articleSite = "https://www.instagram.com" + articleSiteSet.pop()
        fileName = articleSite.split("/")[-2]
        getPostMain(driverExe, articleSite, personalName, fileName)
        print("The {} article：{}, is finish.".format(personalName, fileName))
    pass

def getPostMain(driverExe: selenium, articleUrl: str, personalName: str, fileName: str):
    mainPostAndContentText = getMainPostBlock(driverExe, articleUrl)
    replySoup = loadMoreReplyPost(driverExe, articleUrl)
    replyList = getReplyPost(replySoup)
    with open("./data/{}/{}.txt".format(personalName, fileName), "w", encoding="utf-8")as w:
        poster, article = mainPostAndContentText
        w.write(poster + "|" + article + "\n")
        [w.write(poster + "|" + reply + "\n") for poster, reply in replyList]
    pass


if __name__ == "__main__":
    personalPage = "< personal main page website >"
    driverExe = login("https://www.instagram.com/", "< account >", "< password >")
    appMain(driverExe, personalPage)
