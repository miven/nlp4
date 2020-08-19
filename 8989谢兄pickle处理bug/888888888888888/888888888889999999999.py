
import numpy as np
from sklearn.datasets import load_diabetes

import phe as paillier


keypair = paillier.generate_paillier_keypair(n_length=1024)
pubkey, privkey = keypair



import pickle
tt=pickle.dumps(pubkey)
print(tt,666666666666666666)
tt=pickle.loads(tt)
tmp=np.array([tt.encrypt(i) for i in x])
print(tmp)


tmp2=np.array([privkey.decrypt(i) for i in tmp])
print(tmp2[0])
print(tmp2[1])
print(tmp2[2])
print(tmp2[3])