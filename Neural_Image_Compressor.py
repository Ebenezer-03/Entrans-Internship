import numpy as np

image = np.array([
 [157, 126, 129, 126, 236, 192,  92, 198],
 [125, 241, 218, 212,  38,  62,  82,  83],
 [164, 204, 135,  24,  48, 107,  57, 228],
 [143, 145, 129, 106,  89,  16, 187,  64],
 [ 79,  82, 128,  86,  75, 132,  86,  68],
 [160, 139, 243, 152,  21,  50,  62,  99],
 [105,  16,  11, 166, 125,  41, 253,  25],
 [ 41,  14,  23, 156, 123, 243, 200, 123]
], dtype=np.float32)

image /= 255.0
X = image.flatten().reshape(1, 64)
y = X

U, s, VT = np.linalg.svd(image)
print("Top singular values:", s.round(2))
 #functions 
def relu(x): return np.maximum(0, x)
def relu_derivative(x): return (x > 0).astype(float)
def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x): return x * (1 - x)
#paramenter given
input_size = 64
hidden_size = 16
output_size = 64
learning_rate = 0.05
num_epochs = 7000
#Weigh Initialization
W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2. / input_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2. / hidden_size)
b2 = np.zeros((1, output_size))

for epoch in range(num_epochs):
    hidden_input = X @ W1 + b1
    hidden_output = relu(hidden_input)
    output_input = hidden_output @ W2 + b2
    
    predicted = sigmoid(output_input)
    error = y - predicted
    loss = np.mean(error**2)
    
    grad_output = error * sigmoid_derivative(predicted)
    grad_hidden = (grad_output @ W2.T) * relu_derivative(hidden_output)
    
    #weight Updation
    W2 += learning_rate * (hidden_output.T @ grad_output)
    b2 += learning_rate * np.sum(grad_output, axis=0, keepdims=True)
    W1 += learning_rate * (X.T @ grad_hidden)
    b1 += learning_rate * np.sum(grad_hidden, axis=0, keepdims=True)
    if epoch % 500 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.6f}")
#Output
reconstructed_image = predicted.reshape(8, 8)
print("\nOriginal Image:")
print((image * 255).round(2))
print("\nReconstructed Image (Rounded to 2 decimals):")
print((reconstructed_image * 255).round(2))
