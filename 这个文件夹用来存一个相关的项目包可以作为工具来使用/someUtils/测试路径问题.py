import sys,os
sys.path.append('C:\\')
sys.path.insert(0,'C:\\')


'''
测试结果:发现sys.path只能引入py文件,不能引入其他类型的文件.python只在环境变量path中搜索.py的后缀文件.
'''
import f
# open('213.txt', encoding='utf-8')

from textfilter import filter as ft





'''
python 包之间读文件的方法:

https://www.jianshu.com/p/621359437e8a

总之.每一次读取文件都应该用绝对路径来读取,
写法是.  open(os.path.dirname(__file__)+'/1_abs.txt') 
只有写成这样才能保证打开文件在各个包中引用时候不会出错.

这种读写方法,可以保证其他包引用时候不做任何更改就可以运行.
'''