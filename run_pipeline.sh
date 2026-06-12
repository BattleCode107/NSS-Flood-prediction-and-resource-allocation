#!/bin/bash
set -e
echo "Starting Pipeline..."
source venv/bin/activate
echo "1. Generating Synthetic Data"
python src/data_ingestion/mock_data_generator.py
echo "2. Training ML Models"
python src/models/train.py
echo "3. Predicting Demand"
python src/models/predict.py
echo "4. Running OR-Tools Optimization Engine"
python src/optimization/allocator.py
echo "Pipeline completed successfully!"
