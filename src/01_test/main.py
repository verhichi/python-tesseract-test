import pytesseract
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_PATH = BASE_PATH / 'image/test1.jpg'
OCR_LANG = 'jpn'

# run command
text = pytesseract.image_to_string(Image.open(INPUT_IMAGE_PATH), lang=OCR_LANG)

print(text)
