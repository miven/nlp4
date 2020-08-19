from bs4 import BeautifulSoup
import urllib
htmlfile = open('2.html', 'r', encoding='utf-8')
html = htmlfile.read()
bs = BeautifulSoup(html, "html.parser")

32423
# resp = urllib.request.urlopen('2.html')
# html = resp.read()
# # urllib.request.urlopen(url).read()
# bs = BeautifulSoup(html, "html.parser")