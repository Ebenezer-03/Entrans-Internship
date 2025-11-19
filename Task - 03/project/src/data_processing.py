from __future__ import annotations

import json
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .utils import ensure_directory, get_path_from_config

TARGET_COLUMN = "price"
DATE_COLUMN = "date"


def load_raw_data() -> pd.DataFrame:
    """Load the raw King County housing data set using the configured path."""
    data_path = get_path_from_config("paths", "data")
    return pd.read_csv(data_path, parse_dates=[DATE_COLUMN])


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data frame with all engineered features added."""
    data = df.copy()

    # Basic time-based features
    data["sale_year"] = data[DATE_COLUMN].dt.year
    data["sale_month"] = data[DATE_COLUMN].dt.month

    # Core aggregates
    data["total_rooms"] = data["bedrooms"].fillna(0) + data["bathrooms"].fillna(0)
    data["sqft_per_room"] = np.where(
        data["total_rooms"].replace(0, np.nan).notna(),
        data["sqft_living"] / data["total_rooms"].replace(0, np.nan),
        np.nan,
    )
    data["rooms_per_household"] = np.where(
        data["floors"].replace(0, np.nan).notna(),
        data["total_rooms"] / data["floors"].replace(0, np.nan),
        np.nan,
    )

    data["age_of_house"] = data["sale_year"] - data["yr_built"]
    data["since_renovated"] = np.where(
        data["yr_renovated"] == 0,
        data["age_of_house"],
        data["sale_year"] - data["yr_renovated"],
    )

    data["price_per_sqft"] = np.where(
        data["sqft_living"].replace(0, np.nan).notna(),
        data[TARGET_COLUMN] / data["sqft_living"].replace(0, np.nan),
        np.nan,
    )

    data["lat_long_interaction"] = data["lat"] * data["long"]
    data["is_renovated"] = (data["yr_renovated"] > 0).astype(int)
    
    # Additional features
    data["has_basement"] = (data["sqft_basement"] > 0).astype(int)
    data["was_renovated"] = (data["yr_renovated"] > 0).astype(int)
    data["zipcode_str"] = data["zipcode"].astype(str)

    numeric_cols, categorical_cols = get_feature_groups(data)
    data[categorical_cols] = data[categorical_cols].astype(str)
    data = data.replace([np.inf, -np.inf], np.nan)

    return data


def get_feature_groups(data: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Return the lists of numeric and categorical feature names for modeling."""
    engineered_exclusions = {
        TARGET_COLUMN,
        DATE_COLUMN,
        "id",
        "sale_year",
        "price_per_sqft",
    }

    base_numeric = [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "sqft_above",
        "sqft_basement",
        "lat",
        "long",
        "sqft_living15",
        "sqft_lot15",
        "total_rooms",
        "sqft_per_room",
        "rooms_per_household",
        "age_of_house",
        "since_renovated",
        "lat_long_interaction",
        "has_basement",
        "was_renovated"
    ]

    base_categorical = [
        "waterfront",
        "view",
        "condition",
        "grade",
        "zipcode_str",
        "sale_month",
        "is_renovated",
    ]

    numeric_cols = [col for col in base_numeric if col in data.columns and col not in engineered_exclusions]
    categorical_cols = [col for col in base_categorical if col in data.columns and col not in engineered_exclusions]
    return numeric_cols, categorical_cols


def build_training_frame() -> Tuple[pd.DataFrame, pd.Series, Dict[str, object]]:
    """Load, engineer and return the features, target and metadata."""
    raw = load_raw_data()
    engineered = engineer_features(raw)
    numeric_cols, categorical_cols = get_feature_groups(engineered)

    numeric_frame = engineered[numeric_cols]
    numeric_medians = numeric_frame.median()
    numeric_filled = numeric_frame.fillna(numeric_medians)

    categorical_frame = engineered[categorical_cols].astype(str)
    categorical_modes: Dict[str, str] = {}
    for column in categorical_cols:
        series = categorical_frame[column]
        mode_series = series[series != "nan"].mode(dropna=True)
        categorical_modes[column] = mode_series.iloc[0] if not mode_series.empty else "Unknown"
    categorical_filled = categorical_frame.fillna(pd.Series(categorical_modes))

    X = pd.concat([numeric_filled, categorical_filled], axis=1)
    y = engineered[TARGET_COLUMN]

    metadata = {
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "numeric_medians": {k: float(v) for k, v in numeric_medians.items()},
        "categorical_modes": categorical_modes,
        "target_mean": float(y.mean()),
        "target_std": float(y.std()),
        "row_count": int(len(engineered)),
        "feature_count": int(X.shape[1]),
    }
    return X, y, metadata


def generate_basic_eda() -> Dict[str, Dict[str, object]]:
    """Generate core descriptive statistics suitable for downstream consumption."""
    df = engineer_features(load_raw_data())
    numeric_cols, categorical_cols = get_feature_groups(df)

    artifacts_dir = ensure_directory(get_path_from_config("paths", "eda_artifacts"))
    results: Dict[str, Dict[str, object]] = {}

    results["summary_statistics"] = df[numeric_cols].describe().to_dict()
    results["missing_values"] = df.isnull().sum().to_dict()

    q1 = df[numeric_cols].quantile(0.25)
    q3 = df[numeric_cols].quantile(0.75)
    iqr = q3 - q1
    outlier_mask = (df[numeric_cols] < (q1 - 1.5 * iqr)) | (df[numeric_cols] > (q3 + 1.5 * iqr))
    results["outlier_counts"] = outlier_mask.sum().to_dict()

    correlation = df[numeric_cols].corr()
    correlation_path = artifacts_dir / "correlation_matrix.csv"
    correlation.to_csv(correlation_path, index=True)
    results["correlation_matrix_path"] = str(correlation_path)

    df[categorical_cols].to_csv(artifacts_dir / "categorical_snapshot.csv", index=False)
    results["categorical_columns"] = categorical_cols
    results["numeric_columns"] = numeric_cols

    # Persist summary for backend reuse
    summary_path = artifacts_dir / "eda_summary.json"
    with summary_path.open("w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    results["eda_summary_path"] = str(summary_path)
    return results
