import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(
    page_title="Nirvana - NGO Disaster Relief Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling and aesthetics
st.markdown("""
<style>
    :root {
        --primary: #2B5B84;
        --secondary: #4A90E2;
        --accent: #E24A4A;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f8fafc;
        --text-muted: #94a3b8;
    }
    
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }
    
    .stMetric {
        background-color: var(--surface);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--secondary) !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: opacity 0.2s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
    }
    
    h1, h2, h3 {
        color: var(--text);
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    hr {
        border-color: rgba(255,255,255,0.1);
    }
    
    .css-1d391kg {
        background-color: var(--surface);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌊 Nirvana: Coastal Odisha Relief Analytics")
st.markdown("""
### Welcome to the Predictive Analytics Platform for Disaster & NGO Operations

Nirvana uses advanced machine learning (XGBoost, Random Forest, LightGBM) to forecast relief demand 
across Odisha's coastal districts. By anticipating flood impact, we optimize the allocation of critical 
resources—food, water, medicine, and shelter—minimizing response times and maximizing coverage.

Please use the sidebar to navigate through the modules:
- **Executive Overview**: High-level summary of current risks and operations.
- **Prediction Dashboard**: Detailed forecasts for each district.
- **GIS Map Dashboard**: Interactive geographical visualizations.
- **Resource Allocation**: Optimized distribution plans from NGO hubs.
- **Scenario Analysis**: Simulate custom extreme weather events.
""")

st.image("https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", caption="Optimizing Disaster Relief with AI", use_container_width=True)

st.info("Data Sources Integrated: IMD, Bhuvan, OpenStreetMap, Census India, NDMA, NASA POWER")
