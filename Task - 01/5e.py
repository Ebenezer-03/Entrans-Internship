
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:\\Artificial Intelligence and Data Science\\Task - 01\\clean_sales.pkl"
df = pd.read_pickle(file_path)

def gender_distribution(df):
    gender_counts = df['Customer_Gender'].value_counts()
    
    plt.figure(figsize=(6,6))
    gender_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99'])
    plt.ylabel('')
    plt.title('Gender Distribution')
    plt.savefig('./Output/gender_distribution_pie.jpg')
    plt.show()
if __name__ == "__main__":
    gender_distribution(df) 
    