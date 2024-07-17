import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 讀取資料
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
data = pd.read_csv(file_path)

# 設定字體路徑
font_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# 定義轉換函數，將帶有*號的數據轉換為浮點數
def to_float(value):
    try:
        if isinstance(value, str) and '*' in value:
            return float(value.replace('*', ''))
        return float(value)
    except ValueError:
        return np.nan

# 將轉換函數應用到相關的列
columns_to_check = ['平均氣溫', '總日照時數h', '總日射量MJ/ m2']
for col in columns_to_check:
    data[col] = data[col].apply(to_float)

# 刪除包含NaN值的行
data = data.dropna(subset=columns_to_check)

# 去除離散值（使用IQR法）
Q1 = data[columns_to_check].quantile(0.25)
Q3 = data[columns_to_check].quantile(0.75)
IQR = Q3 - Q1
data = data[~((data[columns_to_check] < (Q1 - 1.5 * IQR)) | (data[columns_to_check] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 定義自變量和應變量
X = data[['總日射量MJ/ m2', '平均氣溫']].values  # 使用總日射量和平均氣溫作為自變量
Y = data['總日照時數h'].values  # 依變量是總日照時數

# 標準化特徵數據
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 將資料分成訓練集和測試集
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.3, random_state=0)

# 擬合隨機森林回歸模型
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=0)
rf_regressor.fit(X_train, Y_train)

# 使用交叉驗證評估模型
cv_scores = cross_val_score(rf_regressor, X_train, Y_train, cv=5, scoring='neg_mean_squared_error')
print(f'交叉驗證均方誤差: {-cv_scores.mean()}')

# 預測並評估模型
Y_pred = rf_regressor.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

print(f'均方誤差: {mse}')
print(f'R平方值: {r2}')

# 繪製結果圖
plt.scatter(Y_test, Y_pred, color='blue', label='實際值 vs 預測值')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], color='red', linewidth=2, label='理想預測')
plt.xlabel('實際總日照時數', fontproperties=font_properties)
plt.ylabel('預測總日照時數', fontproperties=font_properties)
plt.title('隨機森林回歸: 總日射量和平均氣溫 vs 總日照時數', fontproperties=font_properties)
plt.legend(prop=font_properties)

# 在圖表上添加均方誤差和R平方值
plt.text(Y_test.min(), Y_test.max(), f'均方誤差: {mse:.2f}\nR平方值: {r2:.2f}', 
         fontsize=12, verticalalignment='top', fontproperties=font_properties)

output_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\random_forest_regression.png'
plt.savefig(output_path, bbox_inches='tight')

plt.show()
