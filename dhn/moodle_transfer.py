def moon_test_answer_txt(filepath):
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
    ans_list[match_question_num] = ans_list[match_question_num].split(',')
    ans_list[match_question_num][0] = ans_list[match_question_num][0].replace('：', '：\n')
    for i in range(len(ans_list[match_question_num])):
        ans_list[match_question_num][i] = ans_list[match_question_num][i].strip()
    ans_list[match_question_num] = ',\n'.join(ans_list[match_question_num])

    with open('./moodle_ans.txt','w',encoding='utf-8')as w:
        for i in range(len(question_list)):
            w.write(str(i + 1) + '、' + question_list[i].replace('\n', ' ') + '\n')
            w.write(ans_list[i] + '\n' + '\n')

            
# Teach video : https://www.youtube.com/watch?v=4ssigWmExak&list=PLxjXsyRHpX_hmj6048cCcMYvq5llD5cKO
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google.oauth2 import service_account

def moon_test_answer_gsheet(sheet_name, filepath):

    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '<API key file name>.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = '<google sheet ID>'
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    with open(filepath,'r',encoding='utf-8')as f:
        tmp = f.read()
    # 配合題題號
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
    ans_list[match_question_num] = ans_list[match_question_num].split(',')
    ans_list[match_question_num][0] = ans_list[match_question_num][0].replace('：', '：\n')
    for i in range(len(ans_list[match_question_num])):
        ans_list[match_question_num][i] = ans_list[match_question_num][i].strip()
    ans_list[match_question_num] = ',\n'.join(ans_list[match_question_num])

    # 工作表新分頁的設定
    new_sheet_name = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
    }
    # 建立工作表新分頁
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=new_sheet_name).execute()

    data_finish = []
    for i in range(len(question_list)):
        data_finish.append([str(i + 1) + '、' + question_list[i].replace('\n', ' ')])
        data_finish.append([ans_list[i]])
        data_finish.append([])

    SAMPLE_RANGE_NAME = "{}!A{}".format(sheet_name, 1)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                        valueInputOption="USER_ENTERED", body={"values": data_finish}).execute()


if __name__ == "__main__":
    moon_test_answer_gsheet('202108')
