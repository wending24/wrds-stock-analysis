import streamlit as st
import wrds
import pandas as pd
from datetime import date
import plotly.express as px

# --------------------------
# WRDS Connection (Cached)
# --------------------------
@st.cache_resource
def get_wrds_connection():
    try:
        conn = wrds.Connection()
        return conn
    except Exception as e:
        st.error(f"WRDS connection failed: {e}")
        return None

# --------------------------
# Load Data from WRDS (Fixed Date Format)
# --------------------------
def load_wrds_data(conn, permnos, start_date, end_date):
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    permno_list = ",".join([str(p) for p in permnos])

    query = f"""
        SELECT permno, date, prc, ret, shrout
        FROM crsp.dsf
        WHERE permno IN ({permno_list})
          AND date >= '{start_str}'
          AND date <= '{end_str}'
        ORDER BY permno, date;
    """

    try:
        df = conn.raw_sql(query)
        # Convert date column to datetime for plotting
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# --------------------------
# Streamlit UI
# --------------------------
st.title("WRDS Stock Data Loader & Visualizer")

permno_input = st.text_input("PERMNOs (comma-separated, e.g. 12490, 10107)", value="12490,10107")

start_date = st.date_input("Start Date", date(2023, 1, 1))
end_date = st.date_input("End Date", date(2023, 12, 31))

if st.button("Load WRDS Data"):
    conn = get_wrds_connection()
    if conn is None:
        st.stop()

    try:
        permnos = [int(p.strip()) for p in permno_input.split(",")]
    except:
        st.error("PERMNOs must be integers separated by commas.")
        st.stop()

    with st.spinner("Loading data..."):
        df = load_wrds_data(conn, permnos, start_date, end_date)

    if df.empty:
        st.warning("No data returned. Check PERMNOs or date range.")
    else:
        st.success(f"Loaded {df.permno.nunique()} stocks, {len(df)} rows.")
        st.dataframe(df)

        # --------------------------
        # 1. Daily Price Chart
        # --------------------------
        st.subheader("Daily Stock Price (prc)")
        fig_price = px.line(
            df, 
            x="date", 
            y="prc", 
            color="permno",
            title="Daily Stock Price by PERMNO",
            labels={"prc": "Price (USD)", "date": "Date", "permno": "PERMNO"}
        )
        st.plotly_chart(fig_price, use_container_width=True)

        # --------------------------
        # 2. Daily Return Chart
        # --------------------------
        st.subheader("Daily Stock Return (ret)")
        fig_ret = px.line(
            df, 
            x="date", 
            y="ret", 
            color="permno",
            title="Daily Stock Return by PERMNO",
            labels={"ret": "Daily Return", "date": "Date", "permno": "PERMNO"}
        )
        st.plotly_chart(fig_ret, use_container_width=True)

        # --------------------------
        # 3. Cumulative Return Chart
        # --------------------------
        st.subheader("Cumulative Return")
        # Calculate cumulative return for each stock
        df['cumulative_ret'] = df.groupby('permno')['ret'].apply(lambda x: (1 + x).cumprod() - 1).reset_index(drop=True)
        fig_cum_ret = px.line(
            df, 
            x="date", 
            y="cumulative_ret", 
            color="permno",
            title="Cumulative Return by PERMNO",
            labels={"cumulative_ret": "Cumulative Return", "date": "Date", "permno": "PERMNO"}
        )
        st.plotly_chart(fig_cum_ret, use_container_width=True)

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Download CSV", csv, "wrds_data.csv", "text/csv")