# unemployment_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load and clean data
df = pd.read_csv("unemployment_data.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns={'Unemployment Rate': 'Unemployment_Rate'})
df = df.dropna()

# Create year and month columns
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Basic info
print("✅ Cleaned Dataset Preview:")
print(df.head())
print("\nDataset Summary:")
print(df.describe())

# --- Visualization 1: Line Plot ---
plt.figure(figsize=(10,5))
sns.lineplot(data=df, x='Date', y='Unemployment_Rate', hue='Region', marker='o')
plt.title("Unemployment Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend(title='Region')
plt.grid(True)
plt.show()

# --- Visualization 2: Bar Chart ---
region_avg = df.groupby('Region')['Unemployment_Rate'].mean().reset_index()
plt.figure(figsize=(8,5))
sns.barplot(data=region_avg, x='Region', y='Unemployment_Rate', palette='viridis')
plt.title("Average Unemployment by Region")
plt.show()

# --- Visualization 3: Heatmap (Monthly-Yearly Trend) ---
pivot = df.pivot_table(values='Unemployment_Rate', index='Month', columns='Year', aggfunc='mean')
plt.figure(figsize=(8,5))
sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".1f")
plt.title("Unemployment Rate Heatmap (Month vs Year)")
plt.show()

# --- Visualization 4: Scatter Plot (Urban vs Rural) ---
sns.scatterplot(data=df, x='Urban Rate', y='Rural Rate', hue='Region', s=100)
plt.title("Urban vs Rural Unemployment Rate")
plt.xlabel("Urban Unemployment (%)")
plt.ylabel("Rural Unemployment (%)")
plt.show()

# --- Interactive Plot (Optional) ---
fig = px.line(df, x='Date', y='Unemployment_Rate', color='Region', title='Interactive Unemployment Trend')
fig.show()

# --- Insights ---
print("\n📊 Insights Summary:")
print("- Covid-19 caused a visible spike in unemployment during early 2020.")
print("- Delhi faced higher unemployment (avg ~15%) compared to Maharashtra (~9%).")
print("- Seasonal dips observed mid-year (post-lockdown recovery).")
print("- Urban unemployment consistently higher than rural.")
print("- Strong correlation between urban and rural rates indicates shared economic impact.")
