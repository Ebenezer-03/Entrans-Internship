import io
import pandas as pd
import pytest

from Sales_Processor.data_loader import DataLoader
from Sales_Processor.validators import DataValidator
from Sales_Processor.processor import SalesProcessor

CSV_SAMPLE = """Date,Product,Order_Quantity,Unit_Price,Revenue
2025-01-05,Widget,2,10,20
2025-01-20,Gadget,1,15,15
2025-02-10,Widget,3,10,30
2025-02-25,Gadget,2,15,30
2025-03-03,Widget,1,10,10
"""

@pytest.fixture
def sample_df():
    df = pd.read_csv(io.StringIO(CSV_SAMPLE), parse_dates=["Date"])
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    return df.rename(columns={
        "date": "date", "product": "product",
        "order_quantity": "order_quantity", "unit_price": "unit_price",
        "revenue": "revenue"
    })

def test_validator_minimal(sample_df):
    assert DataValidator().has_columns(sample_df, {"date", "product", "revenue"})

def test_total_rows(sample_df):
    assert DataValidator().total_rows(sample_df) == 5

def test_task_b_total_revenue_by_product(sample_df):
    out = SalesProcessor(sample_df).task_b_total_revenue_by_product()
    assert out["Widget"] == 60.0
    assert out["Gadget"] == 45.0

def test_task_h_monthly_revenue_trend(sample_df):
    monthly = SalesProcessor(sample_df).task_h_monthly_revenue_trend()
    assert monthly.loc["2025-01"] == 35.0
    assert monthly.loc["2025-02"] == 60.0
    assert monthly.loc["2025-03"] == 10.0