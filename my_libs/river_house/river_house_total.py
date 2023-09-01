import pandas as pd
import os
from datetime import datetime

def delete_duplicates(df_to_change):
    dp = df_to_change[df_to_change.duplicated(subset='id')]
    print("\n\nПовторяющиеся строки : \n {}".format(dp))
    for i in range (len(dp)-1):
        item = dp.iloc[i,0]
        print(int(df_to_change.loc[df_to_change['id'] == item].mean(numeric_only=True)))
        ind = df_to_change[df_to_change['id'] == item].index.values

        print(len(ind))
    df_to_change.drop_duplicates(inplace=True, subset='id', keep='first')
    dp = df_to_change[df_to_change.duplicated(subset='id')]
    print("\n\nПовторяющиеся строки : \n {}".format(dp))
    return df_to_change

def river_house_total():
    # with open(f'data/river_house/total/2023-05-23total.csv', 'w', encoding='UTF-8') as f:
    #     f.close()


    df2 = pd.read_csv(f'data/river_house/total/total2.csv', encoding='utf-8', delimiter=';')
    print(f'НАЗВАНИЯ СТОЛБЦОВ - {df2.columns.values.tolist()[1]}')
    df = pd.read_csv(f'data/river_house/2023-08-30.csv', encoding='utf-8', delimiter=';')


    df = delete_duplicates(df)
    df2 = delete_duplicates(df2)
    print(df.info())
    print(df2.info())
    # df[df.columns.values.tolist()[1]].astype('int64')
    df = df.astype({df.columns.values.tolist()[1]: "Int64"})
    # df2[df2.columns.values.tolist()[1]].astype('int64')
    for i in df2.columns.values.tolist():

        if i == 'id':
            continue
        df2 = df2.astype({i: "Int64"})
    df3 = df.merge(df2, how='outer')
    # print(df2.iloc[ind[0]].values)
    # print(df2.iloc[ind[1]].values)
    df3[df3.columns.values.tolist()[-1]].astype('int64', errors='ignore')
    print(df3.info())
    df3.to_csv(f'data/river_house/total/total2.csv', encoding='utf-8', sep=';',index=False)
    df3.to_csv(f'data/river_house/total/{datetime.today().date()}-total.csv', encoding='utf-8', sep=';', index=False)

if __name__ == "__main__":
    os.chdir('..')
    river_house_total()

