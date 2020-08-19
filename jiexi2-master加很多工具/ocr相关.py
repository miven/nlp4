import pytesseract
from PIL import Image

# open image
image = Image.open('3.png')
code = pytesseract.image_to_string(image, lang='chi_sim')

