import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Load the data
# file_path = r'D:\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
file_path = r'D:\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Print the columns to check their names
print("Columns in the dataset:", data.columns)

# Load the custom font
font_path = r'D:\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# Columns to check and convert
columns_to_convert = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總降雨量mm']

# Verify which columns exist in the dataset
existing_columns_to_check = [col for col in columns_to_convert if col in data.columns]

# Convert all relevant columns to float
for col in existing_columns_to_check:
    data[col] = data[col].apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values in the relevant columns
data = data.dropna(subset=existing_columns_to_check)

# Calculate IQR and determine upper and lower bounds for outliers
def calculate_iqr_bounds(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    return lower, upper

# Apply IQR bounds to filter outliers
outliers = {}
for col in existing_columns_to_check:
    lower, upper = calculate_iqr_bounds(data[col])
    outliers[col] = data[(data[col] < lower) | (data[col] > upper)]
    data = data[(data[col] >= lower) & (data[col] <= upper)]

# Plotting the boxplot
plt.figure(figsize=(14, 7))
boxplot = plt.boxplot([data[col] for col in existing_columns_to_check],
                      labels=existing_columns_to_check,
                      patch_artist=True, showfliers=True, boxprops=dict(facecolor='lightblue'))

# Adding titles and labels
plt.title('Temperature and Rainfall Boxplot', fontproperties=font_properties)
plt.xlabel('Data Type', fontproperties=font_properties)
plt.ylabel('Value', fontproperties=font_properties)
plt.grid(True)

# Apply font properties to x and y ticks
for label in plt.gca().get_xticklabels():
    label.set_fontproperties(font_properties)
for label in plt.gca().get_yticklabels():
    label.set_fontproperties(font_properties)

# Show and save the plot
plt.savefig(r'D:\github\MLproject_Solar_Irradiance\test\temperature_rainfall_boxplot.png')
plt.show()

# Display outliers
for column, outlier_data in outliers.items():
    print(f"Outliers for {column}:")
    print(outlier_data)
