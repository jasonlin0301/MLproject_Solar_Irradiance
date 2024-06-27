import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn.linear_model import LinearRegression
import numpy as np

# 設定中文字體路徑
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

# 提取日射量並確保其為數值類型
df['總日射量MJ/ m2'] = pd.to_numeric(df['總日射量MJ/ m2'], errors='coerce')
df.dropna(subset=['總日射量MJ/ m2'], inplace=True)

# 提取年份和日射量數據
df['年份'] = df.index.year
annual_radiation = df.groupby('年份')['總日射量MJ/ m2'].mean().reset_index()

# 準備數據進行線性回歸
X = annual_radiation['年份'].values.reshape(-1, 1)
y = annual_radiation['總日射量MJ/ m2'].values

# 擬合線性回歸模型
model = LinearRegression()
model.fit(X, y)

# 預測未來10年的日射量
future_years = np.arange(X[-1, 0] + 1, X[-1, 0] + 11).reshape(-1, 1)
future_radiation = model.predict(future_years)

# 繪製結果
plt.figure(figsize=(10, 6))
plt.plot(annual_radiation['年份'], annual_radiation['總日射量MJ/ m2'], label='實際年均總日射量', marker='o')
plt.plot(annual_radiation['年份'], model.predict(X), label='擬合線性回歸', linestyle='--')
plt.plot(future_years, future_radiation, label='預測年均總日射量', linestyle='--', marker='o')
plt.xlabel('年份', fontproperties=font_prop)
plt.ylabel('總日射量MJ/m²', fontproperties=font_prop)
plt.title('年均總日射量趨勢預測', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True)
plt.show()

# 打印預測結果
print("未來10年預測的年均總日射量：")
for year, radiation in zip(future_years.flatten(), future_radiation):
    print(f"{year}年: {radiation:.2f} MJ/m²")
