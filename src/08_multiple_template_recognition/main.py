from pathlib import Path
import cv2
import glob

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_DIR_PATH = str(BASE_PATH / 'image/*.jpg')
INPUT_IMAGE_FILE_PATHS = glob.glob(INPUT_IMAGE_DIR_PATH)

JANUARY_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/january.jpg'), cv2.IMREAD_GRAYSCALE)
FEBRUARY_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/february.jpg'), cv2.IMREAD_GRAYSCALE)
MARCH_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/march.jpg'), cv2.IMREAD_GRAYSCALE)
APRIL_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/april.jpg'), cv2.IMREAD_GRAYSCALE)
MAY_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/may.jpg'), cv2.IMREAD_GRAYSCALE)
JUNE_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/june.jpg'), cv2.IMREAD_GRAYSCALE)
JULY_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/july.jpg'), cv2.IMREAD_GRAYSCALE)
AUGUST_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/august.jpg'), cv2.IMREAD_GRAYSCALE)
SEPTEMBER_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/september.jpg'), cv2.IMREAD_GRAYSCALE)
OCTOBER_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/october.jpg'), cv2.IMREAD_GRAYSCALE)
NOVEMBER_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/november.jpg'), cv2.IMREAD_GRAYSCALE)
DECEMBER_TEMPLATE_IMAGE = cv2.imread(str(BASE_PATH / 'template/december.jpg'), cv2.IMREAD_GRAYSCALE)

TEMPLATE_IMAGE_LIST = [
  JANUARY_TEMPLATE_IMAGE,
  FEBRUARY_TEMPLATE_IMAGE,
  MARCH_TEMPLATE_IMAGE,
  APRIL_TEMPLATE_IMAGE,
  MAY_TEMPLATE_IMAGE,
  JUNE_TEMPLATE_IMAGE,
  JULY_TEMPLATE_IMAGE,
  AUGUST_TEMPLATE_IMAGE,
  SEPTEMBER_TEMPLATE_IMAGE,
  OCTOBER_TEMPLATE_IMAGE,
  NOVEMBER_TEMPLATE_IMAGE,
  DECEMBER_TEMPLATE_IMAGE,
]

MONTH_LIST = [
  'JANUARY',
  'FEBRUARY',
  'MARCH',
  'APRIL',
  'MAY',
  'JUNE',
  'JULY',
  'AUGUST',
  'SEPTEMBER',
  'OCTOBER',
  'NOVEMBER',
  'DECEMBER'
]

THRESHOLD = 0.9
count = 0

def match_month_template(image, threshold):
    matched = None

    for idx, template in enumerate(TEMPLATE_IMAGE_LIST):
        result = cv2.matchTemplate(
            image,
            template,
            cv2.TM_CCOEFF_NORMED)
        (_1, maxVal, _2, _3) = cv2.minMaxLoc(result)

        if (maxVal >= threshold):
            matched = idx
            break
    
    return matched
    

print('start')
print(f'confidence threshold: {THRESHOLD}')
for path in INPUT_IMAGE_FILE_PATHS:
    print('===')
    print(path)
    base_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    matched_month_index = match_month_template(base_image, THRESHOLD)
    if (matched_month_index is None):
        print('No month matched')
    else:
        print(MONTH_LIST[matched_month_index])

print('end')
