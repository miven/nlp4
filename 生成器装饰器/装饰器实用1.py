from functools import wraps

authdic={'a','b','c'}
def requires_auth(f):
    def decorated(*args, **kwargs):
        # print(args[0]) # 读取函数第一个参数,
        tmp=args[0]
        if tmp in authdic:
            return f(*args, **kwargs)
        return "非法!"

    return decorated


@requires_auth
def f(a):
    return 1111

print(f('a'))
print(f('1'))

'''
总结:
上面这个例子可以看出来,写好装饰器之后,
以后用户验证可以直接从16行开始写.
随便写一个函数,然后传入用户名, 就会自动进入校验函数,进行校验.
好处: 这个校验函数可以用装饰器技术,只写一次,然后后面加入@即可.节省了非常多的代码量.
'''

