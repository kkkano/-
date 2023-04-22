import pandas as pd



df = pd.read_csv('数据2.csv',encoding='utf-8')
df.head()
df.describe()
df.isnull().sum()
df['朝向'].unique()