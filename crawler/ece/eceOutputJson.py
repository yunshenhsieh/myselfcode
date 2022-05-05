import json
from bs4 import BeautifulSoup

def buildItemJson():
    return dict([[inner , {"period" : 0, "cost" : 0}] for inner in ["tuition", "miscellaneous", "material", "activity", "lunch", "snack", "all_in_cost"]])

def buildDayJson():
    return dict([[dayItem, buildItemJson()]for dayItem in ["half_day", "full_day"]])

def buildClassJson():
    tmp_dict = {}
    tmp_dict["duration"] = 0
    tmp_dict["class"] = buildDayJson()
    return dict(tmp_dict)

def buildSemesterJson():
    tmp_dict = {}
    tmp_dict["first_semester"] = buildClassJson()
    tmp_dict["second_semester"] = buildClassJson()
    return dict(tmp_dict)

def buildAgeJson():
    tmp_dict = {}
    tmp_dict["age"] = 0
    tmp_dict["course"] = buildSemesterJson()
    return dict(tmp_dict)

def extractPeriod(soup: BeautifulSoup, ageN, resultJson):
    tuitionPeriod = soup.select("span#GridView{}_lblPT{}1_0".format(ageN, ageN))[0].text
    miscellaneousPeriod = soup.select("span#GridView{}_lblPT{}2_1".format(ageN, ageN))[0].text
    materialPeriod = soup.select("span#GridView{}_lblPT{}2_2".format(ageN, ageN))[0].text
    activityPeriod = soup.select("span#GridView{}_lblPT{}2_3".format(ageN, ageN))[0].text
    lunchPeriod = soup.select("span#GridView{}_lblPT{}2_4".format(ageN, ageN))[0].text
    snackPeriod = soup.select("span#GridView{}_lblPT{}2_5".format(ageN, ageN))[0].text
    periodTuple = (tuitionPeriod, miscellaneousPeriod, materialPeriod, activityPeriod, lunchPeriod, snackPeriod)

    resultJson["course"]["first_semester"]["class"]["half_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["first_semester"]["class"]["half_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["first_semester"]["class"]["half_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["first_semester"]["class"]["half_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["first_semester"]["class"]["half_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["first_semester"]["class"]["half_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["first_semester"]["class"]["half_day"]["all_in_cost"]["period"] = "學期"

    resultJson["course"]["first_semester"]["class"]["full_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["first_semester"]["class"]["full_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["first_semester"]["class"]["full_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["first_semester"]["class"]["full_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["first_semester"]["class"]["full_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["first_semester"]["class"]["full_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"

    resultJson["course"]["second_semester"]["class"]["half_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["second_semester"]["class"]["half_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["second_semester"]["class"]["half_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["second_semester"]["class"]["half_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["second_semester"]["class"]["half_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["second_semester"]["class"]["half_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["second_semester"]["class"]["half_day"]["all_in_cost"]["period"] = "學期"

    resultJson["course"]["second_semester"]["class"]["full_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["second_semester"]["class"]["full_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["second_semester"]["class"]["full_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["second_semester"]["class"]["full_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["second_semester"]["class"]["full_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["second_semester"]["class"]["full_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"

    pass

def extractDuration(soup: BeautifulSoup, ageN, i, resultJson):
    firstMonth = soup.select("span#lblMonth{}{}".format(ageN, i))[0].text
    secendMonth = soup.select("span#lblMonth{}{}".format(ageN, i))[0].text
    resultJson["course"]["first_semester"]["duration"] = float(firstMonth)
    resultJson["course"]["second_semester"]["duration"] = float(secendMonth)
    pass

def extractItemCost(soup: BeautifulSoup, ageN, i, resultJson):
    tmp = [0, "first_semester", "second_semester"]
    halfTuition = soup.select("span#GridView{}_lblHUnit{}{}_0".format(ageN, ageN, i))[0].text
    halfMiscellaneous = soup.select("span#GridView{}_lblHUnit{}{}_1".format(ageN, ageN, i))[0].text
    halfMaterial = soup.select("span#GridView{}_lblHUnit{}{}_2".format(ageN, ageN, i))[0].text
    halfActivity = soup.select("span#GridView{}_lblHUnit{}{}_3".format(ageN, ageN, i))[0].text
    halfLunch = soup.select("span#GridView{}_lblHUnit{}{}_4".format(ageN, ageN, i))[0].text
    halfSnack = soup.select("span#GridView{}_lblHUnit{}{}_5".format(ageN, ageN, i))[0].text
    halfAllCost = soup.select("span#GridView{}_lblHalf{}{}_6".format(ageN, ageN, i))[0].text
    halfDayCostTuple = (halfTuition, halfMiscellaneous, halfMaterial, halfActivity, halfLunch, halfSnack, halfAllCost)

    resultJson["course"][tmp[i]]["class"]["half_day"]["tuition"]["cost"] = int(halfDayCostTuple[0].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["miscellaneous"]["cost"] = int(halfDayCostTuple[1].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["material"]["cost"] = int(halfDayCostTuple[2].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["activity"]["cost"] = int(halfDayCostTuple[3].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["lunch"]["cost"] = int(halfDayCostTuple[4].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["snack"]["cost"] = int(halfDayCostTuple[5].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["half_day"]["all_in_cost"]["cost"] = int(halfDayCostTuple[6].replace(",", ""))
    

    fullTuition = soup.select("span#GridView{}_lblFUnit{}{}_0".format(ageN, ageN, i))[0].text
    fullMiscellaneous = soup.select("span#GridView{}_lblFUnit{}{}_1".format(ageN, ageN, i))[0].text
    fullMaterial = soup.select("span#GridView{}_lblFUnit{}{}_2".format(ageN, ageN, i))[0].text
    fullActivity = soup.select("span#GridView{}_lblFUnit{}{}_3".format(ageN, ageN, i))[0].text
    fullLunch = soup.select("span#GridView{}_lblFUnit{}{}_4".format(ageN, ageN, i))[0].text
    fullSnack = soup.select("span#GridView{}_lblFUnit{}{}_5".format(ageN, ageN, i))[0].text
    fullAllCost = soup.select("span#GridView{}_lblFull{}{}_6".format(ageN, ageN, i))[0].text
    fullDayCostTuple = (fullTuition, fullMiscellaneous, fullMaterial, fullActivity, fullLunch, fullSnack, fullAllCost)

    resultJson["course"][tmp[i]]["class"]["full_day"]["tuition"]["cost"] = int(fullDayCostTuple[0].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["miscellaneous"]["cost"] = int(fullDayCostTuple[1].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["material"]["cost"] = int(fullDayCostTuple[2].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["activity"]["cost"] = int(fullDayCostTuple[3].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["lunch"]["cost"] = int(fullDayCostTuple[4].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["snack"]["cost"] = int(fullDayCostTuple[5].replace(",", ""))
    resultJson["course"][tmp[i]]["class"]["full_day"]["all_in_cost"]["cost"] = int(fullDayCostTuple[6].replace(",", ""))
    pass

def eceParseSimple(soup: BeautifulSoup) -> dict:
    # 9為簡版
    resultJson = dict()
    ageNum = str(soup).count("lblAge")
    name = soup.select("span#lblSchName102")[0].text
    resultJson["name"] = name
    resultJson["data"] = [buildAgeJson() for i in range(ageNum)]
    for i in range(1, ageNum + 1):
        tmpJson = resultJson["data"][i - 1]
        tmpJson["age"] = soup.select("span#lblAge{}".format(i))[0].text
        tmpJson["course"]["first_semester"]["duration"] = float(soup.select("span#lblMonth{}1_2".format(i))[0].text)
        tmpJson["course"]["second_semester"]["duration"] = float(soup.select("span#lblMonth{}2_2".format(i))[0].text)
        tmpJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"
        tmpJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["cost"] = int(soup.select("span#lblFull{}1_2".format(i))[0].text.replace(",", ""))
        tmpJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"
        tmpJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["cost"] = int(soup.select("span#lblFull{}2_2".format(i))[0].text.replace(",", ""))

    return resultJson

def eceParse(soup: BeautifulSoup):
    resultJson = dict()
    ageNum = str(soup).count("lblAge")
    name = soup.select("span#lblSchName102")[0].text
    resultJson["name"] = name
    resultJson["data"] = [buildAgeJson() for i in range(ageNum)]

    for ageN in range(1,ageNum + 1):
        tmpJson = resultJson["data"][ageN - 1]
        age = soup.select("span#lblAge{}".format(ageN))[0].text
        if age:
            extractPeriod(soup, ageN, tmpJson)
            tmpJson["age"] = int(age)
            for i in range(1,3):
                extractDuration(soup, ageN, i, tmpJson)
                extractItemCost(soup, ageN, i, tmpJson)

    return resultJson

if __name__ == "__main__":
    with open("./result/outputtest.txt", "r", encoding="utf-8")as f:
        tmp = f.read()
    soup = BeautifulSoup(tmp, "html.parser")
    # print(eceParseSimple(soup.select("html")[9]))
    # eceParse(soup.select("html")[0])
    # print(eceParse(soup.select("html")[0]))
    dataList = []
    for n, soupHtml in enumerate(soup.select("html")):
        print(n, soupHtml.select("span#lblSchName102")[0].text)
        if "lblDGItemGroup" in str(soupHtml):
            dataList.append(eceParse(soupHtml))
        else:
            dataList.append(eceParseSimple(soupHtml))

    with open("./result/demoOutput.txt", "w", encoding="utf-8")as w:
        w.write(str(dataList))
    with open("./result/demoOutputJson.txt", "w", encoding="utf-8")as w:
        w.write(json.dumps(dataList))
