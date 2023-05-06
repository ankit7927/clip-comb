import os, sys
from src.shorts import ShortsMaker
from src.gui.manager import Manager
from src.constants import TEMP_DIR, IMAGES_DIR, DB_DIR

def prepare():
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)
    if not os.path.isdir(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.isdir(IMAGES_DIR):
        os.mkdir(IMAGES_DIR)

if __name__ == "__main__":
    prepare()
    ShortsMaker()