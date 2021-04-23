# Teach video : https://www.youtube.com/watch?v=4ssigWmExak&list=PLxjXsyRHpX_hmj6048cCcMYvq5llD5cKO
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.
SERVICE_ACCOUNT_FILE = '<API key file name>.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID and range of a sample spreadsheet.
# Example : https://docs.google.com/spreadsheets/d/<google sheet ID>/edit#gid=0
SAMPLE_SPREADSHEET_ID = '<google sheet ID>'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
# SAMPLE_RANGE_NAME is work table name(分頁名)
SAMPLE_RANGE_NAME = "sheet1"
sheet = service.spreadsheets()

# Get sheet all info and data
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
print(result)

# Write data into sheet
n = len(result['values']) + 1
while True:
    input_data = input("keyin data : ")
    input_data = [data.strip() for data in input_data.split(',')]
    SAMPLE_RANGE_NAME = "sheet1!A{}".format(n)
    insert_data = [input_data]
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                valueInputOption="USER_ENTERED",body={"values":insert_data}).execute()
