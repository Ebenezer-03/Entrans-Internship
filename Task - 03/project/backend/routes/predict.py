from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.predict import predict_price
from datetime import datetime
import sqlite3
import os

router = APIRouter()

class PredictionRequest(BaseModel):
    bedrooms: int
    bathrooms: float
    lat: float
    long: float
    sqft: int

class PredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: dict
    feature_contributions: dict
    input_features: dict

def init_db():
    """Initialize the SQLite database for logging predictions."""
    db_path = 'data/predictions.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            bedrooms INTEGER,
            bathrooms REAL,
            lat REAL,
            long REAL,
            sqft INTEGER,
            predicted_price REAL,
            confidence_lower REAL,
            confidence_upper REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def log_prediction(request: PredictionRequest, response: dict):
    """Log prediction to SQLite database."""
    db_path = 'data/predictions.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions 
        (timestamp, bedrooms, bathrooms, lat, long, sqft, predicted_price, confidence_lower, confidence_upper)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        request.bedrooms,
        request.bathrooms,
        request.lat,
        request.long,
        request.sqft,
        response['predicted_price'],
        response['confidence_interval']['lower'],
        response['confidence_interval']['upper']
    ))
    
    conn.commit()
    conn.close()

@router.post('/predict', response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Make prediction
        result = predict_price(
            n_bed=request.bedrooms,
            n_bath=request.bathrooms,
            lat=request.lat,
            long=request.long,
            sqft=request.sqft
        )
        
        # Initialize database if not exists
        init_db()
        
        # Log prediction
        log_prediction(request, result)
        
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Model not found. Please train the model first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")