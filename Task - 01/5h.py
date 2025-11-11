import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def revenue_profit_trend(df, start_month, end_month, year):
    df['Date'] = pd.to_datetime(df['Date'])
    df_filtered = df[(df['Date'].dt.year == year) &
                     (df['Date'].dt.month >= start_month) &
                     (df['Date'].dt.month <= end_month)]
    trend = df_filtered.groupby(df_filtered['Date'].dt.month)[['Revenue','Profit']].sum()

    plt.figure(figsize=(8,5))
    plt.plot(trend.index, trend['Revenue'], marker='o', label='Revenue')
    plt.plot(trend.index, trend['Profit'], marker='o', label='Profit')
    plt.title(f'Monthly Revenue and Profit Trends ({year})')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend()
    plt.savefig('./Output/revenue_profit_trend.jpg')
    plt.show()

if __name__ == "__main__":
    revenue_profit_trend(df, start_month=1, end_month=12, year=2015)