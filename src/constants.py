APP_NAME = "Clip-Combiner"

DB_NAME="shorts.db"
DB_DIR="db/"
DB_PATH=DB_DIR+DB_NAME
IMAGES_DIR="db/images/"
FONTS_DIR="fonts/"
TEMP_DIR="temp/"
ZIP_NAME="db"
OUTPUT_DIR="output/"

AUDIO_NAME=lambda fname : f"{TEMP_DIR}{fname}.mp3"
CLIP_NAME=lambda fname : f"{TEMP_DIR}{fname}_clp.mp4"
FINAL_CLIP_NAME=lambda fname: f"{OUTPUT_DIR}{fname}.mp4"

ALL_FILES_TUP = ("All files", "*.*")
VIDEO_FILE_TUP = ("Video file", "*.mp4")
IMAGE_FILE_TUP = ("Image files", "*.png *.jpg *.jpeg")

ALL_TABLE_QUERY = """select name from sqlite_master where type='table'"""
SEQUENCE_TABLE_NAME = "sqlite_sequence"
TEXT_ID_FROM_CATEGORY = lambda cate : f"select id, text from {cate}"
TEXT_SELECTION_QUERY = lambda cate, id : f"SELECT * FROM {cate} WHERE id={id}"