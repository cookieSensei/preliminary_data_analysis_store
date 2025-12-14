Jumbo & Company
Device Insurance Attach Rate Analysis
Data Science Internship Assignment
December 2025


This report presents a comprehensive analysis of device insurance attach rates across Jumbo & Company stores. The analysis covers 163 stores across 6 branches over a 5-month period (August to December 2025). The primary objective is to understand performance trends, identify top and bottom performers, and forecast future attach rates.

# Monthly attach rate
 <img width="975" height="581" alt="image" src="https://github.com/user-attachments/assets/c1497beb-6667-46eb-b015-021ae954237c" />


# Branch Performance Analysis
<img width="975" height="483" alt="image" src="https://github.com/user-attachments/assets/2bdf02d8-cc28-4023-b6f3-875ef3ccaa94" />


# Top 10 stores

 

7. Bottom 10 Performing Stores
Code to generate bottom 10 stores chart:
# Bottom 10 stores
bottom_10 = df.nsmallest(10, 'Avg_5M')[['Store_Name', 'Branch', 'Avg_5M']].sort_values('Avg_5M')

plt.figure(figsize=(12, 8))
plt.barh(bottom_10['Store_Name'], bottom_10['Avg_5M'], color='#e74c3c')
plt.xlabel('Average Attach Rate (%)')
plt.title('Bottom 10 Stores', fontsize=14, fontweight='bold')
for i, v in enumerate(bottom_10['Avg_5M']):
    plt.text(v + 0.2, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()
 

8. Performance Distribution Analysis
Code to generate performance distribution chart:
# Store categorization
bins = [0, 15, 25, 35, 100]
labels = ['Poor', 'Below Average', 'Average', 'Excellent']
df['Category'] = pd.cut(df['Avg_5M'], bins=bins, labels=labels)
cat_dist = df['Category'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(cat_dist.values, labels=cat_dist.index, autopct='%1.1f%%', startangle=90)
plt.title('Store Performance Distribution', fontsize=14, fontweight='bold')
plt.axis('equal')
plt.show()
 

9. Time Series Forecast - January 2026
Code to generate time series forecast:
# Time series analysis and forecast
date_map = {'Aug':1, 'Sep':2, 'Oct':3, 'Nov':4, 'Dec':5}
ts_data = pd.melt(df, id_vars=['Store_Name', 'Branch'], 
                  value_vars=months, var_name='Month', value_name='Rate')
ts_data['Time'] = ts_data['Month'].map(date_map)
ts_data['Rate'] = ts_data['Rate'] * 100

def forecast_january(store_data):
    X = store_data['Time'].values.reshape(-1, 1)
    y = store_data['Rate'].values
    model = LinearRegression().fit(X, y)
    jan_pred = model.predict([[6]])[0]
    return max(0, min(100, jan_pred))

# Forecast for top 5 stores
plt.figure(figsize=(12, 7))
top_stores = df.nlargest(5, 'Avg_5M')
for _, row in top_stores.iterrows():
    store_data = ts_data[ts_data['Store_Name'] == row['Store_Name']].sort_values('Time')
    if len(store_data) == 5:
        X = store_data['Time'].values.reshape(-1, 1)
        y = store_data['Rate'].values
        model = LinearRegression().fit(X, y)

        x_extended = np.arange(1, 7)
        y_pred = model.predict(x_extended.reshape(-1, 1))

        plt.plot(store_data['Time'], y, 'o-', label=row['Store_Name'], linewidth=2)
        plt.plot(6, y_pred[-1], 's', markersize=8)

plt.title('Time Series Forecast - Top 5 Stores (Jan 2026)', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Attach Rate (%)')
plt.xticks([1, 2, 3, 4, 5, 6], ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan (Forecast)'])
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
 

10. Performance Heatmap - Branch by Month
Code to generate performance heatmap:
# Heatmap - Branch performance by month
branch_month = df.groupby('Branch')[months].mean() * 100

plt.figure(figsize=(10, 6))
sns.heatmap(branch_month, annot=True, fmt='.1f', cmap='RdYlGn', cbar_kws={'label': 'Attach Rate (%)'})
plt.title('Branch Performance Heatmap by Month', fontsize=14, fontweight='bold')
plt.ylabel('Branch')
plt.xlabel('Month')
plt.tight_layout()
plt.show()
 

11. Store Distribution by Branch
Code to generate store distribution by branch:
# Store count by branch
branch_stores = df['Branch'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
branch_stores.plot(kind='bar', color='#9467bd')
plt.title('Number of Stores by Branch', fontsize=14, fontweight='bold')
plt.ylabel('Number of Stores')
plt.xlabel('Branch')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(branch_stores):
    plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()
 

12. Summary Statistics
Code to generate summary statistics:
# Summary statistics
print("Monthly Average Attach Rate:")
print(df[months].mean() * 100)
print("\nBranch-wise Performance:")
print(df.groupby('Branch')[months].mean().mean(axis=1) * 100)
print("\nStore Performance Statistics:")
print(df['Avg_5M'].describe())
Monthly Average Attach Rate:
August	September	October	November	December
12.86%	16.73%	17.09%	21.71%	21.72%

Branch-wise Performance (Average):
Branch	Average Attach Rate
Delhi_Ncr	24.37%
Pune	27.65%
Gujarat	13.46%
Thane	14.86%
Telangana	11.83%
Mumbai	17.35%

Store Performance Statistics:
Statistic	Value
Count	163
Mean	18.02%
Std Dev	10.35%
Min	0.00%
25%	11.70%
Median	16.40%
75%	23.50%
Max	62.20%

13. Conclusion
This report presents a detailed analysis of the device insurance attach rates across Jumbo & Company stores. The analysis includes multiple visualizations and statistical summaries generated using Python with matplotlib and seaborn libraries. The code provided demonstrates data loading, processing, and visualization techniques used in data science applications.
