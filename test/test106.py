import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

# 從CSV加載數據
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# 顯示選定圖像的函數
def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((800, 600))  # 調整圖像大小以適應窗口
    img = ImageTk.PhotoImage(image)
    img_label.config(image=img)
    img_label.image = img

# 創建主窗口
root = tk.Tk()
root.title("CSV查看器與圖片")

# 創建Treeview小部件
tree = ttk.Treeview(root)
tree["columns"] = list(data.columns)
tree["show"] = "headings"

for col in data.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

# 將數據添加到Treeview
for index, row in data.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(side="left", fill="y")

# 創建按鈕和圖像顯示的框架
frame = ttk.Frame(root)
frame.pack(side="right", fill="both", expand=True)

# 創建顯示圖像按鈕
button_texts = [
    ("統計摘要", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\data.png"),
    ("盒鬚圖", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\boxplot_no_outliers.png"),
    ("每日平均日照時數", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\line_H.png"),
    ("平均日照時數常態分佈", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\normaldistribution_H.png"),
    ("每日平均太陽輻射量", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\line_R.png"),
    ("平均日射量常態分佈", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\normaldiszribution_R.png"),
    ("熱力圖", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\heatmap.png"),
    ("線性回歸", r"C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\linear_regression.png"),
]

for text, path in button_texts:
    button = ttk.Button(frame, text=text, command=lambda p=path: display_image(p))
    button.pack(fill="x")

# 顯示圖像的標籤
img_label = ttk.Label(frame)
img_label.pack(fill="both", expand=True)

# 引入並顯示計算器視窗
def open_calculator():
    import calculator
    calculator.main()

calculator_button = ttk.Button(frame, text="開啟計算器", command=open_calculator)
calculator_button.pack(fill="x")

# 運行應用程序
root.mainloop()
