import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="Resource Allocation", page_icon="🚚", layout="wide")

st.title("🚚 Optimal Resource Allocation")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/optimal_allocations.csv")
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Allocation data not found. Please run the optimization pipeline.")
else:
    dates = sorted(df['date'].unique())
    selected_date = st.selectbox("Select Date", options=dates, format_func=lambda x: pd.to_datetime(x).strftime("%Y-%m-%d"))
    
    resource_filter = st.selectbox("Resource Type", options=['All', 'food', 'water', 'medical', 'shelter'])
    
    view_df = df[df['date'] == selected_date]
    if resource_filter != 'All':
        view_df = view_df[view_df['resource'] == resource_filter]
        
    st.subheader("Distribution Routes")
    
    if not view_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # We can visualize this using a Sankey diagram
            sources = view_df['from_hub'].tolist()
            targets = view_df['to_district'].tolist()
            values = view_df['allocated_amount'].tolist()
            
            # Create node lists
            all_nodes = list(set(sources + targets))
            node_indices = {node: i for i, node in enumerate(all_nodes)}
            
            source_indices = [node_indices[s] for s in sources]
            target_indices = [node_indices[t] for t in targets]
            
            fig = go.Figure(data=[go.Sankey(
                node = dict(
                  pad = 15,
                  thickness = 20,
                  line = dict(color = "black", width = 0.5),
                  label = all_nodes,
                  color = "blue"
                ),
                link = dict(
                  source = source_indices,
                  target = target_indices,
                  value = values,
                  color = "rgba(74, 144, 226, 0.4)"
                )
            )])
            
            fig.update_layout(title_text=f"{resource_filter.title() if resource_filter != 'All' else 'All Resources'} Flow from Hubs to Districts", font_size=12, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### Logistics Summary")
            st.metric("Total Items Shipped", f"{int(view_df['allocated_amount'].sum()):,}")
            st.metric("Total Distance Covered (est. km)", f"{int((view_df['distance_km'] * view_df['allocated_amount'] / 1000).sum()):,}")
            
        st.markdown("### Route Details")
        st.dataframe(view_df[['from_hub', 'to_district', 'resource', 'allocated_amount', 'distance_km']], use_container_width=True)
    else:
        st.info("No allocations for this selection.")
