import pandas as pd

# 使用原始字符串以避免路徑問題(路徑請自行修改)
file_path = r'C:\Users\user\Documents\GitHub\jasonlin0301_window\專題\weather_data.csv'

# 讀取 CSV 文件
weather_data = pd.read_csv(file_path)

# 提取站名列並刪除重複的站名
station_names = weather_data[['站名']].drop_duplicates()

# 保存到新的 CSV 文件
output_path = r'C:\Users\user\Documents\GitHub\jasonlin0301_window\專題\station_names.csv'
station_names.to_csv(output_path, index=False)

print(f"站名已保存到 {output_path}")
