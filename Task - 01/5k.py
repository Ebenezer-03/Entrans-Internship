import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def subcategory_performance(df):
    grouped = df.groupby(['Product_Category', 'Sub_Category'])[['Profit','Revenue']].sum().reset_index()
    plt.figure(figsize=(12,6))
    sns.barplot(x='Product_Category', y='Revenue', hue='Sub_Category', data=grouped)
    plt.title('Revenue by Sub-Category within Each Product Category')
    plt.xticks(rotation=45)
    plt.savefig('./Output/subcategory_performance.jpg')
    plt.show()
    
if __name__ == "__main__":
    subcategory_performance(df)
