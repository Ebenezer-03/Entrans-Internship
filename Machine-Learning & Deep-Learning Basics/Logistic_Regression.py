import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# ----------------------------
# 1. Create Dataset
# ----------------------------

X, y = make_classification(
    n_samples=300,
    n_features=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=42
)

y = y.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------
# 2. Sigmoid Function
# ----------------------------

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# ----------------------------
# 3. Parameter Initialization
# ----------------------------

def initialize_params(n_features):
    W = np.zeros((n_features, 1))
    b = 0
    return W, b

# ----------------------------
# 4. Prediction Function
# ----------------------------

def predict_proba(X, W, b):
    z = np.dot(X, W) + b
    return sigmoid(z)

# ----------------------------
# 5. Cost Function
# ----------------------------

def compute_cost(y_true, y_pred):
    m = len(y_true)
    cost = -(1/m) * np.sum(y_true*np.log(y_pred) + (1-y_true)*np.log(1-y_pred))
    return cost

# ----------------------------
# 6. Gradient Descent
# ----------------------------

def gradient_descent(X, y, W, b, y_pred, lr):
    m = len(y)
    dW = (1/m) * np.dot(X.T, (y_pred - y))
    db = (1/m) * np.sum(y_pred - y)

    W = W - lr * dW
    b = b - lr * db

    return W, b

# ----------------------------
# 7. Training Loop
# ----------------------------

def train(X, y, lr=0.01, epochs=2000):
    W, b = initialize_params(X.shape[1])
    costs = []

    for i in range(epochs):
        y_pred = predict_proba(X, W, b)
        cost = compute_cost(y, y_pred)
        W, b = gradient_descent(X, y, W, b, y_pred, lr)

        if i % 200 == 0:
            print(f"Epoch {i}: Cost = {cost}")
            costs.append(cost)

    return W, b, costs

# ----------------------------
# 8. Train Model
# ----------------------------

W, b, costs = train(X_train, y_train)

# ----------------------------
# 9. Plot cost
# ----------------------------

plt.plot(costs)
plt.title("Cost Function Over Time")
plt.xlabel("Iterations (x200)")
plt.ylabel("Cost")
plt.show()

# ----------------------------
# 10. Predict
# ----------------------------

def predict(X, W, b):
    y_prob = predict_proba(X, W, b)
    return (y_prob >= 0.5).astype(int)

y_pred = predict(X_test, W, b)

accuracy = np.mean(y_pred == y_test) * 100
print(f"\nModel Accuracy: {accuracy:.2f}%")
