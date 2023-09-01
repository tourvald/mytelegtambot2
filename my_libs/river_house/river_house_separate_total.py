import pandas as pd
import os
from datetime import datetime

def river_house_separate_total():
    os.chdir('../..')
    print(os.getcwd())
    df = pd.read_csv(f'data/river_house/total/total2.csv', encoding='utf-8', delimiter=';')
    for i in df.columns.values.tolist():
        if i == 'id':
            continue
        df = df.astype({i: "Int64"})

    print(df.info)

    new_df = df['id'].str.split('-', expand=True)
    new_df[new_df.columns.values.tolist()[-1]].astype('int64', errors='ignore')

    df3 = pd.concat([new_df,df],axis=1)

    for i in df3.columns.values.tolist():
        if i == 'id' or '1':
            continue
        df3 = df3.astype({i: "Int64"})

    df3.to_csv(f'data/river_house/total/{datetime.today().date()}-total_separated.csv', encoding='utf-8', sep=';', index=False)

    print (df3.info)


if __name__ == "__main__":
    # os.chdir('..')
    # path = f'data/river_house/total/total2.csv'
    river_house_separate_total()