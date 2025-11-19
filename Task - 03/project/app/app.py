import streamlit as st
from pages import descriptive, inferential, predict

def main():
    # Configure the page
    st.set_page_config(
        page_title="King County House Price Prediction",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f3a93;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
            background: linear-gradient(90deg, #1f3a93, #3a5bc7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .welcome-card {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            text-align: center;
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        }
        .welcome-card h1 {
            color: white;
            margin-bottom: 1rem;
            font-size: 2rem;
        }
        .welcome-card p {
            font-size: 1.2rem;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
        }
        .sidebar-title {
            font-size: 1.3rem;
            color: #1f3a93;
            font-weight: bold;
        }
        .info-box {
            background-color: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        .success-box {
            background-color: #e8f5e9;
            border-left: 5px solid #4caf50;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        .warning-box {
            background-color: #fff8e1;
            border-left: 5px solid #ffc107;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        .stButton>button {
            background-color: #1f3a93;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #3a5bc7;
        }
        footer {
            text-align: center;
            padding: 1rem;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-running {
            background-color: #4CAF50;
        }
        .status-stopped {
            background-color: #f44336;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main header with enhanced styling
    st.markdown('<h1>🏠 King County House Price Prediction</h1>', unsafe_allow_html=True)
    
    # Add a brief introduction with enhanced styling
    st.markdown("""
        <div class="welcome-card">
            <h1>Welcome to the King County House Price Prediction Application</h1>
            <p>This advanced machine learning tool predicts house prices based on key property features. 
            Navigate through the sections to explore comprehensive data insights and make accurate price predictions.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced UI
    with st.sidebar:
        st.markdown('<p class="sidebar-title">🧭 Navigation</p>', unsafe_allow_html=True)
        page = st.radio(
            'Select a page:',
            ['📊 Descriptive Stats', '🔬 Inferential Stats', '🔮 Price Prediction'],
            label_visibility='collapsed'
        )
        
        st.markdown("---")
        st.markdown('<p class="sidebar-title">📋 Project Overview</p>', unsafe_allow_html=True)
        st.markdown("""
        - 📊 Exploratory Data Analysis
        - 🔬 Inferential Statistics
        - 🔮 House Price Prediction
        """)
        
        st.markdown("---")
        st.markdown('<p class="sidebar-title">⚙️ System Status</p>', unsafe_allow_html=True)
        
        # Status indicators
        st.markdown('<span class="status-indicator status-running"></span> Backend API: Running', unsafe_allow_html=True)
        st.markdown('<span class="status-indicator status-running"></span> Model: Trained', unsafe_allow_html=True)
        st.markdown('<span class="status-indicator status-running"></span> Database: Connected', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<p class="sidebar-title">💡 Quick Tips</p>', unsafe_allow_html=True)
        st.info("💡 Tip: Use the navigation menu to switch between different sections of the application.")
        st.info("📈 Tip: The prediction model uses only 5 key features but internally reconstructs all necessary features.")
        st.info("📊 Tip: Explore the descriptive and inferential statistics to understand the data better.")
    
    # Display selected page
    if page == '📊 Descriptive Stats':
        descriptive.show()
    elif page == '🔬 Inferential Stats':
        inferential.show()
    elif page == '🔮 Price Prediction':
        predict.show()
    
    # Footer with enhanced styling
    st.markdown("---")
    st.markdown("""
        <footer>
            King County House Price Prediction App | Built with Streamlit, FastAPI, and Scikit-learn
        </footer>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()