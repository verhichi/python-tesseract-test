# My TESSERACT PRACTICE

Just practicing OCR with pytesseract

## My Environment

- Windows 10 Home
- Python 3.10.4
- Tesseract 5.0.1

## Installation Process

1. Download tesseract installer for windows(https://github.com/UB-Mannheim/tesseract/wiki)
1. Install tesseract(the following is the option I set, which may differ from yours)
   - install location: `E:\Tesseract-OCR`

## Developers

### Install Dependencies

```sh
$ pipenv install
```

### Environment Variables

Set the following environment variable for the code to work correctly

```sh
# Apparently pytesseract tries to get tesseract.exe from a predefined path, and if you placed it somewhere else, the code will result in an error unless you define it like so
PYTESSERACT_PATH=C:\your\path\to\Tesseract-OCR\tesseract.exe
```
