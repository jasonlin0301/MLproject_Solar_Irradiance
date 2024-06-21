# theory 

### 等效日射小時（Equivalent Sun Hours, ESH）和峰值日射小時（Peak Sun Hours, PSH）是與太陽能系統設計相關的重要概念。


> 等效日射小時（Equivalent Sun Hours, ESH）
> [European Society of Hypertension position paper on
renal denervation 2021](https://www.eshonline.org/esh-content/uploads/2021/09/European-Society-of-Hypertesion-position-paper-on-renal-denervation-2021.pdf)

等效日射小時表示一天內太陽能輻射量轉化為在1千瓦每平方公尺（1kW/m²）條件下工作的總時間。這個指標有助於評估太陽能系統在特定地區的性能。等效日射小時的計算公式如下：

# ESH = DailySolarIrradiation (kWh/m²/day) / (1kW/m²)

### 峰值日射小時（Peak Sun Hours, PSH）

峰值日射小時與等效日射小時相似，通常被視為同義詞。它指的是一天中等效於太陽能電池板在最大功率下運行的總小時數。PSH也使用日均太陽能輻射量來計算，兩者的公式是一樣的，因此在實際應用中，*ESH* 和 *PSH* 通常可以互換使用。

#### 系統規模計算

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
# 目標方法

# 資料來源

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

[csv](./weather_data.csv)
```csv
站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month
桃改樹林分場,24.7,33.9,05/30,16.5,05/15,75.5,103.0,2.1,SSW,254.5,427.2,24.6,24.6,24.5,24.9,24.3,24.4,1999,1
茶改北部分場,22.1,31.0,05/12,14.0,05/13,85.8,230.5,1.2,S,249.9,431.5,23.0,23.2,23.2,23.2,23.0,22.2,1999,1
桃園農改,24.4,31.3,05/31,17.5,05/15,82.0,128.5,2.6,WSW,286.0,533.5,25.0,24.3,24.6,24.4,24.9,23.3,1999,1
茶改場,23.9,33.0,05/31,16.6,05/13,76.0,98.0,1.3,W,276.5,504.4,24.8,24.8,24.9,25.0,24.6,23.7,1999,1
農工中心,24.3,33.1,05/31,16.9,05/13,76.4,142.5,1.2,NNW,268.5,478.7,24.5,23.7,24.0,24.0,23.9,24.0,1999,1
桃改五峰分場,20.2,29.1,05/31,13.8,05/16,88.0,152.0,0.6,E,253.8,436.2,20.0,20.0,19.2,19.0,19.6,18.5,1999,1
桃改新埔分場,24.2,33.2,05/31,16.3,05/15,79.1,116.0,1.7,NW,288.9,510.0,25.4,24.7,24.8,24.7,25.0,23.5,1999,1
畜試北區分所,23.9,33.2,05/31,13.3,05/16,84.0,123.0,1.3,NNW,315.6,719.9,24.2,24.2,24.1,24.1,23.9,22.9,1999,1
苗改生物防治研究中心,23.3,32.4,05/31,14.8,05/16,81.5,139.0,1.2,N,297.9,556.5,24.8,25.0,25.1,25.2,25.1,24.5,1999,1
```

[json](./weather_data.json)

```json
{"\u7ad9\u540d":"\u6843\u6539\u6a39\u6797\u5206\u5834","\u5e73\u5747\u6c23\u6eab":"24.7","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"33.9","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/30","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":16.5,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/15","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"75.5","\u7e3d\u964d\u96e8\u91cfmm":"103.0","\u5e73\u5747\u98a8\u901fm\/s":"2.1","\u6700\u591a\u98a8\u5411":"SSW","\u7e3d\u65e5\u7167\u6642\u6578h":"254.5","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"427.2","\u5e73\u5747\u5730\u6eab(0cm)":"24.6","\u5e73\u5747\u5730\u6eab(5cm)":"24.6","\u5e73\u5747\u5730\u6eab(10 cm)":"24.5","\u5e73\u5747\u5730\u6eab(20 cm)":"24.9","\u5e73\u5747\u5730\u6eab(50 cm)":"24.3","\u5e73\u5747\u5730\u6eab(100 cm)":"24.4","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u8336\u6539\u5317\u90e8\u5206\u5834","\u5e73\u5747\u6c23\u6eab":"22.1","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"31.0","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/12","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":14.0,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/13","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"85.8","\u7e3d\u964d\u96e8\u91cfmm":"230.5","\u5e73\u5747\u98a8\u901fm\/s":"1.2","\u6700\u591a\u98a8\u5411":"S","\u7e3d\u65e5\u7167\u6642\u6578h":"249.9","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"431.5","\u5e73\u5747\u5730\u6eab(0cm)":"23.0","\u5e73\u5747\u5730\u6eab(5cm)":"23.2","\u5e73\u5747\u5730\u6eab(10 cm)":"23.2","\u5e73\u5747\u5730\u6eab(20 cm)":"23.2","\u5e73\u5747\u5730\u6eab(50 cm)":"23.0","\u5e73\u5747\u5730\u6eab(100 cm)":"22.2","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u6843\u5712\u8fb2\u6539","\u5e73\u5747\u6c23\u6eab":"24.4","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"31.3","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":17.5,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/15","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"82.0","\u7e3d\u964d\u96e8\u91cfmm":"128.5","\u5e73\u5747\u98a8\u901fm\/s":"2.6","\u6700\u591a\u98a8\u5411":"WSW","\u7e3d\u65e5\u7167\u6642\u6578h":"286.0","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"533.5","\u5e73\u5747\u5730\u6eab(0cm)":"25.0","\u5e73\u5747\u5730\u6eab(5cm)":"24.3","\u5e73\u5747\u5730\u6eab(10 cm)":"24.6","\u5e73\u5747\u5730\u6eab(20 cm)":"24.4","\u5e73\u5747\u5730\u6eab(50 cm)":"24.9","\u5e73\u5747\u5730\u6eab(100 cm)":"23.3","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u8336\u6539\u5834","\u5e73\u5747\u6c23\u6eab":"23.9","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"33.0","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":16.6,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/13","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"76.0","\u7e3d\u964d\u96e8\u91cfmm":"98.0","\u5e73\u5747\u98a8\u901fm\/s":"1.3","\u6700\u591a\u98a8\u5411":"W","\u7e3d\u65e5\u7167\u6642\u6578h":"276.5","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"504.4","\u5e73\u5747\u5730\u6eab(0cm)":"24.8","\u5e73\u5747\u5730\u6eab(5cm)":"24.8","\u5e73\u5747\u5730\u6eab(10 cm)":"24.9","\u5e73\u5747\u5730\u6eab(20 cm)":"25.0","\u5e73\u5747\u5730\u6eab(50 cm)":"24.6","\u5e73\u5747\u5730\u6eab(100 cm)":"23.7","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u8fb2\u5de5\u4e2d\u5fc3","\u5e73\u5747\u6c23\u6eab":"24.3","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"33.1","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":16.9,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/13","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"76.4","\u7e3d\u964d\u96e8\u91cfmm":"142.5","\u5e73\u5747\u98a8\u901fm\/s":"1.2","\u6700\u591a\u98a8\u5411":"NNW","\u7e3d\u65e5\u7167\u6642\u6578h":"268.5","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"478.7","\u5e73\u5747\u5730\u6eab(0cm)":"24.5","\u5e73\u5747\u5730\u6eab(5cm)":"23.7","\u5e73\u5747\u5730\u6eab(10 cm)":"24.0","\u5e73\u5747\u5730\u6eab(20 cm)":"24.0","\u5e73\u5747\u5730\u6eab(50 cm)":"23.9","\u5e73\u5747\u5730\u6eab(100 cm)":"24.0","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u6843\u6539\u4e94\u5cf0\u5206\u5834","\u5e73\u5747\u6c23\u6eab":"20.2","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"29.1","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":13.8,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/16","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"88.0","\u7e3d\u964d\u96e8\u91cfmm":"152.0","\u5e73\u5747\u98a8\u901fm\/s":"0.6","\u6700\u591a\u98a8\u5411":"E","\u7e3d\u65e5\u7167\u6642\u6578h":"253.8","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"436.2","\u5e73\u5747\u5730\u6eab(0cm)":"20.0","\u5e73\u5747\u5730\u6eab(5cm)":"20.0","\u5e73\u5747\u5730\u6eab(10 cm)":"19.2","\u5e73\u5747\u5730\u6eab(20 cm)":"19.0","\u5e73\u5747\u5730\u6eab(50 cm)":"19.6","\u5e73\u5747\u5730\u6eab(100 cm)":"18.5","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u6843\u6539\u65b0\u57d4\u5206\u5834","\u5e73\u5747\u6c23\u6eab":"24.2","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"33.2","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":16.3,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/15","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"79.1","\u7e3d\u964d\u96e8\u91cfmm":"116.0","\u5e73\u5747\u98a8\u901fm\/s":"1.7","\u6700\u591a\u98a8\u5411":"NW","\u7e3d\u65e5\u7167\u6642\u6578h":"288.9","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"510.0","\u5e73\u5747\u5730\u6eab(0cm)":"25.4","\u5e73\u5747\u5730\u6eab(5cm)":"24.7","\u5e73\u5747\u5730\u6eab(10 cm)":"24.8","\u5e73\u5747\u5730\u6eab(20 cm)":"24.7","\u5e73\u5747\u5730\u6eab(50 cm)":"25.0","\u5e73\u5747\u5730\u6eab(100 cm)":"23.5","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u755c\u8a66\u5317\u5340\u5206\u6240","\u5e73\u5747\u6c23\u6eab":"23.9","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"33.2","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":13.3,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/16","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"84.0","\u7e3d\u964d\u96e8\u91cfmm":"123.0","\u5e73\u5747\u98a8\u901fm\/s":"1.3","\u6700\u591a\u98a8\u5411":"NNW","\u7e3d\u65e5\u7167\u6642\u6578h":"315.6","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"719.9","\u5e73\u5747\u5730\u6eab(0cm)":"24.2","\u5e73\u5747\u5730\u6eab(5cm)":"24.2","\u5e73\u5747\u5730\u6eab(10 cm)":"24.1","\u5e73\u5747\u5730\u6eab(20 cm)":"24.1","\u5e73\u5747\u5730\u6eab(50 cm)":"23.9","\u5e73\u5747\u5730\u6eab(100 cm)":"22.9","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u82d7\u6539\u751f\u7269\u9632\u6cbb\u7814\u7a76\u4e2d\u5fc3","\u5e73\u5747\u6c23\u6eab":"23.3","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"32.4","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":14.8,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/16","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"81.5","\u7e3d\u964d\u96e8\u91cfmm":"139.0","\u5e73\u5747\u98a8\u901fm\/s":"1.2","\u6700\u591a\u98a8\u5411":"N","\u7e3d\u65e5\u7167\u6642\u6578h":"297.9","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"556.5","\u5e73\u5747\u5730\u6eab(0cm)":"24.8","\u5e73\u5747\u5730\u6eab(5cm)":"25.0","\u5e73\u5747\u5730\u6eab(10 cm)":"25.1","\u5e73\u5747\u5730\u6eab(20 cm)":"25.2","\u5e73\u5747\u5730\u6eab(50 cm)":"25.1","\u5e73\u5747\u5730\u6eab(100 cm)":"24.5","Year":1999,"Month":1}
{"\u7ad9\u540d":"\u82d7\u6817\u8fb2\u6539","\u5e73\u5747\u6c23\u6eab":"24.3","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab":"34.5","\u7d55\u5c0d\u6700\u9ad8\u6c23\u6eab\u65e5\u671f":"05\/31","\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab":14.3,"\u7d55\u5c0d\u6700\u4f4e\u6c23\u6eab\u65e5\u671f":"05\/16","\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6 %":"80.9","\u7e3d\u964d\u96e8\u91cfmm":"127.0","\u5e73\u5747\u98a8\u901fm\/s":"1.7","\u6700\u591a\u98a8\u5411":"NW","\u7e3d\u65e5\u7167\u6642\u6578h":"301.2","\u7e3d\u65e5\u5c04\u91cfMJ\/ m2":"601.6","\u5e73\u5747\u5730\u6eab(0cm)":"25.7","\u5e73\u5747\u5730\u6eab(5cm)":"25.4","\u5e73\u5747\u5730\u6eab(10 cm)":"25.0","\u5e73\u5747\u5730\u6eab(20 cm)":"24.9","\u5e73\u5747\u5730\u6eab(50 cm)":"25.5","\u5e73\u5747\u5730\u6eab(100 cm)":"25.0","Year":1999,"Month":1}
```

​
