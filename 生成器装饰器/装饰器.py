'''
跟java 里面iou切面一样

'''

from functools import wraps


def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)

    return decorated


@decorator_name
def func():
    return ("Function is running")


can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run
'''
总结装饰器的使用方法:


1.from functools import wraps
2. 写decorate函数.传入一个函数f, 然后@wraps函数 然后写一个函数包起来f(做修饰), 之后return 这个函数即可.
'''






