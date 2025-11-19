import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import numpy as np

# Custom CSS for better styling
st.markdown("""
    <style>
    .prediction-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        border: 1px solid #e9ecef;
    }
    .prediction-result {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .feature-card {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .insight-card {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .stProgress > div > div > div {
        background-color: #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

def predict_price_api(n_bed, n_bath, latitude, longitude, sqft):
    """Call the backend API to make a price prediction."""
    try:
        # Prepare the payload
        payload = {
            'bedrooms': n_bed,
            'bathrooms': n_bath,
            'lat': latitude,
            'long': longitude,
            'sqft': sqft
        }
        
        # Make API call
        response = requests.post('http://localhost:8000/api/predict', json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to prediction API: {e}")
        return None

def show():
    st.title('🔮 House Price Prediction')
    
    st.markdown("""
    <div class="prediction-card">
        <h3>Predict House Prices in King County</h3>
        <p>Enter the key features of the house to get a price prediction along with confidence intervals and feature contributions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create input form with enhanced UI
    with st.form("prediction_form"):
        st.markdown("### 🏠 House Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            n_bed = st.slider('🛏️ Number of Bedrooms', min_value=1, max_value=10, value=3, step=1)
            n_bath = st.slider('🛁 Number of Bathrooms', min_value=1.0, max_value=6.0, value=2.0, step=0.25)
            sqft = st.number_input('📐 Square Feet', min_value=500, max_value=15000, value=2000, step=100,
                                 help="Total interior living space in square feet")
        
        with col2:
            latitude = st.number_input('📍 Latitude', value=47.5112, format="%.4f",
                                     help="Northern coordinate of the property")
            longitude = st.number_input('🗺️ Longitude', value=-122.257, format="%.4f",
                                      help="Western coordinate of the property")
        
        submitted = st.form_submit_button("🔮 Predict Price", type="primary", use_container_width=True)
    
    st.markdown("### ℹ️ Information")
    st.info("The model uses only 5 key features but internally reconstructs all necessary features for accurate predictions.")
    
    st.markdown("### 🎯 Tips")
    st.markdown("""
    - Typical King County homes range from 800-5000 sqft
    - Most homes have 2-5 bedrooms
    - Latitude ranges approximately 47.1-47.8
    - Longitude ranges approximately -122.6 to -121.3
    """)
    
    # Make prediction when form is submitted
    if submitted:
        with st.spinner('🔍 Analyzing property features and making prediction...'):
            result = predict_price_api(n_bed, n_bath, latitude, longitude, sqft)
            
        if result:
            # Display predicted price in a prominent card
            st.markdown('<div class="prediction-result">', unsafe_allow_html=True)
            st.markdown("## 💰 Predicted Price")
            predicted_price = result['predicted_price']
            st.markdown(f"<h1>${predicted_price:,.0f}</h1>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Create columns for key metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric("🛏️ Bedrooms", n_bed)
            
            with metric_col2:
                st.metric("🛁 Bathrooms", n_bath)
            
            with metric_col3:
                st.metric("📐 Square Feet", sqft)
            
            # Display confidence interval with progress bar visualization
            if 'confidence_interval' in result:
                ci = result['confidence_interval']
                st.markdown("### 📊 Confidence Interval")
                
                # Progress bar visualization
                range_size = ci['upper'] - ci['lower']
                position = (predicted_price - ci['lower']) / range_size
                
                st.progress(position)
                st.markdown(f"**95% Confidence Range:** ${ci['lower']:,.0f} - ${ci['upper']:,.0f}")
                
                # Visualization of confidence interval
                fig, ax = plt.subplots(figsize=(10, 2))
                ax.barh([0], [predicted_price], height=0.5, color='#4CAF50', alpha=0.7, label='Predicted Price')
                ax.hlines(0, ci['lower'], ci['upper'], colors='#2196F3', linewidth=5, label='95% Confidence Interval')
                ax.set_xlim(ci['lower'] * 0.9, ci['upper'] * 1.1)
                ax.set_yticks([])
                ax.set_title('Predicted Price with 95% Confidence Interval')
                ax.legend()
                st.pyplot(fig)
            
            # Display feature contributions with enhanced visualization
            if 'feature_contributions' in result and result['feature_contributions']:
                st.markdown("### 📈 Feature Contributions")
                st.info("The following features had the most impact on the prediction:")
                
                # Convert to DataFrame for better visualization
                contributions = result['feature_contributions']
                contrib_df = pd.DataFrame(list(contributions.items()), columns=['Feature', 'Importance'])
                contrib_df = contrib_df.sort_values('Importance', ascending=False).head(10)
                
                # Create bar chart with improved styling
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.barh(contrib_df['Feature'], contrib_df['Importance'], color='#FF9800')
                ax.set_xlabel('Importance Score')
                ax.set_title('Top Feature Contributions to Price Prediction')
                ax.invert_yaxis()  # Highest importance at top
                
                # Add value labels
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width, bar.get_y() + bar.get_height()/2, f'{width:.3f}', 
                            ha='left', va='center', fontsize=9, fontweight='bold')
                
                # Add grid for better readability
                ax.grid(axis='x', alpha=0.3)
                st.pyplot(fig)
                
                # Display as table with styling
                st.dataframe(contrib_df.style.format({'Importance': '{:.4f}'}).background_gradient(cmap='Blues'))
            
            # Display input features in cards
            st.markdown("### 📋 Input Features")
            input_features = result['input_features']
            
            feat_col1, feat_col2, feat_col3, feat_col4, feat_col5 = st.columns(5)
            
            with feat_col1:
                st.markdown(f'<div class="feature-card"><strong>Bedrooms:</strong><br>{n_bed}</div>', unsafe_allow_html=True)
            
            with feat_col2:
                st.markdown(f'<div class="feature-card"><strong>Bathrooms:</strong><br>{n_bath}</div>', unsafe_allow_html=True)
            
            with feat_col3:
                st.markdown(f'<div class="feature-card"><strong>Square Feet:</strong><br>{sqft:,}</div>', unsafe_allow_html=True)
            
            with feat_col4:
                st.markdown(f'<div class="feature-card"><strong>Latitude:</strong><br>{latitude:.4f}</div>', unsafe_allow_html=True)
            
            with feat_col5:
                st.markdown(f'<div class="feature-card"><strong>Longitude:</strong><br>{longitude:.4f}</div>', unsafe_allow_html=True)
            
            # Additional insights with enhanced UI
            st.markdown("### 💡 Market Insights")
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown(f"""
            Based on our analysis:
            
            - 🏠 A {n_bed}-bedroom, {n_bath}-bathroom home of {sqft:,} sqft is estimated at **${predicted_price:,.0f}**
            - 📈 The prediction has a 95% confidence interval of ${ci['lower']:,.0f} to ${ci['upper']:,.0f}
            - 📍 Location significantly impacts pricing, with waterfront properties commanding premium prices
            - 📐 Square footage is typically one of the strongest predictors of house price
            - 🏆 Property grade and condition ratings strongly influence valuation
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("❌ Failed to get prediction. Please make sure the backend API is running.")
            st.info("To start the backend API, run: `uvicorn backend.main:app --reload` in your terminal")
    
    # Information section with improved styling
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    ### 🤖 Prediction Model
    
    This prediction model uses a **Random Forest Regressor** trained on the King County house sales dataset.
    The model takes into account:
    
    #### Property Characteristics
    - 🛏️ Bedrooms and 🛁 bathrooms
    - 📐 Square footage of living space and lot
    
    #### Location Features
    - 🌍 Latitude and longitude coordinates
    - 🏙️ Zipcode and geographic factors
    
    #### Additional Features
    - 📆 Age of house and renovation history
    - 🏞️ View and waterfront status
    - 🏗️ Condition and grade ratings
    
    ### ⚙️ Feature Engineering
    
    The model automatically reconstructs other features based on the 5 inputs you provide to make a comprehensive prediction:
    - Total rooms calculation
    - Price per square foot metrics
    - Age-based features
    - Interaction terms
    
    ### 📊 Model Performance
    
    - **R-squared**: ~0.68 (explains 68% of price variation)
    - **RMSE**: Typically within 15-20% of actual prices
    - **Top Predictors**: Grade, location, and square footage are the strongest predictors
    """)
