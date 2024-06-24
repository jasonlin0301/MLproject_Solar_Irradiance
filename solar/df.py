import json
import pandas as pd

# 读取现有的JSON文件
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\solar\solar.json'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
except FileNotFoundError:
    print(f"找不到文件: {file_path}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"解析JSON時發生錯誤: {e}")
    exit(1)

# 提取需要的键值对
filtered_data = []
for entry in data:
    filtered_entry = {
        '站名': entry.get('站名'),
        '年份': entry.get('年份'),
        '月份': entry.get('月份'),
        '總日照時數h': entry.get('總日照時數h'),
        '總日射量MJ/ m2': entry.get('總日射量MJ/ m2')
    }
    filtered_data.append(filtered_entry)

# 转换为DataFrame
df = pd.DataFrame(filtered_data)

# 打印DataFrame的所有列
print("DataFrame的所有列:")
print(df.columns)

# 检查是否有空值
missing_values = df.isnull().sum()
print("缺失值檢查結果:")
print(missing_values)

# 將'總日照時數h' 和 '總日射量MJ/ m2' 列转换为数值类型
df['總日照時數h'] = pd.to_numeric(df['總日照時數h'], errors='coerce')
df['總日射量MJ/ m2'] = pd.to_numeric(df['總日射量MJ/ m2'], errors='coerce')

# 检查是否有错误值（这里假设错误值为负值）
errors = (df['總日照時數h'] < 0) | (df['總日射量MJ/ m2'] < 0)
error_count = errors.sum()
print(f"错误值的数量: {error_count}")
