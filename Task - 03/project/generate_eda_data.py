import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

# Create reports directory if it doesn't exist
reports_dir = Path("reports/eda")
reports_dir.mkdir(parents=True, exist_ok=True)

# Load the dataset
data = pd.read_csv('data/kc_house_data.csv')

# Generate summary statistics
numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()

# Summary statistics
summary_statistics = data[numeric_cols].describe().to_dict()

# Missing values
missing_values = data.isnull().sum().to_dict()

# Outlier detection
q1 = data[numeric_cols].quantile(0.25)
q3 = data[numeric_cols].quantile(0.75)
iqr = q3 - q1
outlier_mask = (data[numeric_cols] < (q1 - 1.5 * iqr)) | (data[numeric_cols] > (q3 + 1.5 * iqr))
outlier_counts = outlier_mask.sum().to_dict()

# Create the EDA summary
eda_summary = {
    "summary_statistics": summary_statistics,
    "missing_values": missing_values,
    "outlier_counts": outlier_counts
}

# Save to JSON file
summary_path = reports_dir / "eda_summary.json"
with open(summary_path, "w") as f:
    json.dump(eda_summary, f, indent=2)

print(f"EDA summary saved to {summary_path}")