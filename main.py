import os
from src.shorts import ShortsMaker

def prepare():
    if not os.path.isdir("src/raw"):
        os.mkdir("src/raw")

if __name__ == "__main__":
    prepare()
    ShortsMaker()