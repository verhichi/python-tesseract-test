import pytesseract
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv
import cv2

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
# resized_image = cv2.resize(base_image, (0, 0), fx=0.5, fy=0.5)
# resize image to fixed size
resized_image = cv2.resize(base_image, (640, 360))

# initial area
x,y,w,h = 20,70,500,50

# go down each segment
for n in range(5):
    new_y = y + (n*h)
    roi = resized_image[new_y:new_y+h,x:x+w]
    cv2.imshow(f'image{n}', roi)
    text = pytesseract.image_to_string(roi, lang=OCR_LANG)
    print(f'image{n}')
    print(text)
    print('---')

cv2.waitKey(0)
cv2.destroyAllWindows()
