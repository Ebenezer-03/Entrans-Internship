import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import os
import numpy as np

# Custom CSS for better styling
st.markdown("""
    <style>
    .eda-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        border: 1px solid #e9ecef;
    }
    .metric-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-card {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def load_eda_data():
    """Load EDA data from backend API or local files."""
    try:
        # Try to get data from backend API
        response = requests.get('http://localhost:8000/api/eda/descriptive')
        if response.status_code == 200:
            return response.json()
    except:
        # Fallback to local files if API is not available
        pass
    
    # If API fails, try to load from local files
    eda_summary_path = 'reports/eda/eda_summary.json'
    if os.path.exists(eda_summary_path):
        with open(eda_summary_path, 'r') as f:
            return json.load(f)
    
    return None

def show():
    st.title('📊 Descriptive Statistics')
    
    # Load data
    eda_data = load_eda_data()
    
    if eda_data is None:
        st.warning("⚠️ No EDA data available. Please run the EDA notebook first.")
        st.info("You can run the EDA notebook by executing: `jupyter notebook notebooks/EDA.ipynb`")
        return
    
    # Load the actual dataset for visualizations
    try:
        data = pd.read_csv('data/kc_house_data.csv')
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
        return
    
    # Summary Statistics with enhanced UI
    st.markdown('## 📈 Summary Statistics')
    
    # Key metrics at the top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Total Properties**")
        st.markdown(f"**{len(data):,}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Avg Price**")
        st.markdown(f"**${data['price'].mean():,.0f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Avg Sqft**")
        st.markdown(f"**{data['sqft_living'].mean():,.0f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Avg Bedrooms**")
        st.markdown(f"**{data['bedrooms'].mean():.1f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if 'summary_statistics' in eda_data:
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        st.markdown("### Detailed Summary")
        summary_df = pd.DataFrame(eda_data['summary_statistics'])
        st.dataframe(summary_df.style.format(precision=2).background_gradient(cmap='Blues'))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Summary statistics not available.")
    
    # Missing Values Report
    st.markdown('## ❓ Missing Values Report')
    if 'missing_values' in eda_data:
        missing_df = pd.DataFrame.from_dict(eda_data['missing_values'], orient='index', columns=['Missing Count'])
        missing_df['Percentage'] = (missing_df['Missing Count'] / len(data)) * 100
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        
        if len(missing_df) > 0:
            st.markdown('<div class="eda-card">', unsafe_allow_html=True)
            st.dataframe(missing_df.style.format({'Percentage': '{:.2f}%'}).background_gradient(cmap='Reds'))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No missing values found in the dataset!")
    else:
        st.warning("Missing values report not available.")
    
    # Outlier Analysis
    st.markdown('## 🚨 Outlier Analysis')
    if 'outlier_counts' in eda_data:
        outlier_df = pd.DataFrame.from_dict(eda_data['outlier_counts'], orient='index', columns=['Outlier Count'])
        outlier_df['Percentage'] = (outlier_df['Outlier Count'] / len(data)) * 100
        outlier_df = outlier_df[outlier_df['Outlier Count'] > 0].sort_values('Outlier Count', ascending=False)
        
        if len(outlier_df) > 0:
            st.markdown('<div class="eda-card">', unsafe_allow_html=True)
            st.dataframe(outlier_df.style.format({'Percentage': '{:.2f}%'}).background_gradient(cmap='Oranges'))
            
            # Visualization of outliers
            st.markdown("### Outlier Visualization")
            outlier_cols = outlier_df.head(5).index.tolist()
            fig, ax = plt.subplots(figsize=(12, 6))
            data[outlier_cols].boxplot(ax=ax)
            ax.set_title('Distribution of Features with Outliers')
            ax.set_ylabel('Values')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No significant outliers detected!")
    else:
        st.warning("Outlier analysis not available.")
    
    # Distribution Plots
    st.markdown('## 📊 Distribution Plots')
    try:
        # Select columns to plot (limit to prevent overcrowding)
        cols_to_plot = numeric_cols[:min(8, len(numeric_cols))]
        
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        st.markdown("### Price Distribution")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(data['price'], bins=50, edgecolor='black', alpha=0.7, color='#4CAF50')
        ax.set_title('Distribution of House Prices', fontsize=16)
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        # Add statistics
        st.markdown("### Price Statistics")
        price_stats = data['price'].describe()
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Mean", f"${price_stats['mean']:,.0f}")
        
        with stat_col2:
            st.metric("Median", f"${data['price'].median():,.0f}")
        
        with stat_col3:
            st.metric("Min", f"${price_stats['min']:,.0f}")
        
        with stat_col4:
            st.metric("Max", f"${price_stats['max']:,.0f}")
        
        st.markdown("### Feature Distributions")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()
        
        for i, col in enumerate(cols_to_plot[:4]):  # Plot first 4 columns
            axes[i].hist(data[col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#2196F3')
            axes[i].set_title(f'Distribution of {col}', fontsize=14)
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.warning(f"Could not generate distribution plots: {e}")
    
    # Correlation Heatmap
    st.markdown('## 🔗 Correlation Analysis')
    try:
        corr_data = data[numeric_cols].corr()
        
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        st.markdown("### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(14, 12))
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', square=True, 
                    cbar_kws={"shrink": .8}, ax=ax, center=0)
        plt.title('Feature Correlation Matrix', fontsize=16)
        st.pyplot(fig)
        
        # Extract top correlations (excluding self-correlations)
        corr_pairs = []
        for i in range(len(corr_data.columns)):
            for j in range(i+1, len(corr_data.columns)):
                corr_pairs.append({
                    'Feature 1': corr_data.columns[i],
                    'Feature 2': corr_data.columns[j],
                    'Correlation': corr_data.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df['Abs Correlation'] = abs(corr_df['Correlation'])
        top_corr = corr_df.sort_values('Abs Correlation', ascending=False).head(10)
        
        st.markdown("### Top 10 Feature Correlations")
        st.dataframe(top_corr[['Feature 1', 'Feature 2', 'Correlation']].style.format({'Correlation': '{:.3f}'}).background_gradient(cmap='RdYlBu_r', subset=['Correlation']))
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not generate correlation analysis: {e}")
    
    # Scatter Plots
    st.markdown('## 📈 Relationship Analysis')
    try:
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        st.markdown("### Price vs Square Feet")
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(data['sqft_living'], data['price'], alpha=0.5, c=data['grade'], cmap='viridis')
        ax.set_xlabel('Square Feet Living')
        ax.set_ylabel('Price')
        ax.set_title('Price vs Square Feet (colored by grade)')
        plt.colorbar(scatter, ax=ax, label='Grade')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### Price vs Bedrooms")
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='bedrooms', y='price', data=data, ax=ax)
        ax.set_xlabel('Number of Bedrooms')
        ax.set_ylabel('Price')
        ax.set_title('Price Distribution by Number of Bedrooms')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### Price vs Grade")
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='grade', y='price', data=data, ax=ax)
        ax.set_xlabel('Property Grade')
        ax.set_ylabel('Price')
        ax.set_title('Price Distribution by Property Grade')
        ax.grid(True, alpha=0.3)
        plt.setp(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not generate scatter plots: {e}")
    
    # Feature Engineering Exploration
    st.markdown('## ⚙️ Feature Engineering Insights')
    try:
        st.markdown('<div class="eda-card">', unsafe_allow_html=True)
        # Create some engineered features for display
        data['price_per_sqft'] = data['price'] / data['sqft_living']
        data['age'] = 2015 - data['yr_built']  # Using 2015 as reference from the dataset
        data['is_renovated'] = (data['yr_renovated'] > 0).astype(int)
        data['total_rooms'] = data['bedrooms'] + data['bathrooms']
        
        engineered_features = ['price_per_sqft', 'age', 'is_renovated', 'total_rooms']
        
        st.markdown("### Statistical Summary")
        st.dataframe(data[engineered_features].describe().style.format(precision=2).background_gradient(cmap='Purples'))
        
        st.markdown("### Visualizations")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()
        
        # Price per sqft distribution
        axes[0].hist(data['price_per_sqft'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='#FF9800')
        axes[0].set_title('Price per Square Foot Distribution')
        axes[0].set_xlabel('Price per Sqft ($)')
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Age distribution
        axes[1].hist(data['age'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='#E91E63')
        axes[1].set_title('House Age Distribution')
        axes[1].set_xlabel('Age (years)')
        axes[1].set_ylabel('Frequency')
        axes[1].grid(True, alpha=0.3)
        
        # Renovated vs not renovated
        renovated_counts = data['is_renovated'].value_counts()
        axes[2].pie(renovated_counts.values, labels=['Not Renovated', 'Renovated'], autopct='%1.1f%%', 
                    colors=['#2196F3', '#4CAF50'])
        axes[2].set_title('Renovation Status')
        
        # Total rooms distribution
        axes[3].hist(data['total_rooms'].dropna(), bins=20, edgecolor='black', alpha=0.7, color='#9C27B0')
        axes[3].set_title('Total Rooms Distribution')
        axes[3].set_xlabel('Total Rooms')
        axes[3].set_ylabel('Frequency')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('### Key Insights:')
        st.markdown('- 💰 **Price per square foot** helps normalize price across different house sizes')
        st.markdown('- 📆 **Age of house** provides temporal context and affects valuation')
        st.markdown('- 🛠️ **Renovation status** indicates property improvements that add value')
        st.markdown('- 🏠 **Total rooms** combines bedrooms and bathrooms for a holistic view')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not generate feature engineering exploration: {e}")
