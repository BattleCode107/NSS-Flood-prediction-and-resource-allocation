import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")

st.title("📊 Executive Overview")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/forecasted_demand.csv")
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Data not generated yet. Please run the data generation pipeline.")
else:
    # Filter for tomorrow's forecast
    tomorrow = df['date'].min()
    today_df = df[df['date'] == tomorrow]
    
    st.subheader(f"Forecast for {tomorrow.strftime('%Y-%m-%d')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_affected = int(today_df['affected_population'].sum())
    total_food = int(today_df['food_demand'].sum())
    total_water = int(today_df['water_demand'].sum())
    total_shelter = int(today_df['shelter_demand'].sum())
    
    with col1:
        st.metric(label="Total Affected Population", value=f"{total_affected:,}", delta="High Risk")
    with col2:
        st.metric(label="Total Food Packets Reqd", value=f"{total_food:,}")
    with col3:
        st.metric(label="Drinking Water Reqd (L)", value=f"{total_water:,}")
    with col4:
        st.metric(label="Shelter/Tarpaulins Reqd", value=f"{total_shelter:,}")
        
    st.divider()
    
    st.subheader("High Priority Districts")
    
    # Sort districts by affected population
    priority_df = today_df.sort_values(by='affected_population', ascending=False).head(3)
    
    for idx, row in priority_df.iterrows():
        with st.container():
            st.error(f"🚨 **{row['district']}** | Affected: {int(row['affected_population']):,} | Food: {int(row['food_demand']):,} packets")

    st.markdown("### Operational Readiness")
    st.progress(65, text="NGO Current Inventory vs Forecasted Demand")
