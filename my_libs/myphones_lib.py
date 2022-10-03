import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import unidecode
from datetime import datetime
from my_libs.libs_google_sheets import get_myphones_spreadsheet
# def get_myphones_spreadsheet():
#     CREDENTIALS_FILE = 'settings/api_google_sheets_token.json'
#     spreadsheet_id = '1nJHlfoRuqu3boqb7Bf3ymI-NRdV0kIkzE80PqI5igVg'
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(
#         CREDENTIALS_FILE,
#         ['https://www.googleapis.com/auth/spreadsheets',
#          'https://www.googleapis.com/auth/drive'])
#     httpAuth = credentials.authorize(httplib2.Http())
#     service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
#     values = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheet_id,
#         range='mysells',
#         majorDimension='ROWS',
#     ).execute()
#     return values


def get_month_by_number(number):
    months = ['Январь', 'Февраль',"Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
          "Декабрь"]
    month = months[number - 1]
    return month


def remove_symbols(values):
    new_values = []
    for value in values['values']:
        if len(value) > 3:
            new_value = []
            new_value.append(value[0])
            new_value.append(value[1])
            new_value.append(unidecode.unidecode(value[2]).replace(' ', '').replace('R', '').strip())
            new_value.append(value[3])
            new_value.append(unidecode.unidecode(value[4]).replace(' ', '').replace('R', '').strip())
            new_values.append(new_value)
    return new_values


def get_values_by_month(year, month, values):
    values_by_month = []
    for value in values:
        if value[3]:
            if f"{value[3].split('.')[1]}.{value[3].split('.')[2]}" == f'{month}.{year}':
                values_by_month.append(value)
    return values_by_month


def get_month_profit(month, year, values):
    profit = 0
    values_by_month = get_values_by_month(month, year, values)
    for value in values_by_month:
        profit = profit + int(value[4])-int(value[2])
    return profit


def year_profit(year, values):
    profit = 0
    for i in range (1, 12):
        profit = profit + get_month_profit(year, i, values)
    return profit


def get_my_items(values):
    my_items = []
    for value in values:
        if not value[3]:
            my_items.append(value)
    return my_items


def get_month_report(year, month, values):
    values_buy_month = get_values_by_month(year, month, values)
    report = []
    report.append("_____________")
    report.append(get_month_by_number(month))
    report.append(f'Количество продаж : {len(values_buy_month)}')
    report.append(f'Прибыль : {get_month_profit(year, month, values)}')
    report.append(f'Прибыль с одной продажи:{get_month_profit(year, month, values)//len(values_buy_month)}')
    return report

def get_current_month():
    current_month = datetime.today().month
    return current_month

def get_current_year():
    current_year = datetime.today().year
    return current_year

def get_current_month_report(values):
    current_month = get_current_month()
    current_year = get_current_year()
    get_month_report(current_year, current_month, values)

def get_last_3_months_report():
    values = get_myphones_spreadsheet()
    values = remove_symbols(values)
    current_month = get_current_month()
    current_year = get_current_year()

    if current_month == 1:
        months = [11,12,1]
        years = [current_year-1,current_year-1,current_year]
    elif current_month == 2:
        months = [12, 1, 2]
        years = [current_year - 1, current_year, current_year]
    else:
        months = [current_month-2, current_month-1, current_month]
        years = [current_year, current_year, current_year]
    reports = []
    for month, year in zip(months, years):
        reports.append(get_month_report(year, month, values))
    return reports

# for report in reports:
#     print (report)
# values = get_myphones_spreadsheet()
# for value in values['values']:
#     if len(value) > 3:
#         print(value)/myphones_price