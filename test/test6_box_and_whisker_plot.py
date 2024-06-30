import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Load the data
file_path = r'D:\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Load the custom font
font_path = r'D:\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# Convert all relevant columns to float
columns_to_convert = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫']
for col in columns_to_convert:
    data[col] = data[col].apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values in the relevant columns
data = data.dropna(subset=columns_to_convert)

# Plotting the boxplot
plt.figure(figsize=(14, 7))
boxplot = plt.boxplot([data['平均氣溫'], data['絕對最高氣溫'], data['絕對最低氣溫']],
                      labels=['平均氣溫', '絕對最高氣溫', '絕對最低氣溫'],
                      patch_artist=True, showfliers=True, boxprops=dict(facecolor='lightblue'))

# Adding titles and labels
plt.title('Temperature Boxplot', fontproperties=font_properties)
plt.xlabel('Temperature Type', fontproperties=font_properties)
plt.ylabel('Temperature (°C)', fontproperties=font_properties)
plt.grid(True)

# Apply font properties to x and y ticks
for label in plt.gca().get_xticklabels():
    label.set_fontproperties(font_properties)
for label in plt.gca().get_yticklabels():
    label.set_fontproperties(font_properties)

# Show and save the plot
plt.savefig(r'D:\github\MLproject_Solar_Irradiance\test\temperature_boxplot.png')
plt.show()

# Extract outliers
outliers = {}
for i, column in enumerate(columns_to_convert):
    outliers[column] = data[data[column].isin(boxplot['fliers'][i].get_ydata())]

# Display outliers
for column, outlier_data in outliers.items():
    print(f"Outliers for {column}:")
    print(outlier_data)
