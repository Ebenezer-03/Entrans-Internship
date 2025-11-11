import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def plot_customer_age_hist(df):
    plt.figure(figsize=(6,4))
    sns.histplot(df['Customer_Age'], bins=20, kde=True, color='skyblue')
    plt.title('Age Distribution of Customers')
    plt.xlabel('Customer Age')
    plt.ylabel('Count')
    plt.savefig('./Output/customer_age_histogram.jpg')
    plt.show()

if __name__ == "__main__":
    plot_customer_age_hist(df)