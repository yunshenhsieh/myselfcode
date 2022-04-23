import ddddocr, time
from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
    url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
    options = selenium.webdriver.ChromeOptions()
    driver = selenium.webdriver.Chrome(chrome_options=options, executable_path="../../driver/chromedriver.exe")

    driver.get(url)
    WebDriverWait(driver, 50).until(expected_conditions.presence_of_element_located((By.ID, "btnSearch")))
    driver.find_element(By.ID, "btnSearch").click()
    WebDriverWait(driver, 50).until(expected_conditions.presence_of_element_located((By.ID, "divResult")))
    driver.find_element(By.ID, "GridView1_btnMore_0").click()


    time.sleep(5)
    driver.find_element(By.ID, "GridView1_imgValidateCode_0").screenshot("demo.jpg")
    with open("./demo.jpg", "rb")as f:
        tmp = f.read()
        ocr = ddddocr.DdddOcr()
        validValue = ocr.classification(tmp)
        print(validValue)

    time.sleep(5)
    driver.find_element(By.ID, "GridView1_txtVerify_0").send_keys(validValue)
    time.sleep(5)
    driver.find_element(By.ID, "GridView1_lbChgList_0").click()
    time.sleep(5)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(soup.text)
    with open("./demo.txt", "w", encoding="utf-8")as w:
        w.write(soup.text)

if __name__ == "__main__":
    main()
