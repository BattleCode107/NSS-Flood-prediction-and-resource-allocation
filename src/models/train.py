import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression

def load_data(path="data/raw/historical_disaster_data.csv"):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def feature_engineering(df):
    # Encoding district
    df = pd.get_dummies(df, columns=['district'], drop_first=False)
    
    # Month as feature
    df['month'] = df['date'].dt.month
    
    # Drop non-predictive columns
    drop_cols = ['date']
    features = df.drop(columns=[col for col in drop_cols if col in df.columns])
    return features

def train_and_evaluate(X, y, target_name):
    print(f"\n--- Training for {target_name} ---")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Baseline (LR)': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
        'LightGBM': LGBMRegressor(n_estimators=100, learning_rate=0.1, random_state=42, verbose=-1)
    }
    
    best_model = None
    best_mape = float('inf')
    best_name = ""
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        # Ensure no negative predictions
        preds = np.maximum(0, preds)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        
        # MAPE can be tricky with zeros
        mape = mean_absolute_percentage_error(y_test + 1e-5, preds)
        
        print(f"[{name}] MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape*100:.2f}%")
        
        if mape < best_mape and name != 'Baseline (LR)': # Prefer non-baseline if close
            best_mape = mape
            best_model = model
            best_name = name
            
    print(f"Best model for {target_name}: {best_name} (MAPE: {best_mape*100:.2f}%)")
    
    # Train best model on full data
    best_model.fit(X, y)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, f"models/best_{target_name}_model.pkl")
    
    # Save feature columns
    joblib.dump(list(X.columns), f"models/{target_name}_features.pkl")
    
    return best_model

if __name__ == "__main__":
    df = load_data()
    df_processed = feature_engineering(df)
    
    targets = ['affected_population', 'food_demand', 'water_demand', 'medical_demand', 'shelter_demand']
    
    for target in targets:
        # Features X, Target y
        X = df_processed.drop(columns=targets)
        y = df_processed[target]
        train_and_evaluate(X, y, target)
