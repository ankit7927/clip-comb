import os
from src.app import ClipComb
from src.constants import *

def prepare():
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)
    if not os.path.isdir(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.isdir(IMAGES_DIR):
        os.mkdir(IMAGES_DIR)
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

if __name__ == "__main__":
    prepare()
    ClipComb()