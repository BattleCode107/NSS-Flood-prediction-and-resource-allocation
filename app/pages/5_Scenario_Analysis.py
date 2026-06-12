import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Scenario Analysis", page_icon="⛈️", layout="wide")

st.title("⛈️ Extreme Weather Scenario Simulator")

st.markdown("""
Use this module to simulate hypothetical extreme weather events and immediately see their predicted impact on relief operations.
This uses our trained ML models (XGBoost/LightGBM) to infer demand based on your inputs.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Scenario Parameters")
    
    scenario_type = st.selectbox("Preset Scenarios", ["Custom", "Super Cyclone (Category 5)", "Flash Floods (Heavy Rain)", "Moderate Depression"])
    
    if scenario_type == "Super Cyclone (Category 5)":
        rain = 350
        wind = 220
        intensity = 5
    elif scenario_type == "Flash Floods (Heavy Rain)":
        rain = 400
        wind = 60
        intensity = 1
    elif scenario_type == "Moderate Depression":
        rain = 150
        wind = 80
        intensity = 2
    else:
        rain = 100
        wind = 50
        intensity = 0
        
    custom_rain = st.slider("Expected Rainfall (mm in 24h)", 0, 600, rain)
    custom_wind = st.slider("Max Wind Speed (km/h)", 0, 300, wind)
    custom_intensity = st.slider("Cyclone Category (0-5)", 0, 5, intensity)
    
    simulate_btn = st.button("Run Simulation", use_container_width=True)

with col2:
    if simulate_btn:
        st.subheader("Simulation Results")
        with st.spinner("Running ML Inference on all coastal districts..."):
            # Load models
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            try:
                from src.models.predict import load_models
                from src.data_ingestion.mock_data_generator import DISTRICT_DEMOGRAPHICS
                
                models, features = load_models()
                
                if models:
                    results = []
                    for dist, demo in DISTRICT_DEMOGRAPHICS.items():
                        
                        # Build synthetic input row for this district
                        row_dict = {
                            "current_rainfall": custom_rain,
                            "rainfall_3day": custom_rain * 2.5,
                            "rainfall_7day": custom_rain * 5,
                            "rainfall_anomaly": custom_rain / 100.0,
                            "cyclone_intensity": custom_intensity,
                            "wind_speed": custom_wind,
                            "distance_from_coastline": max(1, 60 - demo['elevation_m']),
                            "elevation": demo['elevation_m'],
                            "flood_prone_indicator": 1 if demo['elevation_m'] < 20 else 0,
                            "population_density": demo['population'] / demo['area_sqkm'],
                            "vulnerable_population": demo['population'] * demo['rural_pct'],
                            "rural_population_pct": demo['rural_pct'],
                            "hospitals": demo['hospitals'],
                            "shelters": demo['shelters'],
                            "month": 8, # Peak monsoon
                        }
                        
                        # Add district dummies
                        for d in DISTRICT_DEMOGRAPHICS.keys():
                            row_dict[f"district_{d}"] = 1 if d == dist else 0
                            
                        # Predict
                        dist_result = {"District": dist}
                        for target, model in models.items():
                            X = pd.DataFrame([row_dict], columns=features[target]).fillna(0)
                            pred = max(0, model.predict(X)[0])
                            dist_result[target] = int(pred)
                            
                        results.append(dist_result)
                        
                    res_df = pd.DataFrame(results)
                    
                    st.metric("Total Projected Affected Population", f"{res_df['affected_population'].sum():,}")
                    
                    st.dataframe(res_df.style.background_gradient(cmap='Reds'), use_container_width=True)
                    
                    st.markdown("---")
                    st.subheader("Emergency Resource Allocation Plan")
                    
                    try:
                        from src.optimization.allocator import optimize_allocation
                        
                        # Prepare df for the allocator format
                        alloc_df = res_df.copy()
                        alloc_df.rename(columns={'District': 'district'}, inplace=True)
                        alloc_df['date'] = 'scenario'
                        
                        alloc_results = []
                        for res in ['food', 'water', 'medical', 'shelter']:
                            opt_df = optimize_allocation(alloc_df, 'scenario', res)
                            if opt_df is not None and not opt_df.empty:
                                alloc_results.append(opt_df)
                                
                        if alloc_results:
                            final_alloc = pd.concat(alloc_results, ignore_index=True)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Total Items Shipped", f"{int(final_alloc['allocated_amount'].sum()):,}")
                            with col_b:
                                st.metric("Logistics Cost (est. km-units)", f"{int((final_alloc['distance_km'] * final_alloc['allocated_amount'] / 1000).sum()):,}")
                            
                            # Clean up the output table for display
                            display_df = final_alloc[['resource', 'from_hub', 'to_district', 'allocated_amount', 'demand', 'distance_km']]
                            display_df.columns = ['Resource', 'From Hub', 'To District', 'Allocated Amount', 'Demand', 'Distance (km)']
                            
                            st.dataframe(display_df, use_container_width=True)
                        else:
                            st.info("No resources available to allocate.")
                    except Exception as e:
                        st.error(f"Could not generate allocation plan: {e}")
                else:
                    st.error("Models not found. Train models first.")
            except Exception as e:
                st.error(f"Error running simulation: {e}")
    else:
        st.info("Adjust parameters and click 'Run Simulation' to see results.")
