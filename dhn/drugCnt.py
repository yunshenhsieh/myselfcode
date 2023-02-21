import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

def drugCntUpdateToGsheet(sheet_name: int, data_finish: list):
    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = './{}'.format(os.getenv('google_sheet_api_key'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('drug_cnt_id')
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
                    'index': 0,
                    'gridProperties': {'frozen_row_count': 1}
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
    separateLevelGroupFinishList, nstuList = classifyGroup(dataFinish)

    return separateLevelGroupFinishList, nstuList

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
        uClass
    ]

    paNSTUList = paNSTUClassify(groupClassList)

    separateLevelGroupFinishList = []
    for dataList in groupClassList:
        separateLevelGroupFinishList.append(separateLevel(dataList))

    return separateLevelGroupFinishList, paNSTUList

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

def paNSTUClassify(nstuClassList: list) -> list:
    nClass = nstuClassList[2]
    sClass = nstuClassList[3]
    tClass = nstuClassList[4]
    uClass = nstuClassList[5]
    nstuClassList = [nClass, sClass, tClass, uClass]
    nstuList = [[], [], [], []]

    for index, dataList in enumerate(nstuClassList):
        tmpCntDict = {}
        for data in dataList:
            if data[0][0] == "L":
                tmpCntDict["{},{}".format(data[1], data[4])] = \
                    tmpCntDict.get("{},{}".format(data[1], data[4]), 0) + (int(data[2]) * data[3])

        tmpItemsList = []
        for itemList in tmpCntDict.items():
            tmp = itemList[0].split(",") + [itemList[1]]
            swapIndex = tmp[2]
            tmp[2] = tmp[1]
            tmp[1] = swapIndex
            tmpItemsList.append(tmp)

        tmpItemsList.sort(key= lambda s: s[0])
        nstuList[index] = [["料位號", "總用量", "藥品名稱"]] + tmpItemsList

    return nstuList

def delete_gsheet(sheet_id, gsheet_name_id):
    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = './{}'.format(os.getenv('google_sheet_api_key'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = gsheet_name_id
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # delete sheet json
    new_sheet_name = {
        'requests': [{
            'deleteSheet': {
                'sheetId': sheet_id
            }
        }]
    }
    # delete sheet exe
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=new_sheet_name).execute()

if __name__ == "__main__":
    # version 1.2.0
    load_dotenv()
    recordDate = "20230221"
    separateLevelGroupFinishList, nstuList = drugCntOutput("Batchdata{}.csv".format(recordDate))

    for cnt in range(len(separateLevelGroupFinishList)):
        drugCntUpdateToGsheet("{}".format(recordDate) + "0{}".format(cnt + 1), separateLevelGroupFinishList[cnt])

    for cnt in range(len(nstuList)):
        drugCntUpdateToGsheet("{}".format(recordDate) + "1{}".format(cnt + 1), nstuList[cnt])

    # for cnt in range(6):
    #     delete_gsheet("{}".format(recordDate) + "0{}".format(cnt + 1), os.getenv('drug_cnt_id'))
    #
    # for cnt in range(4):
    #     delete_gsheet("{}".format(recordDate) + "1{}".format(cnt + 1), os.getenv('drug_cnt_id'))
