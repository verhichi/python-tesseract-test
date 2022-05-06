# My TESSERACT PRACTICE

Just practicing OCR with pytesseract

## What I Tested Out

I tested out retrieving information through OCR from the following:

- Static Images(jpg, png)
- Video(mp4)
- Video Stream from OBS

## My Environment

- OS:
  - Windows 10 Home
- Language:
  - Python 3.10.4
- Software:
  - Tesseract 5.0.1
  - OBS 27.2.4 (For Rendering from Stream)
  - Must use [OBS VirtualCam v2.0.5](https://obsproject.com/forum/resources/obs-virtualcam.949/) to capture stream
- Hardware:
  - hardware: [hdmi capture board](https://www.amazon.co.jp/gp/product/B089GZ4N48) to capture console game stream(like switch or playstation)

## Tesseract Installation Process

1. Download tesseract installer for windows(https://github.com/UB-Mannheim/tesseract/wiki)
1. Install tesseract(the following is the option I set, which may differ from yours)
   - install location: `E:\Tesseract-OCR`

## OBS Installation Process(at least for this project)

1. Download OBS installer for windows(https://obsproject.com/)
1. Install OBS
1. Download OBS VirtualCam installer(https://obsproject.com/forum/resources/obs-virtualcam.949/)
1. Install OBS VirtualCam

## Developers

### Install Dependencies

```sh
$ pipenv install
```

### Environment Variables

Set the following environment variable for the code to work correctly
or you can just create a '.env' file in project root directory

```sh
# Apparently pytesseract tries to get tesseract.exe from a predefined path, and if you placed it somewhere else, the code will result in an error unless you define it like so
PYTESSERACT_PATH=C:\your\path\to\Tesseract-OCR\tesseract.exe
```

### Run
