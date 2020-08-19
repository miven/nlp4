from functools import wraps

def log(a, **dkwargs):  # 第一层是给修饰器的参数
 def _log(f):
    def decorated(*args, **kwargs):  #最里面这层是给函数本身的参数.
        # print(args[0]) # 读取函数第一个参数,
        tmp=args[0]
        print(        "decrator param:", a, dkwargs)
        print("打印log_1")

        return f(*args, **kwargs)


    return decorated
 return _log


@log(3)  # 这样可以给修饰器传参数.
def f(a):
    return 1111

print(f('a'))




