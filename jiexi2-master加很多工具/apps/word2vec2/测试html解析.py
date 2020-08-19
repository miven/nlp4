import urllib
from bs4 import BeautifulSoup


tex='12.html'

htmlfile = open(tex, 'r', encoding='utf-8')
html = htmlfile.read()

soup = BeautifulSoup(html, "lxml")

