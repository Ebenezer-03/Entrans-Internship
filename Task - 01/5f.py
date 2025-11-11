import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def revenue_by_age_group(df):
    plt.figure(figsize=(8,5))
    sns.barplot(x='Age_Group', y='Revenue', data=df, estimator='sum', ci=None, palette='viridis')
    plt.title('Revenue by Age Group')
    plt.xticks(rotation=45)
    plt.savefig('./Output/revenue_by_agegroup.jpg')
    plt.show()
    
if __name__ == "__main__":
    revenue_by_age_group(df)
