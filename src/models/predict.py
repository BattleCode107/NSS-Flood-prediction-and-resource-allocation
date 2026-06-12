import pandas as pd
import numpy as np
import joblib
import os

def load_models():
    models = {}
    features = {}
    targets = ['affected_population', 'food_demand', 'water_demand', 'medical_demand', 'shelter_demand']
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    for target in targets:
        model_path = os.path.join(BASE_DIR, "models", f"best_{target}_model.pkl")
        feature_path = os.path.join(BASE_DIR, "models", f"{target}_features.pkl")
        
        if os.path.exists(model_path):
            models[target] = joblib.load(model_path)
            features[target] = joblib.load(feature_path)
        else:
            print(f"Warning: Model for {target} not found.")
            
    return models, features

def predict_demand(input_data_path=None):
    if input_data_path is None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        input_data_path = os.path.join(BASE_DIR, "data", "raw", "current_forecast_data.csv")
    df = pd.read_csv(input_data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # Store original df for joining predictions
    output_df = df[['date', 'district']].copy()
    
    models, features = load_models()
    
    if not models:
        print("No models available for prediction.")
        return None
        
    # Process input data
    df_processed = pd.get_dummies(df, columns=['district'], drop_first=False)
    df_processed['month'] = df['date'].dt.month
    
    for target, model in models.items():
        # Ensure all features are present
        X = pd.DataFrame(columns=features[target])
        
        for col in features[target]:
            if col in df_processed.columns:
                X[col] = df_processed[col]
            else:
                X[col] = 0 # Impute missing dummy columns with 0
                
        preds = model.predict(X)
        output_df[target] = np.maximum(0, preds) # Ensure no negative demand
        
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(BASE_DIR, "data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    output_df.to_csv(os.path.join(out_dir, "forecasted_demand.csv"), index=False)
    
    print("Predictions completed and saved to forecasted_demand.csv")
    return output_df

if __name__ == "__main__":
    predict_demand()
