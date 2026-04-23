# WRDS Stock Analysis Tool
An interactive financial data analysis tool using the WRDS database, built with Streamlit.

## Author
Your Name
Student ID

## Project Overview
This tool connects to WRDS (Wharton Research Data Services), retrieves stock data from CRSP, and provides interactive visualizations and summary statistics for financial analysis.

## Data Source
- CRSP Daily Stock File (dsf)
- Period: 2020–2024
- Identifier: PERMNO

## Features
- Secure connection to WRDS via SQL query
- Stock price trend visualization
- Daily return distribution histogram
- Automatic data cleaning and missing value handling
- Interactive web interface with real-time metrics
- Data preview and descriptive statistics

## Requirements
pip install streamlit wrds pandas matplotlib numpy

## How to Run
streamlit run app.py

## Tools Used
Python, Streamlit, WRDS, Pandas, Matplotlib, SQL