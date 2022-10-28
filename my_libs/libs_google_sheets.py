from pprint import pprint
import os
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


import os

def get_mysells_spreadsheet():
    CREDENTIALS_FILE = 'settings/api_google_sheets_token.json'
    spreadsheet_id = '1nJHlfoRuqu3boqb7Bf3ymI-NRdV0kIkzE80PqI5igVg'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:E20',
        majorDimension='ROWS'
    ).execute()
    return values
def get_myphones_spreadsheet(range='myphones'):
    CREDENTIALS_FILE = 'settings/api_google_sheets_token.json'
    spreadsheet_id = '1nJHlfoRuqu3boqb7Bf3ymI-NRdV0kIkzE80PqI5igVg'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension='ROWS',
    ).execute()
    print(values)
    return values
# os.chdir('..')
# values = get_myphones_spreadsheet(range='mycars')
# print(values)