import tkinter as tk
from tkinter import ttk
import pandas as pd

# 加載數據
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# 移除任何非數字字符並轉換為浮點數
data['總日照時數h'] = pd.to_numeric(data['總日照時數h'], errors='coerce')
data['總日射量MJ/ m2'] = pd.to_numeric(data['總日射量MJ/ m2'], errors='coerce')

# 計算每日值，忽略NaN值
data['每日日照時數h'] = data['總日照時數h'] / 30  # 簡單起見，假設每月30天
data['每日日射量MJ/m2'] = data['總日射量MJ/ m2'] / 30  # 簡單起見，假設每月30天

# 去除選項中的中括號和引號
data['行政區'] = data['行政區'].str.strip("[]''")

# 顯示選定區域數據的函數
def show_data(event):
    selected_area = combo.get()
    filtered_data = data[data['行政區'] == selected_area]
    if not filtered_data.empty:
        average_temp = filtered_data['平均氣溫'].mean()
        daily_sunshine_hours = filtered_data['每日日照時數h'].mean()
        daily_solar_radiation = filtered_data['每日日射量MJ/m2'].mean()
        result.set(f"平均溫度: {average_temp:.2f} °C\n每日日照時數: {daily_sunshine_hours:.2f} h\n每日日射量: {daily_solar_radiation:.2f} MJ/m2")
        
        # 顯示過濾後的數據以便調試
        debug_info.set(f"過濾後的數據:\n{filtered_data.to_string(index=False)}")
    else:
        result.set("無數據")
        debug_info.set("")

# 創建主窗口
root = tk.Tk()
root.title("區域氣象資料")
root.geometry("600x400")

# 下拉菜單的標籤
label = ttk.Label(root, text="選擇區域:")
label.pack(pady=10)

# 下拉菜單
areas = data['行政區'].unique()
combo = ttk.Combobox(root, values=areas)
combo.pack(pady=10)
combo.bind("<<ComboboxSelected>>", show_data)

# 顯示結果的標籤
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result)
result_label.pack(pady=10)

# 顯示調試信息的標籤
debug_info = tk.StringVar()
debug_label = ttk.Label(root, textvariable=debug_info)
debug_label.pack(pady=10)

# 運行主循環
root.mainloop()
