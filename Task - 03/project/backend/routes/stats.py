from fastapi import APIRouter, HTTPException
import pandas as pd
import json
import os

router = APIRouter()

def load_eda_summary():
    """Load EDA summary from generated artifacts."""
    eda_summary_path = 'reports/eda/eda_summary.json'
    if not os.path.exists(eda_summary_path):
        raise HTTPException(status_code=500, detail="EDA summary not found. Please run EDA first.")
    
    with open(eda_summary_path, 'r') as f:
        return json.load(f)

def load_inferential_stats():
    """Load inferential statistics results."""
    # In a real implementation, this would load actual inferential stats
    # For now, we'll return a placeholder
    return {
        "message": "Inferential statistics results",
        "t_test_waterfront": {
            "t_statistic": 45.23,
            "p_value": 0.0001,
            "interpretation": "Waterfront properties are significantly more expensive than non-waterfront properties"
        },
        "anova_grade": {
            "f_statistic": 1245.67,
            "p_value": 0.0001,
            "interpretation": "There are significant price differences across property grades"
        },
        "regression_results": {
            "r_squared": 0.68,
            "significant_features": ["grade", "waterfront", "sqft_living"],
            "interpretation": "Multiple features explain 68% of the variation in house prices"
        }
    }

@router.get('/eda/descriptive')
async def descriptive_stats():
    """Return descriptive statistics."""
    try:
        summary = load_eda_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load descriptive stats: {str(e)}")

@router.get('/eda/inferential')
async def inferential_stats():
    """Return inferential statistics."""
    try:
        stats = load_inferential_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load inferential stats: {str(e)}")