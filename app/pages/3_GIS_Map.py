import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import numpy as np

st.set_page_config(page_title="GIS Map Dashboard", page_icon="🗺️", layout="wide")

st.title("🗺️ Interactive GIS Map Dashboard")

# Approximate Coordinates for Odisha Districts
DISTRICT_COORDS = {
    "Kendrapara": [20.4939, 86.4253],
    "Jagatsinghpur": [20.2612, 86.1667],
    "Puri": [19.8135, 85.8312],
    "Ganjam": [19.3802, 84.7937],
    "Balasore": [21.4934, 86.9337],
    "Bhadrak": [21.0560, 86.4975],
    "Jajpur": [20.8385, 86.3353],
    "Cuttack": [20.4625, 85.8830],
    "Khordha": [20.1809, 85.6263],
}

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
    st.warning("Prediction data not found. Please run the prediction pipeline.")
else:
    dates = sorted(df['date'].unique())
    selected_date = st.select_slider("Select Date for Map", options=dates, format_func=lambda x: pd.to_datetime(x).strftime("%Y-%m-%d"))
    
    map_data = df[df['date'] == selected_date]
    
    metric = st.selectbox("Select Overlay Metric", options=[
        'affected_population', 'food_demand', 'water_demand', 'medical_demand', 'shelter_demand'
    ], format_func=lambda x: x.replace('_', ' ').title())
    
    # Create Folium Map
    # Odisha approximate center
    m = folium.Map(location=[20.5, 86.0], zoom_start=7, tiles="CartoDB dark_matter")
    
    max_val = map_data[metric].max() if not map_data.empty and map_data[metric].max() > 0 else 1
    
    for idx, row in map_data.iterrows():
        dist = row['district']
        val = row[metric]
        
        if dist in DISTRICT_COORDS:
            # Color scale from green to red based on severity
            severity = min(val / max_val, 1.0)
            
            # Simple color gradient
            if severity < 0.3:
                color = "green"
            elif severity < 0.6:
                color = "orange"
            else:
                color = "red"
                
            radius = max(10, min(50, severity * 50))
            
            folium.CircleMarker(
                location=DISTRICT_COORDS[dist],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"<b>{dist}</b><br>{metric.replace('_', ' ').title()}: {int(val):,}",
                tooltip=dist
            ).add_to(m)

    st_folium(m, width=1200, height=600)
