from typing import Dict
import pandas as pd
from .validators import DataValidator
from .utils import normalize_columns

class DataLoader:

    COLUMN_MAP: Dict[str, str] = {
        "revenue": "revenue", "total": "revenue", "total_amount": "revenue", "amount": "revenue",
        "product": "product", "product_name": "product", "product_category": "product_category", "sub_category": "sub_category",
        "order_quantity": "quantity", "quantity": "quantity", "qty": "quantity",
        "unit_price": "unit_price", "unit_cost": "unit_cost", "price": "unit_price",
        "date": "date", "order_date": "date",
        "country": "country", "state": "state",
        "customer": "customer", "customer_name": "customer",
    }

    def __init__(self, filepath: str, read_kwargs: dict | None = None) -> None:
        self.filepath = filepath
        self.read_kwargs = read_kwargs or {}
        self.df: pd.DataFrame | None = None

    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath, **self.read_kwargs)
        df.columns = normalize_columns(df.columns)

        df = df.rename(columns={col: self.COLUMN_MAP[col] for col in df.columns if col in self.COLUMN_MAP})

        DataValidator().validate_minimal(df)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        self.df = df
        return df