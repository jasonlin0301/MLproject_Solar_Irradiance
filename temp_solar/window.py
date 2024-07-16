import tkinter as tk
from tkinter import ttk
import pandas as pd

# Load the data
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Remove any non-numeric characters and convert to float
data['總日照時數h'] = pd.to_numeric(data['總日照時數h'], errors='coerce')
data['總日射量MJ/ m2'] = pd.to_numeric(data['總日射量MJ/ m2'], errors='coerce')

# Calculate daily values, ignoring NaN values
data['每日日照時數h'] = data['總日照時數h'] / 30  # Assuming 30 days in a month for simplicity
data['每日日射量MJ/m2'] = data['總日射量MJ/ m2'] / 30  # Assuming 30 days in a month for simplicity

# Function to display data for the selected area
def show_data(event):
    selected_area = combo.get()
    filtered_data = data[data['行政區'] == selected_area]
    if not filtered_data.empty:
        average_temp = filtered_data['平均氣溫'].mean()
        daily_sunshine_hours = filtered_data['每日日照時數h'].mean()
        daily_solar_radiation = filtered_data['每日日射量MJ/m2'].mean()
        result.set(f"平均溫度: {average_temp:.2f} °C\n每日日照時數: {daily_sunshine_hours:.2f} h\n每日日射量: {daily_solar_radiation:.2f} MJ/m2")
        
        # Display filtered data for debugging
        debug_info.set(f"Filtered Data:\n{filtered_data.to_string(index=False)}")
    else:
        result.set("無數據")
        debug_info.set("")

# Create main window
root = tk.Tk()
root.title("區域氣象資料")
root.geometry("600x400")

# Label for dropdown
label = ttk.Label(root, text="選擇區域:")
label.pack(pady=10)

# Dropdown menu
areas = data['行政區'].unique()
combo = ttk.Combobox(root, values=areas)
combo.pack(pady=10)
combo.bind("<<ComboboxSelected>>", show_data)

# Result label
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result)
result_label.pack(pady=10)

# Debug info label
debug_info = tk.StringVar()
debug_label = ttk.Label(root, textvariable=debug_info)
debug_label.pack(pady=10)

# Run the main loop
root.mainloop()
