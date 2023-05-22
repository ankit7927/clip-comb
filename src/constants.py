import random

APP_NAME:str = "Clip-Combiner"
DB_NAME:str="shorts.db"
DB_DIR:str="db/"
DB_PATH:str=DB_DIR+DB_NAME
IMAGES_DIR:str="db/images/"
FONT_NAME:str="src/RobotoSlab-M.ttf"
TEMP_DIR:str="temp/"
ZIP_NAME:str="db"
OUTPUT_DIR:str="output/"
AUDIO_VOLUME:int=2
AUDIO_SPEED:int=1.2

HOR_IMAGE_POS=("center", 85)
VER_IMAGE_POS=("center", 50)
HOR_IMAGE_HEIGHT=550
VER_IMAGE_HEIGHT=300
HOR_TEXT_POS = ("center", 0.65)
VER_TEXT_POS = ("center", 0.4)
HOR_TEXT_SIZE = (1380, None)
VER_TEXT_SIZE = (480, None)

AUDIO_NAME:str=lambda fname : f"{TEMP_DIR}{fname}.mp3"
CLIP_NAME:str=lambda fname : f"{TEMP_DIR}{fname}_clp.mp4"
FINAL_CLIP_NAME:str=lambda fname: f"{OUTPUT_DIR}{fname}.mp4"

ALL_FILES_TUP = ("All files", "*.*")
VIDEO_FILE_TUP = ("Video file", "*.mp4")
IMAGE_FILE_TUP = ("Image files", "*.png *.jpg *.jpeg")
ARCHIVE_FILE_TUP = ("Archive file", "*.zip")

CREATE_TABLE:str = lambda cate : f"create table {cate} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, image TEXT)"
ALL_TABLE_QUERY:str = "select name from sqlite_master where type='table'"
SEQUENCE_TABLE_NAME:str = "sqlite_sequence"
INSERT_TEXT_IMAGE:str = lambda cate : f"INSERT INTO {cate} VALUES (?, ?, ?)"
TEXT_ID_FROM_CATEGORY:str = lambda cate : f"select id, text from {cate}"
TEXT_SELECTION_QUERY:str = lambda cate, id : f"SELECT * FROM {cate} WHERE id={id}"
ALL_IMAGE:str = lambda cate : f"SELECT image from {cate}"
IMAGE_WITH_ID:str = lambda cate, id : f"SELECT image from {cate} WHERE id={id}"
DELETE_ROW:str = lambda cate, id : f"DELETE FROM {cate} WHERE id={id}"
UPDATE_ROW_TEXT:str = lambda cate : f"UPDATE {cate} SET text=? WHERE id=?"
UPDATE_ROW_IMAGE:str = lambda cate : f"UPDATE {cate} SET image=? WHERE id=?"
DROP_TABLE:str = lambda cate : f"DROP TABLE {cate}"

RANDOM_NAME:str = lambda: str(random.randint(10000000, 99999999))