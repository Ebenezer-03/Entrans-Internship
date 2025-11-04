import numpy as np

A = np.array([[4, -2], [1, 1]])
w,v = np.linalg.eig(A)

print(f"Eigenvalues (lambda): {w}")
print("Eigenvectors (v) [columns]:")
print(v)