import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2])
y = np.array([2,3])

learning_rate = 0.01
iterations = 190


m = len(x)

theta0 = 0.0
theta1 = 0.0

plt.figure(figsize=(10, 8))
plt.scatter(x, y, color='red', s=100, label='Actual Data')
plt.xlim(0,4)
plt.ylim(0,5)
plt.xlabel("Input (X)")
plt.ylabel("Output (Y)")
plt.title("Linear Regression with Gradient Descent")


for i in range(iterations):
    y_pred = theta0 + theta1 * x
    
    if i == 0:
        style = ':'
    elif i == iterations - 1:
        style = '-'
    else:
        style = '--'
        
    plt.plot(x, y_pred, linestyle = style, label=f'Iteration {i+1}')
    

    error = y_pred - y
    loss = np.sum(error ** 2) / (2 * m)
    

    gradient_theta_0 = (1/m) * np.sum(error) 
    gradient_theta_1 = (1/m) * np.sum(error * x)
    
    
    theta0 = theta0 - (learning_rate * gradient_theta_0)
    theta1 = theta1 - (learning_rate * gradient_theta_1)
    
    print(f"Iter {i+1}: Loss={loss:.4f}")
    
plt.legend()
plt.grid(True)
plt.show()
        