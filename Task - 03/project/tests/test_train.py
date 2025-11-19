import pytest
import os
import joblib
from src.train import train_model
from src.predict import load_model

def test_train_model():
    # Train the model
    result = train_model()
    
    # Check that the result contains expected keys
    assert 'model_path' in result
    assert 'metadata_path' in result
    assert 'evaluation' in result
    assert 'best_params' in result
    
    # Check that model file was created
    assert os.path.exists(result['model_path'])
    
    # Check that metadata file was created
    assert os.path.exists(result['metadata_path'])
    
    # Check that we can load the model
    model = load_model()
    assert model is not None
    
    # Check evaluation metrics
    evaluation = result['evaluation']
    assert 'rmse' in evaluation
    assert 'mae' in evaluation
    assert 'r2' in evaluation
    assert 'feature_importances' in evaluation
    
    # Check that metrics are reasonable
    assert evaluation['rmse'] > 0
    assert evaluation['mae'] > 0
    assert 0 <= evaluation['r2'] <= 1

def test_model_persistence():
    # Train model
    result = train_model()
    
    # Load model
    model = joblib.load(result['model_path'])
    assert model is not None
    
    # Check that we can make predictions with the loaded model
    # This is a basic check - in practice, you would test with actual data
    assert hasattr(model, 'predict')