import numpy as np

matrix_a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
U,sigma,Vt = np.linalg.svd(matrix_a)

print(f"Left Singular Vectors (U):\n{U}")
print(f"Singular Values (Sigma):\n{sigma}")
print(f"Right Singular Vectors (V^T):\n{Vt}")

reconstructed_matrix = np.dot(U, np.dot(np.diag(sigma), Vt))
print(f"Reconstructed Matrix from SVD:\n{reconstructed_matrix}")
