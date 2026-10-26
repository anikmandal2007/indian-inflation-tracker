import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="MacroIndia: Indian Inflation Tracker", page_icon="📈", layout="wide")

DEFAULT_DATA = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "Headline_CPI_Percent": [4.9, 4.5, 3.6, 3.4, 4.8, 6.2, 5.5, 6.7, 5.4, 4.9, 4.5],
    "Food_Inflation_Percent": [4.9, 4.2, 1.8, 0.1, 6.7, 7.7, 3.8, 6.6, 7.5, 8.4, 6.1],
    "Core_Inflation_Percent": [4.6, 4.8, 4.6, 5.8, 4.0, 5.5, 6.0, 6.1, 4.3, 3.5, 3.7],
    "RBI_Repo_Rate_Percent": [6.75, 6.25, 6.00, 6.50, 5.15, 4.00, 4.00, 6.25, 6.50, 6.50, 6.00],
}

@st.cache_data
def load_data():
    if os.path.exists("india_inflation.csv"):
        return pd.read_csv("india_inflation.csv")
    return pd.DataFrame(DEFAULT_DATA)

df = load_data()

st.title("📈 MacroIndia: Indian CPI Inflation & Monetary Policy Tracker")
st.markdown(
    "Tracking **All-India Consumer Price Index (CPI)** trends, **Food vs. Core Inflation**, "
    "and the **Reserve Bank of India (RBI)** monetary policy tolerance band (2%–6%). "
    "Data sourced from [MoSPI](https://www.mospi.gov.in/themes/product/9-consumer-price-index-cpi) "
    "and [RBI DBIE](https://data.rbi.org.in/)."
)

latest = df.iloc[-1]
prev = df.iloc[-2]

col1, col2, col3, col4 = st.columns(4)
col1.metric(f"Headline CPI ({int(latest['Year'])})", f"{latest['Headline_CPI_Percent']:.1f}%", f"{latest['Headline_CPI_Percent'] - prev['Headline_CPI_Percent']:+.1f}% YoY", delta_color="inverse")
col2.metric(f"Food Inflation ({int(latest['Year'])})", f"{latest['Food_Inflation_Percent']:.1f}%", f"{latest['Food_Inflation_Percent'] - prev['Food_Inflation_Percent']:+.1f}% YoY", delta_color="inverse")
col3.metric(f"Core Inflation ({int(latest['Year'])})", f"{latest['Core_Inflation_Percent']:.1f}%", f"{latest['Core_Inflation_Percent'] - prev['Core_Inflation_Percent']:+.1f}% YoY", delta_color="inverse")
col4.metric(f"RBI Repo Rate ({int(latest['Year'])})", f"{latest['RBI_Repo_Rate_Percent']:.2f}%", f"{latest['RBI_Repo_Rate_Percent'] - prev['RBI_Repo_Rate_Percent']:+.2f}%")

tab1, tab2, tab3 = st.tabs(["📊 CPI vs. RBI Tolerance Band", "🛒 Personal Inflation Calculator", "💰 Purchasing Power Calculator"])

with tab1:
    st.subheader("Headline, Food & Core CPI vs. RBI Target (4% ± 2%)")
    selected_series = st.multiselect(
        "Select Macroeconomic Series to Compare:",
        options=["Headline_CPI_Percent", "Food_Inflation_Percent", "Core_Inflation_Percent", "RBI_Repo_Rate_Percent"],
        default=["Headline_CPI_Percent", "Food_Inflation_Percent", "RBI_Repo_Rate_Percent"],
    )
    fig = go.Figure()
    fig.add_hrect(y0=2.0, y1=6.0, fillcolor="rgba(46, 204, 113, 0.12)", line_width=0, annotation_text="RBI Tolerance Band (2% - 6%)", annotation_position="top left")
    fig.add_hline(y=4.0, line_dash="dash", line_color="#27ae60", annotation_text="RBI MPC Target (4.0%)", annotation_position="bottom right")
    series_labels = {
        "Headline_CPI_Percent": ("Headline CPI (%)", "#1f77b4"),
        "Food_Inflation_Percent": ("Food Inflation (CFPI %)", "#e67e22"),
        "Core_Inflation_Percent": ("Core Inflation (%)", "#9b59b6"),
        "RBI_Repo_Rate_Percent": ("RBI Repo Rate (%)", "#e74c3c"),
    }
    for col in selected_series:
        label, color = series_labels[col]
        fig.add_trace(go.Scatter(x=df["Year"], y=df[col], mode="lines+markers", name=label, line=dict(color=color, width=3)))
    fig.update_layout(xaxis_title="Year", yaxis_title="Rate (%)", hovermode="x unified", template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Calculate Your Personal Inflation Rate")
    c1, c2 = st.columns(2)
    with c1:
        food_spend = st.number_input("Monthly Food & Groceries (₹)", min_value=0, value=6000, step=500)
        housing_spend = st.number_input("Monthly Rent & Utilities (₹)", min_value=0, value=5000, step=500)
    with c2:
        fuel_spend = st.number_input("Monthly Transport & Fuel (₹)", min_value=0, value=2000, step=500)
        misc_spend = st.number_input("Monthly Education, Healthcare & Misc (₹)", min_value=0, value=3000, step=500)
    total_spend = food_spend + housing_spend + fuel_spend + misc_spend
    if total_spend > 0:
        personal_rate = (food_spend * latest["Food_Inflation_Percent"] + housing_spend * latest["Core_Inflation_Percent"] + fuel_spend * 4.0 + misc_spend * latest["Core_Inflation_Percent"]) / total_spend
        gap = personal_rate - latest["Headline_CPI_Percent"]
        st.info(f"**Your Personal Inflation Rate:** `{personal_rate:.2f}%` ({gap:+.2f}% vs. Official CPI `{latest['Headline_CPI_Percent']:.1f}%`).\n\nNext year's monthly budget needed for the same lifestyle: **₹{total_spend * (1 + personal_rate / 100):,.0f}**.")

with tab3:
    st.subheader("Rupee Purchasing Power Calculator")
    base_amount = st.number_input("Enter Amount in ₹ (e.g., 10,000):", min_value=100, value=10000, step=1000)
    start_year = st.selectbox("Select Starting Year:", options=df["Year"].tolist()[:-1], index=0)
    sub_df = df[df["Year"] >= start_year]
    cumulative_factor = 1.0
    for rate in sub_df["Headline_CPI_Percent"]:
        cumulative_factor *= 1 + (rate / 100.0)
    st.success(
        f"**Purchasing Power Erosion ({start_year} → {int(latest['Year'])}):**\n"
        f"- You need **₹{base_amount * cumulative_factor:,.0f}** today to buy what **₹{base_amount:,.0f}** bought in **{start_year}**.\n"
        f"- ₹{base_amount:,.0f} kept in cash since {start_year} is worth **₹{base_amount / cumulative_factor:,.0f}** in real terms today."
    )

with st.expander("📂 View Raw Macroeconomic Dataset"):
    st.dataframe(df, use_container_width=True)
  
