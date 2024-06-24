import json
import pandas as pd

# 读取现有的JSON文件
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\weather_data.json'

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

# 保存为新的JSON文件
output_json_path = 'solar.json'
with open(output_json_path, 'w', encoding='utf-8') as file:
    for entry in filtered_data:
        json.dump(entry, file, ensure_ascii=False)
        file.write('\n')

# 转换为DataFrame并保存为CSV文件
df = pd.DataFrame(filtered_data)
output_csv_path = 'solar.csv'
df.to_csv(output_csv_path, index=False)

print(f"數據已儲存為 {output_json_path} 和 {output_csv_path}")
