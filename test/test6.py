import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 定义年份范围
start_year = 1999
end_year = 2023

# 加载合并后的数据
file_path = r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2023.csv'
data = pd.read_csv(file_path)

# 将相关列转换为数值类型
data['平均氣溫'] = pd.to_numeric(data['平均氣溫'], errors='coerce')

# 过滤出新北市的数据
new_taipei_data = data[data['行政區'] == '新北市']

# 按年份分组数据
grouped_data = new_taipei_data.groupby('Year')

# 设置中文字体
font_path = r'D:\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_prop = font_manager.FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()

# 新北市平均温度折线图
plt.figure(figsize=(12, 6))
yearly_data = grouped_data['平均氣溫'].mean()
plt.plot(yearly_data.index, yearly_data.values, marker='o', label='新北市')

plt.title('新北市平均溫度', fontproperties=font_prop)
plt.xlabel('年份', fontproperties=font_prop)
plt.ylabel('平均溫度 (°C)', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True)
plt.xticks(range(start_year, end_year + 1, 1))  # 确保X轴显示从1999到2023年
plt.show()
