import pytesseract
import cv2
from constants.constants import PLAYER_NAMES, STAT_REGEXP_PATTERN, MAX_PLAYERS_IN_STAT_SCREEN, TESSERACT_LANG, TESSERACT_CONFIG
import difflib
from logging import getLogger
from math import floor
import re

logger = getLogger(__name__)

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


def get_stat_from_image(image, year, month, uuid_set):
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
            roi_name_th, lang=TESSERACT_LANG, config=TESSERACT_CONFIG).strip()
        stat = pytesseract.image_to_string(
            roi_stat_th, lang=TESSERACT_LANG, config=TESSERACT_CONFIG).strip()

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
        id = f'{year_month}_{closest_match_name}'

        if id in uuid_set:
            logger.debug('uuid already exists -> same data -> continue')
            continue

        data_dict = {
            'id': id,
            'date': f'{year}/{month}',
            'name': closest_match_name,
            'pitching_speed': pitching_speed,
            'control': control,
            'stamina': stamina}

        uuid_set.add(id)
        data_list.append(data_dict)

    return data_list
