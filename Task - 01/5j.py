import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def profit_margin_vs_profit(df):
    df['Profit_Margin'] = (df['Profit'] / df['Revenue']) * 100
    plt.figure(figsize=(8,6))
    sns.scatterplot(x='Profit_Margin', y='Profit', size='Profit', data=df, alpha=0.6)
    plt.title('Profit Margin vs Profit')
    plt.xlabel('Profit Margin (%)')
    plt.ylabel('Profit')
    plt.savefig('./Output/profit_margin_vs_profit.jpg')
    plt.show()
if __name__ == "__main__":
    profit_margin_vs_profit(df)
