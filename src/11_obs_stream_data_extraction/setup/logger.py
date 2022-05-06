from logging import basicConfig, INFO, StreamHandler, FileHandler
import sys
from constants.constants import BASE_PATH, CURRENT_DATETIME


def logger_setup():
    LOGGING_OUTPUT_PATH = str(BASE_PATH / f'log/{CURRENT_DATETIME}.log')
    basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=INFO,
                handlers=[
                    FileHandler(LOGGING_OUTPUT_PATH),
                    StreamHandler(sys.stdout)
                ])
