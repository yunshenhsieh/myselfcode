from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def main():
    # index page
    url = "https://www.agoda.com/zh-tw/search?guid=70c83cc6-4e09-48dd-bd17-bc2c473eab39&asq=mURkMCCYcckMqfcU9Np2E5ufa9Vwpz6XltTHq4n%2B9gOQSmBe1bQlYoBXMqPbVf5y1X8TUQtaw1u%2FC91TYcpyk0oxVtVlBdO9CbcCjEu6WiJIq8drzypSHcV%2FaFqeeUm1%2Fh%2Fe4idk67OoEy6KdHwUNum%2B3QacrQMDUE7JkJAfzu26b2DXIDuOEEqRACkwqPRN6eejEoWuoiGxdwaSfyPEYg%3D%3D&city=14690&tick=637841871605&txtuuid=70c83cc6-4e09-48dd-bd17-bc2c473eab39&locale=zh-tw&ckuid=b645e8fe-3f6b-42cb-97e2-ae1e10151b9e&prid=0&gclid=EAIaIQobChMIu56a0Mfr9gIVFbqWCh20dAZ3EAAYASAAEgKnpvD_BwE&currency=TWD&correlationId=34d08383-257d-49cd-83b7-6b33536b45e2&pageTypeId=1&realLanguageId=20&languageId=20&origin=TW&cid=1891473&tag=c6cac438-31ac-9b9f-bc08-0b36bc6fdc3f&userId=b645e8fe-3f6b-42cb-97e2-ae1e10151b9e&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=28&currencyCode=TWD&htmlLanguage=zh-tw&cultureInfoName=zh-tw&machineName=hk-acmweb-2001&trafficGroupId=5&sessionId=3hrqcpch54bzgvc15e0vzys5&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2022-04-07&checkOut=2022-04-08&rooms=1&adults=2&children=0&priceCur=TWD&los=1&textToSearch=%E9%A6%96%E7%88%BE&travellerType=1&familyMode=off&productType=-1"

    options = selenium.webdriver.ChromeOptions()
    driver = selenium.webdriver.Chrome(chrome_options=options, executable_path='../driver/chromedriver.exe')

    driver.get(url)
    WebDriverWait(driver, 50).until(expected_conditions.presence_of_element_located((By.ID, 'contentContainer')))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup.select("li[class='PropertyCard PropertyCardItem'] a")
    print(soup[0]["href"])

    # hotel page
    url_hotel = "https://www.agoda.com" + soup[0]["href"]
    options = selenium.webdriver.ChromeOptions()
    driver = selenium.webdriver.Chrome(chrome_options=options, executable_path='../driver/chromedriver.exe')

    driver.get(url_hotel)
    WebDriverWait(driver, 50).until(expected_conditions.presence_of_element_located((By.ID, 'review-0')))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup.select("p[class='Review-comment-bodyText']")
    for n, data in enumerate(soup):
        print("第" + str(n + 1) + "則：", data.text)
        print("===========================")

def comment():
    # 取出各別旅館網址
    # with open("./demo","r",encoding="utf-8")as f:
    #     tmp = f.read()
    # soup = BeautifulSoup(tmp, "html.parser")
    # soup = soup.select("li[class='PropertyCard PropertyCardItem'] a")
    # print(soup[0]["href"])

    # 取出評論
    # with open("./hotelpage", "r", encoding="utf-8")as f:
    #     tmp = f.read()
    # soup = BeautifulSoup(tmp, "html.parser")
    # soup = soup.select("p[class='Review-comment-bodyText']")
    # print(soup[0].text)
    pass

if __name__ == "__main__":
    main()
