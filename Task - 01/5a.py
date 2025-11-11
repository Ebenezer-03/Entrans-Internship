import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
# Load your cleaned dataset
df = pd.read_pickle(file_path)


def summary_statistics(df):
    summary = df.describe()
    print(summary)
    summary.to_csv("./Output/summary_statistics.csv")

if __name__ == "__main__":
    summary_statistics(df)
    print("Summary statistics saved.")