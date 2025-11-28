import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Create a nonlinear dataset
np.random.seed(42)
X = np.linspace(-3, 3, 60).reshape(-1, 1)
y = 0.5 * X**3 - X + np.random.randn(60, 1) * 2

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

degrees = [1, 3, 10]  # low, medium, high complexity

plt.figure(figsize=(15, 4))

for i, d in enumerate(degrees):
    poly = PolynomialFeatures(degree=d)
    X_poly = poly.fit_transform(X_train)

    model = LinearRegression()
    model.fit(X_poly, y_train)

    X_test_poly = poly.transform(X_test)
    y_pred = model.predict(X_test_poly)

    # Plot
    plt.subplot(1, 3, i+1)
    plt.scatter(X_train, y_train, color='blue', label='Train')
    plt.scatter(X_test, y_test, color='red', label='Test')
    X_plot = poly.transform(X)
    plt.plot(X, model.predict(X_plot), color='black')
    plt.title(f"Degree {d}\nTrain error: {mean_squared_error(y_train, model.predict(X_poly)):.2f}\nTest error: {mean_squared_error(y_test, y_pred):.2f}")

plt.tight_layout()
plt.show()
