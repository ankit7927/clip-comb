import os, sys
from src.shorts import ShortsMaker
from src.gui.manager import Manager

def prepare():
    if not os.path.isdir("src/temp"):
        os.mkdir("src/temp")
    if not os.path.isdir("src/db/images"):
        os.mkdir("src/db/images")

if __name__ == "__main__":
    arglen = len(sys.argv)
    prepare()
    if arglen == 2 and sys.argv[1] == "-m":
        Manager()
    else:   ShortsMaker()