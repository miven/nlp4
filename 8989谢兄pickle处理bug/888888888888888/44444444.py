print("下面进行性能测试")

import tenseal as ts
import numpy as np
lenth=2000

tmp=np.random.rand(lenth)




tmp=list(tmp)
print("old data",tmp[:5])

context = ts.context(ts.SCHEME_TYPE.CKKS, 2**15, coeff_mod_bit_sizes=[60, 40, 40, 60])
# the context will drop the secret-key at this point

tmp2=context.secret_key()
print(tmp2)
context.make_context_public()


ct = ts.ckks_vector(context, 2**40,tmp)  # scale足够大,就能整数化.
print("after decode",ct.decrypt()[:5])