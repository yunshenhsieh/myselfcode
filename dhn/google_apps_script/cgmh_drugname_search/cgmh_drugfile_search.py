from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

def cgmhDrugfileGsheet(drugFilePath: str, LocationFilePath: list):

    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = './{}'.format(os.getenv('google_sheet_api_key'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('drugfile_sheet_id')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    data_finish = drugFileClean(drugFilePath, LocationFilePath)
    col_header = data_finish[0]
    data_finish = data_finish[1:]

    # 寫入colnum到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format("drugfile", 1)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": [col_header]}).execute()

    # 寫入資料到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format("drugfile", 14)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": data_finish}).execute()
    pass

def locationFileClean(filePath: str) -> dict:
    with open(filePath, "r", encoding="big5")as f:
        tmp = f.readlines()
    for n, content in enumerate(tmp):
        tmp[n] = content.split("\t")
    result = {}
    for content in tmp[1:]:
        result[content[0]] = content[-2]
    return result

def drugFileClean(drugFilePath: str, LocationFilePath: list) -> [[str]]:
    with open(drugFilePath, "r", encoding="utf-8")as f:
        drugFile = f.readlines()
    PBDrugLocationDict = locationFileClean(LocationFilePath[0])
    PPDrugLocationDict = locationFileClean(LocationFilePath[1])
    PADrugLocationDict = locationFileClean(LocationFilePath[2])
    MYEDrugLocationDict = locationFileClean(LocationFilePath[3])
    PKDrugLocationDict = locationFileClean(LocationFilePath[4])

    columnItem = drugFile[0].split(";")
    columnItem = [columnItem[0], columnItem[1], columnItem[2], columnItem[12], columnItem[60], "PB", "PP", "PA", "MYE", "PK"]
    result = [columnItem]
    for content in drugFile[1:]:
        content = content.split(";")
        if len(content) != 117:
            continue
        else:
            if content[12]:
                result.append([content[0], content[1], content[2], content[12], content[60],
                               PBDrugLocationDict.get(content[0], ""),
                               PPDrugLocationDict.get(content[0], ""),
                               PADrugLocationDict.get(content[0], ""),
                               MYEDrugLocationDict.get(content[0], ""),
                               PKDrugLocationDict.get(content[0], "")])
    updateTime = ["更新時間",
                  "Drug檔更新日：{}".format("2025-06-18 10:48"),
                  "PB定位更新日：{}".format("2024-05-05 14:49"),
                  "PP定位更新日：{}".format("2024-05-05 14:49"),
                  "PA定位更新日：{}".format("2024-05-05 14:49"),
                  "MYE定位更新日：{}".format("2024-05-05 14:49"),
                  "PK定位更新日：{}".format("2024-05-05 14:49"),
                  "Web Version：{}".format("2.1.0"),
                  "Backend Version：{}".format("1.7.4")]
    result.append(updateTime)

    return result

if __name__ == "__main__":
    # version 1.7.4
    load_dotenv()
    LocationFilePath = ["D:/PyCharmProjection/allprojection/cgmh/data/pb_location.txt",
                        "D:/PyCharmProjection/allprojection/cgmh/data/pp_location.txt",
                        "D:/PyCharmProjection/allprojection/cgmh/data/pa_location.txt",
                        "D:/PyCharmProjection/allprojection/cgmh/data/mye_location.txt",
                        "D:/PyCharmProjection/allprojection/cgmh/data/pk_location.txt", ]

    cgmhDrugfileGsheet("./data/Adgn.txt", LocationFilePath)
