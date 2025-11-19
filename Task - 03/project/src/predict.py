import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any
import os

def load_model():
    """Load the trained model."""
    model_path = 'models/best_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
    return joblib.load(model_path)

def reconstruct_features(n_bed: int, n_bath: float, lat: float, long: float, sqft: int) -> Dict[str, Any]:
    """Reconstruct all features from the 5 input features."""
    # Basic features
    features = {
        'bedrooms': n_bed,
        'bathrooms': n_bath,
        'lat': lat,
        'long': long,
        'sqft_living': sqft,
        'sqft_lot': sqft * 2,  # Estimate lot size as 2x living space
        'floors': 1.0,
        'waterfront': 0,
        'view': 0,
        'condition': 3,
        'grade': 7,
        'sqft_above': sqft,  # Assume all above ground
        'sqft_basement': 0,
        'yr_built': 1990,
        'yr_renovated': 0,
        'zipcode': '98001',
        'sqft_living15': sqft,
        'sqft_lot15': sqft * 2
    }
    
    # Engineer additional features
    features['total_rooms'] = features['bedrooms'] + features['bathrooms']
    features['sqft_per_room'] = features['sqft_living'] / features['total_rooms'] if features['total_rooms'] > 0 else 0
    features['rooms_per_household'] = features['total_rooms'] / features['floors'] if features['floors'] > 0 else 0
    features['age_of_house'] = 2025 - features['yr_built']
    features['since_renovated'] = features['age_of_house'] if features['yr_renovated'] == 0 else (2025 - features['yr_renovated'])
    features['price_per_sqft'] = np.nan  # Will be calculated after prediction
    features['lat_long_interaction'] = features['lat'] * features['long']
    features['is_renovated'] = 1 if features['yr_renovated'] > 0 else 0
    features['has_basement'] = 1 if features['sqft_basement'] > 0 else 0
    features['was_renovated'] = 1 if features['yr_renovated'] > 0 else 0
    features['zipcode_str'] = str(features['zipcode'])
    
    # Date features (using a fixed date for consistency)
    features['date'] = pd.Timestamp('2015-01-01')
    features['sale_year'] = features['date'].year
    features['sale_month'] = features['date'].month
    
    return features

def predict_price(n_bed: int, n_bath: float, lat: float, long: float, sqft: int) -> Dict[str, Any]:
    """Predict house price based on 5 key features."""
    # Load the model
    model = load_model()
    
    # Reconstruct all features
    features = reconstruct_features(n_bed, n_bath, lat, long, sqft)
    
    # Prepare input data
    input_data = pd.DataFrame([features])
    
    # Make prediction
    predicted_price = model.predict(input_data)[0]
    
    # Calculate confidence interval (simplified approach)
    # In a real application, this would be based on model uncertainty
    confidence_interval = {
        'lower': predicted_price * 0.85,
        'upper': predicted_price * 1.15
    }
    
    # Try to get feature contributions if possible
    feature_contributions = {}
    try:
        # This is a simplified approach - in practice, you would use SHAP or similar
        feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        importances = model.named_steps['regressor'].feature_importances_
        top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:10]
        feature_contributions = dict(top_features)
    except Exception as e:
        print(f"Could not calculate feature contributions: {e}")
    
    return {
        'predicted_price': predicted_price,
        'confidence_interval': confidence_interval,
        'feature_contributions': feature_contributions,
        'input_features': {
            'bedrooms': n_bed,
            'bathrooms': n_bath,
            'latitude': lat,
            'longitude': long,
            'sqft': sqft
        }
    }