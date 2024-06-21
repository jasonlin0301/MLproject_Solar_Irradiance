import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 配置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器

# 使用webdriver-manager安装和管理ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义数据下载范围
start_year = 1999
end_year = 2024
end_month = 5

# 创建空的DataFrame来存储所有数据
all_data = pd.DataFrame()

# 迭代年份和月份，下载数据
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 跳过2024年6月及之后的月份
        if year == 2024 and month > end_month:
            break
        
        # 构建URL
        url = f"https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html?year={year}&month={month}"
        
        # 使用Selenium打开网页
        driver.get(url)
        
        try:
            # 等待表格加载完成
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # 获取表格HTML
            table_html = table.get_attribute('outerHTML')
            
            # 将HTML表格转换为DataFrame
            df = pd.read_html(table_html)[0]
            
            # 添加年月信息
            df['Year'] = year
            df['Month'] = month
            
            # 合并到所有数据的DataFrame中
            all_data = pd.concat([all_data, df], ignore_index=True)
        
        except Exception as e:
            print(f"Failed to retrieve data for {year}-{month}: {e}")
            continue

# 关闭浏览器
driver.quit()

# 保存为CSV和JSON格式
csv_filename = 'weather_data.csv'
json_filename = 'weather_data.json'

all_data.to_csv(csv_filename, index=False)
all_data.to_json(json_filename, orient='records', lines=True)

print(f"Data has been saved as {csv_filename} and {json_filename}")
