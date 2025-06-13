import pandas as pd
import os
import pandas as pd
import datetime
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from avito_parcer_script import mycars_get_avarage_prices



def daily_mean():
    df = pd.read_csv('data/mycars/mycars.csv', encoding='utf-8', delimiter=',')
    return_ = date_mean = df.groupby('date').mean()['total'].astype(int)
    date_mean.to_frame().to_csv('data/mycars/mycarsreport.csv', encoding='utf-8', sep=',')
    date_mean.to_frame().to_csv('data/mycars/mycarsreport.csv', encoding='utf-8', sep=',', delimiter=';')
    return return_

def convert_old_db():
    df = pd.read_csv('data/mycars/mycars.csv', encoding='utf-8', sep=';')
    print(df.head())
    # df = df.sort_index(ascending=True)
    # df.to_csv(f'data/mycars/mycars2.csv', encoding='utf-8', sep=';', index=False)
    # print(df.head())

# if __name__ == "__main__":
