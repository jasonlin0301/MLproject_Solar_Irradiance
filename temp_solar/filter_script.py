
import pandas as pd

# Load the original CSV file
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\Raw_Data\_modified_data_1999_to_2024.csv'
data = pd.read_csv(file_path)

# Define the columns to keep
columns_to_keep = ['站名', '平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2', 'Year', 'Month', '行政區']

# Filter the data to keep only the specified columns
filtered_data = data[columns_to_keep]

# Save the filtered data to a new CSV file
filtered_csv_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\filtered_data_output.csv'
filtered_data.to_csv(filtered_csv_path, index=False, encoding='utf-8-sig')

# Save the filtered data to a new JSON file
filtered_json_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\filtered_data_output.json'
filtered_data.to_json(filtered_json_path, orient='records', force_ascii=False)
