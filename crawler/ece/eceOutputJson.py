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

def checkPeriod(soup: BeautifulSoup, ageN) -> tuple:
    resultPeriod = []
    periodUnitDict = {"月": "Month", "學期": "Semester"}
    tmp = soup.select("table#GridView{}".format(ageN))[0]
    for i in range(1, 7):
        checkVoidValue = tmp.select("tr")[i].select("span")
        if len(checkVoidValue) >= 2:
            if i == 3:
                duration = checkVoidValue[2].text
                if duration.replace(",", "").isdigit():
                    resultPeriod.append(None)
                else:
                    resultPeriod.append(periodUnitDict[duration])
            else:
                duration = checkVoidValue[1].text
                if duration.replace(",", "").isdigit():
                    resultPeriod.append(None)
                else:
                    resultPeriod.append(periodUnitDict[duration])
        else:
            resultPeriod.append(None)
    return tuple(resultPeriod)

def extractPeriod(soup: BeautifulSoup, ageN, resultJson):

    periodTuple = checkPeriod(soup, ageN)

    resultJson["course"]["first_semester"]["class"]["half_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["first_semester"]["class"]["half_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["first_semester"]["class"]["half_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["first_semester"]["class"]["half_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["first_semester"]["class"]["half_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["first_semester"]["class"]["half_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["first_semester"]["class"]["half_day"]["all_in_cost"]["period"] = "Semester"

    resultJson["course"]["first_semester"]["class"]["full_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["first_semester"]["class"]["full_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["first_semester"]["class"]["full_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["first_semester"]["class"]["full_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["first_semester"]["class"]["full_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["first_semester"]["class"]["full_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "Semester"

    resultJson["course"]["second_semester"]["class"]["half_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["second_semester"]["class"]["half_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["second_semester"]["class"]["half_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["second_semester"]["class"]["half_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["second_semester"]["class"]["half_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["second_semester"]["class"]["half_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["second_semester"]["class"]["half_day"]["all_in_cost"]["period"] = "Semester"

    resultJson["course"]["second_semester"]["class"]["full_day"]["tuition"]["period"] = periodTuple[0]
    resultJson["course"]["second_semester"]["class"]["full_day"]["miscellaneous"]["period"] = periodTuple[1]
    resultJson["course"]["second_semester"]["class"]["full_day"]["material"]["period"] = periodTuple[2]
    resultJson["course"]["second_semester"]["class"]["full_day"]["activity"]["period"] = periodTuple[3]
    resultJson["course"]["second_semester"]["class"]["full_day"]["lunch"]["period"] = periodTuple[4]
    resultJson["course"]["second_semester"]["class"]["full_day"]["snack"]["period"] = periodTuple[5]
    resultJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "Semester"

    pass

def extractDuration(soup: BeautifulSoup, ageN, i, resultJson):
    firstMonth = soup.select("span#lblMonth{}{}".format(ageN, i))[0].text
    secendMonth = soup.select("span#lblMonth{}{}".format(ageN, i))[0].text
    resultJson["course"]["first_semester"]["duration"] = float(firstMonth)
    resultJson["course"]["second_semester"]["duration"] = float(secendMonth)
    pass

def checkItemNoData(DayCostDict: dict, resultJson: dict, semester: str, courseDuration: str):
    for k, v in DayCostDict.items():
        if v:
            v = int(v[0].text.replace(",", ""))
            resultJson["course"][semester]["class"][courseDuration][k]["cost"] = v
        else:
            resultJson["course"][semester]["class"][courseDuration][k]["cost"] = None
    pass

def extractItemCost(soup: BeautifulSoup, ageN, i, resultJson):
    tmp = [0, "first_semester", "second_semester"]

    halfTuition = soup.select("span#GridView{}_lblHUnit{}{}_0".format(ageN, ageN, i))
    halfMiscellaneous = soup.select("span#GridView{}_lblHUnit{}{}_1".format(ageN, ageN, i))
    halfMaterial = soup.select("span#GridView{}_lblHUnit{}{}_2".format(ageN, ageN, i))
    halfActivity = soup.select("span#GridView{}_lblHUnit{}{}_3".format(ageN, ageN, i))
    halfLunch = soup.select("span#GridView{}_lblHUnit{}{}_4".format(ageN, ageN, i))
    halfSnack = soup.select("span#GridView{}_lblHUnit{}{}_5".format(ageN, ageN, i))
    halfAllCost = soup.select("span#GridView{}_lblHalf{}{}_6".format(ageN, ageN, i))
    halfDayCostDict = {"tuition": halfTuition, "miscellaneous": halfMiscellaneous,
                       "material": halfMaterial, "activity": halfActivity, "lunch": halfLunch,
                       "snack": halfSnack, "all_in_cost": halfAllCost}
    checkItemNoData(halfDayCostDict, resultJson, tmp[i], "half_day")

    fullTuition = soup.select("span#GridView{}_lblFUnit{}{}_0".format(ageN, ageN, i))
    fullMiscellaneous = soup.select("span#GridView{}_lblFUnit{}{}_1".format(ageN, ageN, i))
    fullMaterial = soup.select("span#GridView{}_lblFUnit{}{}_2".format(ageN, ageN, i))
    fullActivity = soup.select("span#GridView{}_lblFUnit{}{}_3".format(ageN, ageN, i))
    fullLunch = soup.select("span#GridView{}_lblFUnit{}{}_4".format(ageN, ageN, i))
    fullSnack = soup.select("span#GridView{}_lblFUnit{}{}_5".format(ageN, ageN, i))
    fullAllCost = soup.select("span#GridView{}_lblFull{}{}_6".format(ageN, ageN, i))
    fullDayCostDict = {"tuition": fullTuition, "miscellaneous": fullMiscellaneous,
                       "material": fullMaterial, "activity": fullActivity, "lunch": fullLunch,
                       "snack": fullSnack, "all_in_cost": fullAllCost}
    checkItemNoData(fullDayCostDict, resultJson, tmp[i], "full_day")

    pass

def eceParseSimple(soup: BeautifulSoup) -> dict:
    # 9為簡版
    resultJson = dict()
    ageNum = str(soup).count("lblAge")
    name = soup.select("span#lblSchName102")[0].text
    resultJson["name"] = name
    resultJson["data"] = [buildAgeJson() for i in range(ageNum)]
    for ageN in range(1, ageNum + 1):
        age = soup.select("span#lblAge{}".format(ageN))[0].text
        if age:
            tmpJson = resultJson["data"][ageN - 1]
            tmpJson["age"] = soup.select("span#lblAge{}".format(ageN))[0].text
            tmpJson["course"]["first_semester"]["duration"] = float(soup.select("span#lblMonth{}1_2".format(ageN))[0].text)
            tmpJson["course"]["second_semester"]["duration"] = float(soup.select("span#lblMonth{}2_2".format(ageN))[0].text)
            tmpJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"
            tmpJson["course"]["first_semester"]["class"]["full_day"]["all_in_cost"]["cost"] = int(soup.select("span#lblFull{}1_2".format(ageN))[0].text.replace(",", ""))
            tmpJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["period"] = "學期"
            tmpJson["course"]["second_semester"]["class"]["full_day"]["all_in_cost"]["cost"] = int(soup.select("span#lblFull{}2_2".format(ageN))[0].text.replace(",", ""))
        else:
            del resultJson["data"][ageN - 1]
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
        else:
            del resultJson["data"][ageN - 1]

    return resultJson

if __name__ == "__main__":
    with open("./result/outputtest.txt", "r", encoding="utf-8")as f:
        tmp = f.read()
    soup = BeautifulSoup(tmp, "html.parser")
    # print(eceParseSimple(soup.select("html")[9]))
    # eceParse(soup.select("html")[0])
    # print(eceParse(soup.select("html")[0]))
    dataList = []
    for n, soupHtml in enumerate(soup.select("html")[137:138]):
        print(n, soupHtml.select("span#lblSchName102")[0].text)
        if "lblDGItemGroup" in str(soupHtml):
            dataList.append(eceParse(soupHtml))
        else:
            dataList.append(eceParseSimple(soupHtml))

    print(dataList)
    # print(len(dataList))
    # with open("./result/demoOutput.txt", "w", encoding="utf-8")as w:
    #     w.write(str(dataList))
    # with open("./result/demoOutputJson.txt", "w", encoding="utf-8")as w:
    #     w.write(json.dumps(dataList))
