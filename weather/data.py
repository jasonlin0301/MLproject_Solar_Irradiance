import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 設定Chrome選項
chrome_options = Options()
chrome_options.add_argument("--headless")  # 不顯示瀏覽器

# 使用webdriver-manager安裝和管理ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定義數據下載範圍
start_year = 1999
end_year = 2024
end_month = 5

# 建立一個DataFrame来保存所有資料
all_data = pd.DataFrame()

# 循環年份和月份，下載並保存表格資料
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 跳過2024年6月及其後月份
        if year == 2024 and month > end_month:
            break
        
        # 設定下載URL
        url = f"https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html?year={year}&month={month}"
        
        # 使用Selenium開啟網頁
        driver.get(url)
        
        try:
            # 等待表格loading
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # get HTML表格
            table_html = table.get_attribute('outerHTML')
            
            # 將HTML表格轉換為DataFrame
            df = pd.read_html(table_html)[0]
            
            # 增加年月
            df['Year'] = year
            df['Month'] = month
            
            # 合併到所有數據的DataFrame中
            all_data = pd.concat([all_data, df], ignore_index=True)
        
        except Exception as e:
            print(f"Failed to retrieve data for {year}-{month}: {e}")
            continue

# 關閉瀏覽器
driver.quit()

# 將欄位轉換中文
columns_rename = {
    'Year': '年份',
    'Month': '月份',
    # 可增加需要的部分
}

all_data.rename(columns=columns_rename, inplace=True)

# 儲存為CSV和JSON格式
csv_filename = 'weather_data.csv'
json_filename = 'weather_data.json'

all_data.to_csv(csv_filename, index=False)
all_data.to_json(json_filename, orient='records', lines=True, force_ascii=False) #修正不允許儲存為ascii

print(f"Data has been saved as {csv_filename} and {json_filename}")
