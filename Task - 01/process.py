import pandas as pd
file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\sales_data - sales_data.csv"
df = pd.read_csv(file_path)
df.drop_duplicates(inplace=True)
df.to_pickle("clean_sales.pkl")
print("done")