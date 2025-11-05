import pandas as pd
from typing import Set


class DataValidator:

    REQUIRED_MINIMAL: Set[str] = {"date", "product", "revenue"}

    def validate_minimal(self, df: pd.DataFrame) -> None:
        missing = set(self.REQUIRED_MINIMAL) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns for processing: {missing}")

    def has_columns(self, df: pd.DataFrame, required: Set[str]) -> bool:
        return set(required).issubset(set(df.columns))

    def total_rows(self, df: pd.DataFrame) -> int:
        return len(df)

    def column_types(self, df: pd.DataFrame) -> dict:
        return {c: str(t) for c, t in df.dtypes.items()}
