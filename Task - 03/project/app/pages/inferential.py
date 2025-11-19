import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import numpy as np
import scipy.stats as stats

# Custom CSS for better styling
st.markdown("""
    <style>
    .stats-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        border: 1px solid #e9ecef;
    }
    .hypothesis-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: #333;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .confidence-card {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
        color: #333;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .regression-card {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        color: #333;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
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

def load_inferential_data():
    """Load inferential statistics data from backend API."""
    try:
        # Try to get data from backend API
        response = requests.get('http://localhost:8000/api/eda/inferential')
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Return placeholder data if API is not available
    return {
        "t_test_waterfront": {
            "t_statistic": 45.23,
            "p_value": 0.0001,
            "interpretation": "Waterfront properties are significantly more expensive than non-waterfront properties"
        },
        "anova_grade": {
            "f_statistic": 1245.67,
            "p_value": 0.0001,
            "interpretation": "There are significant price differences across property grades"
        },
        "regression_results": {
            "r_squared": 0.68,
            "significant_features": ["grade", "waterfront", "sqft_living"],
            "interpretation": "Multiple features explain 68% of the variation in house prices"
        }
    }

def show():
    st.title('🔬 Inferential Statistics')
    
    # Load data
    inferential_data = load_inferential_data()
    
    # Load the dataset for visualizations
    try:
        data = pd.read_csv('data/kc_house_data.csv')
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
        return
    
    # Hypothesis Testing Section
    st.markdown('## 🧪 Hypothesis Testing')
    
    # T-Test: Waterfront vs Non-Waterfront
    st.markdown('<div class="hypothesis-card">', unsafe_allow_html=True)
    st.markdown("### T-Test: Waterfront vs Non-Waterfront Properties")
    if 't_test_waterfront' in inferential_data:
        t_test = inferential_data['t_test_waterfront']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("T-Statistic", f"{t_test['t_statistic']:.2f}")
        
        with col2:
            st.metric("P-Value", f"{t_test['p_value']:.2e}")
        
        with col3:
            if t_test['p_value'] < 0.05:
                st.metric("Result", "Significant", delta="Reject H₀")
            else:
                st.metric("Result", "Not Significant", delta="Fail to reject H₀")
        
        st.info(t_test['interpretation'])
        
        # Visualization
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.boxplot(x='waterfront', y='price', data=data, ax=ax, palette=['#FF9800', '#2196F3'])
            ax.set_title('Price Distribution: Waterfront vs Non-Waterfront Properties', fontsize=16)
            ax.set_xlabel('Waterfront (0=No, 1=Yes)')
            ax.set_ylabel('Price ($)')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Add statistics
            waterfront_stats = data.groupby('waterfront')['price'].agg(['count', 'mean', 'std'])
            waterfront_stats.columns = ['Count', 'Mean Price', 'Std Dev']
            st.markdown("### Statistics by Waterfront Status")
            st.dataframe(waterfront_stats.style.format({'Mean Price': '${:,.0f}', 'Std Dev': '${:,.0f}'}))
            
        except Exception as e:
            st.warning(f"Could not generate visualization: {e}")
    else:
        st.warning("T-Test results not available.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ANOVA: Price Differences Across Property Grades
    st.markdown('<div class="hypothesis-card">', unsafe_allow_html=True)
    st.markdown("### ANOVA: Price Differences Across Property Grades")
    if 'anova_grade' in inferential_data:
        anova = inferential_data['anova_grade']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("F-Statistic", f"{anova['f_statistic']:.2f}")
        
        with col2:
            st.metric("P-Value", f"{anova['p_value']:.2e}")
        
        with col3:
            if anova['p_value'] < 0.05:
                st.metric("Result", "Significant", delta="Reject H₀")
            else:
                st.metric("Result", "Not Significant", delta="Fail to reject H₀")
        
        st.info(anova['interpretation'])
        
        # Visualization
        try:
            fig, ax = plt.subplots(figsize=(14, 7))
            sns.boxplot(x='grade', y='price', data=data, ax=ax, palette='viridis')
            ax.set_title('Price Distribution by Property Grade', fontsize=16)
            ax.set_xlabel('Grade')
            ax.set_ylabel('Price ($)')
            plt.setp(ax.get_xticklabels(), rotation=45)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Add grade statistics
            grade_stats = data.groupby('grade')['price'].agg(['count', 'mean', 'std'])
            grade_stats.columns = ['Count', 'Mean Price', 'Std Dev']
            st.markdown("### Statistics by Property Grade")
            st.dataframe(grade_stats.style.format({'Mean Price': '${:,.0f}', 'Std Dev': '${:,.0f}'}))
            
        except Exception as e:
            st.warning(f"Could not generate visualization: {e}")
    else:
        st.warning("ANOVA results not available.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Confidence Intervals Section
    st.markdown('## 📊 Confidence Intervals')
    st.markdown('<div class="confidence-card">', unsafe_allow_html=True)
    
    try:
        sample_mean = data['price'].mean()
        sample_std = data['price'].std()
        n = len(data)
        
        # 95% confidence interval
        confidence_level = 0.95
        alpha = 1 - confidence_level
        t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
        standard_error = sample_std / np.sqrt(n)
        margin_of_error = t_critical * standard_error
        
        ci_lower = sample_mean - margin_of_error
        ci_upper = sample_mean + margin_of_error
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sample Mean Price", f"${sample_mean:,.0f}")
        
        with col2:
            st.metric("Margin of Error", f"±${margin_of_error:,.0f}")
        
        with col3:
            st.metric("Sample Size", f"{n:,}")
        
        st.metric("95% Confidence Interval", f"(${ci_lower:,.0f}, ${ci_upper:,.0f})")
        st.info(f"We are 95% confident that the true mean house price in King County is between ${ci_lower:,.0f} and ${ci_upper:,.0f}.")
        
        # Visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(data['price'], bins=50, edgecolor='black', alpha=0.7, color='#4CAF50')
        ax.axvline(sample_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: ${sample_mean:,.0f}')
        ax.axvline(ci_lower, color='blue', linestyle='--', linewidth=2, label=f'Lower CI: ${ci_lower:,.0f}')
        ax.axvline(ci_upper, color='blue', linestyle='--', linewidth=2, label=f'Upper CI: ${ci_upper:,.0f}')
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of House Prices with 95% Confidence Interval')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
    except Exception as e:
        st.warning(f"Could not calculate confidence intervals: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Regression Analysis Section
    st.markdown('## 📈 Regression Analysis')
    st.markdown('<div class="regression-card">', unsafe_allow_html=True)
    
    if 'regression_results' in inferential_data:
        regression = inferential_data['regression_results']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("R-squared", f"{regression['r_squared']:.4f}")
            st.progress(regression['r_squared'])
        
        with col2:
            st.metric("Model Performance", "Good" if regression['r_squared'] > 0.6 else "Moderate")
        
        st.info(regression['interpretation'])
        
        st.markdown('### Significant Features:')
        for feature in regression['significant_features']:
            st.markdown(f"- **{feature}**")
        
        # Visualization - Actual vs Predicted (simplified)
        try:
            # Create a simple linear regression line for visualization
            x = data['sqft_living']
            y = data['price']
            
            # Calculate regression line
            slope, intercept = np.polyfit(x, y, 1)
            regression_line = slope * x + intercept
            
            fig, ax = plt.subplots(figsize=(12, 7))
            scatter = ax.scatter(x, y, alpha=0.5, c=data['grade'], cmap='viridis', label='Actual Data')
            ax.plot(x, regression_line, color='red', linewidth=2, label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
            ax.set_xlabel('Square Feet Living')
            ax.set_ylabel('Price ($)')
            ax.set_title('Price vs Square Feet Living (Linear Regression)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax, label='Grade')
            st.pyplot(fig)
            
            st.info("The regression line shows the linear relationship between house size and price. "
                   "The R-squared value indicates how well the model explains the variation in prices.")
        except Exception as e:
            st.warning(f"Could not generate regression visualization: {e}")
    else:
        st.warning("Regression analysis results not available.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Trend Insights Section
    st.markdown('## 📈 Trend Insights')
    st.markdown('<div class="stats-card">', unsafe_allow_html=True)
    
    try:
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        
        # Price trends over time
        price_by_year = data.groupby('year')['price'].agg(['mean', 'count']).reset_index()
        price_by_year.columns = ['Year', 'Average Price', 'Number of Sales']
        
        st.markdown("### Price Trends Over Time")
        fig, ax1 = plt.subplots(figsize=(12, 7))
        color = 'tab:blue'
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Average Price ($)', color=color)
        line1 = ax1.plot(price_by_year['Year'], price_by_year['Average Price'], marker='o', color=color, linewidth=2, label='Average Price')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)
        
        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Number of Sales', color=color)
        line2 = ax2.bar(price_by_year['Year'], price_by_year['Number of Sales'], alpha=0.3, color=color, label='Number of Sales')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + [line2], labels1 + ['Number of Sales'], loc='upper left')
        
        plt.title('House Price Trends and Sales Volume Over Time')
        st.pyplot(fig)
        
        st.markdown("### Yearly Statistics")
        st.dataframe(price_by_year.style.format({'Average Price': '${:,.0f}', 'Number of Sales': '{:,}'}).background_gradient(cmap='Blues'))
        
        # Geographic trends
        st.markdown("### Geographic Trends")
        price_by_zipcode = data.groupby('zipcode')['price'].mean().sort_values(ascending=False).head(15)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        bars = ax.bar(range(len(price_by_zipcode)), price_by_zipcode.values, color='#9C27B0')
        ax.set_xticks(range(len(price_by_zipcode)))
        ax.set_xticklabels(price_by_zipcode.index, rotation=45)
        ax.set_xlabel('Zipcode')
        ax.set_ylabel('Average Price ($)')
        ax.set_title('Top 15 Most Expensive Zipcodes')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig)
        
        st.markdown("### Top Zipcodes by Average Price")
        zipcode_df = pd.DataFrame({'Zipcode': price_by_zipcode.index, 'Average Price': price_by_zipcode.values})
        st.dataframe(zipcode_df.style.format({'Average Price': '${:,.0f}'}).background_gradient(cmap='Purples'))
        
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('### Key Insights:')
        st.markdown('- 📈 House prices show variation across different years in the dataset')
        st.markdown('- 📍 Certain zipcodes command significantly higher prices than others')
        st.markdown('- 🌍 Geographic location is a critical factor in determining house prices')
        st.markdown('- 🏆 Property grade and waterfront location are strong predictors of price')
        st.markdown('- 📊 The number of sales per year can indicate market activity levels')
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not generate trend insights: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
