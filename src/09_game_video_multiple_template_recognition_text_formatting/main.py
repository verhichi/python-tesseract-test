import pytesseract
from pathlib import Path
import os
from dotenv import load_dotenv
import cv2
from math import floor
import glob
import csv
from datetime import datetime
import re
import time
import difflib
from os import makedirs
from os.path import splitext, dirname, basename, join
from pathlib import Path
from logging import basicConfig, getLogger, DEBUG, StreamHandler, FileHandler
import sys

BASE_PATH = Path(__file__).parent
CURRENT_DATETIME = datetime.now().strftime("%Y%m%d_%H%M%S")

LOGGING_OUTPUT_PATH = str(BASE_PATH / f'log/{CURRENT_DATETIME}.log')
basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=DEBUG,
            handlers=[
                FileHandler(LOGGING_OUTPUT_PATH),
                StreamHandler(sys.stdout)
            ])
logger = getLogger(__name__)

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
INPUT_VIDEO_PATH = str(BASE_PATH / 'video/test.mp4')
OUTPUT_CSV_DIR_PATH = str(BASE_PATH / 'data')
OCR_LANG = 'eng'
CONFIG = '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%'

CURRENT_DATETIME = datetime.now().strftime("%Y%m%d_%H%M%S")
STAT_REGEXP_PATTERN = '^(\\d{3})%[ABCDEFGS](\\d{2}|100)[ABCDEFGS](\\d{2}|100)$'

PLAYER_NAMES = ['Sybil', 'Bruno', 'Wilson']
FIELDS_NAMES = [
    'id',
    'date',
    'iteration',
    'name',
    'pitching_speed',
    'control',
    'stamina']
PLAYER_DATE_STAT_ITERATION = {
    'Sybil': {},
    'Bruno': {},
    'Wilson': {}
}
uuid_set = set()

THRESHOLD = 0.9
MAX_PLAYERS_IN_STAT_SCREEN = 5

STAT_TEMPLATE_IMAGE = cv2.imread(
    str(BASE_PATH / 'template/stat.jpg'), cv2.IMREAD_GRAYSCALE)

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

NEW_YEAR_MONTH_NUM = 1

# resize image to fixed size
base_w = 1920
base_h = 1080

# area coefficient
mx = 32
my = 5.14
mw = 1.28
mh = 7.35

# calculate area based on coefficient and base width and height
x = floor(base_w / mx)
y = floor(base_h / my)
w = floor(base_w / mw)
h = floor(base_h / mh)


def match_stat_template(image):
    result = cv2.matchTemplate(
        image,
        STAT_TEMPLATE_IMAGE,
        cv2.TM_CCOEFF_NORMED)
    (_minVal, _maxVal, _minLoc, maxLoc) = cv2.minMaxLoc(result)
    (_, startY) = maxLoc

    return startY == 210


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


def get_stat_from_image(image, year, month):
    data_list = []
    for n in range(MAX_PLAYERS_IN_STAT_SCREEN):
        new_y = y + (n * h)
        roi = image[new_y:new_y + h, x:x + w]

        roi_name = roi[20:70, 50:270]
        _, roi_name_th = cv2.threshold(
            roi_name, 150, 255, cv2.THRESH_BINARY)

        roi_stat = roi[70:130, 340:710]
        _, roi_stat_th = cv2.threshold(
            roi_stat, 190, 255, cv2.THRESH_BINARY)

        name = pytesseract.image_to_string(
            roi_name_th, lang=OCR_LANG, config=CONFIG).strip()
        stat = pytesseract.image_to_string(
            roi_stat_th, lang=OCR_LANG, config=CONFIG).strip()

        logger.debug('Checking for closest name')
        closest_match_name_list = difflib.get_close_matches(
            name, PLAYER_NAMES, 1)

        if (not closest_match_name_list):
            logger.debug('Did not match any names -> continue')
            continue

        closest_match_name = closest_match_name_list[0]
        logger.debug(f'Found closest name: {name} = {closest_match_name}')

        stat_match_group = re.match(STAT_REGEXP_PATTERN, stat)
        logger.debug(f'OCR Result: name: {closest_match_name}, stat: {stat}')
        logger.debug(f'RE Match Result: {stat_match_group}')

        if not closest_match_name or not stat_match_group:
            logger.debug('Broken data -> continue')
            continue

        (pitching_speed, control, stamina) = stat_match_group.groups()
        year_month = f'{year}{month}'
        id = f'{year_month}_{closest_match_name}_{pitching_speed}{control}{stamina}'

        if id in uuid_set:
            logger.debug('uuid already exists -> same data -> continue')
            continue

        if (year_month in PLAYER_DATE_STAT_ITERATION[closest_match_name]):
            PLAYER_DATE_STAT_ITERATION[closest_match_name][year_month] += 1
        else:
            PLAYER_DATE_STAT_ITERATION[closest_match_name][year_month] = 1

        data_dict = {
            'id': id,
            'date': year_month,
            'iteration': PLAYER_DATE_STAT_ITERATION[closest_match_name][year_month],
            'name': closest_match_name,
            'pitching_speed': pitching_speed,
            'control': control,
            'stamina': stamina}

        uuid_set.add(id)
        data_list.append(data_dict)

    return data_list


def main(video_path: str, START_YEAR: int, START_MONTH_NUM: int):
    CURRENT_YEAR = START_YEAR
    CURRENT_MONTH_NUM = str(START_MONTH_NUM).zfill(2)

    with open(f'{OUTPUT_CSV_DIR_PATH}/{CURRENT_DATETIME}.csv', 'a', encoding='UTF8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS_NAMES)
        writer.writeheader()

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return

        idx = 0
        while cap.isOpened():
            idx += 1
            ret, raw_frame = cap.read()

            if (raw_frame is None):
                break

            frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)

            if ret:
                if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  # 0秒のフレームを保存
                    continue
                elif idx < cap.get(cv2.CAP_PROP_FPS):
                    continue
                else:  # 1秒ずつフレームを保存
                    second = int(cap.get(cv2.CAP_PROP_POS_FRAMES) / idx)
                    logger.debug(f'Checking following second: {second}')

                    if (match_stat_template(frame)):
                        logger.debug('Stat Template Matched: TRUE')
                        frame_data_list = get_stat_from_image(
                            frame, CURRENT_YEAR, CURRENT_MONTH_NUM)
                        for frame_data in frame_data_list:
                            writer.writerow(frame_data)
                        idx = 0
                        continue
                    else:
                        logger.debug('Stat Template Matched: FALSE')

                    matched_month_num = match_month_template(frame, THRESHOLD)
                    if (matched_month_num is not None):
                        logger.debug('Month Template Matched: TRUE')
                        CURRENT_MONTH_NUM = matched_month_num
                        if (matched_month_num == NEW_YEAR_MONTH_NUM):
                            CURRENT_YEAR += 1
                        idx = 0
                        continue
                    else:
                        logger.debug('Month Template Matched: FALSE')

                    idx = 0

            else:
                break


start = time.process_time()
logger.debug('START')
main(INPUT_VIDEO_PATH, 2028, 8)
end = time.process_time() - start
logger.debug('END')
logger.debug(f'Process took: {end} seconds')
