import perceptron
import numpy as np
import matplotlib.pyplot as plt

# read data from CSV (without header)
data = np.genfromtxt('data.csv', dtype=float, delimiter=',')

# first 2 columns are X
X = data[:,:2]

# third column is y
y = data[:,2]

# do it
boundary_lines = perceptron.trainPerceptronAlgorithm(X, y)

# plot it
plt.scatter(X[:,0], X[:,1], marker='o', c=y, cmap='bwr')
plt.xlim(-0.5, 1.5)
plt.ylim(-0.5, 1.5)
plt.savefig("output.png")