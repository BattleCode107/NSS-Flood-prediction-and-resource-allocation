import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="Prediction Dashboard", page_icon="📈", layout="wide")

st.title("📈 Demand Prediction Dashboard")

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
    districts = df['district'].unique()
    selected_district = st.selectbox("Select District", options=["All"] + list(districts))
    
    if selected_district != "All":
        view_df = df[df['district'] == selected_district]
    else:
        view_df = df.groupby('date').sum(numeric_only=True).reset_index()
        view_df['district'] = "All"
        
    st.subheader(f"7-Day Forecast for {selected_district}")
    
    # Let user select which demand to visualize
    metric = st.selectbox("Select Metric", options=[
        'affected_population', 'food_demand', 'water_demand', 'medical_demand', 'shelter_demand'
    ], format_func=lambda x: x.replace('_', ' ').title())
    
    # Plotly Line Chart
    fig = px.line(
        view_df, 
        x='date', 
        y=metric, 
        title=f"Predicted {metric.replace('_', ' ').title()} Over Time",
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#4A90E2']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Detailed Data Table")
    st.dataframe(
        view_df[['date', 'affected_population', 'food_demand', 'water_demand', 'medical_demand', 'shelter_demand']].style.format({
            'affected_population': '{:,.0f}',
            'food_demand': '{:,.0f}',
            'water_demand': '{:,.0f}',
            'medical_demand': '{:,.0f}',
            'shelter_demand': '{:,.0f}'
        }),
        use_container_width=True
    )
