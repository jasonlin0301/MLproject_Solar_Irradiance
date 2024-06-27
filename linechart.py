import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 設定字體路徑
font_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_prop = FontProperties(fname=font_path)

# 設定全域字體
plt.rcParams['font.sans-serif'] = ['ChocolateClassicalSans-Regular']
plt.rcParams['axes.unicode_minus'] = False

# 讀取現有的JSON文件
file_path_json = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\solar\solar_with_districts.json'

# 讀取JSON數據
with open(file_path_json, 'r', encoding='utf-8') as file:
    data_json = [json.loads(line) for line in file]

# 將JSON數據轉換為DataFrame
df = pd.DataFrame(data_json)

# 將'年份'和'月份'列轉換為datetime格式
df['日期'] = pd.to_datetime(df['年份'].astype(str) + '-' + df['月份'].astype(str) + '-01')

# 設置日期為索引
df.set_index('日期', inplace=True)

# 提取日照時間並確保其為數值類型
df['總日照時數h'] = pd.to_numeric(df['總日照時數h'], errors='coerce')
df.dropna(subset=['總日照時數h'], inplace=True)

# 按區域分組繪製折線圖
regions = df['行政區'].unique()
plt.figure(figsize=(14, 10))

for region in regions:
    region_data = df[df['行政區'] == region]
    plt.plot(region_data.index, region_data['總日照時數h'], label=region)

# 設置圖表標題和標籤
plt.xlabel('時間', fontproperties=font_prop)
plt.ylabel('總日照時數h', fontproperties=font_prop)
plt.title('不同區域的總日照時數趨勢', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True)
plt.tight_layout()

# 顯示圖表
plt.show()
