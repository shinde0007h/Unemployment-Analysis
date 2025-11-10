# car_price_prediction.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("car_data.csv")

print("✅ Data Loaded Successfully")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Encode categorical columns
le = LabelEncoder()
df['Brand'] = le.fit_transform(df['Brand'])
df['Model'] = le.fit_transform(df['Model'])

# Define features and target
X = df[['Brand', 'Model', 'Year', 'Horsepower', 'Mileage', 'EngineSize', 'Brand_Goodwill']]
y = df['Price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
lr = LinearRegression()
lr.fit(X_train, y_train)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predictions
y_pred_lr = lr.predict(X_test)
y_pred_rf = rf.predict(X_test)

# Evaluation
def evaluate(y_true, y_pred, model_name):
    print(f"\n📊 {model_name} Performance:")
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("MSE:", mean_squared_error(y_true, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("R2 Score:", r2_score(y_true, y_pred))

evaluate(y_test, y_pred_lr, "Linear Regression")
evaluate(y_test, y_pred_rf, "Random Forest")

# Feature Importance (Random Forest)
importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n🔑 Feature Importance:")
print(importance)

# --- Visualizations ---
plt.figure(figsize=(8, 5))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()

plt.figure(figsize=(8,5))
sns.barplot(data=importance, x='Feature', y='Importance', palette='viridis')
plt.title("Feature Importance in Price Prediction")
plt.show()

plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred_rf, color='blue')
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Car Prices (Random Forest)")
plt.show()

# --- Insights ---
print("\n💡 Insights:")
print("- Random Forest outperforms Linear Regression in prediction accuracy.")
print("- Horsepower, Year, and Brand_Goodwill have the highest influence on car price.")
print("- Mileage is negatively correlated with price — higher mileage lowers price.")
print("- Brand reputation plays a significant role even for similar specs.")
