import json
import pandas as pd

# 读取现有的JSON文件和包含站名与行政区信息的CSV文件
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\solar\solar.json'
stations_districts_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\District\stations_districts.csv'

# 读取JSON数据
with open(file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

# 转换为DataFrame
df = pd.DataFrame(data)

# 读取包含站名和行政区信息的CSV文件
stations_districts_df = pd.read_csv(stations_districts_path)

# 合并两个DataFrame，基于'站名'列
df = df.merge(stations_districts_df, on='站名', how='left')

# 检查合并结果
print("合并后的DataFrame:")
print(df.head())

# 保存为新的CSV文件
output_csv_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\solar\solar_with_districts.csv'
df.to_csv(output_csv_path, index=False)

# 保存为新的JSON文件
output_json_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\solar\solar_with_districts.json'
df.to_json(output_json_path, orient='records', lines=True, force_ascii=False)

print("数据已成功保存为CSV和JSON文件。")
