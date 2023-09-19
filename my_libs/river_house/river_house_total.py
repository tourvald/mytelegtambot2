import platform

import pandas as pd
import os
from datetime import datetime
import platform
# Определяем в какой системе мы находимся и задаем параметр для спуска в корневую дирректорию
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	chdir_path = '../..'
else:
	chdir_path = '../..'
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
    df = pd.read_csv(f'data/river_house/{datetime.today().date()}.csv', encoding='utf-8', delimiter=';')


    df = delete_duplicates(df).dropna()
    df2 = delete_duplicates(df2).dropna()
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

def river_house_total_2():

    filename = datetime.today().date()
    filepath = f'data/river_house/backups/{filename}-total.xlsx'
    # Читаем файл ДБ, делаем бекап с датой, удаляем nan, присваиваем значения int
    df = pd.read_excel('data/river_house/total/total.xlsx', engine='openpyxl')
    df = df.fillna('0')
    print(df.head(400))
    for i in list(df)[2:]:
        if i == 'id':
            continue
        df[i] = df[i].astype(int)

#     Читаем новый файл дб спарешные сегодня
    filepath = f'data/river_house/{filename}.csv'
    df2 = pd.read_csv(filepath, encoding='utf-8', sep=';')
    print(df2.head(400))

    df3 = df.merge(df2, how='outer')
    df3 = df3.fillna('0')
    print(list(df3))
    for i in list(df3)[1:]:
        if i == 'id':
            continue
        df3[i] = df3[i].astype(int)
    print(df3.head(400))
    call_to_replace_name = list(df2)[1]
    coll_to_replace = df3[call_to_replace_name]
    df3 = df3.drop(call_to_replace_name, axis=1)
    df3.insert(1, call_to_replace_name, coll_to_replace)

    filepath = f'data/river_house/backups/{filename}-total.xlsx'
    df3.to_excel(filepath, engine='openpyxl', index=False)
    filepath = f'data/river_house/total/total.xlsx'
    df3.to_excel(filepath, engine='openpyxl', index=False)

def separatate_first_column():
    df = pd.read_excel('data/river_house/total/total.xlsx', engine='openpyxl')
    df = df.fillna('0')
    print(df.head(400))
    for i in list(df)[2:]:
        if i == 'id':
            continue
        df[i] = df[i].astype(int)

    new_df = df['id'].str.split('-', expand=True)
    df = pd.concat([new_df, df], axis=1)
    df = df.astype(str)
    df = df.rename(columns={0: 'комнатность', 1:'метраж', 2:'этаж'})
    print(df.head())
    filename = datetime.today().date()
    df.to_excel(f'data/river_house/total/total-{filename}.xlsx', engine='openpyxl', index=False)


if __name__ == "__main__":

    os.chdir(chdir_path)
    # print(os.getcwd())
    # river_house_total_2()
    separatate_first_column()

