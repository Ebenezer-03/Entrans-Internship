import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------
# 1. PCA From Scratch (Optimized & Vectorized)
# ---------------------------------------------------------
class PCA:
    def __init__(self, n_components):
        self.n_components = n_components

    def fit(self, X):
        # Standardize
        X = StandardScaler().fit_transform(X)
        self.mean = X.mean(axis=0)
        X_centered = X - self.mean

        # Covariance matrix
        cov_matrix = np.cov(X_centered, rowvar=False)

        # Eigenvalues and eigenvectors
        eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)

        # Sort by largest eigenvalues
        sorted_idx = np.argsort(eig_vals)[::-1]
        self.eig_vals = eig_vals[sorted_idx]
        self.eig_vecs = eig_vecs[:, sorted_idx]

        # Select top components
        self.components = self.eig_vecs[:, :self.n_components]

    def transform(self, X):
        X = StandardScaler().fit_transform(X)
        X_centered = X - X.mean(axis=0)
        return np.dot(X_centered, self.components)


# ---------------------------------------------------------
# 2. Load Dataset (Iris)
# ---------------------------------------------------------
iris = load_iris()
X = iris.data
y = iris.target
target_names = iris.target_names


# ---------------------------------------------------------
# 3. Apply PCA
# ---------------------------------------------------------
pca = PCA(n_components=2)
pca.fit(X)
X_reduced = pca.transform(X)

print("Explained eigenvalues (variance):")
print(pca.eig_vals[:2])


# ---------------------------------------------------------
# 4. Visualization (Saved, Non-blocking)
# ---------------------------------------------------------
plt.figure(figsize=(8, 6))
colors = ['red', 'green', 'blue']

for i, target in enumerate(np.unique(y)):
    plt.scatter(
        X_reduced[y == target, 0],
        X_reduced[y == target, 1],
        color=colors[i],
        label=target_names[i]
    )

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA on Iris Dataset (2 Components)")
plt.legend()

plt.savefig("pca_output.png", dpi=300)
print("\nPlot saved as: pca_output.png")
