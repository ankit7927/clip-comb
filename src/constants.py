APP_NAME = "Clip-Combiner"

DB_NAME="shorts.db"
DB_DIR="db/"
DB_PATH=DB_DIR+DB_NAME
IMAGES_DIR="db/images/"
FONTS_DIR="fonts/"
TEMP_DIR="temp/"
ZIP_NAME="db"
OUTPUT_DIR="output/"

HOR_IMAGE_POS=("center", 85)
VER_IMAGE_POS=("center", 50)
HOR_TEXT_POS = ("center", 0.65)
VER_TEXT_POS = ("center", 0.4)
HOR_TEXT_SIZE = (1380, None)
VER_TEXT_SIZE = (480, None)

AUDIO_NAME=lambda fname : f"{TEMP_DIR}{fname}.mp3"
CLIP_NAME=lambda fname : f"{TEMP_DIR}{fname}_clp.mp4"
FINAL_CLIP_NAME=lambda fname: f"{OUTPUT_DIR}{fname}.mp4"

ALL_FILES_TUP = ("All files", "*.*")
VIDEO_FILE_TUP = ("Video file", "*.mp4")
IMAGE_FILE_TUP = ("Image files", "*.png *.jpg *.jpeg")
ARCHIVE_FILE_TUP = ("Archive file", "*.zip")

CREATE_TABLE = lambda cate : f"create table {cate} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, image TEXT)"
ALL_TABLE_QUERY = """select name from sqlite_master where type='table'"""
SEQUENCE_TABLE_NAME = "sqlite_sequence"
INSERT_TEXT_IMAGE = lambda cate : f"INSERT INTO {cate} VALUES (?, ?, ?)"
TEXT_ID_FROM_CATEGORY = lambda cate : f"select id, text from {cate}"
TEXT_SELECTION_QUERY = lambda cate, id : f"SELECT * FROM {cate} WHERE id={id}"
ALL_IMAGE = lambda cate : f"SELECT image from {cate}"
IMAGE_WITH_ID = lambda cate, id : f"SELECT image from {cate} WHERE id={id}"
DELETE_ROW = lambda cate, id : f"DELETE FROM {cate} WHERE id={id}"
UPDATE_ROW = lambda cate : f"UPDATE {cate} SET text=?, image=? WHERE id=?"
DROP_TABLE = lambda cate : f"DROP TABLE {cate}"