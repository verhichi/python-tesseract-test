from dotenv import load_dotenv
import pytesseract
import os

# setup


def tesseract_setup():
    load_dotenv()
    pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')
