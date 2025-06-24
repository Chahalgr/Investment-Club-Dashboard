import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv('cleaned_corporate_positions.csv')

# Convert numeric columns
numeric_columns = ['Qty', 'Price', 'Price Chng $', 'Price Chng %',
                   'Mkt Val', 'Day Chng $', 'Day Chng %',
                   'Cost Basis', 'Gain $', 'Gain %', '% of Acct']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Sidebar filters
st.sidebar.title("📊 Portfolio Filters")
selected_rating = st.sidebar.multiselect("Select Ratings", options=df['Ratings'].unique(), default=df['Ratings'].unique())
selected_type = st.sidebar.multiselect("Select Security Type", options=df['Security Type'].unique(), default=df['Security Type'].unique())

df_filtered = df[df['Ratings'].isin(selected_rating) & df['Security Type'].isin(selected_type)]

# Main dashboard
st.title("💼 SIC Portfolio Dashboard")

# Top-level metrics
total_value = df_filtered['Mkt Val'].sum()
total_gain = df_filtered['Gain $'].sum()
avg_gain_pct = (df_filtered['Gain $'].sum()/ df_filtered['Cost Basis'].sum())  if df_filtered['Cost Basis'].sum() != 0 else 0

st.metric("Total Market Value", f"${total_value:,.2f}")
st.metric("Total Gain ($)", f"${total_gain:,.2f}")
st.metric("Average Gain (%)", f"{avg_gain_pct:.2%}")

# Pie chart - Allocation by Symbol
st.subheader("📌 Portfolio Allocation")
fig_pie = px.pie(df_filtered, names='Symbol', values='Mkt Val', title='Allocation by Symbol')
st.plotly_chart(fig_pie)

# Bar chart - Top Gainers
st.subheader("📈 Top Gainers")
top_gainers = df_filtered.sort_values(by='Gain $', ascending=False).head(10)
fig_bar = px.bar(top_gainers, x='Symbol', y='Gain $', color='Gain $', title='Top 10 Gainers', text='Gain $')
st.plotly_chart(fig_bar)

# Data table
st.subheader("📋 Detailed Positions")
st.dataframe(df_filtered)

# Footer
st.markdown("---")
st.markdown("Data Source: Corporate-Positions-2025-03-10")
