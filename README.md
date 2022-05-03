# My TESSERACT PRACTICE

Just practicing OCR with pytesseract

## My Environment

- Windows 10 Home
- Python 3.10.4
- Tesseract 4.1.0(win32)
  - **Using version 4.1.0 win32 because training data commands were not compatible with v5 or 4.1.0(win64)**

## Installation Process

1. Download tesseract installer for windows(https://github.com/UB-Mannheim/tesseract/wiki)
1. Install tesseract(the following is the option I set, which may differ from yours)
   - install location: `E:\Tesseract-OCR`
   - additional options: `Japanese` (did not get Japanese vertical)

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

### Creating Training Data

Followed this youtube video's instructions: https://www.youtube.com/watch?v=1v8BPw0Dn0I

PLace your custom train data name in `langname`

```sh
$ tesseract {langname}.GenJyuuGothicL-Bold.exp0.tiff {langname}.GenJyuuGothicL-Bold.exp0 batch.nochop makebox
$ tesseract {langname}.GenJyuuGothicL-Bold.exp0.tiff {langname}.GenJyuuGothicL-Bold.exp0 box.train
$ unicharset_extractor {langname}.GenJyuuGothicL-Bold.exp0.box
$ echo GenJyuuGothicL-Bold 0 1 0 0 0 > font_properties
$ mftraining -F font_properties -U unicharset -O {langname}.unicharset {langname}.GenJyuuGothicL-Bold.exp0.tr
$ cntraining {langname}.GenJyuuGothicL-Bold.exp0.tr
$ combine_tessdata {langname}.
```
