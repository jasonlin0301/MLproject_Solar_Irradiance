> 等效日射小時（Equivalent Sun Hours, ESH）和峰值日射小時（Peak Sun Hours, PSH）是與太陽能系統設計相關的重要概念。

## 等效日射小時（Equivalent Sun Hours, ESH）
[European Society of Hypertension position paper on
renal denervation 2021](https://www.eshonline.org/esh-content/uploads/2021/09/European-Society-of-Hypertesion-position-paper-on-renal-denervation-2021.pdf)

等效日射小時表示一天內太陽能輻射量轉化為在1千瓦每平方公尺（1kW/m²）條件下工作的總時間。這個指標有助於評估太陽能系統在特定地區的性能。等效日射小時的計算公式如下：

ESH = DailySolarIrradiation (kWh/m²/day) / (1kW/m²)

## 峰值日射小時（Peak Sun Hours, PSH）

峰值日射小時與等效日射小時相似，通常被視為同義詞。它指的是一天中等效於太陽能電池板在最大功率下運行的總小時數。PSH也使用日均太陽能輻射量來計算，兩者的公式是一樣的，因此在實際應用中，*ESH* 和 *PSH* 通常可以互換使用。

​## 系統規模計算

P=η×ESH/E

E 是每日能量需求（kWh/day）
η 是系統效率

```python
class SolarSystemScale:
    def __init__(self, daily_energy_demand, system_efficiency, equivalent_sun_hours):
        self.daily_energy_demand = daily_energy_demand  # 每日能量需求 (kWh/day)
        self.system_efficiency = system_efficiency      # 系統效率
        self.equivalent_sun_hours = equivalent_sun_hours  # 等效日射小時 (hours/day)

    def calculate_system_size(self):
        # 計算系統規模
        system_size = self.daily_energy_demand / (self.system_efficiency * self.equivalent_sun_hours)
        return system_size

# 使用範例
daily_energy_demand = 30  # 替換為你的每日能量需求
system_efficiency = 0.85  # 替換為你的系統效率
equivalent_sun_hours = 5  # 替換為你的等效日射小時

solar_system = SolarSystemScale(daily_energy_demand, system_efficiency, equivalent_sun_hours)
system_size = solar_system.calculate_system_size()
print(f"需要的系統規模是: {system_size:.2f} kW")
```

> 交通部中央氣象署 首頁>生活>農業>農業觀測>全部觀測網月資料

## [日射量資料](https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html)
​
> 使用selenium及webdriver-manager建立虛擬webviewer抓取java資料庫資料並建立.csv及.json

```python

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

```

​
