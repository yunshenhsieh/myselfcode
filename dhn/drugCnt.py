import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

def drugCntUpdateToGsheet(sheet_name: int, data_finish: list):
    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = './{}'.format(os.getenv('<py_gsheet_key_filename>'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('<drug_cnt_gsheet_id>')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()


    # 工作表新分頁的設定
    new_sheet_name = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'sheetId': sheet_name,
                    'title': str(sheet_name),
                    'index': 0
                }
            }
        }]
    }
    # 建立工作表新分頁
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=new_sheet_name).execute()

    # 寫入資料到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format(sheet_name, 1)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": data_finish}).execute()

def drugCntOutput(fileName: str) -> list:
    with open("./history/{}".format(fileName), "r", encoding="big5")as f:
        tmp = f.readlines()
        print(len(tmp))
        resource = []
        for data in tmp:
            data = data.strip().split(",")
            resource.append(data)

    dataFinish = dataClean(resource)
    dataFinish = classifyGroup(dataFinish)

    return dataFinish

def dataClean(resource: list) -> list:
    dataFinish = []
    valDict = {}
    dataDict = {}
    for content in resource[1:]:
        if "L02A" in content[2] or "L02E" in content[2]:
            level = content[2][:6]
            valDict["{},{},{},{}".format(level, content[3], content[6], content[5])] = \
                valDict.get("{},{},{},{}".format(level, content[3], content[6], content[5]), 0) + 1
        else:
            level = content[2][:4]
            valDict["{},{},{},{}".format(level, content[3], content[6], content[5])] = \
                valDict.get("{},{},{},{}".format(level, content[3], content[6], content[5]), 0) + 1

    for k, v in valDict.items():
        k = k.split(",")
        dataDict[k[0]] = dataDict.get(k[0], []) + [[k[1], k[2], v, k[3]]]

    for k, v in dataDict.items():
        tmp = []
        for val in v:
            tmp = tmp + [[k] + val]

        tmp.sort(key= lambda s: s[1])

        dataFinish = dataFinish + tmp

    return dataFinish

def classifyGroup(dataFinish: list) -> list:
    nClass = []
    oClass = []
    pClass = []
    sClass = []
    tClass = []
    uClass = []

    for v_list in dataFinish:
        if ord(v_list[1][0]) <= 77:
            oClass.append(v_list)
        elif v_list[1][0] == "N":
            nClass.append(v_list)
        elif v_list[1][0] in ("P", "Q", "R"):
            pClass.append(v_list)
        elif v_list[1][0] in ("S", "V", "W", "X", "Y"):
            sClass.append(v_list)
        elif v_list[1][0] in ("T"):
            tClass.append(v_list)
        elif v_list[1][0] in ("U"):
            uClass.append(v_list)

    groupClassList = [
        oClass,
        pClass,
        nClass,
        sClass,
        tClass,
        uClass]

    separateLevelGroupFinishList = []
    for dataList in groupClassList:
        separateLevelGroupFinishList.append(separateLevel(dataList))

    return separateLevelGroupFinishList

def separateLevel(groupClassList: list) -> list:
    separateFinishList = []
    prevLevel = groupClassList[0][0]
    for dataList in groupClassList:
        if prevLevel != dataList[0].strip():
            separateFinishList.append([])
            separateFinishList.append([])
            separateFinishList.append(dataList)
            prevLevel = dataList[0]
        else:
            separateFinishList.append(dataList)

    separateFinishList = [["樓層", "料位號", "使用數量", "幾組", "藥品名稱"]] + separateFinishList
    return separateFinishList


if __name__ == "__main__":
    # version 1.0.0
    load_dotenv()
    recordDate = "<drug use data date>"
    data = drugCntOutput("Batchdata{}.csv".format(recordDate))
    print(type(data))
    print(len((data)))
    for cnt in range(len(data)):
        drugCntUpdateToGsheet("{}".format(recordDate) + "0{}".format(cnt + 1), data[cnt])
