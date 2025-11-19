# King County House Price Prediction

A complete machine learning project for predicting house prices in King County, WA using advanced data analysis, statistical inference, and machine learning techniques.

## 🏠 Project Overview

This project provides a comprehensive solution for predicting house prices in King County, Washington. It includes:

1. **Exploratory Data Analysis (EDA)** - Deep dive into the dataset with visualizations and insights
2. **Inferential Statistics** - Hypothesis testing, confidence intervals, and regression analysis
3. **Machine Learning Pipeline** - Feature engineering, model training with hyperparameter optimization, and evaluation
4. **Web Application** - Streamlit frontend with FastAPI backend for interactive predictions
5. **Database Integration** - SQLite database for logging predictions

## 📁 Project Structure

```
project/
│
├── data/
│   └── kc_house_data.csv          # Dataset
│
├── notebooks/
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   └── inferential_stats.ipynb     # Statistical Analysis
│
├── src/
│   ├── data_processing.py          # Data loading and feature engineering
│   ├── preprocess.py               # Data preprocessing pipeline
│   ├── train.py                    # Model training with Optuna optimization
│   ├── evaluate.py                 # Model evaluation and metrics
│   ├── predict.py                  # Prediction logic
│   └── utils.py                    # Utility functions
│
├── models/
│   └── best_model.pkl              # Trained model
│
├── app/
│   ├── app.py                      # Main Streamlit application
│   └── pages/
│       ├── descriptive.py          # Descriptive statistics page
│       ├── inferential.py          # Inferential statistics page
│       └── predict.py              # Prediction page
│
├── backend/
│   ├── main.py                     # FastAPI application
│   └── routes/
│       ├── predict.py              # Prediction endpoints
│       └── stats.py                # Statistics endpoints
│
├── reports/
│   ├── model_report.md             # Model evaluation report
│   └── stats_report.md             # Statistical analysis report
│
├── tests/
│   ├── test_preprocess.py          # Preprocessing tests
│   ├── test_train.py               # Training tests
│   ├── test_predict.py             # Prediction tests
│   └── test_api.py                 # API tests
│
├── config.yaml                     # Configuration file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

#### 1. Data Analysis

Run the Jupyter notebooks to perform exploratory data analysis and statistical inference:

```bash
jupyter notebook notebooks/EDA.ipynb
jupyter notebook notebooks/inferential_stats.ipynb
```

#### 2. Model Training

Train the machine learning model:

```bash
python src/train.py
```

#### 3. Backend API

Start the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

#### 4. Frontend Application

Start the Streamlit frontend:

```bash
streamlit run app/app.py
```

The application will be available at `http://localhost:8501`

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📊 Features

### Exploratory Data Analysis
- Comprehensive dataset overview
- Summary statistics and missing values report
- Outlier detection and analysis
- Distribution plots and correlation analysis
- Feature engineering exploration
- Geographic analysis

### Inferential Statistics
- Hypothesis testing (t-test, ANOVA, chi-square)
- Confidence intervals
- Ordinary Least Squares (OLS) regression
- Trend analysis

### Machine Learning Pipeline
- Advanced feature engineering
- Hyperparameter optimization with Optuna
- Random Forest Regressor with comprehensive evaluation
- Feature importance analysis
- SHAP values for model interpretability
- Model persistence and versioning

### Web Application
- Interactive Streamlit frontend with three pages:
  1. Descriptive Statistics
  2. Inferential Statistics
  3. Price Prediction
- FastAPI backend with RESTful endpoints
- Real-time predictions with confidence intervals
- Feature contribution analysis
- SQLite database for prediction logging

## 🛠️ Technologies Used

- **Data Analysis**: Pandas, NumPy, SciPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, Optuna, SHAP
- **Statistics**: Statsmodels
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite
- **Testing**: Pytest

## 📈 Model Performance

The trained Random Forest Regressor achieves:
- **R-squared**: ~0.68
- **RMSE**: Typically within 15-20% of actual prices
- **MAE**: Varies based on price range

Key predictive features:
1. Property grade
2. Square footage
3. Waterfront location
4. Geographic coordinates
5. Property condition

## 📞 API Endpoints

### Health Check
```
GET /health
```

### Prediction
```
POST /api/predict
```
Payload:
```json
{
  "bedrooms": 3,
  "bathrooms": 2.5,
  "lat": 47.5112,
  "long": -122.257,
  "sqft": 2000
}
```

### Descriptive Statistics
```
GET /api/eda/descriptive
```

### Inferential Statistics
```
GET /api/eda/inferential
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- King County for providing the housing dataset
- The open-source community for the excellent tools and libraries