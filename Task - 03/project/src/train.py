from __future__ import annotations

import json
import optuna
from pathlib import Path
from typing import Any, Dict

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

from .evaluate import evaluate_model
from .preprocess import prepare_features
from .utils import ensure_directory, get_path_from_config, load_config


def objective(trial, X_train, y_train, X_test, y_test, preprocessor):
    """Objective function for Optuna hyperparameter optimization."""
    # Define hyperparameters to optimize
    n_estimators = trial.suggest_int('n_estimators', 100, 500, step=50)
    max_depth = trial.suggest_int('max_depth', 5, 30, step=5)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
    max_features = trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
    
    # Create pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    # Train model
    pipeline.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False) if hasattr(mean_squared_error, 'squared') else mean_squared_error(y_test, y_pred) ** 0.5
    
    return rmse


def optimize_hyperparameters(X_train, y_train, X_test, y_test, preprocessor, n_trials=50):
    """Optimize hyperparameters using Optuna."""
    # Create study
    study = optuna.create_study(direction='minimize')
    
    # Optimize
    study.optimize(
        lambda trial: objective(trial, X_train, y_train, X_test, y_test, preprocessor),
        n_trials=n_trials
    )
    
    return study


def train_model() -> Dict[str, Any]:
    """Train the regression pipeline, evaluate it and persist artifacts."""
    config = load_config()
    X, y, preprocessor, metadata = prepare_features()

    train_cfg = config["training"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=train_cfg.get("test_size", 0.2),
        random_state=train_cfg.get("random_state", 42),
    )

    # Optimize hyperparameters
    print("Optimizing hyperparameters with Optuna...")
    study = optimize_hyperparameters(X_train, y_train, X_test, y_test, preprocessor)
    
    # Get best parameters
    best_params = study.best_params
    print(f"Best parameters: {best_params}")
    
    # Create pipeline with best parameters
    best_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=best_params['n_estimators'],
            max_depth=best_params['max_depth'],
            min_samples_split=best_params['min_samples_split'],
            min_samples_leaf=best_params['min_samples_leaf'],
            max_features=best_params['max_features'],
            random_state=train_cfg.get("random_state", 42),
            n_jobs=-1
        ))
    ])
    
    # Train final model
    print("Training final model with best parameters...")
    best_pipeline.fit(X_train, y_train)

    # Evaluate model
    evaluation = evaluate_model(
        pipeline=best_pipeline,
        X_test=X_test,
        y_test=y_test,
        metadata={**metadata, "random_state": train_cfg.get("random_state", 42)},
    )

    model_dir = ensure_directory(config["paths"]["model_dir"])
    model_path = get_path_from_config("paths", "model_artifact")
    metadata_path = get_path_from_config("paths", "model_metadata")

    joblib.dump(best_pipeline, model_path)

    training_summary = {
        "best_params": best_params,
        "best_score": study.best_value,
        "evaluation": evaluation,
        "metadata": metadata,
        "study_trials": [trial.params for trial in study.trials]
    }

    with metadata_path.open("w", encoding="utf-8") as fh:
        json.dump(training_summary, fh, indent=2)

    return {
        "model_path": str(model_path),
        "metadata_path": str(metadata_path),
        "evaluation": evaluation,
        "best_params": best_params,
    }


if __name__ == "__main__":
    train_model()
