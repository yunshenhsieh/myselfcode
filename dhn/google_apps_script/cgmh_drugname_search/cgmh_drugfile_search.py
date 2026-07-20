from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os, charset_normalizer
import pandas as pd

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

    deletePreviousData(sheet, SAMPLE_SPREADSHEET_ID)

    data_finish = drugFileClean(drugFilePath, LocationFilePath)
    col_header = data_finish[0]
    data_finish = data_finish[1:]
    print(len(data_finish))

    # 寫入colnum到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format("< sheet name >", < start row number >)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": [col_header]}).execute()

    # 寫入資料到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format("< sheet name >", < start row number >)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": data_finish}).execute()
    pass

def deletePreviousData(sheet, SAMPLE_SPREADSHEET_ID: str):
    SAMPLE_RANGE_NAME = "{}!A:A".format("< sheet name >")
    result =sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # 取得最大 row 數（有資料的列數）
    max_row = len(values)
    # 要清除的範圍
    range_to_clear = "{}!A14:Z{}".format("< sheet name >", max_row)
    # 執行清除
    sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_clear, body={}).execute()
    pass

def detectTxtEncoding(filePath: str) -> str:
    result = charset_normalizer.from_path(filePath)
    txtEncoding = result.best()
    if txtEncoding is None:
        txtEncoding = 'big5'
    else:
        txtEncoding = txtEncoding.encoding
    return txtEncoding

def locationFileClean(filePath: str) -> dict:
    txtEncoding = detectTxtEncoding(filePath)
    with open(filePath, "r", encoding=txtEncoding)as f:
        tmp = f.readlines()
    for n, content in enumerate(tmp):
        tmp[n] = content.split("\t")
    result = {}
    for content in tmp[1:]:
        result[content[0]] = content[-2]
    return result

def drugFileClean(drugFilePath: str, LocationFilePath: list) -> [[str]]:

    df = pd.read_excel(drugFilePath).fillna('')
    header = df.columns.tolist()
    rows = df.values.tolist()
    columnItem =  header + ["PB", "PP", "PA", "MYE", "PK"]

    PBDrugLocationDict = locationFileClean(LocationFilePath[0])
    PPDrugLocationDict = locationFileClean(LocationFilePath[1])
    PADrugLocationDict = locationFileClean(LocationFilePath[2])
    MYEDrugLocationDict = locationFileClean(LocationFilePath[3])
    PKDrugLocationDict = locationFileClean(LocationFilePath[4])


    result = [columnItem]
    for content in rows:
        if len(content) < 10:
            content = content + ['' for x in range(10)]

        if ("臨床試驗" not in str(content[1])):
            result.append([content[0], content[1], content[2], '\'' + content[3], content[4],
                           PBDrugLocationDict.get(content[0], ""),
                           PPDrugLocationDict.get(content[0], ""),
                           PADrugLocationDict.get(content[0], ""),
                           MYEDrugLocationDict.get(content[0], ""),
                           PKDrugLocationDict.get(content[0], "")])

    updateTime = ["更新時間",
                  "Drug檔更新日：{}".format("< Update time >"),
                  "PB定位更新日：{}".format("< Update time >"),
                  "PP定位更新日：{}".format("< Update time >"),
                  "PA定位更新日：{}".format("< Update time >"),
                  "MYE定位更新日：{}".format("< Update time >"),
                  "PK定位更新日：{}".format("< Update time >"),                
                  "Web Version：{}".format("< Version number >"),
                  "Backend Version：{}".format("< Version number >")]
    result.append(updateTime)

    return result

if __name__ == "__main__":
    # version 2.2.0
    load_dotenv()
    LocationFilePath = ["< PB location filepath >",
                        "< PP location filepath >",
                        "< PA location filepath >",
                        "< MYE location filepath >",
                        "< PK location filepath >"]

    cgmhDrugfileGsheet("< drugfile filepath >", LocationFilePath)
