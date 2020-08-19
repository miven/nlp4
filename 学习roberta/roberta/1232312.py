import _pickle as cPickle
import tenseal as ts
import dill as pickle

poly_mod_degree = 4096
coeff_mod_bit_sizes = [40, 20, 40]
ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
ctx_eval.global_scale = 2 ** 20
ctx_eval.generate_galois_keys()

a_lst = [[i for i in range(1, 10)] for j in range(100)]
enc_a_lst = [ts.ckks_vector(ctx_eval, x) for x in a_lst]

#使用pickle模块将数据对象保存到文件

import pickle

data1 =enc_a_lst

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

output = open('data.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(data1, output)

# Pickle the list using the highest protocol available.
pickle.dump(selfref_list, output, -1)

output.close()
