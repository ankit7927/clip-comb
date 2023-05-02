DB_NAME="shorts.db"
DB_DIR="db/"
DB_PATH=DB_DIR+DB_NAME
IMAGES_DIR="db/images/"
FONTS_DIR="fonts/"
TEMP_DIR="temp/"

AUDIO_NAME=lambda fname : f"{TEMP_DIR}{fname}.mp3"
CLIP_NAME=lambda fname : f"{TEMP_DIR}{fname}_clp.mp4"
FINAL_CLIP_NAME=lambda fname: f"{fname}.mp4"