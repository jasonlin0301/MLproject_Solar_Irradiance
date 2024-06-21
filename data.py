import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# 定義資料下載範圍
start_year = 1999
end_year = 2024
end_month = 5

# 創建空的DataFrame來存儲所有資料
all_data = pd.DataFrame()

# 迭代年份和月份，下載資料
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 跳過2024年6月及之後的月份
        if year == 2024 and month > end_month:
            break
        
        # 構建URL，假設URL格式如下（實際情況可能不同）
        url = f"https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html?year={year}&month={month}"
        
        # 發送HTTP請求並獲取回應
        response = requests.get(url)
        
        # 檢查請求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 解析表格資料，假設資料在table標籤中
            table = soup.find('table')
            
            # 將HTML表格轉換為DataFrame
            if table:
                df = pd.read_html(str(table))[0]
                
                # 添加年月信息
                df['Year'] = year
                df['Month'] = month
                
                # 合併到所有資料的DataFrame中
                all_data = pd.concat([all_data, df], ignore_index=True)

# 保存為CSV和JSON格式
csv_filename = 'weather_data.csv'
json_filename = 'weather_data.json'

all_data.to_csv(csv_filename, index=False)
all_data.to_json(json_filename, orient='records', lines=True)

print(f"資料已保存為 {csv_filename} 和 {json_filename}")
