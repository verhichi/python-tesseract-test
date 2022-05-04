import pytesseract
from pathlib import Path
import os
from dotenv import load_dotenv
import cv2
from math import floor

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_PATH = BASE_PATH / 'image/test2.png'
INPUT_IMAGE_PATH_STRING = str(INPUT_IMAGE_PATH)
OCR_LANG = 'eng'
CONFIG = '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%'

base_image = cv2.imread(INPUT_IMAGE_PATH_STRING, cv2.IMREAD_GRAYSCALE)

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
    new_y = y + (n * h)
    roi = resized_image[new_y:new_y + h, x:x + w]

    roi_name = roi[20:70, 50:270]
    ret, roi_name_th = cv2.threshold(roi_name, 150, 255, cv2.THRESH_BINARY)

    roi_stat = roi[70:130, 340:710]
    ret, roi_stat_th = cv2.threshold(roi_stat, 190, 255, cv2.THRESH_BINARY)

    cv2.imshow(f'image_name_{n}', roi_name_th)
    cv2.imshow(f'image_stat_{n}', roi_stat_th)
    name = pytesseract.image_to_string(
        roi_name_th, lang=OCR_LANG, config=CONFIG)
    stat = pytesseract.image_to_string(
        roi_stat_th, lang=OCR_LANG, config=CONFIG)
    print(f'image_name_{n}')
    print(name)
    print('---')
    print(f'image_stat_{n}')
    print(stat)
    print('===')

cv2.waitKey(0)
cv2.destroyAllWindows()
