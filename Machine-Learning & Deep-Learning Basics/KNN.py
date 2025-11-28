import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# --------------------------------------------------------
# 1. Distance Function (Euclidean)
# --------------------------------------------------------
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


# --------------------------------------------------------
# 2. KNN Class (From Scratch)
# --------------------------------------------------------
class KNN:
    def __init__(self, k=5):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict_one(self, x):
        # Compute distances to all training samples
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]

        # Pick K nearest neighbors
        k_idx = np.argsort(distances)[:self.k]

        # Their labels
        k_neighbor_labels = self.y_train[k_idx]

        # Majority vote
        most_common = Counter(k_neighbor_labels).most_common(1)[0][0]
        return most_common

    def predict(self, X):
        return np.array([self.predict_one(x) for x in X])


# --------------------------------------------------------
# 3. Create a Dataset
# --------------------------------------------------------
X, y = make_classification(
    n_samples=400,
    n_features=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# --------------------------------------------------------
# 4. Train KNN Model
# --------------------------------------------------------
model = KNN(k=5)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\nKNN Accuracy = {acc * 100:.2f}%\n")


# --------------------------------------------------------
# 5. Decision Boundary Visualization
# --------------------------------------------------------
h = 0.02  # mesh step size

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

xx, yy = np.meshgrid(
    np.arange(x_min, x_max, h),
    np.arange(y_min, y_max, h)
)

# Predict on grid
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.4, cmap="RdBu")
plt.scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu", edgecolors='k')
plt.title("KNN Decision Boundary (k = 5)")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
