import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the data
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed_data.csv'
data = pd.read_csv(file_path)

# Function to convert values to float, replace non-numeric values with NaN
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return np.nan

# Apply the conversion function to the relevant columns
data['絕對最高氣溫'] = data['絕對最高氣溫'].apply(to_float)

# Drop rows with NaN values in 絕對最高氣溫
data = data.dropna(subset=['絕對最高氣溫'])

# Define the independent (Year) and dependent (絕對最高氣溫) variables
X = data[['Year']].values.reshape(-1, 1)  # Reshape for sklearn
Y = data['絕對最高氣溫'].values

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Fit the Linear Regression model
linear_regressor = LinearRegression()
linear_regressor.fit(X_train, Y_train)

# Predict and evaluate the model
Y_pred = linear_regressor.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Ensure plots are displayed
plt.figure(figsize=(10, 6))
plt.scatter(X_test, Y_test, color='blue', label='Actual')
plt.plot(X_test, Y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('Year')
plt.ylabel('絕對最高氣溫')
plt.title('Linear Regression: Year vs 絕對最高氣溫')
plt.legend()
plt.grid(True)
plt.show()
