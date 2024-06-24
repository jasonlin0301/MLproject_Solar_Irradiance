import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器

# 使用webdriver-manager安装和管理ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义数据下载范围
start_year = 1999
end_year = 2024
end_month = 5

# 创建一个DataFrame来保存所有数据
all_data = pd.DataFrame()

# 循环年份和月份，下载并保存表格数据
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 跳过2024年6月及其后月份
        if year == 2024 and month > end_month:
            break
        
        # 设置URL
        url = f"https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html?year={year}&month={month}"
        
        # 使用Selenium打开网页
        driver.get(url)
        
        try:
            # 等待表格加载
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # 获取HTML表格
            table_html = table.get_attribute('outerHTML')
            
            # 将HTML表格转换为DataFrame
            df = pd.read_html(table_html)[0]
            
            # 增加年月
            df['Year'] = year
            df['Month'] = month
            
            # 合并到所有数据的DataFrame中
            all_data = pd.concat([all_data, df], ignore_index=True)
        
        except Exception as e:
            print(f"Failed to retrieve data for {year}-{month}: {e}")
            continue

# 关闭浏览器
driver.quit()

# 将列名转换为中文
columns_rename = {
    'Year': '年份',
    'Month': '月份',
    # 根据你的数据，添加其他需要转换的列名
}

all_data.rename(columns=columns_rename, inplace=True)

# 保存为CSV和JSON格式
csv_filename = 'weather_data.csv'
json_filename = 'weather_data.json'

all_data.to_csv(csv_filename, index=False)
all_data.to_json(json_filename, orient='records', lines=True, force_ascii=False) #修正不允許儲存為ascii

print(f"Data has been saved as {csv_filename} and {json_filename}")
