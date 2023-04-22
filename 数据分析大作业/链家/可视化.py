import pandas as pd
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
from pyecharts import options as opts

df = pd.read_csv('二手房多页.csv', encoding='utf-8')
df.head
df.describe()
df.isnull().sum()
df['是否有电梯'].unique()
