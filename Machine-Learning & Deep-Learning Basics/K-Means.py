import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


# --------------------------------------------------------
# 1. K-Means Class (Optimized from Scratch)
# --------------------------------------------------------
class KMeans:
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol  # tolerance for centroid movement

    def initialize_centroids(self, X):
        """Pick K random unique points from dataset as initial centroids."""
        idx = np.random.choice(len(X), self.k, replace=False)
        return X[idx]

    def compute_distances(self, X, centroids):
        """Compute distance from each point to each centroid (vectorized)."""
        return np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)

    def assign_clusters(self, distances):
        """Assign each point to closest centroid."""
        return np.argmin(distances, axis=1)

    def update_centroids(self, X, labels):
        """Update centroid positions (vectorized mean)."""
        return np.array([X[labels == i].mean(axis=0) for i in range(self.k)])

    def compute_inertia(self, X, labels, centroids):
        """Compute WCSS (Within-Cluster Sum of Squares)."""
        return np.sum((X - centroids[labels])**2)

    def fit(self, X):
        self.centroids = self.initialize_centroids(X)

        for _ in range(self.max_iters):
            old_centroids = self.centroids.copy()

            distances = self.compute_distances(X, self.centroids)
            self.labels = self.assign_clusters(distances)
            self.centroids = self.update_centroids(X, self.labels)

            # Check convergence
            movement = np.linalg.norm(self.centroids - old_centroids)
            if movement < self.tol:
                break

        self.inertia_ = self.compute_inertia(X, self.labels, self.centroids)

    def predict(self, X):
        distances = self.compute_distances(X, self.centroids)
        return np.argmin(distances, axis=1)


# --------------------------------------------------------
# 2. Create Dataset (Blobs)
# --------------------------------------------------------
X, _ = make_blobs(
    n_samples=600,
    n_features=2,
    centers=3,
    cluster_std=1.2,
    random_state=42
)

# --------------------------------------------------------
# 3. Train K-Means
# --------------------------------------------------------
kmeans = KMeans(k=3)
kmeans.fit(X)

print(f"\nFinal Centroids:\n{kmeans.centroids}")
print(f"\nInertia (WCSS): {kmeans.inertia_:.2f}\n")


# --------------------------------------------------------
# 4. Plot Clusters (Saved Automatically)
# --------------------------------------------------------
colors = np.array(['red', 'blue', 'green'])

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=colors[kmeans.labels], alpha=0.6)
plt.scatter(
    kmeans.centroids[:, 0],
    kmeans.centroids[:, 1],
    c='black',
    s=200,
    marker='X',
    label='Centroids'
)

plt.title("K-Means Clustering (K=3)")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()

plt.savefig("kmeans_clusters.png", dpi=300)
print("Cluster plot saved as: kmeans_clusters.png")
