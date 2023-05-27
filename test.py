import numpy as np

a = np.array([1, 2, -1, 5, 6, 9, 10, 2, -5, 0, 0.1])
top_indices = a.argsort()[0]
print(top_indices)
