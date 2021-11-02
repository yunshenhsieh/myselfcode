import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def moon_test_main(filepath) -> [[str]]:
    with open(filepath,'r',encoding='utf-8')as f:
        tmp = f.read()
    # 配合題題數
    match_question_num = 16
    match_question_num = match_question_num - 1

    soup = BeautifulSoup(tmp, 'html.parser')
    # 題目
    question_list = []
    for i in soup.select('div.qtext'):
        question_list.append(i.text.strip())
    # 答案
    ans_list = []
    for i in soup.select('div.rightanswer'):
        ans_list.append(i.text)

    # 排整齊答案用
    for i in range(len(ans_list)):
        ans_list[i] = ans_list[i].replace('\n', ' ')

    # 排整齊配合題用
    ans_list[match_question_num] = ans_list[match_question_num].split(', ')
    ans_list[match_question_num][0] = ans_list[match_question_num][0].replace('：', '：\n')
    for i in range(len(ans_list[match_question_num])):
        ans_list[match_question_num][i] = ans_list[match_question_num][i].strip()
    ans_list[match_question_num] = ',\n'.join(ans_list[match_question_num])

    # 整理成寫入google sheet的格式
    data_finish = []
    for i in range(len(question_list)):
        data_finish.append([str(i + 1) + '、' + question_list[i].replace('\n', ' ')])
        data_finish.append([ans_list[i]])
        data_finish.append([])

    return data_finish

from googleapiclient.discovery import build
from google.oauth2 import service_account

def moon_test_answer_gsheet(sheet_name, filepath):

    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '../{}'.format(os.getenv('py_gsheet_key_filename'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('moon_test_answer_gsheet_id')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    data_finish = moon_test_main(filepath)

    # 工作表新分頁的設定
    new_sheet_name = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'sheetId':sheet_name,
                    'title': str(sheet_name)
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

    
def delete_gsheet(sheet_id, gsheet_name_id):
    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '../{}'.format(os.getenv('py_gsheet_key_filename'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = gsheet_name_id
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # 工作表新分頁的設定
    new_sheet_name = {
        'requests': [{
            'deleteSheet': {
                'sheetId':sheet_id
            }
        }]
    }
    # 建立工作表新分頁
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=new_sheet_name).execute()

if __name__ == "__main__":
    load_dotenv()
    moon_test_answer_gsheet(<sheet id>, filepath)
    gsheet_id = os.getenv('moon_test_answer_gsheet_id')
    delete_gsheet(<sheet id>, gsheet_id)
