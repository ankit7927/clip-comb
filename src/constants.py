import random
from datetime import datetime

APP_NAME:str = "Clip-Combiner"
DB_NAME:str="shorts.db"
DB_DIR:str="db/"
DB_PATH:str=DB_DIR+DB_NAME
FONT_ROBOTO:str="src/assets/RobotoSlab-M.ttf"
TEMP_DIR:str="temp/"
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
FINAL_CLIP_NAME:str=lambda fname: f"{OUTPUT_DIR}{fname}.mp4"

ALL_FILES_TUP = ("All files", "*.*")
VIDEO_FILE_TUP = ("Video file", "*.mp4")
AUDIO_FILE_TUP = ("Audio file", "*.mp3")
IMAGE_FILE_TUP = ("Image files", "*.png *.jpg *.jpeg")
ARCHIVE_FILE_TUP = ("Archive file", "*.zip")

CREATE_TABLE:str = lambda cate : f"CREATE TABLE {cate} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, image TEXT)"
ALL_TABLE_QUERY:str = "SELECT name FROM sqlite_master WHERE type='table'"
SEQUENCE_TABLE_NAME:str = "sqlite_sequence"
INSERT_TEXT_IMAGE:str = lambda cate : f"INSERT INTO {cate} VALUES (?, ?, ?)"
RANDOM_TITLE:str = f"SELECT text, image FROM titles ORDER BY RANDOM() LIMIT 1"
TEXT_ID_FROM_CATEGORY:str = lambda cate : f"SELECT id, text FROM {cate}"
TEXT_IMAGE_FROM_CATEGORY:str = lambda cate : f"SELECT text, image FROM {cate}"
TEXT_SELECTION_QUERY:str = lambda cate: f"SELECT * FROM {cate} WHERE id=?"
ALL_IMAGE:str = lambda cate : f"SELECT image FROM {cate}"
IMAGE_WITH_ID:str = lambda cate, id : f"SELECT image FROM {cate} WHERE id={id}"
DELETE_ROW:str = lambda cate, id : f"DELETE FROM {cate} WHERE id={id}"
UPDATE_ROW_TEXT:str = lambda cate : f"UPDATE {cate} SET text=? WHERE id=?"
UPDATE_ROW_IMAGE:str = lambda cate : f"UPDATE {cate} SET image=? WHERE id=?"
DROP_TABLE:str = lambda cate : f"DROP TABLE {cate}"

RANDOM_NAME:str = lambda: str(random.randint(10000000, 99999999))
def TIME_STR_CONVERTER(time_string:str):
    time = datetime.strptime(time_string, "%H.%M.%S")
    return time.strftime("%H:%M:%S")