# Nirvana: NGO Disaster Relief Predictive Analytics Platform 🌊

Nirvana is an end-to-end AI-powered predictive analytics platform designed to help NGOs optimize disaster relief resource allocation. Built specifically for the flood-prone coastal districts of Odisha, India, this platform predicts relief demand (food, water, medicine, shelter) and uses linear programming to generate optimal distribution routes.

## Features
* **Demand Forecasting:** Predicts the exact number of people affected and the required quantity of food packets, drinking water, medical kits, and tarpaulins using an ensemble of Machine Learning models (Random Forest, XGBoost, LightGBM).
* **Resource Optimization:** Uses Google OR-Tools to solve the complex logistics problem of routing limited resources from NGO hubs to high-priority districts efficiently.
* **Interactive Dashboard:** Built with Streamlit, offering modules for Executive Overview, Predictions, GIS Mapping, and Scenario Analysis.
* **GIS Visualization:** Uses Folium to provide an interactive map of the predicted risk zones across Odisha.

## Tech Stack
* **Backend / Data:** Python, Pandas, Numpy, Scikit-Learn, XGBoost, LightGBM
* **Optimization:** Google OR-Tools
* **Frontend:** Streamlit, Plotly, Streamlit-Folium
* **Deployment:** Docker, Docker Compose

## Setup Instructions (Local)

1. **Clone the repository and navigate to the directory**
   ```bash
   cd "ngo_disaster_relief"
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the complete Data & ML Pipeline**
   This simulates data fetching, trains the models, makes predictions, and runs the optimizer.
   ```bash
   python src/data_ingestion/mock_data_generator.py
   python src/models/train.py
   python src/models/predict.py
   python src/optimization/allocator.py
   ```

4. **Launch the Dashboard**
   ```bash
   streamlit run app/main.py
   ```

## Setup Instructions (Docker)

1. Ensure Docker and Docker Compose are installed.
2. Build and run the containers:
   ```bash
   cd docker
   docker-compose up --build -d
   ```
3. Access the dashboard at `http://localhost:8501`.

## Project Structure
* `app/`: Streamlit dashboard code.
* `data/`: Raw and processed data outputs.
* `docker/`: Container configurations.
* `src/`: Core logic (data ingestion, ML models, optimization engine).
* `operational_playbook.md`: Standard operating procedures for NGOs.
