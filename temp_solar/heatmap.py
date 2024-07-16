import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 讀取數據
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# 將所有相關列轉換為浮點數
columns_to_convert = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']
for col in columns_to_convert:
    data[col] = data[col].apply(pd.to_numeric, errors='coerce')

# 刪除相關列中包含任何NaN值的行
data = data.dropna(subset=columns_to_convert)

# 計算相關矩陣
correlation_matrix = data[columns_to_convert].corr()

# 加載自定義字體
font_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# 更新matplotlib的字體屬性
plt.rcParams['font.family'] = font_properties.get_name()

# 生成熱圖
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

# 使用自定義字體設置標題和標籤
plt.title('Correlation Heatmap of Weather Attributes', fontproperties=font_properties)
plt.xticks(fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)

# 保存圖片
output_path = os.path.join(os.path.dirname(file_path), 'correlation_heatmap.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
