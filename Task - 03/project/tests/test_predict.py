import pytest
import numpy as np
from src.predict import predict_price, reconstruct_features

def test_predict():
    # Test prediction with sample features
    n_bed = 3
    n_bath = 2.0
    lat = 47.5112
    long = -122.257
    sqft = 2000
    
    # Test that prediction returns expected structure
    result = predict_price(n_bed, n_bath, lat, long, sqft)
    
    # Check that result contains expected keys
    assert 'predicted_price' in result
    assert 'confidence_interval' in result
    assert 'feature_contributions' in result
    assert 'input_features' in result
    
    # Check that predicted price is reasonable (positive)
    assert result['predicted_price'] > 0
    
    # Check confidence interval
    ci = result['confidence_interval']
    assert 'lower' in ci
    assert 'upper' in ci
    assert ci['lower'] <= result['predicted_price'] <= ci['upper']
    
    # Check input features
    input_features = result['input_features']
    assert input_features['bedrooms'] == n_bed
    assert input_features['bathrooms'] == n_bath
    assert input_features['latitude'] == lat
    assert input_features['longitude'] == long
    assert input_features['sqft'] == sqft

def test_reconstruct_features():
    # Test feature reconstruction
    n_bed = 3
    n_bath = 2.0
    lat = 47.5112
    long = -122.257
    sqft = 2000
    
    features = reconstruct_features(n_bed, n_bath, lat, long, sqft)
    
    # Check that all expected features are present
    expected_features = [
        'bedrooms', 'bathrooms', 'lat', 'long', 'sqft_living', 'sqft_lot',
        'floors', 'waterfront', 'view', 'condition', 'grade', 'sqft_above',
        'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'sqft_living15',
        'sqft_lot15', 'total_rooms', 'sqft_per_room', 'rooms_per_household',
        'age_of_house', 'since_renovated', 'lat_long_interaction', 'is_renovated',
        'has_basement', 'was_renovated', 'zipcode_str'
    ]
    
    for feature in expected_features:
        assert feature in features, f"Missing feature: {feature}"
    
    # Check specific values
    assert features['bedrooms'] == n_bed
    assert features['bathrooms'] == n_bath
    assert features['lat'] == lat
    assert features['long'] == long
    assert features['sqft_living'] == sqft
    assert features['total_rooms'] == n_bed + n_bath