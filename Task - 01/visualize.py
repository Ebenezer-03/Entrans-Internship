import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)

sns.histplot(df["Customer_Age"]) # type: ignore
plt.savefig("age_hist.png")
plt.close()

sns.countplot(x=df["Customer_Gender"])
plt.savefig("gender.png")
plt.close()

sns.barplot(x=df["Age_Group"], y=df["Revenue"])
plt.savefig("age_revenue.png")
plt.close()

df.groupby("Product_Category")["Profit"].sum().sort_values().plot(kind="barh")
plt.savefig("profit_category.png")
plt.close()

print("done")