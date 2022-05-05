import cv2
from os import makedirs
from os.path import splitext, dirname, basename, join
from pathlib import Path
import time

BASE_PATH = Path(__file__).parent
INPUT_VIDEO_PATH = str(BASE_PATH / 'video/test.mp4')
INPUT_TEMPLATE_PATH = str(BASE_PATH / 'template/template.jpg')
OUTPUT_IMAGE_DIR_PATH = str(BASE_PATH / 'filtered')


def save_frames(video_path: str, frame_dir: str, name="image", ext="jpg"):
    TEMPLATE_IMAGE = cv2.imread(INPUT_TEMPLATE_PATH)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    v_name = splitext(basename(video_path))[0]
    if frame_dir[-1:] == "\\" or frame_dir[-1:] == "/":
        frame_dir = dirname(frame_dir)
    frame_dir_ = join(frame_dir, v_name)

    makedirs(frame_dir_, exist_ok=True)
    base_path = join(frame_dir_, name)

    idx = 0
    while cap.isOpened():
        idx += 1
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  # 0秒のフレームを保存
                continue
            elif idx < cap.get(cv2.CAP_PROP_FPS):
                continue
            else:  # 1秒ずつフレームを保存
                second = int(cap.get(cv2.CAP_PROP_POS_FRAMES) / idx)
                print(f'Checking following second: {second}')
                filled_second = str(second).zfill(8)

                result = cv2.matchTemplate(
                  frame,
                  TEMPLATE_IMAGE,
                  cv2.TM_CCOEFF_NORMED)

                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
                (startX, startY) = maxLoc

                if(startY == 210):
                    print(f'SAVED: {second}')
                    endX = startX + TEMPLATE_IMAGE.shape[1]
                    endY = startY + TEMPLATE_IMAGE.shape[0]

                    cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 3)
                    cv2.imwrite("{}_{}.{}".format(base_path, filled_second, ext), frame)
                idx = 0
        else:
            break

start = time.process_time()
print('START')
save_frames(INPUT_VIDEO_PATH, OUTPUT_IMAGE_DIR_PATH)
end = time.process_time() - start
print('END')
print(f'Process took: {end} seconds')
