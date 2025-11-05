import pandas as pd
file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\sales_data - sales_data.csv"

df = pd.read_csv(file_path)
print(df.head())
print(df.info())
