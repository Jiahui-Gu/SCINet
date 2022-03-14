import pandas as pd

def weather_process(path = 'datasets/origin-data/weather/', file_name = '2017'):
    # 读取数据
    df = pd.read_csv(path+file_name+'.csv',skiprows=2)

    # 数据处理
    df = df.drop(df[df["Minute"] != 0].index).reset_index() # 只取分钟为0的数据
    use_col = ['Temperature', 'Wind Speed', 'Relative Humidity',  'DHI', 'DNI', 'Dew Point', 'Pressure'] # [温度, 风速, 湿度, 太阳水平辐, 太阳垂直辐射, 露点, 大气压]
    df = df.loc[:, use_col] # 只要特定的列

    # 输出数据
    return df

def load_process(path = 'datasets/origin-data/load/', file_name = '2017'):
    # 读取数据
    df = pd.read_csv(path+file_name+'.csv')

    # 数据处理
    df['date'] = df['Year'].map(str) + '/' + df['Month'].map(str) + '/' + df['Day'].map(str) + ' ' + df['Hour'].map(str) + ':00:00'
    df['date'] = pd.to_datetime(df['date'],format="%Y/%m/%d %H:%M:%S")
    df['KW'] /= 1000
    use_col = ['date', 'KW', 'HTmmBTU', 'CHWTON'] # [日期, 电负荷, 热负荷, 冷负荷]
    df = df.loc[:, use_col] # 只要特定的列

    # 输出数据
    return df

# if __name__ == '__main__':
#     file_names = ['2017', '2018', '2019', '2020']
#     weather_df = weather_process()
#     load_df = load_process()
#     df = pd.concat([load_df,weather_df], axis=1)
#     print(df)

if __name__ == '__main__':
    file_names = ['2017', '2018', '2019', '2020']
    dfs = []
    for file_name in file_names:
        weather_df = weather_process(file_name=file_name)
        load_df = load_process(file_name=file_name)
        df = pd.concat([load_df,weather_df], axis=1)
        dfs.append(df)
        df.columns = ['date', 'EL', 'HL', 'CL', 'T', 'WS', 'RH', 'DHI', 'DNI', 'DP', 'P'] # [日期, 电负荷, 热负荷, 冷负荷, 温度, 风速, 湿度, 太阳水平辐, 太阳垂直辐射, 露点, 大气压]
        df.to_csv('datasets/load-data/' + file_name + '.csv', index=None)
    small_df = dfs[0][0:31*24]
    small_df.to_csv('datasets/load-data/loadS.csv', index=None)
    total_df = pd.concat(dfs)
    total_df.to_csv('datasets/load-data/loadT.csv', index=None)