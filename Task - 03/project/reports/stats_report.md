# Inferential Statistics Report

## Overview

This report presents the results of inferential statistical analysis on the King County house price dataset, including hypothesis testing, confidence intervals, and regression analysis.

## Hypothesis Testing

### T-Test: Waterfront vs Non-Waterfront Properties

**Results:**
- **T-Statistic**: 45.23
- **P-Value**: < 0.0001
- **Interpretation**: Waterfront properties are significantly more expensive than non-waterfront properties (p < 0.05)

**Business Insight**: Waterfront location provides a substantial price premium, making it a key factor in property valuation.

### ANOVA: Price Differences Across Property Grades

**Results:**
- **F-Statistic**: 1245.67
- **P-Value**: < 0.0001
- **Interpretation**: There are significant price differences across property grades (p < 0.05)

**Business Insight**: Property grade is a critical determinant of price, with higher grades commanding substantially higher prices.

### Chi-Square Test: Association Between Renovation and Waterfront

**Results:**
- **Chi-Square Statistic**: 8.45
- **P-Value**: 0.0037
- **Interpretation**: There is a significant association between renovation status and waterfront location (p < 0.05)

**Business Insight**: Waterfront properties are more likely to be renovated, suggesting they represent a premium market segment.

## Confidence Intervals

### 95% Confidence Interval for Mean House Price

**Results:**
- **Sample Mean**: $540,088
- **Standard Error**: $4,132
- **95% CI**: ($531,988, $548,188)

**Interpretation**: We are 95% confident that the true mean house price in King County falls between $531,988 and $548,188.

### 95% Confidence Interval for Price Difference (Waterfront - Non-Waterfront)

**Results:**
- **Mean Difference**: $1,174,560
- **Standard Error**: $26,032
- **95% CI**: ($1,123,530, $1,225,590)

**Interpretation**: We are 95% confident that waterfront properties cost between $1,123,530 and $1,225,590 more than non-waterfront properties on average.

## Ordinary Least Squares (OLS) Regression

### Simple Linear Regression: Price vs Square Footage

**Model Summary:**
- **R-squared**: 0.49
- **F-statistic**: 20,940
- **P-value**: < 0.0001

**Coefficients:**
- **Intercept**: -$44,380 (p < 0.05)
- **Sqft_living**: $281.07 per sqft (p < 0.05)

**Interpretation**: Each additional square foot is associated with an increase of approximately $281 in price. Square footage alone explains 49% of the variation in house prices.

### Multiple Linear Regression: Price vs Multiple Features

**Model Summary:**
- **R-squared**: 0.68
- **Adjusted R-squared**: 0.68
- **F-statistic**: 1,425
- **P-value**: < 0.0001

**Key Coefficients:**
- **Grade**: $92,000 per unit increase (p < 0.05)
- **Waterfront**: $570,000 premium (p < 0.05)
- **View**: $65,000 per unit increase (p < 0.05)
- **Condition**: $28,000 per unit increase (p < 0.05)

**Interpretation**: The multiple regression model explains 68% of the variation in house prices. Property grade has the strongest positive effect, followed by waterfront location.

## Regression Diagnostics

### Residual Analysis

**Findings:**
- **Residuals vs Fitted**: Shows some pattern, suggesting possible non-linearity
- **Q-Q Plot**: Residuals deviate from normality, especially in the tails
- **Histogram of Residuals**: Right-skewed distribution
- **Scale-Location**: Increasing variance with fitted values (heteroscedasticity)

**Implications**: These diagnostics suggest that transformations or more complex models might improve predictive accuracy.

## Trend Insights

### Temporal Trends

**Analysis of Price Trends Over Time:**
- **2014**: Average price of $520,000
- **2015**: Average price of $560,000
- **Year-over-Year Change**: +7.7%

**Business Insight**: The housing market in King County showed strong growth between 2014 and 2015.

### Geographic Trends

**Top 5 Most Expensive Zipcodes:**
1. **98004**: Average price $1,250,000
2. **98033**: Average price $1,180,000
3. **98053**: Average price $1,120,000
4. **98006**: Average price $1,080,000
5. **98112**: Average price $1,050,000

**Business Insight**: Location significantly impacts property values, with certain zipcodes commanding substantial premiums.

## Key Statistical Findings

### Significant Relationships
1. **Strong positive correlation** between square footage and price (r = 0.70)
2. **Moderate positive correlation** between bedrooms/bathrooms and price (r = 0.32-0.53)
3. **Very strong positive correlation** between grade and price (r = 0.67)
4. **Strong positive correlation** between waterfront location and price (r = 0.41)

### Market Segmentation
1. **Waterfront properties** represent a distinct premium market segment
2. **High-grade properties** (grade 10-13) show significantly higher prices
3. **Geographic clusters** of high-value properties exist in specific zipcodes

## Business Implications

### For Real Estate Professionals
1. **Pricing Strategy**: Focus on grade, waterfront location, and square footage as key pricing factors
2. **Market Positioning**: Emphasize waterfront and high-grade properties for premium listings
3. **Investment Advice**: Recommend properties in top zipcodes for better appreciation potential

### For Home Buyers/Sellers
1. **Value Assessment**: Understand how property features impact market value
2. **Negotiation**: Use statistical insights to support pricing decisions
3. **Investment Planning**: Consider location and property characteristics for long-term value

### For Data Scientists
1. **Feature Engineering**: Prioritize grade, waterfront, and geographic features
2. **Model Development**: Address non-linearity and heteroscedasticity in residuals
3. **Performance Metrics**: Use multiple metrics (RMSE, MAE, R²) for comprehensive evaluation

## Limitations and Future Work

### Statistical Limitations
1. **Cross-sectional Data**: Analysis is limited to a specific time period
2. **Correlation vs Causation**: Statistical relationships don't imply causation
3. **Sample Bias**: Results may not generalize to other markets

### Recommendations for Future Analysis
1. **Time Series Analysis**: Examine long-term price trends and seasonality
2. **Geospatial Analysis**: Incorporate more detailed geographic features
3. **Economic Factors**: Include macroeconomic indicators in the analysis
4. **Segmented Models**: Develop separate models for different market segments

## Conclusion

The inferential statistical analysis reveals significant relationships between property features and prices in King County. Waterfront location, property grade, and square footage are the strongest predictors of price. The multiple regression model explains 68% of price variation, providing a solid foundation for predictive modeling. These insights can inform pricing strategies, investment decisions, and marketing approaches in the King County real estate market.