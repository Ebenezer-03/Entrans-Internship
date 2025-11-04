import numpy as np

def calculate_gradient(w):
    return 2 * w

w = 10.0
learning_rate = 0.1
num_iterations = 20

print(f"Starting at w = {w:.4f}\n")

for i in range(num_iterations):
    gradient = calculate_gradient(w)
    w -= learning_rate * gradient
    loss = w**2
    print(f"Iteration {i+1}: w = {w:.4f},  Loss = {loss:.4f},  Gradient = {gradient:.4f}")

print(f"\nOptimization finished.")
print(f"The minimum is at w = {w:.4f}")
