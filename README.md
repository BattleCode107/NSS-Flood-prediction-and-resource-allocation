# Nirvana: NGO Disaster Relief Predictive Analytics Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)](https://streamlit.io/)
[![Google OR-Tools](https://img.shields.io/badge/Google_OR--Tools-Optimization-green.svg)](https://developers.google.com/optimization)

**Nirvana** is an end-to-end AI-powered predictive analytics platform designed to help Non-Governmental Organizations (NGOs) optimize disaster relief resource allocation. 

Built specifically for the highly vulnerable, flood-prone coastal districts of Odisha, India, this platform replaces estimation with data-driven decision making. It predicts exact relief demand (food, water, medicine, shelter) based on weather forecasts, and utilizes linear programming to mathematically generate the most efficient distribution routes for supply logistics.

---

## Submitted By

| Name | Enrollment Number | Email |
|--------|--------|--------|
| Nishant | 241137089 | nishant1@me.iitr.ac.in |
| Vedant Ganesh Halkude | 24112113 | vedant_gh@ch.iitr.ac.in |
| Aric Sukhija | 24126019 | aric_s@ch.iitr.ac.in|
| Harsh Deep | 24112048 | harsh_d@ch.iitr.ac.in |
| Gaurang Jindal | 24112045 | gaurang_j@ch.iitr.ac.in |


## The Problem & The Solution
During natural disasters, NGOs face chaotic environments characterized by limited supplies and broken communication lines. 

**The Solution:** Nirvana leverages Machine Learning to analyze 7-day weather forecasts and predict precisely where the damage will occur. It then calculates the optimal allocation strategy, outputting the exact quantity of supplies to be dispatched from specific NGO warehouses to target districts, maximizing human impact while minimizing logistical costs.

## Key Features
* **Demand Forecasting:** Predicts the exact number of people affected and the required quantity of food packets, drinking water, medical kits, and tarpaulins using an ensemble of advanced Machine Learning models (Random Forest, XGBoost, LightGBM).
* **Resource Optimization:** Utilizes Google OR-Tools to solve the complex logistics puzzle of routing limited resources from central NGO hubs (e.g., Bhubaneswar) to high-priority districts.
* **Interactive Dashboard:** A responsive, enterprise-grade web interface built with Streamlit. It includes modules for an Executive Overview, time-series Predictions, and a hypothetical Scenario Simulator.
* **GIS Visualization:** Employs Folium to provide an interactive, color-coded map of the predicted risk zones across Odisha.

---

## Tech Stack
* **Backend & Data Processing:** Python, Pandas, Numpy, Scikit-Learn
* **Machine Learning:** XGBoost, LightGBM, Random Forest
* **Logistics Optimization:** Google OR-Tools
* **Frontend UI:** Streamlit, Plotly, Streamlit-Folium
* **Deployment:** Docker, Docker Compose

---

## Setup Instructions (Local Deployment)

Follow these steps to run the platform locally.

**1. Clone the repository and navigate to the directory**
```bash
git clone https://github.com/BattleCode107/NSS-Flood-prediction-and-resource-allocation.git
cd ngo_disaster_relief
```

**2. Create a virtual environment and install dependencies**
It is highly recommended to use a virtual environment to isolate the application dependencies.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Run the AI Backend Pipeline**
A master bash script is included to automatically execute data generation, model training, future prediction, and route optimization sequentially.
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```
*(Alternatively, you can run the python scripts sequentially: `mock_data_generator.py` -> `train.py` -> `predict.py` -> `allocator.py`)*

**4. Launch the Dashboard**
Start the Streamlit server to view the interactive user interface.
```bash
streamlit run app/main.py
```
*The application will open automatically in your browser at `http://localhost:8501`.*

---

## Setup Instructions (Docker Deployment)

For a seamless, production-ready setup, the platform can be deployed via Docker containers.

1. Ensure **Docker** and **Docker Compose** are installed on your machine.
2. Build and run the containers in detached mode:
   ```bash
   cd docker
   docker-compose up --build -d
   ```
3. Access the dashboard at `http://localhost:8501`.

---

## Project Structure

```text
ngo_disaster_relief/
├── app/                        # Streamlit frontend (main.py and pages)
├── data/                       # Contains raw generated CSVs and processed predictions
├── docker/                     # Dockerfile and compose configurations
├── notebooks/                  # Jupyter notebooks containing model accuracy reports
├── src/                        
│   ├── data_ingestion/         # Scripts to generate/fetch weather and demographic data
│   ├── models/                 # Machine learning training and inference scripts
│   └── optimization/           # Google OR-Tools logistics algorithms
├── operational_playbook.md     # Standard Operating Procedures (SOPs) for NGOs
├── requirements.txt            # Python dependencies
└── run_pipeline.sh             # Master automation script
```
