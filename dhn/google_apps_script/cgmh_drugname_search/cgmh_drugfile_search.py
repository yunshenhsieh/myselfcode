from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

def cgmhDrugfileGsheet(drugFilePath, PBLocationFilePath, PPLocationFilePath):

    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '../{}'.format(os.getenv('py_gsheet_key_filename'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('< gsheet ID >')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    data_finish = drugFileClean(drugFilePath, PBLocationFilePath, PPLocationFilePath)[1:]

    # 寫入資料到google sheet
    SAMPLE_RANGE_NAME = "{}!A{}".format("< sheet name >", < start row number >)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body={"values": data_finish}).execute()


def locationFileClean(filePath) -> dict:
    with open(filePath, "r", encoding="big5")as f:
        tmp = f.readlines()
    for n, content in enumerate(tmp):
        tmp[n] = content.split("\t")
    result = {}
    for content in tmp[1:]:
        result[content[0]] = content[-2]
    return result

def drugFileClean(drugFilePath, PBLocationFilePath, PPLocationFilePath) -> [[str]]:
    with open(drugFilePath, "r", encoding="big5-hkscs")as f:
        drugFile = f.readlines()
    PBDrugLocationDict = locationFileClean(PBLocationFilePath)
    PPDrugLocationDict = locationFileClean(PPLocationFilePath)
    columnItem = drugFile[0].split(";")
    columnItem = [columnItem[0], columnItem[1], columnItem[2], columnItem[12], columnItem[57], "PB", "PP"]
    result = [columnItem]
    for content in drugFile[1:]:
        content = content.split(";")
        if content[12]:
            result.append([content[0], content[1], content[2], content[12], content[57],
                           PBDrugLocationDict.get(content[0], ""), PPDrugLocationDict.get(content[0], "")])
    updateTime = ["更新時間",
                  "Drug檔更新日：{}".format("< Update time >"),
                  "PB定位更新日：{}".format("< Update time >"),
                  "PP定位更新日：{}".format("< Update time >"),
                  "Version：{}".format("< Version number >")]
    result.append(updateTime)

    return result

if __name__ == "__main__":
    load_dotenv()
    cgmhDrugfileGsheet("< drugfile filepath >", "< PB location filepath >", "< PP location filepath >")
