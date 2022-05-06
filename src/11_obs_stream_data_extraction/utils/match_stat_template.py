import cv2
from constants.constants import BASE_PATH

STAT_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/stat.jpg'), cv2.IMREAD_GRAYSCALE)


def match_stat_template(image):
    result = cv2.matchTemplate(
        image,
        STAT_TEMPLATE_IMAGE,
        cv2.TM_CCOEFF_NORMED)
    (_minVal, _maxVal, _minLoc, maxLoc) = cv2.minMaxLoc(result)
    (_, startY) = maxLoc

    return startY == 210
