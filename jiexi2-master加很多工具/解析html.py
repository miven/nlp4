
from bs4 import BeautifulSoup
import  urllib
from html.parser import HTMLParser
def get_content(url):
    resp = urllib.request.urlopen(url)
    html = resp.read()
    bs = BeautifulSoup(html, "html.parser")
    # bs.
    tmp=bs.get_text()

    return bs.get_text()











# fasdffdsf
#
#
#
#
tmp=urllib.request.urlopen(r'file:///D:/zhangbo340/Desktop/1.html').read()


#
# import re
# from html import unescape
#
#
# def html_to_plain_text(html):
#     text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
#     text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
#     text = re.sub('<.*?>', '', text, flags=re.M | re.S)
#     text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
#     return unescape(text)
#
#
# import re
# from html import unescape
#
#
#
#
#



