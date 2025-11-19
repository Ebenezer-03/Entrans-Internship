import pytest
import pandas as pd
import numpy as np
from src.preprocess import build_preprocessor
from src.data_processing import load_raw_data, engineer_features, get_feature_groups

def test_preprocess():
    # Load and engineer data
    raw_data = load_raw_data()
    engineered_data = engineer_features(raw_data)
    numeric_cols, categorical_cols = get_feature_groups(engineered_data)
    
    # Test that we have the expected columns
    assert 'sqft_per_room' in engineered_data.columns
    assert 'rooms_per_household' in engineered_data.columns
    assert 'age_of_house' in engineered_data.columns
    assert 'has_basement' in engineered_data.columns
    assert 'was_renovated' in engineered_data.columns
    
    # Test that we have both numeric and categorical columns
    assert len(numeric_cols) > 0
    assert len(categorical_cols) > 0
    
    # Test preprocessor creation
    preprocessor = build_preprocessor(numeric_cols, categorical_cols)
    assert preprocessor is not None
    
    # Test with a small sample
    sample_data = engineered_data.head(100)
    numeric_frame = sample_data[numeric_cols]
    categorical_frame = sample_data[categorical_cols].astype(str)
    X = pd.concat([numeric_frame, categorical_frame], axis=1)
    
    # Test that preprocessor can transform data
    X_transformed = preprocessor.fit_transform(X)
    assert X_transformed is not None
    assert X_transformed.shape[0] == X.shape[0]