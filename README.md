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

[csv](./Raw_Data/_data_1999_to_2024.csv)
```csv
 站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month
 茶改場,15.3,25.5,1/23,7.6,1/15,82.6,73.5,4.0,*,63.3,*176.74,*16.4,*16.4,*16.8,*17.2,*17.9,*19.5,1999,1 
 桃園農改,16.1,23.3,1/19,8.8,1/15,81.0,65.5,5.4,45.0,65.7,175.6,17.8,17.5,17.3,18.0,18.9,19.9,1999,1
 五峰站,11.9,21.1,1/14,3.5,1/15,91.3,118.5,0.4,135.0,88.6,227.5,14.6,14.6,14.9,15.3,15.9,17.1,1999,1
 苗栗農改,15.7,25.7,1/19,8.6,1/15,95.9,39.5,2.4,22.5,XXX,XXX,17.8,18.1,18.3,18.5,18.9,19.9,1999,1
 台中農改,17.1,27.4,1/19,10.7,1/15,83.2,16.0,2.5,360.0,166.4,237.07,19.6,19.9,20.3,20.6,21.0,21.8,1999,1
```

[json](./Raw_Data/_data_1999_to_2024.json)

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

    import pandas as pd
    import json
    from bs4 import BeautifulSoup

    # HTML原始碼
    html_code = """
    <select id="ST" name="st" size="1"><optgroup label="新北市" id="新北市"><option value="72AI40">桃改樹林分場</option><option value="82A750">茶改北部分場</option></optgroup><optgroup label="桃園市" id="桃園市"><option value="72C440">桃園農改</option><option value="82C160">茶改場</option><option value="A2C560">農工中心</option></optgroup><optgroup label="新竹縣" id="新竹縣"><option value="72D080">桃改五峰分場</option><option value="72D680">桃改新埔分場</option></optgroup><optgroup label="苗栗縣" id="苗栗縣"><option value="B2E890">畜試北區分所</option><option value="K2E710">苗改生物防治研究中心</option><option value="K2E360">苗栗農改</option></optgroup><optgroup label="臺中市" id="臺中市"><option value="K2F750">種苗繁殖</option><option value="G2F820">農業試驗所</option></optgroup><optgroup label="彰化縣" id="彰化縣"><option value="CAG100">王功漁港</option><option value="72G600">臺中農改</option></optgroup><optgroup label="南投縣" id="南投縣"><option value="72HA00">中改埔里分場</option><option value="E2HA20">林試畢祿溪站</option><option value="U2HA40">臺大內茅埔</option><option value="U2HA30">臺大和社</option><option value="U2H480">臺大溪頭</option><option value="U2HA50">臺大竹山</option><option value="82H320">茶改中部分場</option><option value="82H840">茶改南部分場</option><option value="42HA10">萬大發電廠</option><option value="E2H360">蓮華池</option></optgroup><optgroup label="雲林縣" id="雲林縣"><option value="72K220">南改斗南分場</option><option value="12J990">口湖工作站</option><option value="E2K600">四湖植物園</option><option value="A2K360">水試臺西試驗場</option><option value="CAJ050">海口故事園區</option><option value="A2K630">臺大雲林校區</option><option value="V2K620">麥寮合作社</option></optgroup><optgroup label="嘉義市" id="嘉義市"><option value="G2L020">農試嘉義分所</option></optgroup><optgroup label="嘉義縣" id="嘉義縣"><option value="72M360">南改義竹分場</option><option value="72M700">南改鹿草分場</option><option value="CAL110">布袋國中</option><option value="G2M350">農試溪口農場</option></optgroup><optgroup label="臺南市" id="臺南市"><option value="72N240">七股研究中心</option><option value="CAN140">六官養殖協會</option><option value="CAN130">水試所海水繁養殖中心</option><option value="B2N890">畜試所</option><option value="A2N290">臺南蘭花園區</option><option value="72N100">臺南農改</option></optgroup><optgroup label="高雄市" id="高雄市"><option value="E2P980">林試六龜中心</option><option value="E2P990">林試扇平站</option><option value="G2P820">農試鳳山分所</option><option value="72V140">高改旗南分場</option></optgroup><optgroup label="屏東縣" id="屏東縣"><option value="CAQ030">崎峰國小</option><option value="12Q980">恆春工作站</option><option value="12Q970">東港工作站</option><option value="B2Q810">畜試南區分所</option><option value="72Q010">高雄農改</option></optgroup><optgroup label="宜蘭縣" id="宜蘭縣"><option value="B2U990">畜試東區分所</option><option value="72U480">花改蘭陽分場</option></optgroup><optgroup label="花蓮縣" id="花蓮縣"><option value="72T250">花蓮農改</option></optgroup><optgroup label="臺東縣" id="臺東縣"><option value="72S200">東改班鳩分場</option><option value="72S590">東改賓朗果園</option><option value="E2S980">林試太麻里1</option><option value="E2S960">林試太麻里2</option><option value="82S580">茶改東部分場</option></optgroup></select>
    """

    # 解析HTML
    soup = BeautifulSoup(html_code, 'html.parser')

    # 提取站名和對應的行政區
    district_mapping = {}
    for optgroup in soup.find_all('optgroup'):
        district = optgroup['label']
        for option in optgroup.find_all('option'):
            station = option.text
            district_mapping[station] = district

    # 手動添加未匹配的站名對應行政區
    # 因為政府機關兩邊頁面的名稱不同，只能手動。
    additional_mappings = {
        '五峰站': '新竹縣',
        '台中農改': '台中市',
        '雲林分場': '雲林縣',
        '義竹分場': '嘉義縣',
        '恆春畜試': '屏東縣',
        '蘭陽分場': '宜蘭縣',
        '斑鳩分場': '台東縣',
        '文山茶改': '台北市',
        '大湖分場': '苗栗縣',
        '新竹畜試': '新竹縣',
        '凍頂茶改': '南投縣',
        '魚池茶改': '南投縣',
        '嘉義農試': '嘉義縣',
        '旗南農改': '屏東縣',
        '鳳山農試': '高雄市',
        '臺東茶改': '台東縣',
        '賓朗果園': '屏東縣',
        '旗南分場': '屏東縣'
    }
    district_mapping.update(additional_mappings)

    # 讀取CSV文件
    csv_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2024.csv'
    csv_data = pd.read_csv(csv_file)

    # 讀取JSON文件
    json_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2024.json'
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 添加行政區到CSV數據
    csv_data['行政區'] = csv_data['站名'].map(district_mapping)

    # 找出沒有匹配的站名
    unmatched_stations = csv_data[csv_data['行政區'].isna()]['站名'].unique()

    # 打印沒有匹配的站名
    print("未匹配的站名:")
    print(unmatched_stations)

    # 保存修改後的CSV文件
    csv_data.to_csv(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2024.csv', index=False)

    # 添加行政區到JSON數據
    for entry in json_data:
        station_name = entry.get('站名')
        entry['行政區'] = district_mapping.get(station_name, '')

    # 保存修改後的JSON文件
    with open(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2024.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


```

``` CSV

    站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month,行政區
    茶改場,15.3,25.5,1/23,7.6,1/15,82.6,73.5,4.0,*,63.3,*176.74,*16.4,*16.4,*16.8,*17.2,*17.9,*19.5,1999,1,桃園市
    桃園農改,16.1,23.3,1/19,8.8,1/15,81.0,65.5,5.4,45.0,65.7,175.6,17.8,17.5,17.3,18.0,18.9,19.9,1999,1,桃園市
    五峰站,11.9,21.1,1/14,3.5,1/15,91.3,118.5,0.4,135.0,88.6,227.5,14.6,14.6,14.9,15.3,15.9,17.1,1999,1,新竹縣
    苗栗農改,15.7,25.7,1/19,8.6,1/15,95.9,39.5,2.4,22.5,XXX,XXX,17.8,18.1,18.3,18.5,18.9,19.9,1999,1,苗栗縣
    台中農改,17.1,27.4,1/19,10.7,1/15,83.2,16.0,2.5,360.0,166.4,237.07,19.6,19.9,20.3,20.6,21.0,21.8,1999,1,台中市

```

``` JSON

{
        "站名": "茶改場",
        "平均氣溫": "15.3",
        "絕對最高氣溫": "25.5",
        "絕對最高氣溫日期": "1/23",
        "絕對最低氣溫": "7.6",
        "絕對最低氣溫日期": "1/15",
        "平均相對濕度 %": "82.6",
        "總降雨量mm": "73.5",
        "平均風速m/s": "4.0",
        "最多風向": "*",
        "總日照時數h": "63.3",
        "總日射量MJ/ m2": "*176.74",
        "平均地溫(0cm)": "*16.4",
        "平均地溫(5cm)": "*16.4",
        "平均地溫(10 cm)": "*16.8",
        "平均地溫(20 cm)": "*17.2",
        "平均地溫(50 cm)": "*17.9",
        "平均地溫(100 cm)": "*19.5",
        "Year": 1999,
        "Month": 1,
        "行政區": "桃園市"
    },
    {
        "站名": "桃園農改",
        "平均氣溫": "16.1",
        "絕對最高氣溫": "23.3",
        "絕對最高氣溫日期": "1/19",
        "絕對最低氣溫": "8.8",
        "絕對最低氣溫日期": "1/15",
        "平均相對濕度 %": "81.0",
        "總降雨量mm": "65.5",
        "平均風速m/s": "5.4",
        "最多風向": "45.0",
        "總日照時數h": "65.7",
        "總日射量MJ/ m2": "175.6",
        "平均地溫(0cm)": "17.8",
        "平均地溫(5cm)": "17.5",
        "平均地溫(10 cm)": "17.3",
        "平均地溫(20 cm)": "18.0",
        "平均地溫(50 cm)": "18.9",
        "平均地溫(100 cm)": "19.9",
        "Year": 1999,
        "Month": 1,
        "行政區": "桃園市"
    },
    {
        "站名": "五峰站",
        "平均氣溫": "11.9",
        "絕對最高氣溫": "21.1",
        "絕對最高氣溫日期": "1/14",
        "絕對最低氣溫": "3.5",
        "絕對最低氣溫日期": "1/15",
        "平均相對濕度 %": "91.3",
        "總降雨量mm": "118.5",
        "平均風速m/s": "0.4",
        "最多風向": "135.0",
        "總日照時數h": "88.6",
        "總日射量MJ/ m2": "227.5",
        "平均地溫(0cm)": "14.6",
        "平均地溫(5cm)": "14.6",
        "平均地溫(10 cm)": "14.9",
        "平均地溫(20 cm)": "15.3",
        "平均地溫(50 cm)": "15.9",
        "平均地溫(100 cm)": "17.1",
        "Year": 1999,
        "Month": 1,
        "行政區": "新竹縣"
    },
    {
        "站名": "苗栗農改",
        "平均氣溫": "15.7",
        "絕對最高氣溫": "25.7",
        "絕對最高氣溫日期": "1/19",
        "絕對最低氣溫": "8.6",
        "絕對最低氣溫日期": "1/15",
        "平均相對濕度 %": "95.9",
        "總降雨量mm": "39.5",
        "平均風速m/s": "2.4",
        "最多風向": "22.5",
        "總日照時數h": "XXX",
        "總日射量MJ/ m2": "XXX",
        "平均地溫(0cm)": "17.8",
        "平均地溫(5cm)": "18.1",
        "平均地溫(10 cm)": "18.3",
        "平均地溫(20 cm)": "18.5",
        "平均地溫(50 cm)": "18.9",
        "平均地溫(100 cm)": "19.9",
        "Year": 1999,
        "Month": 1,
        "行政區": "苗栗縣"
    },
    {
        "站名": "台中農改",
        "平均氣溫": "17.1",
        "絕對最高氣溫": "27.4",
        "絕對最高氣溫日期": "1/19",
        "絕對最低氣溫": "10.7",
        "絕對最低氣溫日期": "1/15",
        "平均相對濕度 %": "83.2",
        "總降雨量mm": "16.0",
        "平均風速m/s": "2.5",
        "最多風向": "360.0",
        "總日照時數h": "166.4",
        "總日射量MJ/ m2": "237.07",
        "平均地溫(0cm)": "19.6",
        "平均地溫(5cm)": "19.9",
        "平均地溫(10 cm)": "20.3",
        "平均地溫(20 cm)": "20.6",
        "平均地溫(50 cm)": "21.0",
        "平均地溫(100 cm)": "21.8",
        "Year": 1999,
        "Month": 1,
        "行政區": "台中市"
    },
```