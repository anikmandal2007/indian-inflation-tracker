# 📈 MacroIndia: Indian CPI Inflation & Monetary Policy Tracker

[[https://static.streamlit.io/badges/streamlit_badge_black_white.svg]](https://indian-inflation-tracker-dbggqxricdbnnbsqrabffq.streamlit.app)

**Live Interactive Web App:** [https://indian-inflation-tracker-dbggqxricdbnnbsqrabffq.streamlit.app](https://indian-inflation-tracker-dbggqxricdbnnbsqrabffq.streamlit.app)

## 📌 Project Overview
**MacroIndia** is an interactive macroeconomic analytics web application that bridges **Economics** and **Computer Science**. It tracks All-India Consumer Price Index (CPI) trends, decomposes Headline vs. Food and Core inflation, and evaluates monetary policy transmission against the **Reserve Bank of India's (RBI)** Flexible Inflation Targeting (FIT) tolerance band (4.0% ± 2.0%).

## 🚀 Key Features
- **📊 CPI vs. RBI Tolerance Band Visualizer:** Interactive Plotly time-series chart comparing Headline CPI, Consumer Food Price Index (CFPI), Core Inflation, and the RBI Repo Rate against the shaded 2%–6% MPC target band.
- **🛒 Personal Inflation Calculator:** Computes an individual's custom inflation rate based on their monthly household expenditure across food, housing, fuel, and education/healthcare—quantifying the gap between personal inflation and official headline CPI.
- **💰 Rupee Purchasing Power Calculator:** Calculates cumulative real value erosion and equivalent purchasing power of the Indian Rupee (₹) across any user-selected base year from 2015 to 2025.
- **📖 Economic Methodology & Raw Data Export:** Includes formal macroeconomic equations and one-click CSV dataset export.

## 🛠️ Tech Stack & Data Sources
- **Programming & Analytics:** Python, Pandas
- **Interactive Visualization & UI:** Plotly, Streamlit
- **Primary Macroeconomic Data:** [Ministry of Statistics and Programme Implementation (MoSPI)](https://www.mospi.gov.in/themes/product/9-consumer-price-index-cpi) & [RBI Database on Indian Economy (DBIE)](https://data.rbi.org.in/)

## 📂 Repository Structure
- `app.py` — Main Streamlit dashboard application and econometric calculators
- `requirements.txt` — Python package dependencies for cloud deployment
- `india_inflation.csv` — Curated historical Indian CPI & RBI Repo Rate dataset (2015–2025)
