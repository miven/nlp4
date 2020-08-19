import numpy as np
adj=np.array([[1,2],[3,4]])
b=adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)

print(b)