import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Load the annual averages CSV file
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\annual_averages.csv'
data = pd.read_csv(file_path)

# Function to visualize average daily sunshine hours for each region
def visualize_all_regions_sunshine_hours():
    regions = data['行政區'].unique()
    
    plt.figure(figsize=(15, 10))
    
    for region in regions:
        filtered_data = data[data['行政區'] == region]
        plt.plot(filtered_data['Year'], filtered_data['平均每日日照時數'], marker='o', linestyle='-', label=region)
    
    plt.title('Annual Average Daily Sunshine Hours for All Regions', fontproperties=font_properties)
    plt.xlabel('Year', fontproperties=font_properties)
    plt.ylabel('Average Daily Sunshine Hours (hours)', fontproperties=font_properties)
    plt.legend(prop=font_properties, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Path to the custom font
font_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# Visualize average daily sunshine hours for all regions
visualize_all_regions_sunshine_hours()
