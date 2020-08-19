from pydocx import PyDocX
html = PyDocX.to_html("111.docx")
f = open("test.html", 'w', encoding="utf-8")
f.write(html)

f.close()