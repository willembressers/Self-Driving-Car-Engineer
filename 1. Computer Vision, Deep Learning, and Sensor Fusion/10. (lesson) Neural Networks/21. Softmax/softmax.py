import numpy as np

# Write a function that takes as input a list of numbers, and returns
# the list of values given by the softmax function.
def softmax(L):
    exponentials = np.exp(L)
    return [exponential / sum(exponentials) for exponential in exponentials]