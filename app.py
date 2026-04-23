import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="WRDS Stock Analysis Tool", layout="wide")
st.title("WRDS Stock Data Analysis Tool")

# Sidebar Inputs
st.sidebar.header("Parameters")
wrds_username = st.sidebar.text_input("WRDS Username", value="your_username")

# 🔹 Multiple PERMNO input (comma separated)
permno_input = st.sidebar.text_input("Stock PERMNOs (comma separated, e.g. 14593,10078)", value="14593")

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

# Load WRDS Data with caching
@st.cache_data
def load_wrds_data(username, permno_list, start, end):
    db = wrds.Connection(wrds_username=username)
    all_dfs = []

    for permno in permno_list:
        query = f"""
            select date, permno, prc, ret, shrout, vol
            from crsp.dsf
            where permno = {permno}
            and date between '{start}' and '{end}'
            order by date
        """
        df = db.raw_sql(query)
        if not df.empty:
            all_dfs.append(df)

    db.close()

    if not all_dfs:
        return pd.DataFrame()

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df["date"] = pd.to_datetime(final_df["date"])
    final_df = final_df.dropna(subset=["prc", "ret"])
    final_df["price"] = final_df["prc"].abs()
    final_df = final_df.sort_values(["permno", "date"])
    return final_df

# Parse PERMNO list
def parse_permnos(input_str):
    try:
        return [int(p.strip()) for p in input_str.split(",") if p.strip().isdigit()]
    except:
        return []

permno_list = parse_permnos(permno_input)

# Run Analysis
if st.sidebar.button("Load WRDS Data"):
    if not permno_list:
        st.error("Please enter valid PERMNO numbers separated by commas.")
    else:
        with st.spinner("Connecting to WRDS..."):
            try:
                df = load_wrds_data(
                    wrds_username,
                    permno_list,
                    start_date,
                    end_date
                )

                if df.empty:
                    st.warning("No data returned for the selected PERMNOs and date range.")
                else:
                    st.subheader("📊 Data Overview")
                    st.metric("Total Observations", len(df))
                    st.metric("Number of Stocks", int(df['permno'].nunique()))

                    # Price Trend (multiple PERMNOs in one plot)
                    st.subheader("Stock Price Trend")
                    fig, ax = plt.subplots(figsize=(12, 5))
                    for pno in df['permno'].unique():
                        sub = df[df['permno'] == pno]
                        ax.plot(sub["date"], sub["price"], label=f"PERMNO {pno}")
                    ax.set_title("Price Trend by Stock")
                    ax.legend()
                    st.pyplot(fig)

                    # Return Distribution
                    st.subheader("Daily Return Distribution")
                    fig2, ax2 = plt.subplots(figsize=(10, 3))
                    ax2.hist(df["ret"].dropna(), bins=50, alpha=0.7)
                    ax2.set_title("Overall Return Distribution")
                    st.pyplot(fig2)

                    # Data Preview
                    st.subheader("Data Preview")
                    st.dataframe(df.head(15))

                    st.success("✅ WRDS data analysis completed successfully!")

            except Exception as e:
                st.error(f"Failed to connect to WRDS: {str(e)}")