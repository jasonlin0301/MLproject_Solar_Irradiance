# theory 

### 等效日射小時（Equivalent Sun Hours, ESH）和峰值日射小時（Peak Sun Hours, PSH）是與太陽能系統設計相關的重要概念。


> 等效日射小時（Equivalent Sun Hours, ESH）

> 來源：
> * Solarmazd​ ([SOALRMAZD](https://solarmazd.com/peak-sun-hours-psh-what-does-it-mean-and-how-to-estimate-it/))​
> * RenewableWise​ ([Renewablewise](https://www.renewablewise.com/peak-sun-hours-calculator/))​
> * Palmetto​ ([Palmetto](https://palmetto.com/solar/what-are-peak-sun-hours))​
> * Dot Watts​ ([Dot Watts®](https://palmetto.com/solar/what-are-peak-sun-hours))

等效日射小時表示一天內太陽能輻射量轉化為在1千瓦每平方公尺（1kW/m²）條件下工作的總時間。這個指標有助於評估太陽能系統在特定地區的性能。等效日射小時的計算公式如下：

# **ESH = DailySolarIrradiation (kWh/m²/day) / (1kW/m²)**

### 峰值日射小時（Peak Sun Hours, PSH）

峰值日射小時與等效日射小時相似，通常被視為同義詞。它指的是一天中等效於太陽能電池板在最大功率下運行的總小時數。PSH也使用日均太陽能輻射量來計算，兩者的公式是一樣的，因此在實際應用中，**ESH** 和 **PSH** 通常**可以互換使用**。

* 如果某地一天接收到 6 kWh/m² 的太陽能量，則該地的 ESH 為 6 小時，意味著該地接收到相當於 6 小時的 1000 W/m² 的陽光。

* Daily Energy Production=Power Rating of Panel×ESH

    - 每日能量產出=太陽能板功率×ESH

* example : If you have a 200-watt solar panel and the ESH in your location is 5 hours. Daily Energy Production=200 W×5 hours=1,000 Wh or 1 kWh.

    - 如果你有一塊 200 瓦的太陽能板，而你所在位置的 ESH 為 5 小時，每日能量產出=200 W×5 小時=1000 Wh 或 1 kWh

#### 系統規模計算

P=Sxη×ESH/E
- S 是系統容量(KW)
- E 是每日能量需求（kWh/day）
- η 是系統效率

```python
class SolarSystem:
    def __init__(self, system_capacity, efficiency, esh, energy_demand):
        self.system_capacity = system_capacity  # 系統容量 (kW)
        self.efficiency = efficiency  # 系統效率
        self.esh = esh  # 等效日射小時 (hours/day)
        self.energy_demand = energy_demand  # 每日能量需求 (kWh/day)

    def calculate_system_capacity(self):
        # 計算所需的系統容量 P
        P = self.system_capacity * self.efficiency * self.esh / self.energy_demand
        return P

    def calculate_energy_demand(self):
        # 計算每日能量需求 E
        E = self.system_capacity * self.efficiency * self.esh
        return E

# 使用示例
system_capacity = 8  # kW
efficiency = 0.75  # 系統效率
esh = 5  # 等效日射小時 (hours/day)
energy_demand = 30  # 每日能量需求 (kWh/day)

solar_system = SolarSystem(system_capacity, efficiency, esh, energy_demand)

# 計算所需的系統容量
required_capacity = solar_system.calculate_system_capacity()
print(f'Required System Capacity: {required_capacity:.2f} kW')

# 計算每日能量需求
daily_energy = solar_system.calculate_energy_demand()
print(f'Daily Energy Production: {daily_energy:.2f} kWh')
```
# 目標方法

1. 計算該地區平均日射量
2. 使用者輸入欲建置的太陽能總瓦數
3. 使用者輸入地址
4. 使用者輸入建置面積
5. 使用者輸入欲建置年度
6. 依趨勢線計算出P
7. 計算建置費用

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

```

[csv](./weather_data.csv)
```csv
站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),年份,月份
桃改樹林分場,24.7,33.9,05/30,16.5,05/15,75.5,103.0,2.1,SSW,254.5,427.2,24.6,24.6,24.5,24.9,24.3,24.4,1999,1
茶改北部分場,22.1,31.0,05/12,14.0,05/13,85.8,230.5,1.2,S,249.9,431.5,23.0,23.2,23.2,23.2,23.0,22.2,1999,1
桃園農改,24.4,31.3,05/31,17.5,05/15,82.0,128.5,2.6,WSW,286.0,533.5,25.0,24.3,24.6,24.4,24.9,23.3,1999,1
茶改場,23.9,33.0,05/31,16.6,05/13,76.0,98.0,1.3,W,276.5,504.4,24.8,24.8,24.9,25.0,24.6,23.7,1999,1
```

[json](./weather_data.json)

```json
{"站名":"桃改樹林分場","平均氣溫":"24.7","絕對最高氣溫":"33.9","絕對最高氣溫日期":"05\/30","絕對最低氣溫":16.5,"絕對最低氣溫日期":"05\/15","平均相對濕度 %":"75.5","總降雨量mm":"103.0","平均風速m\/s":"2.1","最多風向":"SSW","總日照時數h":"254.5","總日射量MJ\/ m2":"427.2","平均地溫(0cm)":"24.6","平均地溫(5cm)":"24.6","平均地溫(10 cm)":"24.5","平均地溫(20 cm)":"24.9","平均地溫(50 cm)":"24.3","平均地溫(100 cm)":"24.4","年份":1999,"月份":1}
{"站名":"茶改北部分場","平均氣溫":"22.1","絕對最高氣溫":"31.0","絕對最高氣溫日期":"05\/12","絕對最低氣溫":14.0,"絕對最低氣溫日期":"05\/13","平均相對濕度 %":"85.8","總降雨量mm":"230.5","平均風速m\/s":"1.2","最多風向":"S","總日照時數h":"249.9","總日射量MJ\/ m2":"431.5","平均地溫(0cm)":"23.0","平均地溫(5cm)":"23.2","平均地溫(10 cm)":"23.2","平均地溫(20 cm)":"23.2","平均地溫(50 cm)":"23.0","平均地溫(100 cm)":"22.2","年份":1999,"月份":1}
{"站名":"桃園農改","平均氣溫":"24.4","絕對最高氣溫":"31.3","絕對最高氣溫日期":"05\/31","絕對最低氣溫":17.5,"絕對最低氣溫日期":"05\/15","平均相對濕度 %":"82.0","總降雨量mm":"128.5","平均風速m\/s":"2.6","最多風向":"WSW","總日照時數h":"286.0","總日射量MJ\/ m2":"533.5","平均地溫(0cm)":"25.0","平均地溫(5cm)":"24.3","平均地溫(10 cm)":"24.6","平均地溫(20 cm)":"24.4","平均地溫(50 cm)":"24.9","平均地溫(100 cm)":"23.3","年份":1999,"月份":1}
{"站名":"茶改場","平均氣溫":"23.9","絕對最高氣溫":"33.0","絕對最高氣溫日期":"05\/31","絕對最低氣溫":16.6,"絕對最低氣溫日期":"05\/13","平均相對濕度 %":"76.0","總降雨量mm":"98.0","平均風速m\/s":"1.3","最多風向":"W","總日照時數h":"276.5","總日射量MJ\/ m2":"504.4","平均地溫(0cm)":"24.8","平均地溫(5cm)":"24.8","平均地溫(10 cm)":"24.9","平均地溫(20 cm)":"25.0","平均地溫(50 cm)":"24.6","平均地溫(100 cm)":"23.7","年份":1999,"月份":1}
{"站名":"農工中心","平均氣溫":"24.3","絕對最高氣溫":"33.1","絕對最高氣溫日期":"05\/31","絕對最低氣溫":16.9,"絕對最低氣溫日期":"05\/13","平均相對濕度 %":"76.4","總降雨量mm":"142.5","平均風速m\/s":"1.2","最多風向":"NNW","總日照時數h":"268.5","總日射量MJ\/ m2":"478.7","平均地溫(0cm)":"24.5","平均地溫(5cm)":"23.7","平均地溫(10 cm)":"24.0","平均地溫(20 cm)":"24.0","平均地溫(50 cm)":"23.9","平均地溫(100 cm)":"24.0","年份":1999,"月份":1}
```

## 主要設備

建立一個完整的太陽能蓄電系統需要以下主要設備和相應的價格範圍(USD)：

### 太陽能板 (Solar Panels)

* Monocrystalline Panels: 單價約為每瓦 $0.60 至 $1.00，400W 的單板價格約為 $250-$360​ <[Solar](https://www.solar.com/learn/solar-panel-cost/)><[GoGreenSolar.com](https://www.gogreensolar.com/pages/solar-components-101)>​​
* Polycrystalline Panels: 單價約為每瓦 $0.50 至 $0.80，300W 的單板價格約為 $150-$240。
* Thin-Film Panels: 單價約為每瓦 $0.40 至 $0.70，適用於特定應用場景如柔性安裝​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

    - 單晶矽太陽能板的大小和主流功率:
        > 目前，主流的單晶矽太陽能板功率為400W左右。這類太陽能板的尺寸一般約為1.7平方米（1.7m²），具體尺寸因製造商而異，但大多數在1.6米×1米左右。

    - 屋頂面積和可安裝容量計算
        >台灣30坪的樓地板面積約為99平方米（1坪約等於3.3平方米）。假設屋頂面積與樓地板面積相當，即約99平方米。

    - 每片400W的單晶矽太陽能板大約需要1.7平方米的安裝面積。要計算可以安裝的總容量，首先需要確定可用的實際屋頂面積，考慮到可能的遮蔽物（如通風口、煙囪等）和維護通道。假設**可用面積約為70%**：

        > 可用屋頂面積：
        99m²×0.70=69.3m²
        99平方米×0.70=69.3平方米

        > 每片太陽能板的安裝面積為1.7平方米，計算可安裝的太陽能板數量：
        69.3m²/1.7m²(片)≈40.76(片)
        取整數，最多可安裝40片太陽能板。

        > 每片太陽能板功率為400W，總容量為：
        40(片)×400(W/片)=16000W，即16kW。

### 太陽能架設與安裝設備 (Racking and Mounting Equipment)

* Roof Mounts: 單個系統價格約為 $1000 至 $3000。
* Ground Mounts: 單個系統價格約為 $2000 至 $4000​ <[EnergySage](https://www.energysage.com/solar/solar-panel-setup-what-you-need-to-know/)​​><[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>。

### 逆變器 (Inverters)

* String Inverters: 單價約為 $1000 至 $2500，壽命約 10-15 年。
* Microinverters: 單價約為每瓦 $1.00 至 $1.20，系統總價約為 $3000-$5000，壽命約 25 年<[GoGreenSolar.com](https://www.gogreensolar.com/pages/solar-components-101)><[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

### 蓄電池 (Batteries)

* 鉛酸電池: 每千瓦時價格約為 $200 至 $300。
* 鋰離子電池: 每千瓦時價格約為 $400 至 $700，10kWh 系統價格約為 $4000-$7000​ <[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>​。

### 電力調節器 (Charge Controllers)

* MPPT Controllers: 單價約為 $100 至 $500，根據系統規模和功能不同​ <[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>​。

### 斷路器 (Disconnect Switch)

* 單價約為 $50 至 $200，用於安全維護和緊急關閉系統​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

### 勞力與技術費用

* 安裝太陽能系統的人工成本約為 $3000 至 $7000，根據系統規模和複雜性而異。專業電工的費用可能更高​ <[Solar](https://www.solar.com/learn/solar-panel-cost/)>​。

#### 施工時間

建置一個完整的家庭太陽能系統一般需要 1-3 週，包括現場勘查、系統設計、安裝和測試​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

## 計算太陽能系統的產生度數

給定的條件：
* EHS (Equivalent Sun Hours) = 2.5 小時
* 系統容量 = 16000W (16kW)
* 系統效率 = 80%

計算公式：

P=Sxη×ESH/E
- S 是系統容量(KW)
- E 是每日能量需求（kWh/day）
- η 是系統效率

16000W×2.5hr×0.80=32000Wh，可以產生32度電。

## 台灣平均家戶用電量

根據台灣電力公司（Taipower）和其他相關資料，台灣家庭的平均每月用電量約為300至400度電​ (ShopSolar.com)​​ (Fenice Energy)​。我們取中間值350度電來做進一步分析。

> 計算年用電量和每日用電量

平均每月用電量=350kWh
平均每年用電量=350kWh×12月=4200kWh
平均每日用電量=4200kWhx365天≈11.5kWh，11.5度電

32 > 11.5， Z大於B，只是沒有錢，我也不住透天。
所以不是日照量的問題，是大樓跟公寓的住宅密集度的問題....(?
