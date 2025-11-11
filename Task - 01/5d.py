import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)

def boxplot_revenue_by_age(df):
    plt.figure(figsize=(12,8))
    sns.boxplot(x='Age_Group', y='Revenue', data=df)
    plt.title('Revenue Distribution Across Age Groups')
    plt.xticks(rotation=45)
    plt.savefig('./Output/revenue_boxplot_agegroup.jpg')
    plt.show()

if __name__ == "__main__":
    boxplot_revenue_by_age(df)