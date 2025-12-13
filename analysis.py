
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

import re
import os


# Load the data
for i in os.listdir():
    if re.search("xls", i.lower()):
        print(i)
        df = pd.read_excel(i, engine="xlrd")



# Data processing
months = ['Dec', 'Nov', 'Oct', 'Sep', 'Aug']
df[months] = df[months].astype(float)
df['Avg_Perf'] = df[months].mean(axis=1) * 100

print(f"Dataset: {len(df)} stores across {df['Branch'].nunique()} branches")

# # Monthly trend
# monthly_avg = df[months].mean() * 100
# fig = px.line(x=months[::-1], y=monthly_avg.values[::-1], 
#               title="Monthly Attach Rate Trend (Aug-Dec 2025)")
# fig.show()

# Time series forecast
date_map = {'Aug':1, 'Sep':2, 'Oct':3, 'Nov':4, 'Dec':5}
ts_data = pd.melt(df, id_vars=['Store_Name','Branch'], 
                  value_vars=months, var_name='Month', value_name='Rate')
ts_data['Time'] = ts_data['Month'].map(date_map)
ts_data['Rate'] = ts_data['Rate'] * 100

def forecast_jan(store_data):
    X = store_data['Time'].values.reshape(-1,1)
    y = store_data['Rate'].values
    model = LinearRegression().fit(X, y)
    return max(0, model.predict([[6]])[0])

# Top 10 store forecasts
top10 = df.nlargest(10, 'Avg_Perf')
forecasts = []
for i, row in top10.iterrows():
    store_data = ts_data[ts_data['Store_Name']==row['Store_Name']]
    jan_fc = forecast_jan(store_data)
    forecasts.append([row['Store_Name'], row['Branch'], 
                     row['Avg_Perf'], jan_fc])

print("\nJANUARY 2026 FORECASTS (Top 10 Stores):")
forecast_df = pd.DataFrame(forecasts, 
    columns=['Store','Branch','5M_Avg','Jan_Forecast']).round(1)
print(forecast_df)

print(f"\nCompany Jan Forecast: {forecast_df['Jan_Forecast'].mean():.1f}%")
