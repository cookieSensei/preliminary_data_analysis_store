import streamlit as st
import pandas as pd
import plotly.express as px
import re
import os


# Load the data
for i in os.listdir():
    if re.search("xls", i.lower()):
        print(i)
        df = pd.read_excel(i, engine="xlrd")



# Convert percentages to float
months = ['Dec', 'Nov', 'Oct', 'Sep', 'Aug']
df[months] = df[months].astype(float)

# Add Avg_5M and change from Nov to Dec
df['Avg_5M'] = df[months].mean(axis=1)
df['Change_Nov_to_Dec'] = df['Dec'] - df['Nov']

# Monthly trend (Aug–Dec)
monthly_avg = df[months].mean().round(3)
monthly_df = pd.DataFrame({
    'Month': ['Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
    'Avg_Performance': monthly_avg.values * 100  # Convert to %
})

# Branch-wise performance
branch_perf = df.groupby('Branch')[months].mean().round(3)
branch_perf['Avg_5M'] = branch_perf.mean(axis=1).round(3)
branch_perf = branch_perf.sort_values('Avg_5M', ascending=False)
branch_df = branch_perf.reset_index()[['Branch', 'Avg_5M']]
branch_df['Avg_5M'] = branch_df['Avg_5M'] * 100

# Top 10 and bottom 10 stores
top_10 = df[['Store_Name', 'Branch', 'Avg_5M']].sort_values('Avg_5M', ascending=False).head(10).copy()
top_10['Avg_5M'] = top_10['Avg_5M'] * 100

bottom_10 = df[['Store_Name', 'Branch', 'Avg_5M']].sort_values('Avg_5M', ascending=True).head(10).copy()
bottom_10['Avg_5M'] = bottom_10['Avg_5M'] * 100

# Streamlit app
st.set_page_config(page_title='Jumbo Company Dashboard', layout='wide')
st.title('Jumbo Company Store Performance Dashboard (Aug–Dec)')

# Sidebar filters
st.sidebar.header('Filters')
selected_branch = st.sidebar.selectbox('Filter by Branch', ['All'] + sorted(df['Branch'].unique().tolist()))

if selected_branch != 'All':
    filtered_df = df[df['Branch'] == selected_branch]
else:
    filtered_df = df

# KPIs
st.subheader('Key Metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Avg (Dec)', f'{df["Dec"].mean()*100:.1f}%')
col2.metric('Avg (Nov)', f'{df["Nov"].mean()*100:.1f}%')
col3.metric('Avg (Oct)', f'{df["Oct"].mean()*100:.1f}%')
col4.metric('Avg (Sep)', f'{df["Sep"].mean()*100:.1f}%')
col5.metric('Avg (Aug)', f'{df["Aug"].mean()*100:.1f}%')

# Charts
st.subheader('Monthly Trend (All Stores)')
fig_trend = px.line(monthly_df, x='Month', y='Avg_Performance',
                   title='Average Performance Trend (Aug–Dec)',
                   markers=True, text='Avg_Performance')
fig_trend.update_traces(texttemplate='%{text:.1f}%', textposition='top center')
fig_trend.update_layout(yaxis_title='Avg Performance (%)')
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader('Performance by Branch')
fig_branch = px.bar(branch_df, x='Branch', y='Avg_5M',
                  title='Average Performance by Branch (Aug–Dec)',
                  text='Avg_5M')
fig_branch.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_branch.update_layout(yaxis_title='Avg 5M Performance (%)')
st.plotly_chart(fig_branch, use_container_width=True)

st.subheader('Top 10 Stores (5‑Month Avg)')
fig_top = px.bar(top_10, y='Store_Name', x='Avg_5M', orientation='h',
                title='Top 10 Stores by 5‑Month Average Performance',
                text='Avg_5M')
fig_top.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
fig_top.update_layout(xaxis_title='Avg 5M Performance (%)')
st.plotly_chart(fig_top, use_container_width=True)

st.subheader('Bottom 10 Stores (5‑Month Avg)')
fig_bottom = px.bar(bottom_10, y='Store_Name', x='Avg_5M', orientation='h',
                   title='Bottom 10 Stores by 5‑Month Average Performance',
                   text='Avg_5M')
fig_bottom.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
fig_bottom.update_layout(xaxis_title='Avg 5M Performance (%)')
st.plotly_chart(fig_bottom, use_container_width=True)

# Data table
st.subheader('Raw Data')
st.dataframe(filtered_df[['Branch', 'Store_Name'] + months + ['Avg_5M', 'Change_Nov_to_Dec']].round(3))

# Download button
st.download_button(
    label='Download Cleaned Data as CSV',
    data=df.to_csv(index=False),
    file_name='Jumbo_Company_Analysis.csv',
    mime='text/csv'
)

# Run the app with: streamlit run dashboard.py
st.markdown('---')
st.markdown('Dashboard built with Streamlit and Plotly. Run with `streamlit run dashboard.py`')
