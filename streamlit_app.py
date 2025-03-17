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

st.dataframe(df)

# Bar chart (filtered or not)
st.bar_chart(df, x="Category", y="Sales")

# Aggregated chart
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")
