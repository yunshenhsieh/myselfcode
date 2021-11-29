def setBackgroundColor_gsheet(gsheet_name_id):
    # If modifying these scopes, delete the file token.json.
    SERVICE_ACCOUNT_FILE = '../{}'.format(os.getenv('py_gsheet_key_filename'))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    # Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
    SAMPLE_SPREADSHEET_ID = gsheet_name_id
    service = build('sheets', 'v4', credentials=creds)

    # body = {
    #     "requests": [
    #         {
    #             'addSheet': {
    #                 'properties': {
    #                     'sheetId': 200,
    #                     'title': str(200),
    #                     'index': 0
    #                 }
    #             }
    #         }
    #   ]
    # }
    # service.spreadsheets().batchUpdate(
    #     spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

    body = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 200,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 6
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                # "red": 1.0,
                                # "green": 0.8549,
                                # "blue": 0.72549
                                "red": 1.0,
                                "green": 0.62745,
                                "blue": 0.47843
                                # "red": 255/255,
                                # "green": 255/255,
                                # "blue": 255/255
                            },
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor)"
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

    row_data = {'values' : [['1+1']]}
    SAMPLE_RANGE_NAME = "{}!A{}".format(200, 1)
    service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                          valueInputOption="USER_ENTERED", body=row_data).execute()
