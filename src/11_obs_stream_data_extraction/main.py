from constants.constants import OUTPUT_CSV_PATH, FIELD_NAMES, CAMERA_ID, MONTH_MATCH_THRESHOLD, NEW_YEAR_MONTH_NUM
from logging import getLogger
from utils.get_stat_from_image import get_stat_from_image
from utils.match_month_template import match_month_template
from utils.match_stat_template import match_stat_template
from setup.tesseract import tesseract_setup
from setup.logger import logger_setup
import cv2
import csv
import time

tesseract_setup()
logger_setup()

uuid_set = set()

base_w = 1920
base_h = 1080

logger = getLogger(__name__)


def main(START_YEAR: int, START_MONTH_NUM: int):
    CURRENT_YEAR = START_YEAR
    CURRENT_MONTH_NUM = str(START_MONTH_NUM).zfill(2)

    with open(OUTPUT_CSV_PATH, 'a', encoding='UTF8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()

        cap = cv2.VideoCapture(CAMERA_ID)
        if not cap.isOpened():
            return

        idx = 0
        while cap.isOpened():
            idx += 1
            ret, raw_frame = cap.read()

            if (raw_frame is None):
                break

            gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(gray_frame, (base_w, base_h))

            if ret:
                if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  # 0秒のフレームを保存
                    continue
                elif idx < cap.get(cv2.CAP_PROP_FPS):
                    continue
                else:  # 1秒ずつフレームを保存
                    logger.debug(f'Checking following frame: {idx}')

                    if (match_stat_template(frame)):
                        frame_data_list = get_stat_from_image(
                            frame, CURRENT_YEAR, CURRENT_MONTH_NUM, uuid_set)
                        logger.info(f'Stat Template Matched at frame: {idx}')
                        logger.info(f'Matched Data: {frame_data_list}')
                        for frame_data in frame_data_list:
                            writer.writerow(frame_data)
                        continue
                    else:
                        logger.debug('Stat Template Matched: FALSE')

                    matched_month_num = match_month_template(
                        frame, MONTH_MATCH_THRESHOLD)
                    if (matched_month_num is not None):
                        logger.info(f'Month Template Matched frame: {idx}')
                        logger.info(f'Matched Month: {matched_month_num}')
                        CURRENT_MONTH_NUM = matched_month_num
                        if (matched_month_num == NEW_YEAR_MONTH_NUM):
                            CURRENT_YEAR += 1
                        continue
                    else:
                        logger.debug('Month Template Matched: FALSE')

            else:
                break

        cap.release()

start = time.process_time()
logger.debug('START')
main(2031, 5)
end = time.process_time() - start
logger.debug('END')
logger.debug(f'Process took: {end} seconds')
