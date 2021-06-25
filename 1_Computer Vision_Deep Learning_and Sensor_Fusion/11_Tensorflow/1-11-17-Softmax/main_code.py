# Solution is available in the other "solution.py" tab
import numpy as np


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    exponent = np.exp(x)
    
    return exponent / np.sum(exponent, axis=0)
    
logits = [3.0, 1.0, 0.2]
print(softmax(logits))
