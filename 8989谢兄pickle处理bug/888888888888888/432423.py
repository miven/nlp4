import syft as sy
import torch as th
import numpy as np
from syft.frameworks.torch.he.paillier import generate_paillier_keypair
# hook PyTorch to add extra functionalities like the ability to encrypt torch tensors
hook = sy.TorchHook(th)

# Generate CKKS public and secret keys

pubkey, privkey = generate_paillier_keypair()

arr1 = np.ones(3, dtype=float)

a = PaillierTensor(pubkey, arr1)
b = TensorBase(arr1)
c = a * b
for i in range(25):
    c = b * c
    if c.decrypt(privkey).data.all() == arr1.all():
        print(i, '_mul_depth =', c._mul_depth, '    decryption functional:', c.decrypt(privkey))
    else:
        print(i, ' _mul_depth =', c._mul_depth, '    decryption failed:', c.decrypt(privkey))
        break

