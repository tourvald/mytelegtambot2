import pandas as pd
import os
def daily_mean():
    df = pd.read_csv('data/mycars/mycars.csv', encoding='utf-8', delimiter=';'))
    return_ = date_mean = df.groupby('date').mean()['total'].astype(int)
    date_mean.to_frame().to_csv('data/mycars/mycarsreport.csv', encoding='utf-8', sep=',')
    date_mean.to_frame().to_csv('data/mycars/mycarsreport.csv', encoding='utf-8', sep=',', delimiter=';'))
    return return_
if __name__ == "__main__":
    os.chdir('..')
    print(daily_mean())