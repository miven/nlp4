
import re
tmp=re.search(r'[\u4e00-\u9fa5]{1,3}? *发 *?\〔|\[[0-9]{4}\〕|\][0-9]*? *号',"国发[2006]6号")
tmp=re.search(r'[\u4e00-\u9fa5]{1,3}? *发 *?\〔|\[',"国发[2006]6号")
tmp=re.search(r'[\u4e00-\u9fa5]{1,3}? *发 *?\〔|\[',"国发[")
#注意括号,来区分.
tmp=re.search('[\u4e00-\u9fa5]{1,3} *发 *(\〔|\[)[0-9]{4}(\]|〕)[0-9]*? *号',"aaaaa国发[2006]6号aaa")
# tmp=re.search(r'\[|\(',"(")
# tmp=re.search('(',"("))
# tmp=re.search('[\u4e00-\u9fa5]{1,3}? *发? *?〔|[',"国发[")




'''
url中文编码
'''


from urllib.request import quote, unquote
import urllib.parse
name = urllib.parse.quote('中文')
name=unquote('%E4%B8%AD%E6%96%87')
from urllib.request import quote, unquote
name=unquote('中文')





