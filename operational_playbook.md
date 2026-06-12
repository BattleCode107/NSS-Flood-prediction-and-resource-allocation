# Nirvana - NGO Disaster Relief Operations Playbook

## 1. Introduction
This playbook outlines the standard operating procedures (SOPs) for NGOs using the Nirvana AI Predictive Analytics Platform during flood and cyclone events in the Odisha coastal districts.

## 2. Risk Levels & Recommended Actions

### 🟢 Low Risk (No immediate threat)
* **Trigger:** Routine weather, no cyclone warnings.
* **Actions:**
  - Weekly review of the Prediction Dashboard.
  - Ensure data ingestion pipelines are functioning.
  - Maintain baseline inventory at hubs (Khordha, Cuttack, Balasore).

### 🟡 Moderate Risk (Depression forming in Bay of Bengal)
* **Trigger:** IMD alert for heavy rainfall (70-150mm) or mild cyclone.
* **Actions:**
  - Daily review of 7-day forecast.
  - Run **Scenario Analysis** to simulate potential escalation.
  - Alert local volunteers in vulnerable districts (e.g., Kendrapara, Jagatsinghpur).
  - Verify inventory counts against the `medical` and `shelter` baseline demands.

### 🟠 High Risk (Severe Cyclone or Extreme Rainfall Warning)
* **Trigger:** IMD Red Alert, Cyclone Category 3+, Rainfall > 200mm.
* **Actions:**
  - Check the **Resource Allocation** dashboard for optimal dispatch routes.
  - Begin pre-positioning supplies 48 hours before predicted impact.
  - Focus on highest-priority districts highlighted in the **Executive Overview**.
  - Mobilize transportation assets (trucks, boats) based on the Allocation Engine's route recommendations.

### 🔴 Severe Risk (Landfall imminent, Category 4/5)
* **Trigger:** Imminent super cyclone or catastrophic flooding.
* **Actions:**
  - Dispatch maximum resources immediately according to OR-Tools optimized routing.
  - Use **GIS Map** to identify safe shelter locations and avoid inundated roads.
  - Communicate exact resource quantities needed to partner NGOs and government authorities based on the predicted `food_demand` and `water_demand` metrics.

## 3. Workflow Definitions

### Data Collection Workflow
1. Automated cron jobs trigger the data ingestion scripts (`mock_data_generator.py` in the demo).
2. Data is fetched from IMD APIs, Bhuvan GIS servers, and NDMA incident reports.
3. Raw data is stored in the PostgreSQL/Data Warehouse.

### Forecast Generation Workflow
1. ETL pipeline processes raw data, engineered features (e.g., `rainfall_7day`, `distance_from_coastline`).
2. The ML Pipeline (`predict.py`) loads the pre-trained XGBoost/LightGBM/RF ensemble models.
3. Predictions for `affected_population`, `food`, `water`, `medical`, and `shelter` demand are generated for the next 7 days.

### Resource Allocation Workflow
1. The Optimization Engine (`allocator.py`) runs daily using Google OR-Tools.
2. It takes the forecasted demand and the current NGO hub inventory as inputs.
3. It solves a Linear Programming problem to minimize distance/transport cost while maximizing demand fulfillment.
4. Results are published to the Resource Allocation dashboard.

### Emergency Response Workflow
1. NGO Coordinators log into the **Nirvana Dashboard**.
2. They review the **Executive Overview** for daily priorities.
3. They download the Route Manifest from the **Resource Allocation** page.
4. Truck drivers and local coordinators execute the delivery based on the optimized routes.
