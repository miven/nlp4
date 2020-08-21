'''
看看如何同时运行多个python程序

'''

from multiprocessing import Process
import sys, os
import time
# 让python同时运行多个程序
def a():
    return os.system('python 00000000000022222222.py')


def b():
  return os.system('python 56.py')
funcs=[a,b]






def works(funcs):
  proc_record = []
  for func in funcs:
    p = Process(target = func)
    p.start()
    proc_record.append(p)
  for p in proc_record:
    p.join()# 让代码都堵住.
if __name__ == '__main__':

  works(funcs)
# os.system('python 1212.py')

