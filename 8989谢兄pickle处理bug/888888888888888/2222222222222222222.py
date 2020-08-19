'''
教程目录:
https://github.com/OpenMined/TenSEAL/blob/master/tutorials/Tutorial%200%20-%20Getting%20Started.ipynb


python3 -m pip install --upgrade pip


https://pypi.org/project/tenseal/
'''


import tenseal as ts

context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
context

public_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
print("Is the context private?", ("Yes" if public_context.is_private() else "No"))
print("Is the context public?", ("Yes" if public_context.is_public() else "No"))

sk = public_context.secret_key()

# the context will drop the secret-key at this point
public_context.make_context_public()
print("Secret-key dropped")
print("Is the context private?", ("Yes" if public_context.is_private() else "No"))
print("Is the context public?", ("Yes" if public_context.is_public() else "No"))

1111111111111








# 下面我们还是使用最开始的public版本context
plain_vector = [60, 66, 73, 81, 90]
encrypted_vector = ts.bfv_vector(context, plain_vector)
print("We just encrypted our plaintext vector of size:", encrypted_vector.size())
print(encrypted_vector,888888888)

add_result = encrypted_vector + [1, 2, 3, 4, 5]
print(add_result.decrypt())


sub_result = encrypted_vector - [1, 2, 3, 4, 5]
print(sub_result.decrypt())


mul_result = encrypted_vector * [1, 2, 3, 4, 5]
print(mul_result.decrypt())



encrypted_add = add_result + sub_result
print(encrypted_add.decrypt())

encrypted_sub = encrypted_add - encrypted_vector
print(encrypted_sub.decrypt())


encrypted_mul = encrypted_add * encrypted_sub
print(encrypted_mul.decrypt())


from time import time

t_start = time()
_ = encrypted_add * encrypted_mul
t_end = time()
print("c2c multiply time: {} ms".format((t_end - t_start) * 1000))

t_start = time()
_ = encrypted_add * [1, 2, 3, 4, 5]
t_end = time()
print("c2p multiply time: {} ms".format((t_end - t_start) * 1000))


print("下面进行性能测试")


import numpy as np
lenth=2000

tmp=np.random.rand(lenth)

tmp=list(tmp)
print("old data",tmp[:5])

context = ts.context(ts.SCHEME_TYPE.CKKS, 2**15, coeff_mod_bit_sizes=[60, 40, 40, 60])

ct = ts.ckks_vector(context, 2**40,tmp)  # scale足够大,就能整数化.
print("after decode",ct.decrypt()[:5])

















