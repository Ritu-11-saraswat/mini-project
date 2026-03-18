import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os

def train_risk_model(data_path="synthetic_student_data.csv"):
    """
    Trains a predictive model for student risk probability.
    In a real scenario, bias mitigation (like fairlearn) would be applied to the data 
    before feeding it into the model to ensure fair predictions across socioeconomic statuses.
    """
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Data file not found. Ensure the data generator has been run.")
        return None
        
    # Feature selection
    features = ['attendance_rate', 'assignments_completed', 'lms_login_frequency']
    X = df[features]
    y = df['risk_probability']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model trained successfully. Mean Squared Error: {mse:.4f}")
    
    # Save the model
    model_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(model_dir, "saved_models"), exist_ok=True)
    
    model_path = os.path.join(model_dir, "saved_models", "risk_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Model saved to {model_path}")
    return model

if __name__ == "__main__":
    train_risk_model()
