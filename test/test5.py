import pandas as pd
import numpy as np

# Load the original CSV file
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\filtered_data_output.csv'
data = pd.read_csv(file_path)

# Function to convert values based on the given rules
def custom_convert(value):
    value_str = str(value).strip()
    if value_str == 'XXX' or value_str == '-':
        return np.nan
    if value_str.startswith('-') and value_str[1:].replace('.', '', 1).isdigit():
        return float(value_str)
    if value_str.replace('.', '', 1).isdigit():
        return float(value_str)
    if value_str.startswith('*'):
        return value_str  # keep '*' values as is for further processing
    return np.nan

# Columns to check and convert
columns_to_check = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']

# Apply the custom conversion function to the specified columns
for col in columns_to_check:
    data[col] = data[col].apply(custom_convert)

# Function to replace '*' values with the mean of adjacent years
def replace_star_values(df, columns):
    consecutive_star_years = []

    for col in columns:
        for index, row in df.iterrows():
            if isinstance(row[col], str) and row[col].startswith('*'):
                year = row['Year']
                month = row['Month']
                station = row['站名']

                prev_year_value = df[(df['Year'] == year - 1) & (df['Month'] == month) & (df['站名'] == station)][col]
                next_year_value = df[(df['Year'] == year + 1) & (df['Month'] == month) & (df['站名'] == station)][col]

                if len(prev_year_value) > 0 and len(next_year_value) > 0:
                    prev_year_value = prev_year_value.values[0]
                    next_year_value = next_year_value.values[0]

                    if isinstance(prev_year_value, str) and prev_year_value.startswith('*'):
                        consecutive_star_years.append((year - 1, month, col, station))
                    if isinstance(next_year_value, str) and next_year_value.startswith('*'):
                        consecutive_star_years.append((year + 1, month, col, station))

                    if not (isinstance(prev_year_value, str) and prev_year_value.startswith('*')) and \
                            not (isinstance(next_year_value, str) and next_year_value.startswith('*')):
                        df.at[index, col] = (float(prev_year_value) + float(next_year_value)) / 2

    return df, consecutive_star_years

# Replace '*' values and get list of consecutive star years
data, consecutive_star_years = replace_star_values(data, columns_to_check)

# Check for missing values again
missing_values = data.isnull().sum()
print(missing_values)

# Save the processed data to new files
processed_csv_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed_data.csv'
processed_json_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed__data.json'
data.to_csv(processed_csv_path, index=False, encoding='utf-8-sig')
data.to_json(processed_json_path, orient='records', force_ascii=False)

# Output the list of consecutive star years
consecutive_star_years
