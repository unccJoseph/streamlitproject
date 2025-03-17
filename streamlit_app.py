import streamlit as st
import pandas as pd

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

# Dropdown for Category selection
category_options = ["All"] + df["Category"].unique().tolist()
selected_category = st.selectbox("Select a Category:", category_options)

# Filter data by selected category if not "All"
filtered_df = df[df["Category"] == selected_category] if selected_category != "All" else df

# Multi-select for Sub_Category within the selected Category
sub_category_options = filtered_df["Sub_Category"].unique().tolist()
selected_sub_categories = st.multiselect("Select Sub-Categories:", sub_category_options, default=sub_category_options)

# Filter by selected sub-categories
filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_sub_categories)]

# Calculate metrics
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Calculate overall average profit margin across all products
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0

# Calculate delta for profit margin
profit_margin_delta = profit_margin - overall_profit_margin

# Display metrics
st.write("### (4) Key Metrics for Selected Items")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%", f"{profit_margin_delta:.2f}%")

st.dataframe(filtered_df)

# Bar chart (filtered)
st.bar_chart(filtered_df, x="Category", y="Sales")

# Aggregated chart
st.dataframe(filtered_df.groupby("Category").sum())
st.bar_chart(filtered_df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
filtered_df.set_index('Order_Date', inplace=True)
sales_by_month = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.write("### (3) Sales Over Time for Selected Items")
st.line_chart(sales_by_month, y="Sales")

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")
