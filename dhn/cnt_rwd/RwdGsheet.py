from googleapiclient.discovery import build
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SERVICE_ACCOUNT_FILE = '<API key file name>.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID and range of a sample spreadsheet.
# Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
SAMPLE_SPREADSHEET_ID = '<google sheet ID>'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def updateDataToGsheet(data, sheet_name, rowCnt):
    row_data = {
        'values': [data]
    }

    SAMPLE_RANGE_NAME = "{}!A{}".format(sheet_name, rowCnt)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body=row_data).execute()

def createGsheet(sheet_name):
    # 工作表新分頁的設定
    new_sheet_name = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_name,
                    'index': 0,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                }
            }
        }]
    }

    # 建立工作表新分頁
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=new_sheet_name).execute()

    header = {
        'values': [['料位號', '總合', '算式', '算式加總', '自行輸入', '自行輸入加總', '姓名', '時間']]
    }

    SAMPLE_RANGE_NAME = "{}!A{}".format(sheet_name, 1)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body=header).execute()

def getRowCnt(sheet_name):
    SAMPLE_RANGE_NAME = sheet_name
    rwdCnt = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                 range=SAMPLE_RANGE_NAME).execute()
    return rwdCnt
