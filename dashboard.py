import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from processing import load_and_clean
from analytics import run_all_analytics

st.set_page_config(page_title="Books Dashboard", layout="wide")

st.title("📊 Books Sales Dashboard")

folders = ["data/DATA1", "data/DATA2", "data/DATA3"]
tabs = st.tabs(["DATA1", "DATA2", "DATA3"])

for tab, folder in zip(tabs, folders):
    with tab:
        st.header(f"Dataset: {folder}")

        
        books, orders, users = load_and_clean(folder)
        results = run_all_analytics(books, orders, users)

        
        st.subheader("Top 5 Revenue Days")
        st.dataframe(results['top_5_days'].style.format({"paid_price": "{:.2f}"}))

        
        st.subheader("Unique Users")
        st.write(results['unique_users'])

        
        st.subheader("Unique Author Sets")
        st.write(results['unique_author_sets'])

        
        st.subheader("Most Popular Authors")
        st.write(results['most_popular_authors'])

        
        st.subheader("Top Customers (all aliases)")
        st.write(results['top_customers'])

        
        st.subheader("Daily Revenue Chart")
        daily = orders.groupby('date')['paid_price'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(daily['date'], daily['paid_price'], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Revenue ($)")
        ax.set_title(f"Daily Revenue - {folder}")
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
