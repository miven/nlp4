
# 这个脚本用来去除所有的tag,然后得到里面的text.也就是我们爬虫一般最后需要的懂系


from w3lib.html import *
doc = '''<div>232323<script type="text/javascript">


<p>3243242<p>
try {
var pageTracker = _gat._getTracker(UA-7245624-1);
pageTracker._trackPageview()
} catch(err) {}</script>

</div>'''
tmp=replace_tags(doc,'')
print(tmp)


# import re
#
#
# tmp=re.sub(r'<script.*</script>','',"111111111111<script>dfdsfaadsf</script>111")
#
# print(tmp)


tmp='\r\n'.join(['dsfsdafasd','fdsfasdfdasf'])
with open('34343443434', 'w', encoding='utf-8') as f:
    f.write(tmp)