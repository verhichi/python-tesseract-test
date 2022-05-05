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

start = time.process_time()
print('start')

# setup
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('PYTESSERACT_PATH')

# initialize variables
BASE_PATH = Path(__file__).parent
INPUT_IMAGE_DIR_PATH = str(BASE_PATH / 'filtered/*.jpg')
INPUT_IMAGE_FILE_PATHS = glob.glob(INPUT_IMAGE_DIR_PATH)
OUTPUT_CSV_DIR_PATH = str(BASE_PATH / 'data')
OCR_LANG = 'eng'
CONFIG = '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%'

CURRENT_DATETIME = datetime.now().strftime("%Y%m%d_%H%M%S")
STAT_REGEXP_PATTERN = '^(\\d{3})%[ABCDEFGS](\\d{2,3})[ABCDEFGS](\\d{2,3})$'

PLAYER_NAMES = ['Sybil', 'Bruno', 'Wilson']
field_names = ['id', 'name', 'pitching_speed', 'control', 'stamina']
uuid_set = set()

with open(f'{OUTPUT_CSV_DIR_PATH}/{CURRENT_DATETIME}.csv', 'a', encoding='UTF8') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()

    for path in INPUT_IMAGE_FILE_PATHS:
        print('===')
        print(f'Reading file:', path)
        base_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        # resize image to fixed size
        base_w = 1920
        base_h = 1080

        resized_image = cv2.resize(base_image, (base_w, base_h))

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

        MAX_PLAYERS_IN_SCREEN = 5
        for n in range(MAX_PLAYERS_IN_SCREEN):
            new_y = y + (n * h)
            roi = resized_image[new_y:new_y + h, x:x + w]

            roi_name = roi[20:70, 50:270]
            ret, roi_name_th = cv2.threshold(
                roi_name, 150, 255, cv2.THRESH_BINARY)

            roi_stat = roi[70:130, 340:710]
            ret, roi_stat_th = cv2.threshold(
                roi_stat, 190, 255, cv2.THRESH_BINARY)

            name = pytesseract.image_to_string(
                roi_name_th, lang=OCR_LANG, config=CONFIG).strip()
            stat = pytesseract.image_to_string(
                roi_stat_th, lang=OCR_LANG, config=CONFIG).strip()

            print('Checking for closest name')
            closest_match_name_list = difflib.get_close_matches(name, PLAYER_NAMES, 1)

            if (not closest_match_name_list):
                print('Did not match any names -> continue')
                continue

            closest_match_name = closest_match_name_list[0]
            print(f'Found closest name: {name} = {closest_match_name}')

            stat_match_group = re.match(STAT_REGEXP_PATTERN, stat)
            print('---')
            print(f'OCR Result: name: {closest_match_name}, stat: {stat}')
            print(f'RE Match Result: {stat_match_group}')

            if not closest_match_name or not stat_match_group:
                print('Broken data -> continue')
                continue

            (pitching_speed, control, stamina) = stat_match_group.groups()
            id = f'{closest_match_name}{pitching_speed}{control}{stamina}'
            data_dict = {
                'id': id,
                'name': closest_match_name,
                'pitching_speed': pitching_speed,
                'control': control,
                'stamina': stamina}

            if id in uuid_set:
                print('uuid already exists -> same data -> continue')
                continue

            uuid_set.add(id)
            print('Write data in csv')
            writer.writerow(data_dict)

end = time.process_time() - start
print('END')
print(f'Process took: {end} seconds')
