import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="WRDS Stock Analysis Tool", layout="wide")
st.title("WRDS Stock Data Analysis Tool")

st.sidebar.header("Parameters")
wrds_username = st.sidebar.text_input("WRDS Username", value="your_username")
permno = st.sidebar.number_input("Stock PERMNO", value=14593, step=1)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

@st.cache_data
def load_wrds_data(username, permno, start, end):
    db = wrds.Connection(wrds_username=username)
    query = f"""
        select date, prc, ret, shrout, vol
        from crsp.dsf
        where permno = {permno}
        and date between '{start}' and '{end}'
        order by date
    """
    df = db.raw_sql(query)
    db.close()

    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["prc", "ret"])
    df["price"] = df["prc"].abs()
    df = df.sort_values("date")
    return df

if st.sidebar.button("Load WRDS Data"):
    with st.spinner("Connecting to WRDS..."):
        try:
            df = load_wrds_data(
                wrds_username,
                permno,
                start_date,
                end_date
            )

            st.subheader("📊 Data Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latest Price", f"${df['price'].iloc[-1]:.2f}")
            with col2:
                st.metric("Latest Daily Return", f"{df['ret'].iloc[-1]:.2%}")
            with col3:
                st.metric("Observations", len(df))

            st.subheader("Stock Price Trend")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df["date"], df["price"], label="Price")
            ax.set_title(f"PERMNO {permno} Price Trend")
            ax.legend()
            st.pyplot(fig)

            st.subheader("Daily Return Distribution")
            fig2, ax2 = plt.subplots(figsize=(10, 3))
            ax2.hist(df["ret"].dropna(), bins=50, alpha=0.7)
            ax2.set_title("Return Distribution")
            st.pyplot(fig2)

            st.subheader("Data Preview")
            st.dataframe(df.head(10))

            st.success("✅ WRDS data analysis completed successfully!")

        except Exception as e:
            st.error(f"Failed to connect to WRDS: {str(e)}")