import os
from src.shorts import ShortsMaker

def prepare():
    if not os.path.isdir("src/temp"):
        os.mkdir("src/temp")

if __name__ == "__main__":
    prepare()
    ShortsMaker()