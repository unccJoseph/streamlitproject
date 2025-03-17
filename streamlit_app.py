import streamlit as st
import pandas as pd

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

# Dropdown for Category selection
category_options = ["All"] + df["Category"].unique().tolist()
selected_category = st.selectbox("Select a Category:", category_options)

# Filter data by selected category if not "All"
if selected_category != "All":
    df = df[df["Category"] == selected_category]

# Multi-select for Sub_Category within the selected Category
sub_category_options = df["Sub_Category"].unique().tolist()
selected_sub_categories = st.multiselect("Select Sub-Categories:", sub_category_options, default=sub_category_options)

# Filter by selected sub-categories
df = df[df["Sub_Category"].isin(selected_sub_categories)]

# Calculate metrics
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Display metrics
st.write("### (4) Key Metrics for Selected Items")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")

st.dataframe(df)

# Bar chart (filtered)
st.bar_chart(df, x="Category", y="Sales")

# Aggregated chart
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.write("### (3) Sales Over Time for Selected Items")
st.line_chart(sales_by_month, y="Sales")

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")
