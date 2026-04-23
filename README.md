# WRDS Stock Analysis Tool
An interactive stock data analysis tool built with Python and Streamlit, using WRDS CRSP daily stock data.

## Author
wending
Student ID: 2470050

## Project Overview
This tool allows users to easily retrieve, visualize, and compare historical stock data without writing complex SQL or Python code. It is designed for finance students and researchers to support coursework and basic empirical analysis.

## Analytical Problem
Many users struggle with database connections, date formatting issues, and multi-stock comparison. This tool automates data extraction, cleaning, and visualization.

## Dataset
Source: WRDS CRSP Daily Stock File (dsf)
Variables: permno, date, price (prc), return (ret), shares outstanding (shrout)
Reason: Academically reliable, standardized, and widely used in finance research

## Python Libraries Used
- `wrds`: Database connection and SQL queries
- `pandas`: Data cleaning and processing
- `plotly`: Interactive visualizations
- `streamlit`: Web interface

## Key Features
- Multi-stock support (comma-separated PERMNOs)
- Interactive price, return, and cumulative return charts
- Data table preview
- CSV download function
- Fixed date-format bug for accurate data retrieval

## How to Run
1. Install required packages:
   ```bash
   pip install wrds pandas plotly streamlit
