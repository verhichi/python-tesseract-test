from pathlib import Path
import cv2
import glob

# initialize variables
BASE_PATH = Path(__file__).parent

INPUT_IMAGE_DIR_PATH = str(BASE_PATH / 'image/*.jpg')
INPUT_IMAGE_FILE_PATHS = glob.glob(INPUT_IMAGE_DIR_PATH)

INPUT_TEMPLATE_PATH = str(BASE_PATH / 'template/template.jpg')
TEMPLATE_IMAGE = cv2.imread(INPUT_TEMPLATE_PATH)

for path in INPUT_IMAGE_FILE_PATHS:
    base_image = cv2.imread(path)
    result = cv2.matchTemplate(
        base_image,
        TEMPLATE_IMAGE,
        cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    (startX, startY) = maxLoc

    if(startY == 210):
        endX = startX + TEMPLATE_IMAGE.shape[1]
        endY = startY + TEMPLATE_IMAGE.shape[0]

        cv2.rectangle(base_image, (startX, startY),
                      (endX, endY), (255, 0, 0), 3)
        cv2.imshow(path, base_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
