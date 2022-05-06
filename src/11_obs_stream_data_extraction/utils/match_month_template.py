import cv2
from constants.constants import BASE_PATH

JANUARY_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/january.jpg'), cv2.IMREAD_GRAYSCALE)
FEBRUARY_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/february.jpg'), cv2.IMREAD_GRAYSCALE)
MARCH_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/march.jpg'), cv2.IMREAD_GRAYSCALE)
APRIL_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/april.jpg'), cv2.IMREAD_GRAYSCALE)
MAY_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/may.jpg'), cv2.IMREAD_GRAYSCALE)
JUNE_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/june.jpg'), cv2.IMREAD_GRAYSCALE)
JULY_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/july.jpg'), cv2.IMREAD_GRAYSCALE)
AUGUST_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/august.jpg'), cv2.IMREAD_GRAYSCALE)
SEPTEMBER_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/september.jpg'), cv2.IMREAD_GRAYSCALE)
OCTOBER_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/october.jpg'), cv2.IMREAD_GRAYSCALE)
NOVEMBER_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/november.jpg'), cv2.IMREAD_GRAYSCALE)
DECEMBER_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/december.jpg'), cv2.IMREAD_GRAYSCALE)

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


def match_month_template(image, threshold):
    matched_month_num = None

    for idx, template in enumerate(TEMPLATE_IMAGE_LIST):
        result = cv2.matchTemplate(
            image,
            template,
            cv2.TM_CCOEFF_NORMED)
        (_1, maxVal, _2, _3) = cv2.minMaxLoc(result)

        if (maxVal >= threshold):
            matched_month_num = str(idx + 1).zfill(2)
            break

    return matched_month_num
