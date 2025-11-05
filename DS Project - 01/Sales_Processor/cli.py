import argparse
from .data_loader import DataLoader
from .processor import SalesProcessor
import sys


def main():
    parser = argparse.ArgumentParser(description="Sales Processor CLI")
    parser.add_argument("filepath", help="Path to sales CSV file")
    parser.add_argument("--show", choices=["product_revenue", "monthly_trend"], help="What to print")
    args = parser.parse_args()

    try:
        loader = DataLoader(args.filepath)
        df = loader.load()
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        raise SystemExit(1)

    processor = SalesProcessor(df)

    if args.show == "product_revenue":
        out = processor.product_revenue()
        print("Product revenue (product -> revenue):")
        for p, r in out.items():
            print(f"{p}: {r:.2f}")
    elif args.show == "monthly_trend":
        monthly = processor.monthly_trend()
        print("Monthly revenue trend (YYYY-MM -> revenue):")
        print(monthly.to_string())
    else:
        print("Data loaded successfully. Use --show to display product_revenue or monthly_trend.")


if __name__ == "__main__":
    main()
