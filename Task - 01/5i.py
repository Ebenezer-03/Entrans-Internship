import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def profit_margin_per_product(df):
    df['Profit_Margin'] = (df['Profit'] / df['Revenue']) * 100
    plt.figure(figsize=(8,6))
    sns.scatterplot(x='Product', y='Profit_Margin', data=df, color='purple')
    plt.title('Average Profit Margin per Product')
    plt.xticks([], [])
    plt.ylabel('Profit Margin (%)')
    plt.savefig('./Output/profit_margin_scatter.jpg')
    plt.show()
if __name__ == "__main__":
    profit_margin_per_product(df)