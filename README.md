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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 初始化啟動chrome webdriver
driverpath = r"D:\github\MLproject_Solar_Irradiance\chromedriver-win64\chromedriver.exe"  # 瀏覽器驅動程式路徑
service = Service(driverpath)

# 設置Chrome選項以啟用無頭模式
options = Options()
options.add_argument('--headless')  # 啟用無頭模式
options.add_argument('--disable-gpu')  # 如果你使用的是Windows系統，這一步是必要的
options.add_argument('--no-sandbox')  # 對於Linux系統可能是必要的
options.add_argument('--disable-dev-shm-usage')  # 共享內存設置

browser = webdriver.Chrome(service=service, options=options)  # 模擬瀏覽器
wait = WebDriverWait(browser, 10)  # 設置顯式等待時間

url = 'https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html'
browser.get(url)  # 以get方式進入網站
time.sleep(3)  # 網站有loading時間

# 初始化總存儲數據的列表
all_years_data = []

# 遍歷1999年至2024年
for year in range(1999, 2025):
    # 找出年份和月份的選單定位
    year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]')))  # 使用XPath定位年份選單
    month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Month"]')))  # 使用XPath定位月份選單

    # 打開年份選單並選擇對應年份
    year_dropdown.click()
    time.sleep(1)  # 確保下拉選單打開
    year_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Year"]/option[text()="{year}"]')))
    year_option.click()

    # 初始化存儲每年數據的列表
    yearly_data = []

    # 遍歷每年的12個月
    for month in range(1, 13):
        # 打開月份選單並選擇對應月份
        month_dropdown.click()
        time.sleep(1)  # 確保下拉選單打開

        # 檢查月份選項是否存在
        try:
            month_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Month"]/option[text()="{month}"]')))
            month_option.click()
        except:
            print(f"{year}年{month}月的數據不可用，跳過")
            continue

        # 顯式等待表格加載完成
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
            time.sleep(3)  # 追加等待時間確保數據完全加載
        except:
            print(f"{year}年{month}月的數據表格未加載，跳過")
            continue

        # 使用pandas讀取HTML表格
        try:
            tables = pd.read_html(browser.page_source)
            df = tables[0]
        except ValueError:
            print(f"{year}年{month}月的表格數據讀取失敗，跳過")
            continue

        # 添加年份和月份列
        df['Year'] = year
        df['Month'] = month

        # 將數據添加到年度列表中
        yearly_data.append(df)

    # 合併每年的數據
    if yearly_data:
        yearly_df = pd.concat(yearly_data, ignore_index=True)

        # 打印每年抓取到的數據
        print(f"{year}年的數據：")
        print(yearly_df)

        # 保存每年的數據為CSV
        yearly_df.to_csv(f'data_{year}.csv', index=False, encoding='utf-8-sig')

        # 保存每年的數據為JSON
        yearly_df.to_json(f'data_{year}.json', orient='records', force_ascii=False)

        # 將每年的數據添加到總列表中
        all_years_data.append(yearly_df)

# 關閉瀏覽器
browser.quit()

# 合併所有年份的數據
if all_years_data:
    final_df = pd.concat(all_years_data, ignore_index=True)

    # 打印所有年份抓取到的數據
    print("所有年份的數據：")
    print(final_df)

    # 保存所有年份的數據為CSV
    final_df.to_csv('_data_1999_to_2024.csv', index=False, encoding='utf-8-sig')

    # 保存所有年份的數據為JSON
    final_df.to_json('_data_1999_to_2024.json', orient='records', force_ascii=False)

    print("1999年至2024年的數據已保存為CSV和JSON格式")

```

[csv](./weather/weather_data.csv)
```csv
站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month
茶改場,15.3,25.5,1/23,7.6,1/15,82.6,73.5,4.0,*,63.3,*176.74,*16.4,*16.4,*16.8,*17.2,*17.9,*19.5,1999,1
桃園農改,16.1,23.3,1/19,8.8,1/15,81.0,65.5,5.4,45.0,65.7,175.6,17.8,17.5,17.3,18.0,18.9,19.9,1999,1
五峰站,11.9,21.1,1/14,3.5,1/15,91.3,118.5,0.4,135.0,88.6,227.5,14.6,14.6,14.9,15.3,15.9,17.1,1999,1
苗栗農改,15.7,25.7,1/19,8.6,1/15,95.9,39.5,2.4,22.5,XXX,XXX,17.8,18.1,18.3,18.5,18.9,19.9,1999,1
台中農改,17.1,27.4,1/19,10.7,1/15,83.2,16.0,2.5,360.0,166.4,237.07,19.6,19.9,20.3,20.6,21.0,21.8,1999,1
```

[json](./weather//weather_data.json)

```json
{"站名":"茶改場","平均氣溫":"15.3","絕對最高氣溫":"25.5","絕對最高氣溫日期":"1\/23","絕對最低氣溫":"7.6","絕對最低氣溫日期":"1\/15","平均相對濕度 %":"82.6","總降雨量mm":"73.5","平均風速m\/s":"4.0","最多風向":"*","總日照時數h":"63.3","總日射量MJ\/ m2":"*176.74","平均地溫(0cm)":"*16.4","平均地溫(5cm)":"*16.4","平均地溫(10 cm)":"*16.8","平均地溫(20 cm)":"*17.2","平均地溫(50 cm)":"*17.9","平均地溫(100 cm)":"*19.5","Year":1999,"Month":1},{"站名":"桃園農改","平均氣溫":"16.1","絕對最高氣溫":"23.3","絕對最高氣溫日期":"1\/19","絕對最低氣溫":"8.8","絕對最低氣溫日期":"1\/15","平均相對濕度 %":"81.0","總降雨量mm":"65.5","平均風速m\/s":"5.4","最多風向":"45.0","總日照時數h":"65.7","總日射量MJ\/ m2":"175.6","平均地溫(0cm)":"17.8","平均地溫(5cm)":"17.5","平均地溫(10 cm)":"17.3","平均地溫(20 cm)":"18.0","平均地溫(50 cm)":"18.9","平均地溫(100 cm)":"19.9","Year":1999,"Month":1},{"站名":"五峰站","平均氣溫":"11.9","絕對最高氣溫":"21.1","絕對最高氣溫日期":"1\/14","絕對最低氣溫":"3.5","絕對最低氣溫日期":"1\/15","平均相對濕度 %":"91.3","總降雨量mm":"118.5","平均風速m\/s":"0.4","最多風向":"135.0","總日照時數h":"88.6","總日射量MJ\/ m2":"227.5","平均地溫(0cm)":"14.6","平均地溫(5cm)":"14.6","平均地溫(10 cm)":"14.9","平均地溫(20 cm)":"15.3","平均地溫(50 cm)":"15.9","平均地溫(100 cm)":"17.1","Year":1999,"Month":1}
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

    - 每片400W的單晶矽太陽能板大約需要1.7平方米的安裝面積。要計算可以安裝的總容量，首先需要確定可用的實際屋頂面積，考慮到可能的遮蔽物（如通風口、屋頂突出物等）和維護通道。假設**可用面積約為70%**：

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

## 由html label新增行政區

> F12 謝謝你

```pyhton

import json
import pandas as pd

# 載入原始json
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

# 選擇需要的key&value
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

# 存為新的JSON檔案
output_json_path = 'solar.json'
with open(output_json_path, 'w', encoding='utf-8') as file:
    for entry in filtered_data:
        json.dump(entry, file, ensure_ascii=False)
        file.write('\n')

# 轉DataFrame儲存為新CSV檔
df = pd.DataFrame(filtered_data)
output_csv_path = 'solar.csv'
df.to_csv(output_csv_path, index=False)

print(f"數據已儲存為 {output_json_path} 和 {output_csv_path}")

```

``` CSV

站名,年份,月份,總日照時數h,總日射量MJ/ m2
桃改樹林分場,1999,1,254.5,427.2
茶改北部分場,1999,1,249.9,431.5
桃園農改,1999,1,286.0,533.5
茶改場,1999,1,276.5,504.4

```

``` JSON

{"站名": "桃改樹林分場", "年份": 1999, "月份": 1, "總日照時數h": "254.5", "總日射量MJ/ m2": "427.2"}
{"站名": "茶改北部分場", "年份": 1999, "月份": 1, "總日照時數h": "249.9", "總日射量MJ/ m2": "431.5"}
{"站名": "桃園農改", "年份": 1999, "月份": 1, "總日照時數h": "286.0", "總日射量MJ/ m2": "533.5"}
{"站名": "茶改場", "年份": 1999, "月份": 1, "總日照時數h": "276.5", "總日射量MJ/ m2": "504.4"}
{"站名": "農工中心", "年份": 1999, "月份": 1, "總日照時數h": "268.5", "總日射量MJ/ m2": "478.7"}

```

## 找出各農改場所在行政區域

```python

import pandas as pd

# 使用原始字符串以避免路徑問題
file_path = 'weather_data.csv'

# 讀取 CSV 文件
weather_data = pd.read_csv(file_path)

# 提取站名列並刪除重複的站名
station_names = weather_data[['站名']].drop_duplicates()

# 保存到新的 CSV 文件
output_path = 'station_names.csv'
station_names.to_csv(output_path, index=False)

print(f"站名已保存到 {output_path}")
```

```csv
站名
桃改樹林分場
茶改北部分場
桃園農改
茶改場
農工中心
桃改五峰分場
桃改新埔分場
畜試北區分所
苗改生物防治研究中心
苗栗農改
種苗繁殖
農業試驗所
王功漁港
臺中農改
中改埔里分場
林試畢祿溪站
臺大內茅埔
臺大和社
臺大溪頭
臺大竹山
茶改中部分場
茶改南部分場
萬大發電廠
蓮華池
南改斗南分場
口湖工作站
四湖植物園
水試臺西試驗場
海口故事園區
臺大雲林校區
麥寮合作社
農試嘉義分所
南改義竹分場
南改鹿草分場
布袋國中
農試溪口農場
七股研究中心
六官養殖協會
水試所海水繁養殖中心
畜試所
臺南蘭花園區
臺南農改
林試六龜中心
林試扇平站
農試鳳山分所
高改旗南分場
崎峰國小
恆春工作站
東港工作站
畜試南區分所
高雄農改
畜試東區分所
花改蘭陽分場
花蓮農改
東改班鳩分場
東改賓朗果園
林試太麻里1
林試太麻里2
茶改東部分場
```

```python
# 創建一個站名到區域的對照表
station_to_district = {
    '桃改樹林分場': '新北市',
    '茶改北部分場': '新北市',
    '桃園農改': '桃園市',
    '茶改場': '南投縣',
    '農工中心': '台中市',
    '桃改五峰分場': '新竹縣',
    '桃改新埔分場': '新竹縣',
    '畜試北區分所': '苗栗縣',
    '苗改生物防治研究中心': '苗栗縣',
    '苗栗農改': '苗栗縣',
    '種苗繁殖': '台中市',
    '農業試驗所': '台中市',
    '王功漁港': '彰化縣',
    '臺中農改': '台中市',
    '中改埔里分場': '南投縣',
    '林試畢祿溪站': '南投縣',
    '臺大內茅埔': '南投縣',
    '臺大和社': '南投縣',
    '臺大溪頭': '南投縣',
    '臺大竹山': '南投縣',
    '茶改中部分場': '南投縣',
    '茶改南部分場': '嘉義縣',
    '萬大發電廠': '南投縣',
    '蓮華池': '南投縣',
    '南改斗南分場': '雲林縣',
    '口湖工作站': '雲林縣',
    '四湖植物園': '雲林縣',
    '水試臺西試驗場': '雲林縣',
    '海口故事園區': '雲林縣',
    '臺大雲林校區': '雲林縣',
    '麥寮合作社': '雲林縣',
    '農試嘉義分所': '嘉義市',
    '南改義竹分場': '嘉義縣',
    '南改鹿草分場': '嘉義縣',
    '布袋國中': '嘉義縣',
    '農試溪口農場': '嘉義縣',
    '七股研究中心': '台南市',
    '六官養殖協會': '台南市',
    '水試所海水繁養殖中心': '台南市',
    '畜試所': '屏東縣',
    '臺南蘭花園區': '台南市',
    '臺南農改': '台南市',
    '林試六龜中心': '高雄市',
    '林試扇平站': '高雄市',
    '農試鳳山分所': '高雄市',
    '高改旗南分場': '高雄市',
    '崎峰國小': '屏東縣',
    '恆春工作站': '屏東縣',
    '東港工作站': '屏東縣',
    '畜試南區分所': '屏東縣',
    '高雄農改': '高雄市',
    '畜試東區分所': '台東縣',
    '花改蘭陽分場': '宜蘭縣',
    '花蓮農改': '花蓮縣',
    '東改班鳩分場': '花蓮縣',
    '東改賓朗果園': '花蓮縣',
    '林試太麻里1': '台東縣',
    '林試太麻里2': '台東縣',
    '茶改東部分場': '台東縣'
}

# 將對照表轉換成DataFrame
df = pd.DataFrame(list(station_to_district.items()), columns=['站名', '區域'])

# 保存為CSV文件
csv_file_path = 'stations_districts.csv'
df.to_csv(csv_file_path, index=False)

print(f"CSV file saved to {csv_file_path}")
```

得到一個依照行政區排列的CSV

```CSV
站名,區域
桃改樹林分場,新北市
茶改北部分場,新北市
桃園農改,桃園市
茶改場,南投縣
農工中心,台中市
桃改五峰分場,新竹縣
桃改新埔分場,新竹縣
畜試北區分所,苗栗縣
苗改生物防治研究中心,苗栗縣
苗栗農改,苗栗縣
種苗繁殖,台中市
農業試驗所,台中市
王功漁港,彰化縣
臺中農改,台中市
中改埔里分場,南投縣
林試畢祿溪站,南投縣
臺大內茅埔,南投縣
臺大和社,南投縣
臺大溪頭,南投縣
臺大竹山,南投縣
茶改中部分場,南投縣
茶改南部分場,嘉義縣
萬大發電廠,南投縣
蓮華池,南投縣
南改斗南分場,雲林縣
口湖工作站,雲林縣
四湖植物園,雲林縣
水試臺西試驗場,雲林縣
海口故事園區,雲林縣
臺大雲林校區,雲林縣
麥寮合作社,雲林縣
農試嘉義分所,嘉義市
南改義竹分場,嘉義縣
南改鹿草分場,嘉義縣
布袋國中,嘉義縣
農試溪口農場,嘉義縣
七股研究中心,台南市
六官養殖協會,台南市
水試所海水繁養殖中心,台南市
畜試所,屏東縣
臺南蘭花園區,台南市
臺南農改,台南市
林試六龜中心,高雄市
林試扇平站,高雄市
農試鳳山分所,高雄市
高改旗南分場,高雄市
崎峰國小,屏東縣
恆春工作站,屏東縣
東港工作站,屏東縣
畜試南區分所,屏東縣
高雄農改,高雄市
畜試東區分所,台東縣
花改蘭陽分場,宜蘭縣
花蓮農改,花蓮縣
東改班鳩分場,花蓮縣
東改賓朗果園,花蓮縣
林試太麻里1,台東縣
林試太麻里2,台東縣
茶改東部分場,台東縣
```

