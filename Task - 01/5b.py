import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)


def total_counts(df):
    print("Unique Product Categories:", df['Product_Category'].nunique())
    print("Unique Sub Categories:", df['Sub_Category'].nunique())
    print("Unique Products:", df['Product'].nunique())

if __name__ == "__main__":
    total_counts(df)
    print("Total counts printed.")