import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import collections
from googleapiclient.discovery import build
from google.oauth2 import service_account

def lab_data_transfer(file_path) -> [[str]]:
    with open(file_path,'r',encoding='utf-8')as f:
        tmp = f.read()
        data = tmp.split('\n')

    # 建立生化組、血液組的有序字典
    check_group_dict = collections.OrderedDict()
    # 記錄現在讀取到第幾行用
    row_cnt = 0

    for content in data:
        if '採檢日期' in content:
            check_group_name = content[5:9].strip()
            sample_group_name = content[19:24].strip()
            sample_group_ps = data[row_cnt + 1][6:11].strip()
            check_group = check_group_name + '({}:{})'.format(sample_group_name, sample_group_ps)

            # 如果字典內沒有此群組名，則產生一個lab_data_group類別實體，讓這個群組名的字典指定到這個實體。
            if check_group not in check_group_dict:
                check_group_dict[check_group] = lab_data_group(check_group)
                tmp = check_group_dict[check_group]
            else:
                tmp = check_group_dict[check_group]

            # 使用lab_data_group類別內的方法，加入採檢時間。
            tmp.add_time(content.split('時間:')[-1].strip() + '5')

            row_cnt += 1
            continue

        # 用長度判斷是否為需要的資訊
        if len(content) > 72 and len(content) < 76 :
            data_item = content[:16].strip()
            data_item_unit = content[39:49].strip()
            data_item_value = content[16:39].strip()
            data_key = '{}||{}'.format(data_item, data_item_unit)

            # 如果下一行長度為71的話，表示此行的參考值有部份被截斷到下一行了，在這邊進行處理。
            if len(data[row_cnt + 1]) == 71:
                link_use = data[row_cnt + 1].strip()
                normal_value = content[52:].rstrip() + link_use
            else:
                normal_value = content[52:].strip()

            # 使用lab_data_group類別內的方法，加入檢查項目，單位，數值，參考值。
            tmp.add_check_data(data_key=data_key, data_content=data_item_value, normal_value=normal_value)
            row_cnt += 1
        else:
            row_cnt += 1

    data_to_gsheet = []
    # 把字典內所有的實體資料都取出，整理成可以直接輸出給google試算表的格式
    for k, v in check_group_dict.items():
        data_to_gsheet.append([k])
        data_to_gsheet = data_to_gsheet + v.get_data()

    return data_to_gsheet

class lab_data_group():
    def __init__(self,group_name):
        self.group_name = group_name
        self.check_item_dict = collections.OrderedDict()
        self.check_item_dict['檢驗項目||單位'] = [[],['參考值']]

    def add_time(self, date_time):
        self.check_item_dict['檢驗項目||單位'][0].append(date_time)

    def add_check_data(self, data_key, data_content, normal_value):
        list_len = len(self.check_item_dict['檢驗項目||單位'][0])
        if data_key not in self.check_item_dict.keys():
            self.check_item_dict[data_key] = [[],[]]
            # 後面的產生器是為了要讓現在list的長度，變的跟現在總共有的採檢時間一樣長。
            self.check_item_dict[data_key][0] = self.check_item_dict[data_key][0] + \
                                             ['' for _ in range(list_len - len(self.check_item_dict[data_key][0]))]
            # 因為現在新增的數值，跟時間剛好會對應在list的最後一格
            self.check_item_dict[data_key][0][-1] = data_content
            # 寫入參考值
            self.check_item_dict[data_key][1].append(normal_value)
        else:
            # 後面的產生器是為了要讓現在list的長度，變的跟現在總共有的採檢時間一樣長。
            self.check_item_dict[data_key][0] = self.check_item_dict[data_key][0] + \
                                             ['' for _ in range(list_len - len(self.check_item_dict[data_key][0]))]
            # 因為現在新增的數值，跟時間剛好會對應在list的最後一格
            self.check_item_dict[data_key][0][-1] = data_content

    def get_data(self) -> [[str]]:
        data = []
        list_len = len(self.check_item_dict['檢驗項目||單位'][0])
        for k, v in self.check_item_dict.items():
            """因為有些檢驗不是最後一次都會有檢查，所以最後要處理檢驗值list的長度，
            讓它跟採檢時間list的長度一致，這樣參考值才可以全部在最後一欄時是一樣的column上"""
            if len(v[0]) < list_len:
                v[0] = v[0] + ['' for _ in range(list_len - len(v[0]))]
                k_v = k.split('||') + v[0][::-1] + v[1]
                data.append(k_v)
            else:
                k_v = k.split('||') + v[0][::-1] + v[1]
                data.append(k_v)
        return data

def lab_data_transfer_gsheet(file_path, sheet_name):

    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '../{}'.format(os.getenv('py_gsheet_key_filename'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = os.getenv('lab_data_transfer_gsheet_id')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    lab_data_list = lab_data_transfer(file_path)

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

    SAMPLE_RANGE_NAME = "{}!A{}".format(sheet_name,1)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                        valueInputOption="USER_ENTERED", body={"values": lab_data_list}).execute()

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
    gsheet_id_list = [os.getenv('lab_data_transfer_gsheet_id'), os.getenv('<gsheet name id>')]
   
    # demo = lab_data_transfer('<filepath>')
    # for i in demo:
    #     print(i)

    # lab_data_transfer_gsheet('<filepath>', '<gsheet name>')
    # delete_gsheet(<gsheet id>, gsheet_id_list[0])
