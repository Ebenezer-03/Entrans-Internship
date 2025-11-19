import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import shap
import os

def evaluate_model(pipeline, X_test, y_test, metadata=None):
    """Evaluate the model and generate comprehensive metrics and visualizations."""
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    rmse = mean_squared_error(y_test, y_pred, squared=False) if hasattr(mean_squared_error, 'squared') else mean_squared_error(y_test, y_pred) ** 0.5
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Feature importance
    try:
        feature_importances = pipeline.named_steps['regressor'].feature_importances_
        feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
        
        # Sort features by importance
        indices = np.argsort(feature_importances)[::-1]
        top_features = [(feature_names[i], feature_importances[i]) for i in indices[:15]]
        
        # Plot feature importance
        plt.figure(figsize=(10, 8))
        features, importances = zip(*top_features)
        y_pos = np.arange(len(features))
        plt.barh(y_pos, importances)
        plt.yticks(y_pos, features)
        plt.xlabel('Feature Importance')
        plt.title('Top 15 Feature Importances')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('reports/feature_importance.png')
        plt.close()
    except Exception as e:
        print(f"Could not generate feature importance plot: {e}")
        top_features = []
    
    # Residuals plot
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residuals vs Predicted Values')
    plt.tight_layout()
    plt.savefig('reports/residuals_plot.png')
    plt.close()
    
    # Actual vs Predicted plot
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs Predicted Values')
    plt.tight_layout()
    plt.savefig('reports/actual_vs_predicted.png')
    plt.close()
    
    # Save evaluation report
    with open('reports/model_report.md', 'w') as f:
        f.write('# Model Evaluation Report\n\n')
        f.write(f'## Performance Metrics\n\n')
        f.write(f'- RMSE: ${rmse:,.2f}\n')
        f.write(f'- MAE: ${mae:,.2f}\n')
        f.write(f'- R²: {r2:.4f}\n\n')
        
        f.write(f'## Top Feature Importances\n\n')
        for feature, importance in top_features[:10]:
            f.write(f'- {feature}: {importance:.4f}\n')
    
    # Try to generate SHAP values if possible
    try:
        # Create a small sample for SHAP explanation
        sample = X_test.sample(min(100, len(X_test)))
        
        # Create SHAP explainer
        explainer = shap.Explainer(pipeline.predict, sample)
        shap_values = explainer(sample)
        
        # Summary plot
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, sample, show=False)
        plt.tight_layout()
        plt.savefig('reports/shap_summary.png')
        plt.close()
    except Exception as e:
        print(f"Could not generate SHAP plots: {e}")
    
    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "feature_importances": top_features
    }