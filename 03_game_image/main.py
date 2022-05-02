import pytesseract
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv
import cv2
import numpy as np
from math import floor

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_PATH = BASE_PATH / 'image/test1.png'
INPUT_IMAGE_PATH_STRING = str(INPUT_IMAGE_PATH)
OCR_LANG = 'jpn'

base_image = cv2.imread(INPUT_IMAGE_PATH_STRING)

# Preprocess Image
# # resize image to fixed size
# resized_image = cv2.resize(base_image, (640, 360))

# # initial area
# x,y,w,h = 20,70,500,50


# resize image to fixed size
base_w = 1920
base_h = 1080

resized_image = cv2.resize(base_image, (base_w, base_h))

# initial area
mx = 32
my = 5.14
mw = 1.28
mh = 7.35

x = floor(base_w / mx)
y = floor(base_h / my)
w = floor(base_w / mw)
h = floor(base_h / mh)

# go down each segment
for n in range(5):
    new_y = y + (n*h)
    roi = resized_image[new_y:new_y+h,x:x+w]
    grey_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresholded_image =  cv2.threshold(grey_roi,175,255,cv2.THRESH_BINARY)
    cv2.imshow(f'image{n}', thresholded_image)
    text = pytesseract.image_to_string(thresholded_image, lang=OCR_LANG)
    print(f'image{n}')
    print(text)
    print('---')

cv2.waitKey(0)
cv2.destroyAllWindows()
