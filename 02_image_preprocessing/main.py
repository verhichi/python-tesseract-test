import pytesseract
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv
import cv2
import numpy as np

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_PATH = BASE_PATH / 'image/test1.jpg'
INPUT_IMAGE_PATH_STRING = str(INPUT_IMAGE_PATH)
OCR_LANG = 'eng'

# Preprocess Image
# get image shape size
image = cv2.imread(INPUT_IMAGE_PATH_STRING)
print('image.shape:', image.shape)
print('image')
text = pytesseract.image_to_string(image, lang=OCR_LANG)
print(text)
print('---')

# resize image to fixed size
image_400x400 = cv2.resize(image, (400,400))
print('image_400x400.shape:', image_400x400.shape)
print('image_400x400')
text_400x400 = pytesseract.image_to_string(image_400x400, lang=OCR_LANG)
print(text_400x400)
print('---')

# resize image by ratio
half_size_image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
print('half_size_image.shape:', half_size_image.shape)
print('half_size_image')
half_size_text = pytesseract.image_to_string(half_size_image, lang=OCR_LANG)
print(half_size_text)
print('---')

# gray scale image
grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grey_image_text = pytesseract.image_to_string(grey_image, lang=OCR_LANG)
print('grey_image')
print(grey_image_text)
print('---')

# noise removal image
noise_removed_image = cv2.medianBlur(image,5)
noise_removed_image_text = pytesseract.image_to_string(noise_removed_image, lang=OCR_LANG)
print('noise_removed_image')
print(noise_removed_image_text)
print('---')

# # thresholded image
# thresholded_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# dilated image
dilated_image = cv2.dilate(image, np.ones((5,5),np.uint8), iterations = 1)
dilated_image_text = pytesseract.image_to_string(dilated_image, lang=OCR_LANG)
print('dilated_image')
print(dilated_image_text)
print('---')

# eroded image
eroded_image = cv2.erode(image, np.ones((5,5),np.uint8), iterations = 1)
eroded_image_text = pytesseract.image_to_string(eroded_image, lang=OCR_LANG)
print('eroded_image')
print(eroded_image_text)
print('---')
