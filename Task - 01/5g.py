import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def profit_by_product_category(df):
    profit_data = df.groupby('Product_Category')['Profit'].sum().sort_values()
    plt.figure(figsize=(10,6))
    profit_data.plot(kind='barh', color='teal')
    plt.title('Profit by Product Category')
    plt.xlabel('Total Profit')
    plt.ylabel('Product Category')
    plt.savefig('./Output/profit_by_product_category.jpg')
    plt.show()
    
if __name__ == "__main__":
    profit_by_product_category(df)
