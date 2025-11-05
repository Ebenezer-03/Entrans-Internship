from typing import Dict
import pandas as pd

class SalesProcessor:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()
        if "revenue" in self.df.columns:
            self.df["revenue"] = pd.to_numeric(self.df["revenue"], errors="coerce").fillna(0.0)
        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")

    def task_b_total_revenue_by_product(self) -> Dict[str, float]:
        if "product" not in self.df.columns or "revenue" not in self.df.columns:
            raise ValueError("Missing 'product' or 'revenue' column.")
        return {str(k): float(v) for k, v in self.df.groupby("product", dropna=False)["revenue"].sum().items()}

    def task_h_monthly_revenue_trend(self) -> pd.Series:
        if "date" not in self.df.columns or "revenue" not in self.df.columns:
            raise ValueError("Missing 'date' or 'revenue' column.")
        df = self.df.dropna(subset=["date"])
        monthly = df.set_index("date").resample("ME")["revenue"].sum()
        monthly.index = pd.DatetimeIndex(monthly.index).to_period("M").astype(str)
        return monthly.sort_index()

    def product_revenue(self) -> Dict[str, float]:
        return self.task_b_total_revenue_by_product()

    def monthly_trend(self) -> pd.Series:
        return self.task_h_monthly_revenue_trend()